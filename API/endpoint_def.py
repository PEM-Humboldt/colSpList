from io import BytesIO
from flask import Flask, render_template, jsonify, g, send_file
from flask_restful import Resource, Api
from taxo import manageInputTax, get_gbif_parsed_from_sci_name, childrenList, checkCdTax, deleteTaxo, modifyTaxo
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from security import new_user, delete_user, valid_password, user_exists, get_user, generate_auth_token, verify_auth_token, grant_user, revoke_user, grant_edit, revoke_edit, grant_admin, revoke_admin,change_password, get_user_list
from manageStatus import manageInputThreat, manageInputEndem, manageInputExot
from getStatus import testEndemStatus, testExotStatus, testThreatStatus, getListExot, getListEndem, getListThreat, getListTax, getListReferences, getTax
from webargs import fields, validate,missing
from webargs.flaskparser import parser
from webargs.flaskparser import use_args,use_kwargs,abort
from flask_httpauth import HTTPBasicAuth
import psycopg2
import psycopg2.extras
import os
import input_args
import errors

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




# performance
class CleanDb(Resource):
    @use_kwargs(input_args.CleanDbDeleteArgs,location="query")
    @use_kwargs(input_args.CleanDbDeleteArgs,location="json")
    @auth.login_required(role=['edit','admin'])
    def delete(self,**cdbArgs):
        cd_taxs=[]
        cd_refs=[]
        cd_status=[]
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        if cdbArgs.get('status_no_ref'):
            cd_status+=delStatus_no_reference(conn)
        if cdbArgs.get('ref_no_status'):
            cd_refs+=delReference_no_status(conn)
        if cdbArgs.get('syno_no_tax'):
            cd_taxs+=delSyno_no_tax(conn)
        if cdbArgs.get('tax_no_status'):
            cd_taxs+=delTaxo_no_status(conn)
        conn.close()
        return {'cd_tax':cd_taxs,'cd_refs':cd_refs,'cd_st': cd_status}
        
class Performance(Resource):
    @use_kwargs(input_args.PerformancePutArgs,location="query")
    @use_kwargs(input_args.PerformancePutArgs,location="json")
    @auth.login_required(role=['admin'])
    def put(self,**perfArgs):
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        conn.set_isolation_level(0)
        if perfArgs.get('vacuum'):
            SQL = 'VACUUM '
        if perfArgs.get('analyse'):
            SQL += 'ANALYSE'
        cur=conn.cursor()
        cur.execute(SQL)
        conn.commit()
        conn.close()
        
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
    
    @use_kwargs(input_args.UserPostArgs,location="query")
    @use_kwargs(input_args.UserPostArgs,location="json")
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
    
    @use_kwargs(input_args.UserPutArgs,location="json")
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
    @use_kwargs(input_args.AdminUsersDeleteArgs,location="query")
    @use_kwargs(input_args.AdminUsersDeleteArgs,location="json")
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
    @use_kwargs(input_args.AdminUsersPutArgs,location="query")
    @use_kwargs(input_args.AdminUsersPutArgs,location="json")
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

class GetTaxon(Resource):
    @use_kwargs(input_args.TaxGetArgs,location="query")
    @use_kwargs(input_args.TaxGetArgs,location="json")
    def get(self, **taxInput):
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        if not taxInput.get('cd_tax'):
            taxInput.update(manageInputTax(connection=conn,insert=False,**taxInput))
        taxOutput = getTax(conn,taxInput.get('cd_tax'))
        return taxOutput

