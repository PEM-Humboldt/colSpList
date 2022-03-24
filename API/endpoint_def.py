from flask import Flask, render_template, jsonify, g
from flask_restful import Resource, Api
from taxo import manageInputTax
from itsdangerous import (TimedJSONWebSignatureSerializer                          as Serializer, BadSignature, SignatureExpired)
from security import new_user, delete_user, valid_password, user_exists, get_user, generate_auth_token, verify_auth_token, grant_user, revoke_user, grant_edit, revoke_edit, grant_admin, revoke_admin,change_password, get_user_list
from manageStatus import manageInputThreat, manageInputEndem, manageInputExot
from getStatus import testEndemStatus, testExotStatus, testThreatStatus
from webargs import fields, validate,missing
from webargs.flaskparser import parser
from webargs.flaskparser import use_args,use_kwargs,abort
from flask_httpauth import HTTPBasicAuth
import psycopg2
import psycopg2.extras
import os

DATABASE_URL = os.environ['DATABASE_URL']
PYTHONIOENCODING="UTF-8"
auth=HTTPBasicAuth()



@auth.verify_password
def verify_password(username,password):
    conn=psycopg2.connect(DATABASE_URL, sslmode='require')
    cur=conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    user=verify_auth_token(username,cur)
    res = user is not None
    if res:
        user['authenticatedThrough']='Token'
    else:
        if user_exists(cur,username):
            res = valid_password(cur,username,password)
            if res:
                user = get_user(cur,get_hash=False,username=username)
                user['authenticatedThrough']='username/password'
        else:
            res = False
    g.user=user
    cur.close()
    conn.close()
    return res

@auth.get_user_roles
def get_roles(authenticated):
    if not authenticated:
        raise Exception("User was not authenticated, no role can be determined")
    return g.user.get('roles')
    


taxInputArgs = {'gbifkey':fields.Int(required=False), 'scientificname':fields.Str(required=False), 'canonicalname':fields.Str(required=False), 'authorship':fields.Str(required=False), 'syno':fields.Bool(required=False), 'rank': fields.Str(required=False), 'parentgbifkey':fields.Int(required=False), 'parentcanonicalname':fields.Str(required=False), 'parentscientificname':fields.Str(required=False), 'synogbifkey':fields.Int(required=False), 'synocanonicalname':fields.Str(required=False), 'synoscientificname':fields.Str(required=False) }

# TODO: check, for link, how to authorize some of the element of a list to be None and how to force the link and ref_citation to be of the same size

newUserArgs = {'username':fields.Str(required=False), 'password':fields.Str(required=False)}

modifyUserAdminArgs={'grant_user':fields.Bool(required=False),'grant_edit':fields.Bool(required=False),'grant_admin':fields.Bool(required=False),'revoke_user':fields.Bool(required=False),'revoke_edit':fields.Bool(required=False),'revoke_admin':fields.Bool(required=False),'newPassword':fields.Str(required=False)}
modifyUserAdminArgs.update(newUserArgs)

modifyPw={'newPassword':fields.Str(required=True)}

