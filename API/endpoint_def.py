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
        """
        Description
		-----------
		Delete status without references, references without status nor taxa, synonyms without accepted tax, and/or taxa without statuses ( and which are not synonyms or parents of taxa with statuses)
		
		Optional arguments
		------------------
		status_no_ref: Bool
			Whether to delete statuses without associated bibliographic references
		ref_no_status: Bool
			Whether to delete references which are not associated with any status or taxon
		syno_no_tax: Bool
			Whether to delete synonym without accepted names
		tax_no_status: Bool
			Whether to delete taxa which have no status in the database (and are neither synonym or parents of a taxon with status)

		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
		cd_ref: Int
			Identificator of the bibliographic reference
		cd_st: List(Int)
			List of status identificators (since a taxon can only have only a status in each category, corresponds to the cd_tax)
        """
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
        """
        Description
		-----------
		Run VACUUM and/or ANALYSE in the postgres database

		Required arguments
		--------------------
		vacuum: Bool
			Run the VACUUM command of the postgreSQL database
		analysis: Bool
			Run the ANALYSIS command in the postgreSQL database
        """
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
        """
        Description
		-----------
		Creates an authenticating token and returns the rights of the user

		Optional arguments
		------------------
		create_token: Bool
			Whether to create a new authentication token.
		
		Returns
		-----------
		uid: Int
			Identificator of a user
		username: Str
			User name
		roles: List(Str)
			List of roles (permissions, rights) for a user
		token: Str
			Authentication token for a user
        """
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
        """
        Description
		-----------
		Creates a user without editing/admin rights
		
		Required arguments
		--------------------
		username: Str
			Name of a user
		password: Str
			Password of a user for its creation
		
		Returns
		-----------
		uid: Int
			Identificator of a user
        """
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        newId, username = new_user(conn,**userArgs)
        conn.close()
        return {'newId': newId, 'username': username}
    
    @auth.login_required
    def delete(self):
        """
        Description
		-----------
		Delete the authenticated user

		Returns
		-----------
		uid: Int
			Identificator of a user
		username: Str
			User name
        """
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
        """
		Description
		-----------
		Change password for the autenticated user

		Required arguments
		--------------------
		newPassword: Str
			New password of the user

		Returns
		-----------
		uid: Int
			Identificator of a user
        """
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
        """
        Description
		-----------
		Delete a user

		Optional arguments
		------------------
		uid: Int
			Identificator of a user in the API database
		username: Str
			Name of a user

		Returns
		-----------
		uid: Int
			Identificator of a user
		username: Str
			User name
        """
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        delId, delUsername = delete_user(conn,**userArgs)
        conn.close()
        return {'delId':delId, 'delUsername': delUsername}
    
    @auth.login_required(role='admin')
    def get(self):
        """
        Description
		-----------
		Returns the list of users and their permissions. Format may be JSON or CSV

		Optional arguments
		------------------
		format: Str
			JSON or CSV format in GET methods

		Returns
		-----------
        List of dictonary, or csv table with:
		uid: Int
			Identificator of a user
		username: Str
			User name
		roles: List(Str)
			List of roles (permissions, rights) for a user
        """
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
        """
        Description
		-----------
		Change permission and/or password of a user.

		Optional arguments
		------------------
		uid: Int
			Identificator of a user in the API database
		username: Str
			Name of a user
		grant_user: Bool
			Whether to grant or not the user basic permissions to the user
		revoke_user: Bool
			Whether to revoke basic rights of a user
		grant_edit: Bool
			Whether to grant or not the editing permission to the user
		revoke_edit: Bool
			Whether to revoke edition rights of a user
		grant_admin: Bool
			Whether to grant or not the administrative permission to the user
		revoke_admin: Bool
			Whether to revoke administrative rights of a user
		newPassword: Str
			New password of the user

		Returns
		-----------
		uid: Int
			Identificator of a user
		username: Str
			User name
        """
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
        """
        Description
		-----------
		Returns the information about one taxon.

		Optional arguments
		------------------
		cd_tax: Int
			Identificator of a taxon in the database
		gbifkey: Int
			Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
		scientificname: Str
			Complete name of a taxon, with authorship
		canonicalname: Str
			Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format

		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
		scientificname: Str
			Name of a taxon, with associated authorship
		canonicalname: Str
			Name of the taxon, without authorship (corresponds to canonicalNameWithMarkers in the GBIF DarwinCore format)
		authorship: Str
			Authorship associated with the taxon name
		tax_rank: Str
			Taxonomic level (from FORM to DOMAIN)
		cd_parent: Int
			Identitificator of the parent taxon
		parentname: Str
			Name of the direct parent taxon
		cd_accepted: Int
			Identificator of the accepted taxon
		acceptedname: Str
			Name of the accepted taxon
		status: Str
			Taxonomic status of a taxon
		gbifkey: Int
			Identificator of a taxon in the GBIF backbone
		hasEndemStatus: Bool
			Whether the taxon has an endemism status in the database
		hasExotStatus: Bool
			Whether the taxon has an alien/invasive status in the database
		hasThreatStatus: Bool
			Whether the taxon has a threat status in the database
        """
        conn=psycopg2.connect(DATABASE_URL, sslmode='require')
        if not taxInput.get('cd_tax'):
            taxInput.update(manageInputTax(connection=conn,insert=False,**taxInput))
        taxOutput = getTax(conn,taxInput.get('cd_tax'))
        return taxOutput

