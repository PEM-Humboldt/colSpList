from io import BytesIO
from flask import Flask, render_template, jsonify, g, send_file, abort
from flask_restful import Resource, Api
from taxo import manageInputTax, get_gbif_parsed_from_sci_name, childrenList, checkCdTax, deleteTaxo, modifyTaxo
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from security import new_user, delete_user, valid_password, user_exists, get_user, generate_auth_token, verify_auth_token, grant_user, revoke_user, grant_edit, revoke_edit, grant_admin, revoke_admin,change_password, get_user_list
from errors_def import Abort500Error
from manageStatus import manageInputThreat, manageInputEndem, manageInputExot
from getStatus import testEndemStatus, testExotStatus, testThreatStatus, getListExot, getListEndem, getListThreat, getListTax, getListReferences, getTax
from error_handling import testEndemGet_err_hand, testExotGet_err_hand, testThreatGet_err_hand, ListEndem_err_hand, ListThreat_err_hand, ListExot_err_hand, ListTax_err_hand, GetTaxon_err_hand, ListTax_err_hand, ListRef_err_hand, cleanDbDel_err_hand, userPost_err_hand, userPut_err_hand,adminUserDel_err_hand, adminUserGet_err_hand, manageTaxPost_err_hand,manageTaxDel_err_hand, manageTaxPut_err_hand, manageEndemPost_err_hand,manageEndemDel_err_hand,manageEndemPut_err_hand,manageExotPost_err_hand, manageExotDel_err_hand, manageExotPut_err_hand, manageThreatPost_err_hand, manageThreatDel_err_hand, manageThreatPut_err_hand, manageRefDel_err_hand, manageRefPut_err_hand, adminUserPut_err_hand
from webargs import fields, validate,missing
from webargs.flaskparser import parser
from webargs.flaskparser import use_args,use_kwargs,abort
from flask_httpauth import HTTPBasicAuth
import psycopg2
import psycopg2.extras
import os
import input_args


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

@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(422, errors=str(err))


# performance
class CleanDb(Resource):

    @auth.login_required(role=['edit','admin'])
    @use_kwargs(input_args.CleanDbDeleteArgs,location="query")
    @use_kwargs(input_args.CleanDbDeleteArgs,location="json")
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
        try:
            conn=psycopg2.connect(DATABASE_URL, sslmode='require')
            res=cleanDbDel_err_hand(conn,**cdbArgs)
            return res
        finally:
            conn.close()
        
class Performance(Resource):

    @auth.login_required(role=['admin'])
    @use_kwargs(input_args.PerformancePutArgs)
    def put(self,**perfArgs):
        """
        Description
        -----------:        
		Run VACUUM and/or ANALYSE in the postgres database

		Required arguments
		--------------------
		vacuum: Bool
			Run the VACUUM command of the postgreSQL database
		analysis: Bool
			Run the ANALYSIS command in the postgreSQL database
        """
        try:
            conn=psycopg2.connect(DATABASE_URL, sslmode='require')
            conn.set_isolation_level(0)
            if perfArgs.get('vacuum'):
                SQL = 'VACUUM '
            if perfArgs.get('analyse'):
                SQL += 'ANALYSE'
            cur=conn.cursor()
            cur.execute(SQL)
            conn.commit()
        finally:
            conn.close()
        
# security
class User(Resource):

    @use_kwargs(input_args.UserPostArgs)
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
        try:
            conn=psycopg2.connect(DATABASE_URL, sslmode='require')
            res = userPost_err_hand(conn, **userArgs)
            return res
        finally:
            conn.close()
    
    @auth.login_required
    @use_kwargs(input_args.UserGetArgs)
    def get(self,**userArgs):
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
        try:
            conn=psycopg2.connect(DATABASE_URL, sslmode='require')
            user=g.get('user')
            if userArgs.get('create_token'):
                token = generate_auth_token(conn,g.user.get('id')).decode('ascii')
                user['token']=token
            user['uid'] = user.pop('id')
            return user
        finally:
            conn.close()
    
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
        try:
            user=g.get('user')
            conn=psycopg2.connect(DATABASE_URL, sslmode='require')
            res= adminUserDel_err_hand(connection=conn,**user) # Note we use the same function and user handler than in the case of the deletion by an admin
            return res
        finally:
            conn.close()
    
    @use_kwargs(input_args.UserPutArgs)
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
        try:
            conn=psycopg2.connect(DATABASE_URL, sslmode='require')
            return userPut_err_hand(conn,**newPassword)
        finally:
            conn.close()
    
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
        try:
            conn=psycopg2.connect(DATABASE_URL, sslmode='require')
            res= adminUserDel_err_hand(conn,**userArgs)
            return res
        finally:
            conn.close()
    
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
        try:
            conn=psycopg2.connect(DATABASE_URL, sslmode='require')
            user_list=adminUserGet_err_hand(conn)
            return user_list
        finally:
            conn.close()
    
    @auth.login_required(role='admin')
    @use_kwargs(input_args.AdminUsersPutArgs)
    #@use_kwargs(input_args.AdminUsersPutArgs,location="json")
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
        try:
            conn=psycopg2.connect(DATABASE_URL, sslmode='require')
            res=adminUserPut_err_hand(conn,**modifyArgs)
            return res
        finally:
            conn.close()

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
        try:
            conn=psycopg2.connect(DATABASE_URL, sslmode='require')
            res = GetTaxon_err_hand(conn,**taxInput)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