class TestEndem(Resource):
    @use_kwargs(input_args.TestEndemGetArgs,location="query")
    @use_kwargs(input_args.TestEndemGetArgs,location="json")
    def get(self, **inputArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        res = manageInputTax(connection=conn, insert=False, **inputArgs)
        if res.get('alreadyInDb'):
            res.update(testEndemStatus(conn,res.get('cd_tax_acc')))
        else:
            res.update({'hasEndemStatus':False,'cd_status':None,'comments':None,'references':list(),'links':list()})
        conn.close()
        return res
        
class TestExot(Resource):
    @use_kwargs(input_args.TestExotGetArgs,location="query")
    @use_kwargs(input_args.TestExotGetArgs,location="json")
    def get(self, **inputArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        res = manageInputTax(connection=conn, insert=False, **inputArgs)
        if res.get('alreadyInDb'):
            res.update(testExotStatus(conn,res.get('cd_tax_acc')))
        else:
            res.update({'hasExotStatus':False,'is_alien':None,'is_invasive':None,'comments':None,'references':list(),'links':list()})
        conn.close()
        return res

class TestThreat(Resource):
    @use_kwargs(input_args.TestThreatGetArgs,location="query")
    @use_kwargs(input_args.TestThreatGetArgs,location="json")
    def get(self, **inputArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        res = manageInputTax(connection=conn, insert=False,**inputArgs)
        if res.get('alreadyInDb'):
            res.update(testThreatStatus(conn,res.get('cd_tax_acc')))
        else:
            res.update({'hasThreatStatus':False,'cd_status':None,'comments':None,'references':list(),'links':list()})
        conn.close()
        return res

class ListExot(Resource):
    @use_kwargs(input_args.ListExotGetArgs,location="query")
    @use_kwargs(input_args.ListExotGetArgs,location="json")
    def get(self, **listArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        if listArgs.get('childrenOf'):
            parsed = get_gbif_parsed_from_sci_name(listArgs.get('childrenOf'))
            if parsed.get('scientificName') and parsed.get('canonicalNameComplete') and parsed.get('scientificName')==parsed.get('canonicalNameComplete'):
                parent=manageInputTax(connection=conn, insert=False,canonicalname=listArgs.get('childrenOf'))
            else:
                parent=manageInputTax(connection=conn, insert=False,scientificname=listArgs.get('childrenOf'))
            if parent.get('alreadyInDb'):
                cursor=conn.cursor()
                listChildren=childrenList(cursor,parent.get('cd_tax_acc'))
                cursor.close()
                res=getListExot(connection=conn, listChildren=listChildren, formatExport=listArgs.get('format'))
            else:
                raise TaxonNotFoundDbError(tax=listArgs.get('childrenOf'), message='\'childrenOf\' taxon not recognized')
                #raise Exception("childrenOfNotFound")
        else:
            res = getListExot(connection=conn, listChildren=[], formatExport=listArgs.get('format'))
        conn.close()
        if listArgs.get('format')=="CSV":
            response_stream = BytesIO(res.to_csv().encode())
            return send_file(response_stream, mimetype = "text/csv", attachment_filename = "export.csv")
        else:
            return res
            
class ListEndem(Resource):
    @use_kwargs(input_args.ListEndemGetArgs,location="query")
    @use_kwargs(input_args.ListEndemGetArgs,location="json")
    def get(self, **listArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        if listArgs.get('childrenOf'):
            parsed = get_gbif_parsed_from_sci_name(listArgs.get('childrenOf'))
            if parsed.get('scientificName') and parsed.get('canonicalNameComplete') and parsed.get('scientificName')==parsed.get('canonicalNameComplete'):
                parent=manageInputTax(connection=conn, insert=False,canonicalname=listArgs.get('childrenOf'))
            else:
                parent=manageInputTax(connection=conn, insert=False,scientificname=listArgs.get('childrenOf'))
            if parent.get('alreadyInDb'):
                cursor=conn.cursor()
                listChildren=childrenList(cursor,parent.get('cd_tax_acc'))
                cursor.close()
                res=getListEndem(connection=conn, listChildren=listChildren, formatExport=listArgs.get('format'))
            else:
                raise TaxonNotFoundDbError(tax=listArgs.get('childrenOf'), message='\'childrenOf\' taxon not recognized')
                #raise Exception("childrenOfNotFound")
        else:
            res = getListEndem(connection=conn, listChildren=[], formatExport=listArgs.get('format'))
        conn.close()
        if listArgs.get('format')=="CSV":
            response_stream = BytesIO(res.to_csv().encode())
            return send_file(response_stream, mimetype = "text/csv", attachment_filename = "export.csv")
        else:
            return res

class ListThreat(Resource):
    @use_kwargs(input_args.ListThreatGetArgs,location="query")
    @use_kwargs(input_args.ListThreatGetArgs,location="json")
    def get(self, **listArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        if listArgs.get('childrenOf'):
            parsed = get_gbif_parsed_from_sci_name(listArgs.get('childrenOf'))
            if parsed.get('scientificName') and parsed.get('canonicalNameComplete') and parsed.get('scientificName')==parsed.get('canonicalNameComplete'):
                parent=manageInputTax(connection=conn, insert=False,canonicalname=listArgs.get('childrenOf'))
            else:
                parent=manageInputTax(connection=conn, insert=False,scientificname=listArgs.get('childrenOf'))
            if parent.get('alreadyInDb'):
                cursor=conn.cursor()
                listChildren=childrenList(cursor,parent.get('cd_tax_acc'))
                cursor.close()
                res=getListThreat(connection=conn, listChildren=listChildren, formatExport=listArgs.get('format'))
            else:
                raise TaxonNotFoundDbError(tax=listArgs.get('childrenOf'), message='\'childrenOf\' taxon not recognized')
                #raise Exception("childrenOfNotFound")
        else:
            res = getListThreat(connection=conn, listChildren=[], formatExport=listArgs.get('format'))
        conn.close()
        if listArgs.get('format')=="CSV":
            response_stream = BytesIO(res.to_csv().encode())
            return send_file(response_stream, mimetype = "text/csv", attachment_filename = "export.csv")
        else:
            return res

class ListTax(Resource):
    @use_kwargs(input_args.ListTaxGetArgs,location="query")
    @use_kwargs(input_args.ListTaxGetArgs,location="json")
    def get(self, **listArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        if listArgs.get('childrenOf'):
            parsed = get_gbif_parsed_from_sci_name(listArgs.get('childrenOf'))
            if parsed.get('scientificName') and parsed.get('canonicalNameComplete') and parsed.get('scientificName')==parsed.get('canonicalNameComplete'):
                parent=manageInputTax(connection=conn, insert=False,canonicalname=listArgs.get('childrenOf'))
            else:
                parent=manageInputTax(connection=conn, insert=False,scientificname=listArgs.get('childrenOf'))
            if parent.get('alreadyInDb'):
                cursor=conn.cursor()
                listChildren=childrenList(cursor,parent.get('cd_tax_acc'))
                cursor.close()
                res=getListTax(connection=conn, listChildren=listChildren, formatExport=listArgs.get('format'))
            else:
                raise TaxonNotFoundDbError(tax=listArgs.get('childrenOf'), message='\'childrenOf\' taxon not recognized')
                #raise Exception("childrenOfNotFound")
        else:
            res = getListTax(connection=conn, listChildren=[], formatExport=listArgs.get('format'))
        conn.close()
        if listArgs.get('format')=="CSV":
            response_stream = BytesIO(res.to_csv().encode())
            return send_file(response_stream, mimetype = "text/csv", attachment_filename = "export.csv")
        else:
            return res

class ListReferences(Resource):
    @use_kwargs(input_args.ListReferencesGetArgs,location="query")
    @use_kwargs(input_args.ListReferencesGetArgs,location="json")
    def get(self, **listRefArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        listRef = getListReferences(connection=conn, formatExport= listRefArgs.get('format'), onlyEndem= listRefArgs.get('onlyEndem'), onlyExot= listRefArgs.get('onlyExot'), onlyThreat= listRefArgs.get('onlyThreat'))
        conn.close()
        if listRefArgs.get('format')=="CSV":
            response_stream = BytesIO(listRef.to_csv().encode())
            return send_file(response_stream, mimetype = "text/csv", attachment_filename = "export.csv")
        else:
            return listRef

class ManageEndem(Resource):
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageEndemPostArgs)
    def post(self,**inputEndem):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        res = manageInputTax(connection=conn, insert=True,**inputEndem)
        res.update(manageInputEndem(res.get('cd_tax_acc'), connection = conn, **inputEndem))
        return res
    
    @auth.login_required(role='edit')
    def delete(self,**inputEndem):
        pass
    
    @auth.login_required(role='edit')
    def put(self,**inputEndem):
        pass

class ManageExot(Resource):
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageExotPostArgs)
    def post(self, **inputExot):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        res = manageInputTax(connection=conn, insert=True, **inputExot)
        res.update(manageInputExot(res.get('cd_tax_acc'), connection = conn, **inputExot))
        return res
    
class ManageThreat(Resource):
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageThreatPostArgs)
    def post(self, **inputThreat):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        res = manageInputTax(connection=conn, insert=True,**inputThreat)
        res.update(manageInputThreat(res.get('cd_tax_acc'), connection = conn, **inputThreat))
        conn.close()
        return res

class ManageTax(Resource):
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageTaxoPostArgs)
    def post(self,**dictInput):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        res = manageInputTax(connection=conn, insert=True,**dictInput)
        conn.close()
        return res
    
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageTaxoDeleteArgs)
    def delete(self,**delTaxArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cd_tax = delTaxArgs.get('cd_tax')
        if delTaxArgs.get('canonicalname') or delTaxArgs.get('scientificname') or delTaxArgs.get('gbifkey'):
            if not checkCdTax(connection=conn, cd_tax=cd_tax, **delTaxArgs):
                raise Exception('noCompatibilityCdTaxInputTax')
        res = deleteTaxo(connection, cd_tax)
        conn.close()
        return res
        
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageTaxoPutArgs)
    def put(self,**putTaxArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cd_tax = putTaxArgs.get('cd_tax')
        res = modifyTaxo(connection=connection, cd_tax=cd_tax,**putTaxArgs)
        conn.close()
        return res

class ManageRef(Resource):
    pass
    
# This error handler is necessary for usage with Flask-RESTful
@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(error_status_code, errors=err.messages)