class TestEndem(Resource):
    @use_kwargs(input_args.TestEndemGetArgs,location="query")
    @use_kwargs(input_args.TestEndemGetArgs,location="json")
    def get(self, **inputArgs):
        """
        Description
		-----------
		Look for a species. If the found species has an endemism status, returns its status and associated references

		Optional arguments
		------------------
		gbifkey: Int
			Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
		scientificname: Str
			Complete name of a taxon, with authorship
		canonicalname: Str
			Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format

		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
		alreadyInDb: Bool
			Whether the taxon was already in the database when the endpoint was accessed
		foundGbif: Bool
			Whether the taxon was found in GBIF
		matchedname: Str
			Name of the taxon matched with the provided one, in the API database, or from the GBIF API
		acceptedname: Str
			Name of the accepted taxon
		gbifkey: Int
			Identificator of a taxon in the GBIF backbone
		syno: Bool
			Whether a taxon is a synonym
		insertedTax: List(Int)
			List of inserted taxa
		hasEndemStatus: Bool
			Whether the taxon has an endemism status in the database
		cd_status: Str
			Status of the species (IUCN threat status, or description of the endemism level)
		comments: Str
			Comments on the taxon status
		references: List(Str)
			List of blibliographic references
		links: List(Str)
			List of internet links (URLs) for resources (usually datasets or pdf) associated with a bibliographic reference
        """
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
        """
        Description
		-----------
		Look for a species. If the found species has an exotic status, returns its status and associated references

		Optional arguments
		------------------
		gbifkey: Int
			Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
		scientificname: Str
			Complete name of a taxon, with authorship
		canonicalname: Str
			Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format

		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
		alreadyInDb: Bool
			Whether the taxon was already in the database when the endpoint was accessed
		foundGbif: Bool
			Whether the taxon was found in GBIF
		matchedname: Str
			Name of the taxon matched with the provided one, in the API database, or from the GBIF API
		acceptedname: Str
			Name of the accepted taxon
		gbifkey: Int
			Identificator of a taxon in the GBIF backbone
		syno: Bool
			Whether a taxon is a synonym
		insertedTax: List(Int)
			List of inserted taxa
		hasExotStatus: Bool
			Whether the taxon has an alien/invasive status in the database
		is_alien: Bool
			Whether a taxon is alien for Colombia (part of the exotic status)
		is_invasive: Bool
			Whether a taxo is invasive in Colombia (part of the exotic status)
		comments: Str
			Comments on the taxon status
		references: List(Str)
			List of blibliographic references
		links: List(Str)
			List of internet links (URLs) for resources (usually datasets or pdf) associated with a bibliographic reference
        """
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
        """
        Description
		-----------
		Look for a species. If the found species has an threat status, returns its status and associated references
		
		Optional arguments
		------------------
		gbifkey: Int
			Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
		scientificname: Str
			Complete name of a taxon, with authorship
		canonicalname: Str
			Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format

		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
		alreadyInDb: Bool
			Whether the taxon was already in the database when the endpoint was accessed
		foundGbif: Bool
			Whether the taxon was found in GBIF
		matchedname: Str
			Name of the taxon matched with the provided one, in the API database, or from the GBIF API
		acceptedname: Str
			Name of the accepted taxon
		gbifkey: Int
			Identificator of a taxon in the GBIF backbone
		syno: Bool
			Whether a taxon is a synonym
		insertedTax: List(Int)
			List of inserted taxa
		hasThreatStatus: Bool
			Whether the taxon has a threat status in the database
		cd_status: Str
			Status of the species (IUCN threat status, or description of the endemism level)
		comments: Str
			Comments on the taxon status
		references: List(Str)
			List of blibliographic references
		links: List(Str)
			List of internet links (URLs) for resources (usually datasets or pdf) associated with a bibliographic reference
        """
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
        """
        Description
		-----------
		Returns of exotic taxa and associated reference. Without argument, returns the complete list. With the “childrenOf” argument, returns only the taxa from a taxonomic clade.  Export format may be JSON or CSV
		
		Optional arguments
		------------------
		childrenOf: Str
			canonicalname or scientificname of the parent taxon for which we want to get the list of children taxa (and their statuses)
		format: Str
			JSON or CSV format in GET methods
		
		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
		scientificname: Str
			Name of a taxon, with associated authorship
		parentname: Str
			Name of the direct parent taxon
		tax_rank: Str
			Taxonomic level (from FORM to DOMAIN)
		gbifkey: Int
			Identificator of a taxon in the GBIF backbone
		synonyms: List(Str)
			List of synonyms associated with a taxon
		is_alien: Bool
			Whether a taxon is alien for Colombia (part of the exotic status)
		is_invasive: Bool
			Whether a taxo is invasive in Colombia (part of the exotic status)
		comments: Str
			Comments on the taxon status
		references: List(Str)
			List of blibliographic references
		links: List(Str)
			List of internet links (URLs) for resources (usually datasets or pdf) associated with a bibliographic reference
        """
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
        """
        Description
		-----------
		Returns of endemic taxa and associated reference. Without argument, returns the complete list. With the “childrenOf” argument, returns only the taxa from a taxonomic clade.  Export format may be JSON or CSV

		Optional arguments
		------------------
		childrenOf: Str
			canonicalname or scientificname of the parent taxon for which we want to get the list of children taxa (and their statuses)
		format: Str
			JSON or CSV format in GET methods

		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
		scientificname: Str
			Name of a taxon, with associated authorship
		parentname: Str
			Name of the direct parent taxon
		tax_rank: Str
			Taxonomic level (from FORM to DOMAIN)
		gbifkey: Int
			Identificator of a taxon in the GBIF backbone
		synonyms: List(Str)
			List of synonyms associated with a taxon
		cd_status: Str
			Status of the species (IUCN threat status, or description of the endemism level)
		comments: Str
			Comments on the taxon status
		references: List(Str)
			List of blibliographic references
		links: List(Str)
			List of internet links (URLs) for resources (usually datasets or pdf) associated with a bibliographic reference
        """
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
        """
        Description
		-----------
		Returns of threatened taxa and associated reference. Without argument, returns the complete list. With the “childrenOf” argument, returns only the taxa from a taxonomic clade.  Export format may be JSON or CSV
		
		Optional arguments
		------------------
		childrenOf: Str
			canonicalname or scientificname of the parent taxon for which we want to get the list of children taxa (and their statuses)
		format: Str
			JSON or CSV format in GET methods

		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
		scientificname: Str
			Name of a taxon, with associated authorship
		parentname: Str
			Name of the direct parent taxon
		tax_rank: Str
			Taxonomic level (from FORM to DOMAIN)
		gbifkey: Int
			Identificator of a taxon in the GBIF backbone
		synonyms: List(Str)
			List of synonyms associated with a taxon
		cd_status: Str
			Status of the species (IUCN threat status, or description of the endemism level)
		comments: Str
			Comments on the taxon status
		references: List(Str)
			List of blibliographic references
		links: List(Str)
			List of internet links (URLs) for resources (usually datasets or pdf) associated with a bibliographic reference
        """
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
        """
        Description
		-----------
		Returns a list of tax integrated in the API database.  Without argument, returns the complete list. With the “childrenOf” argument, returns only the taxa from a taxonomic clade.  Export format may be JSON or CSV

		Optional arguments
		------------------
		childrenOf: Str
			canonicalname or scientificname of the parent taxon for which we want to get the list of children taxa (and their statuses)
		format: Str
			JSON or CSV format in GET methods

		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
		scientificname: Str
			Name of a taxon, with associated authorship
		canonicalname: Str
			Name of the taxon, without authorship (corresponds to canonicalNameWithMarkers in the GBIF DarwinCore format)
		authorship: Str
			Authorship associated with the taxon name
		tax_rank: Str
			Taxonomic level (from FORM to DOMAIN)
		cd_parent: Int
			Identitificator of the parent taxon
		parentname: Str
			Name of the direct parent taxon
		cd_accepted: Int
			Identificator of the accepted taxon
		acceptedname: Str
			Name of the accepted taxon
		status: Str
			Taxonomic status of a taxon
		gbifkey: Int
			Identificator of a taxon in the GBIF backbone
		hasEndemStatus: Bool
			Whether the taxon has an endemism status in the database
		hasExotStatus: Bool
			Whether the taxon has an alien/invasive status in the database
		hasThreatStatus: Bool
			Whether the taxon has a threat status in the database
        """
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
        """
        Description
		-----------
		Returns a list of bibliographic references from the database, with the number of taxa with statuses (endemism, alien and threatened). Format may be JSON or CSV
		
		Optional arguments
		------------------
		onlyExot: Bool
			Whether to returns only the exotic-related references
		onlyEndem: Bool
			Whether to returns only the endemism-related references
		onlyThreat: Bool
			Whether to returns only the threat-related references
		
		Returns
		-----------
		cd_ref: Int
			Identificator of the bibliographic reference
		ref_citation: Str
			Bibliographic reference descriptor
		link: Str
			Internet link for resources (usually datasets or pdf) associated with a bibliographic reference
		nbExot: Int
			Number of exotic taxa associated with a bibliographic reference
		nbEndem: Int
			Number of endemic taxa associated with a bibliographic reference
		nbThreat: Int
			Number of threatened taxa associated with a bibliographic reference
        """
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
        """
        Description
		-----------
		Add references to an endemic status, or insert references and status if the taxon has no status yet. If the taxon is not yet in the database, insert the taxon as well (by the same process as in the /manageTaxo endpoint). The optional parameter “priority” control the behavior of the function when the endemic status already exists in the database: if “high”, replace the preexisting status, if low, only add new references. If not provided, or null, and the status from the database is different from the provided status, returns an error and no modification is applied in the database.

		Required arguments
		--------------------
		endemstatus: Str
			Endemic status to insert or edit in the database
		ref_citation: List(Str)
			Bibliographic references justifying the status of a taxon
		
		Optional arguments
		------------------
		gbifkey: Int
			Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
		scientificname: Str
			Complete name of a taxon, with authorship
		canonicalname: Str
			Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format
		authorship: Str
			Authorship of a taxon (usually corresponds to the difference between scientificname and canonicalname)
		syno: Bool
			Whether the taxon is a synonym
		parentgbifkey: Int
			gbifkey of the parent taxon
		parentcanonicalname: Str
			canonicalname of the parent taxon
		parentscientificname: Str
			scientificname of the parent taxon
		synogbifkey: Int
			Accepted taxon gbifkey (when the sent taxon is a synonym)
		synocanonicalname: Str
			Accepted taxon canonicalname (when the sent taxon is a synonym)
		synoscientificname: Str
			Accepted taxon scientificname (when the sent taxon is a synonym)
		link: List(Str)
			Link, or link list for the resources associated with a bibliographic reference which justify the status of a taxon (if provided, it needs to have the same length as ref_citation)
		comments: Str
			Comments and supplementary information about a taxon status
		replace_comment: Bool
			Whether to delete the preexisting comment in a taxon status, before inserting the provided comments
		priority: Str
			“high” if the provided status is prioritary on (must replace) the preexisting status, “low” if the preexisting status should not be modified (in this case only the new references are added in the database)

		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
		alreadyInDb: Bool
			Whether the taxon was already in the database when the endpoint was accessed
		foundGbif: Bool
			Whether the taxon was found in GBIF
		matchedname: Str
			Name of the taxon matched with the provided one, in the API database, or from the GBIF API
		acceptedname: Str
			Name of the accepted taxon
		gbifkey: Int
			Identificator of a taxon in the GBIF backbone
		syno: Bool
			Whether a taxon is a synonym
		insertedTax: List(Int)
			List of inserted taxa
		cd_status: Str
			Status of the species (IUCN threat status, or description of the endemism level)
		cd_refs: List(Int)
			List of identificators of bibliographic references
        """
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        res = manageInputTax(connection=conn, insert=True,**inputEndem)
        res.update(manageInputEndem(res.get('cd_tax_acc'), connection = conn, **inputEndem))
        return res
    
    @auth.login_required(role='edit')
    def delete(self,**inputEndem):
        """
        Description
		-----------
		Delete a link between a taxon and its endemic status, or the status of a taxon.

		Required arguments
		--------------------
		cd_tax: Int
			Identificator of a taxon in the database

		Optional arguments
		------------------
		cd_ref: Int
			Identificator of a bibliographic reference
		delete_status: Bool
			Whether to suppress the whole status of a taxon in the delete methods (if negative or null, only the association between a reference and a status is deleted)

		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
		cd_refs: List(Int)
			List of identificators of bibliographic references
        """
        pass
    
    @auth.login_required(role='edit')
    def put(self,**inputEndem):
        """
        Description
		-----------
		Modify the parameters of an endemic status of a species, and insert the references associated with the new endemic status

		Required arguments
		--------------------
		cd_tax: Int
			Identificator of a taxon in the database
		endemstatus: Str
			Endemic status to insert or edit in the database
		ref_citation: List(Str)
			Bibliographic references justifying the status of a taxon
		
		Optional arguments
		------------------
		link: List(Str)
			Link, or link list for the resources associated with a bibliographic reference which justify the status of a taxon (if provided, it needs to have the same length as ref_citation)
		comments: Str
			Comments and supplementary information about a taxon status
		replace_comment: Bool
			Whether to delete the preexisting comment in a taxon status, before inserting the provided comments

		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
		cd_refs: List(Int)
			List of identificators of bibliographic references
        """
        pass