"""Multiple version for the getTaxon class"""
class ListGetTaxon(Resource):
    @use_kwargs(input_args.MultiTaxGetArgs,location="query")
    @use_kwargs(input_args.MultiTaxGetArgs,location="json")
    def post(self,**inputTax):
        try:
            conn=psycopg2.connect(DATABASE_URL, sslmode='require')
            res=[GetTaxon_err_hand(conn, **i) for i in inputTax.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()


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
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res=testEndemGet_err_hand(conn, **inputArgs)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

class ListTestEndem(Resource):
    """
    same as previous but for multiple tests as once.
    Input arguments must be in a dictionary with one element:'list' which contains a JSON list of all element described previously
    """
    @use_kwargs(input_args.ListTestEndemGetArgs, location="json")
    def post(self,**inputList):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res=[testEndemGet_err_hand(conn, **i) for i in inputList.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

        
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
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = testExotGet_err_hand(connection=conn,**inputArgs)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

class ListTestExot(Resource):
    """
    same as previous but for multiple tests as once.
    Input arguments must be in a dictionary with one element:'list' which contains a JSON list of all element described previously
    """
    @use_kwargs(input_args.ListTestExotGetArgs, location="json")
    def post(self,**inputList):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res=[testExotGet_err_hand(conn, **i) for i in inputList.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

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
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = testThreatGet_err_hand(connection=conn,**inputArgs)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

class ListTestThreat(Resource):
    """
    same as previous but for multiple tests as once.
    Input arguments must be in a dictionary with one element:'list' which contains a JSON list of all element described previously
    """
    @use_kwargs(input_args.ListTestThreatGetArgs, location="json")
    def post(self,**inputList):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res=[testThreatGet_err_hand(conn, **i) for i in inputList.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

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
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = ListExot_err_hand(conn,**listArgs)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()
            
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
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = ListEndem_err_hand(conn,**listArgs)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()


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
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = ListThreat_err_hand(conn,**listArgs)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

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
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = ListTax_err_hand(conn, **listArgs)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

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
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = ListRef_err_hand(conn,**listRefArgs)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

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
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = manageEndemPost_err_hand(connection=conn, **inputEndem)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()
    
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageEndemDeleteArgs)
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
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = manageEndemDel_err_hand(connection=conn, **inputEndem)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()
    
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageEndemPutArgs)
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
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = manageEndemPut_err_hand(connection=conn, **inputEndem)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

class ManageExot(Resource):
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageExotPostArgs)
    def post(self, **inputExot):
        """
        """
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = manageExotPost_err_hand(connection=conn, **inputExot)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageExotDeleteArgs)
    def delete(self, **inputExot):
        """
        """
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = manageExotDel_err_hand(connection=conn, **inputExot)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageExotPutArgs)
    def put(self, **inputExot):
        """
        """
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = manageExotPut_err_hand(connection=conn, **inputExot)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()
    
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
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = manageThreatPost_err_hand(connection=conn, **inputThreat)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageThreatDeleteArgs)
    def delete(self, **inputThreat):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = manageThreatDel_err_hand(connection=conn, **inputThreat)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageThreatPutArgs)
    def put(self, **inputThreat):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = manageThreatPut_err_hand(connection=conn, **inputThreat)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

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
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = manageTaxPost_err_hand(conn,**dictInput)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()
    
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
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = manageTaxDel_err_hand(conn,**delTaxArgs)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()
        
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
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = manageTaxPut_err_hand(conn,**putTaxArgs)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()
        
