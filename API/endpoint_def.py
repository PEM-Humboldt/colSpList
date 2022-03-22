from flask import Flask, render_template, jsonify, g
from flask_restful import Resource, Api
from taxo import manageInputTax
from itsdangerous import (TimedJSONWebSignatureSerializer                          as Serializer, BadSignature, SignatureExpired)
from manageStatus import manageInputThreat
from manageStatus import manageInputEndem
from manageStatus import manageInputExot
from security import new_user
from security import delete_user
from security import valid_password
from security import user_exists
from security import get_user
from security import user_from_id
from security import get_secret_key
from security import generate_auth_token
from security import testProtectedFun
from getStatus import testEndemStatus
from getStatus import testExotStatus
from getStatus import testThreatStatus
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

def verify_auth_token(token,cur):
    sc=get_secret_key(cur)
    s = Serializer(sc)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token
    user=user_from_id(cur,data['id'])
    return user

@auth.verify_password
def verify_password(username,password):
    conn=psycopg2.connect(DATABASE_URL, sslmode='require')
    cur=conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    user=verify_auth_token(username,cur)
    res = user is not None
    if not res:
        if user_exists(cur,username):
            res = valid_password(cur,username,password)
            if res:
                user = get_user(cur,username)
        else:
            res = False
    g.user=user
    cur.close()
    conn.close()
    return res



taxInputArgs = {'gbifkey':fields.Int(required=False), 'scientificname':fields.Str(required=False), 'canonicalname':fields.Str(required=False), 'authorship':fields.Str(required=False), 'syno':fields.Bool(required=False), 'rank': fields.Str(required=False), 'parentgbifkey':fields.Int(required=False), 'parentcanonicalname':fields.Str(required=False), 'parentscientificname':fields.Str(required=False), 'synogbifkey':fields.Int(required=False), 'synocanonicalname':fields.Str(required=False), 'synoscientificname':fields.Str(required=False) }

# TODO: check, for link, how to authorize some of the element of a list to be None and how to force the link and ref_citation to be of the same size

newUserArgs = {'username':fields.Str(required=False), 'password':fields.Str(required=False)}

inputThreatArgs={'threatstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'link': fields.List(fields.Str(), required = False), 'comments': fields.Str(required=False)}
inputThreatArgs.update(taxInputArgs)


inputEndemArgs={'endemstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'link': fields.List(fields.Str(), required = False), 'comments': fields.Str(required=False)}
inputEndemArgs.update(taxInputArgs)

inputExotArgs={'is_alien':fields.Bool(required=True), 'is_invasive': fields.Bool(required=True), 'occ_observed': fields.Bool(required=False),'cryptogenic': fields.Bool(required=False), 'ref_citation':fields.List(fields.Str(),required=True), 'link': fields.List(fields.Str(),required=False), 'comments': fields.Str(required=False)}
inputExotArgs.update(taxInputArgs)

# security
class User(Resource):
    @use_kwargs(newUserArgs,location="query")
    @use_kwargs(newUserArgs,location="json")
    def post(self, **userArgs):
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        newId, username = new_user(conn,**userArgs)
        conn.close()
        return {'newId': newId, 'username': username}
    
    @use_kwargs(newUserArgs,location="query")
    @use_kwargs(newUserArgs,location="json")
    def delete(self,**userArgs):
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        delId, delUsername = delete_user(conn,**userArgs)
        conn.close()
        return {'delId':delId, 'delUsername': delUsername}

class token(Resource):
    @auth.login_required
    def get(self):
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        token = generate_auth_token(conn,g.user.get('id'))
        #user = dict(g.user)
        conn.close()
        #return(user)
        return {'token': token.decode('ascii')}


class testProt(Resource):
    @auth.login_required
    def get(self):
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        nbTax = testProtectedFun(conn)
        conn.close()
        return {'user':g.user.get('username'), 'numTax':nbTax}

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