inputThreatArgs={'threatstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'link': fields.List(fields.Str(), required = False), 'comments': fields.Str(required=False)}
inputThreatArgs.update(taxInputArgs)


inputEndemArgs={'endemstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'link': fields.List(fields.Str(), required = False), 'comments': fields.Str(required=False)}
inputEndemArgs.update(taxInputArgs)

inputExotArgs={'is_alien':fields.Bool(required=True), 'is_invasive': fields.Bool(required=True), 'occ_observed': fields.Bool(required=False),'cryptogenic': fields.Bool(required=False), 'ref_citation':fields.List(fields.Str(),required=True), 'link': fields.List(fields.Str(),required=False), 'comments': fields.Str(required=False)}
inputExotArgs.update(taxInputArgs)

testArgs={'go_further':fields.Bool(required=False)}

# security
class User(Resource):
    @auth.login_required
    def get(self):
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        token = generate_auth_token(conn,g.user.get('id')).decode('ascii')
        user=g.get('user')
        user['token']=token
        #user = dict(g.user)
        conn.close()
        #return(user)
        return user
    
    @use_kwargs(newUserArgs,location="query")
    @use_kwargs(newUserArgs,location="json")
    def post(self, **userArgs):
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        newId, username = new_user(conn,**userArgs)
        conn.close()
        return {'newId': newId, 'username': username}
    
    @auth.login_required
    def delete(self):
        user=g.get('user')
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        cur=conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        delId, delUsername = delete_user(conn,**user)
        conn.commit()
        cur.close()
        conn.close()
        return uid
    
    @use_kwargs(modifyPw,location="json")
    @auth.login_required
    def put(self,**newPassword):
        user=g.get('user')
        user.update(newPassword)
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        cur=conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        uid = change_password(cur,**user)
        conn.commit()
        cur.close()
        conn.close()
        return uid
    
  
    
class AdminUsers(Resource):
    @auth.login_required(role='admin')
    @use_kwargs(newUserArgs,location="query")
    @use_kwargs(newUserArgs,location="json")
    def delete(self,**userArgs):
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        delId, delUsername = delete_user(conn,**userArgs)
        conn.close()
        return {'delId':delId, 'delUsername': delUsername}
    
    @auth.login_required(role='admin')
    def get(self):
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        cur=conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        user_list=get_user_list(cur)
        cur.close()
        conn.close()
        return user_list
    
    @auth.login_required(role='admin')
    @use_kwargs(modifyUserAdminArgs,location="query")
    @use_kwargs(modifyUserAdminArgs,location="json")
    def put(self,**modifyArgs):
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        cur=conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        res=dict()
        if modifyArgs.get('grant_user'):
            res.update({'grant_user':grant_user(cur,**modifyArgs)})
        if modifyArgs.get('grant_edit'):
            res.update({'grant_edit':grant_edit(cur,**modifyArgs)})
        if modifyArgs.get('grant_admin'):
            res.update({'grant_admin':grant_admin(cur,**modifyArgs)})
        if modifyArgs.get('revoke_user'):
            res.update({'revoke_user':revoke_user(cur,**modifyArgs)})
        if modifyArgs.get('revoke_edit'):
            res.update({'revoke_edit':revoke_edit(cur,**modifyArgs)})
        if modifyArgs.get('revoke_admin'):
            res.update({'revoke_admin':revoke_admin(cur,**modifyArgs)})
        if modifyArgs.get('newPassword'):
            res.append({'newPassword':change_password(cur,**modifyArgs)})
        conn.commit()
        cur.close()
        conn.close()
        return res

"""
class token(Resource):
    @auth.login_required
    def get(self):
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        token = generate_auth_token(conn,g.user.get('id'))
        #user = dict(g.user)
        conn.close()
        #return(user)
        return {'token': token.decode('ascii')}
"""

class testUserWithoutLogin(Resource):
    def get(self):
        if g.get('user') is not None:
            res=g.get('user')
        else:
            res={'message': 'no user provided'}
        return res
"""
class testProt(Resource):
    @use_kwargs(testArgs,location="query")
    @use_kwargs(testArgs,location="json")
    def get(self,**testArgs):
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        res=dict()
        res['nbTax']= testProtectedFun(conn)
        if testArgs.get('go_further'):
            @auth.login_required()
        if testArgs.get('go_further')    
        res['user']=g.user.get('username')
        conn.close()
        return res
"""

class testEndem(Resource):
    @use_kwargs(taxInputArgs,location="query")
    @use_kwargs(taxInputArgs,location="json")
    def get(self, **inputArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cd_tax = manageInputTax(**inputArgs)
        res = testEndemStatus(conn,cd_tax)
        conn.close()
        return res
        
        
class testExot(Resource):
    @use_kwargs(taxInputArgs,location="query")
    @use_kwargs(taxInputArgs,location="json")
    def get(self, **inputArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cd_tax = manageInputTax(**inputArgs)
        res = testExotStatus(conn,cd_tax)
        conn.close()
        return res

class testThreat(Resource):
    @use_kwargs(taxInputArgs,location="query")
    @use_kwargs(taxInputArgs,location="json")
    def get(self, **inputArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cd_tax = manageInputTax(**inputArgs)
        res = testThreatStatus(conn,cd_tax)
        conn.close()
        return res

class insertEndem(Resource):
    @use_kwargs(inputEndemArgs)
    def post(self,**inputEndem):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cd_tax = manageInputTax(**inputEndem)
        res = manageInputEndem(cd_tax, connection = conn, **inputEndem)
        return res

class insertExot(Resource):
    @use_kwargs(inputExotArgs)
    def post(self, **inputExot):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cd_tax = manageInputTax(**inputExot)
        res = manageInputExot(cd_tax, connection = conn, **inputExot)
        return res
    
class insertThreat(Resource):
    @use_kwargs(inputThreatArgs)
    def post(self, **inputThreat):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cd_tax = manageInputTax(**inputThreat)
        res = manageInputThreat(cd_tax, connection = conn, **inputThreat)
        conn.close()
        return res

class insertTaxo(Resource):
    @use_kwargs(taxInputArgs)
    def post(self,**dictInput):
        return manageInputTax(**dictInput)

    
# This error handler is necessary for usage with Flask-RESTful
@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(error_status_code, errors=err.messages)