class ManageRef(Resource):
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageRefDeleteArgs)
    def delete(self, **delRefArgs):
        try:
            conn=psycopg2.connect(DATABASE_URL, sslmode='require')
            res= manageRefDel_err_hand(conn,**delRefArgs)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

    @auth.login_required(role='edit')
    @use_kwargs(input_args.ManageRefPutArgs)
    def put(self,**putRefArgs):
        try:
            conn=psycopg2.connect(DATABASE_URL, sslmode='require')
            res=manageRefPut_err_hand(conn,**putRefArgs)
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()
    
 

"""
multiple version of manageTax
"""
class MultiManageTax(Resource):
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ListManageTaxoPostArgs)
    def post(self,**multiManageTaxPostArgs):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = [manageTaxPost_err_hand(conn,**i) for i in multiManageTaxPostArgs.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

    @auth.login_required(role='edit')
    @use_kwargs(input_args.ListManageTaxoDeleteArgs)
    def delete(self,**multiManageTaxDelArgs):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = [manageTaxDel_err_hand(conn,**i) for i in multiManageTaxDelArgs.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

    @auth.login_required(role='edit')
    @use_kwargs(input_args.ListManageTaxoPutArgs)
    def put(self,**multiManageTaxPutArgs):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = [manageTaxPut_err_hand(conn,**i) for i in multiManageTaxPutArgs.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()
        

"""
multiple version of manageEndem
"""
class MultiManageEndem(Resource):
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ListManageEndemPostArgs)
    def post(self,**multiManageEndemPostArgs):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = [manageEndemPost_err_hand(conn,**i) for i in multiManageEndemPostArgs.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

    @auth.login_required(role='edit')
    @use_kwargs(input_args.ListManageEndemDeleteArgs)
    def delete(self,**multiManageEndemDelArgs):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = [manageEndemDel_err_hand(conn,**i) for i in multiManageEndemDelArgs.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

    @auth.login_required(role='edit')
    @use_kwargs(input_args.ListManageEndemPutArgs)
    def put(self,**multiManageEndemPutArgs):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = [manageEndemPut_err_hand(conn,**i) for i in multiManageEndemPutArgs.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()
        

"""
multiple version of manageExot
"""
class MultiManageExot(Resource):
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ListManageExotPostArgs)
    def post(self,**multiManageExotPostArgs):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = [manageExotPost_err_hand(conn,**i) for i in multiManageExotPostArgs.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

    @auth.login_required(role='edit')
    @use_kwargs(input_args.ListManageExotDeleteArgs)
    def delete(self,**multiManageExotDelArgs):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = [manageExotDel_err_hand(conn,**i) for i in multiManageExotDelArgs.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

    @auth.login_required(role='edit')
    @use_kwargs(input_args.ListManageExotPutArgs)
    def put(self,**multiManageExotPutArgs):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = [manageExotPut_err_hand(conn,**i) for i in multiManageExotPutArgs.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()
        

"""
multiple version of manageThreat
"""
class MultiManageThreat(Resource):
    @auth.login_required(role='edit')
    @use_kwargs(input_args.ListManageThreatPostArgs)
    def post(self,**multiManageThreatPostArgs):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = [manageThreatPost_err_hand(conn,**i) for i in multiManageThreatPostArgs.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

    @auth.login_required(role='edit')
    @use_kwargs(input_args.ListManageThreatDeleteArgs)
    def delete(self,**multiManageThreatDelArgs):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = [manageThreatDel_err_hand(conn,**i) for i in multiManageThreatDelArgs.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

    @auth.login_required(role='edit')
    @use_kwargs(input_args.ListManageThreatPutArgs)
    def put(self,**multiManageThreatPutArgs):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            res = [manageThreatPut_err_hand(conn,**i) for i in multiManageThreatPutArgs.get('list')]
        except Abort500Error as e:
            abort(500,str(e))
        else:
            return res
        finally:
            conn.close()

"""
multiple version of manageReferences
"""
class ListManageRef(Resource):
    @auth.login_required(role='edit')
    @use_kwargs(input_args.MultiManageRefDeleteArgs)
    def delete(self, **delMultiRefArgs):
        try:
            conn=psycopg2.connect(DATABASE_URL, sslmode='require')
            res = [manageRefDel_err_hand(conn,**i) for i in delMultiRefArgs.get('list')]
            return res
        except Abort500Error as e:
            abort(500,str(e))
        finally:
            conn.close()

    @auth.login_required(role='edit')
    @use_kwargs(input_args.MultiManageRefPutArgs)
    def put(self,**putMultiRefArgs):
        try:
            conn=psycopg2.connect(DATABASE_URL, sslmode='require')
            res = [manageRefPut_err_hand(conn,**i) for i in putMultiRefArgs.get('list')]
            return res
        except Abort500Error as e:
            abort(500,str(e))
        finally:
            conn.close()