class ManageExot(Resource):
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageExotPostArgs)
    def post(self, **inputExot):
        """
        """
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        res = manageInputTax(connection=conn, insert=True, **inputExot)
        res.update(manageInputExot(res.get('cd_tax_acc'), connection = conn, **inputExot))
        return res
    
class ManageThreat(Resource):
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageThreatPostArgs)
    def post(self, **inputThreat):
        """
        Description
		-----------
		Add references to an exotic (alien/invasive) status, or insert references and status if the taxon has no status yet. If the taxon is not yet in the database, insert the taxon as well (by the same process as in the /manageTaxo endpoint). The optional parameter “priority” control the behavior of the function when the exotic status already exists in the database: if “high”, replace the preexisting status, if low, only add new references. If not provided, or null, and the status from the database is different from the provided status, returns an error and no modification is applied in the database.
		

		Required arguments
		--------------------
		is_alien: Bool
			Part of the exotic status of a taxon: is it considered alien in Colombia?
		is_invasive: Bool
			Part of the exotic status of a taxon: is it considered invasive in Colombia?
		ref_citation: List(Str)
			Bibliographic references justifying the status of a taxon
		

		Optional arguments
		------------------
		gbifkey: Int
			Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
		scientificname: Str
			Complete name of a taxon, with authorship
		canonicalname: Str
			Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format
		authorship: Str
			Authorship of a taxon (usually corresponds to the difference between scientificname and canonicalname)
		syno: Bool
			Whether the taxon is a synonym
		parentgbifkey: Int
			gbifkey of the parent taxon
		parentcanonicalname: Str
			canonicalname of the parent taxon
		parentscientificname: Str
			scientificname of the parent taxon
		synogbifkey: Int
			Accepted taxon gbifkey (when the sent taxon is a synonym)
		synocanonicalname: Str
			Accepted taxon canonicalname (when the sent taxon is a synonym)
		synoscientificname: Str
			Accepted taxon scientificname (when the sent taxon is a synonym)
		link: List(Str)
			Link, or link list for the resources associated with a bibliographic reference which justify the status of a taxon (if provided, it needs to have the same length as ref_citation)
		comments: Str
			Comments and supplementary information about a taxon status
		replace_comment: Bool
			Whether to delete the preexisting comment in a taxon status, before inserting the provided comments
		priority: Str
			“high” if the provided status is prioritary on (must replace) the preexisting status, “low” if the preexisting status should not be modified (in this case only the new references are added in the database)
		

		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
		alreadyInDb: Bool
			Whether the taxon was already in the database when the endpoint was accessed
		foundGbif: Bool
			Whether the taxon was found in GBIF
		matchedname: Str
			Name of the taxon matched with the provided one, in the API database, or from the GBIF API
		acceptedname: Str
			Name of the accepted taxon
		gbifkey: Int
			Identificator of a taxon in the GBIF backbone
		syno: Bool
			Whether a taxon is a synonym
		insertedTax: List(Int)
			List of inserted taxa
		is_alien: Bool
			Whether a taxon is alien for Colombia (part of the exotic status)
		is_invasive: Bool
			Whether a taxo is invasive in Colombia (part of the exotic status)
		cd_refs: List(Int)
			List of identificators of bibliographic references
        """
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        res = manageInputTax(connection=conn, insert=True,**inputThreat)
        res.update(manageInputThreat(res.get('cd_tax_acc'), connection = conn, **inputThreat))
        conn.close()
        return res

class ManageTax(Resource):
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageTaxoPostArgs)
    def post(self,**dictInput):
        """
        Description
		-----------
		Insert a taxon in the datababase (with its accepted taxon, if synonym, and parent taxa)

		Optional arguments
		------------------
		gbifkey: Int
			Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
		scientificname: Str
			Complete name of a taxon, with authorship
		canonicalname: Str
			Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format
		authorship: Str
			Authorship of a taxon (usually corresponds to the difference between scientificname and canonicalname)
		syno: Bool
			Whether the taxon is a synonym
		parentgbifkey: Int
			gbifkey of the parent taxon
		parentcanonicalname: Str
			canonicalname of the parent taxon
		parentscientificname: Str
			scientificname of the parent taxon
		synogbifkey: Int
			Accepted taxon gbifkey (when the sent taxon is a synonym)
		synocanonicalname: Str
			Accepted taxon canonicalname (when the sent taxon is a synonym)
		synoscientificname: Str
			Accepted taxon scientificname (when the sent taxon is a synonym)
		

		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
		alreadyInDb: Bool
			Whether the taxon was already in the database when the endpoint was accessed
		foundGbif: Bool
			Whether the taxon was found in GBIF
		matchedname: Str
			Name of the taxon matched with the provided one, in the API database, or from the GBIF API
		acceptedname: Str
			Name of the accepted taxon
		gbifkey: Int
			Identificator of a taxon in the GBIF backbone
		syno: Bool
			Whether a taxon is a synonym
		insertedTax: List(Int)
			List of inserted taxa
        """
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        res = manageInputTax(connection=conn, insert=True,**dictInput)
        conn.close()
        return res
    
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageTaxoDeleteArgs)
    def delete(self,**delTaxArgs):
        """
        Description
		-----------
		Delete a taxon and its statuses in the database. Note that if the taxon has synonyms and/or children taxa, it might cause problems in the app. Use carefully.
		
		Required arguments
		--------------------
		cd_tax: Int
			Identificator of a taxon in the database

		Optional arguments
		------------------
		gbifkey: Int
			Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
		scientificname: Str
			Complete name of a taxon, with authorship
		canonicalname: Str
			Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format

		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
		cd_children: List(Int)
			List of identificators of children taxa
		cd_synos: List(Int)
			List of synonym identificators
        """
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
        """
        Description
		-----------
		Modify a taxon in the database, if the arguments gbifkey, parentgbifkey, or synogbifkey are provided, information is extracted from GBIF. Otherwise the information concerning the taxon is extracted from provided arguments
		

		Required arguments
		--------------------
		cd_tax: Int
			Identificator of a taxon in the database
		

		Optional arguments
		------------------
		gbifkey: Int
			Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
		scientificname: Str
			Complete name of a taxon, with authorship
		canonicalname: Str
			Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format
		authorship: Str
			Authorship of a taxon (usually corresponds to the difference between scientificname and canonicalname)
		syno: Bool
			Whether the taxon is a synonym
		parentgbifkey: Int
			gbifkey of the parent taxon
		parentcanonicalname: Str
			canonicalname of the parent taxon
		parentscientificname: Str
			scientificname of the parent taxon
		synogbifkey: Int
			Accepted taxon gbifkey (when the sent taxon is a synonym)
		synocanonicalname: Str
			Accepted taxon canonicalname (when the sent taxon is a synonym)
		synoscientificname: Str
			Accepted taxon scientificname (when the sent taxon is a synonym)
		status: Str
			Taxonomic status (ACCEPTED, DOUBTFUL or SYNONYM) Note: doubtful synonym are “SYNONYM”
		reference: Str
			Bibliographic references for the taxonomic status of a taxon
		link: List(Str)
			Link, or link list for the resources associated with a bibliographic reference which justify the status of a taxon (if provided, it needs to have the same length as ref_citation)
		cd_ref: Int
			Identificator of a bibliographic reference
		

		Returns
		-----------
		cd_tax: Int
			Identificator of a taxon in the API database
        """
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
