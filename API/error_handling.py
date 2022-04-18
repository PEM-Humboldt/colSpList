"""
In this file we redirect the errors before passing them to the endpoints
We manage here 2 types of errors:
1. if the error is due to user input, the functions should returns a result consisting of a dictionary with a key 'error' and the explicative message for the user
2. if the error is due to a problem in the api code or database, the function raises a "Abort500Error" in order to indicate to the endpoint that it should use the abort method with the "500" html error code and the message from the initial error code
"""

from errors_def import MissingArgError, DatabaseUncompatibilityValueError, DatabaseUncompatibilityError, AlreadyExistsDbError, DeleteMissingElementDbError, ModifyMissingStatusDbError, TaxonNotFoundDbError, GrantExistingRightError, RevokeUnexistingRightError, UncompatibilityGbifKeyCanonicalname, DbIntegrityError, UncompatibleStatusError, UnauthorizedValueError,UncompatibilityCdTaxInputTaxError, ModifyMissingRefDbError, UserNotFoundError, Abort500Error
from taxo import manageInputTax, get_gbif_parsed_from_sci_name,childrenList,deleteTaxo, checkCdTax,modifyTaxo
from flask import abort, g
from getStatus import testEndemStatus, testExotStatus, testThreatStatus, getListTax,getListExot, getListEndem, getListThreat, getTax, getListReferences
from manageStatus import manageSource,deleteRef,mergeRefs, modifyRef, deleteExot, deleteEndem,deleteThreat,modifyEndem,modifyThreat,modifyExot,manageInputEndem,manageInputThreat,manageInputExot
from security import new_user, delete_user, valid_password, user_exists, get_user, generate_auth_token, verify_auth_token, grant_user, revoke_user, grant_edit, revoke_edit, grant_admin, revoke_admin,change_password, get_user_list
from admin import delReference_no_status,delTaxo_no_status,delStatus_no_reference,delSyno_no_tax
import psycopg2
from psycopg2 import sql
import psycopg2.extras
from io import BytesIO
from flask import send_file

def testEndemGet_err_hand(connection, **testEndemArgs):
    """
    Description
    -----------
    Look for a species. If the found species has an endemism status, returns its status and associated references
    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    testEndemArgs: dict
        Dictionary with the following elements:
        gbifkey: Int [optional]
            Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
        scientificname: Str [optional]
            Complete name of a taxon, with authorship
        canonicalname: Str [optional]
            Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format

    Returns
    -----------
    cd_tax: Int
        Identifier of a taxon in the API database
    cd_tax_acc: Int
        Identifier of the accepted taxon
    alreadyInDb: Bool
        Whether the taxon was already in the database when the endpoint was accessed
    foundGbif: Bool
        Whether the taxon was found in GBIF
    matchedname: Str
        Name of the taxon matched with the provided one, in the API database, or from the GBIF API
    acceptedname: Str
        Name of the accepted taxon
    gbifkey: Int
        Identifier of a taxon in the GBIF backbone
    syno: Bool
        Whether a taxon is a synonym
    insertedTax: List(Int)
        List of inserted taxa
    hasEndemStatus: Bool
        Whether the taxon has an endemism status in the database
    cd_nivel: Int
        Endemism level (from 0: unsuficient information to 4: endemic)
    endemism: Str
        Endemism level (Spanish)
    endemism_en: Str
        Endemism level (English)
    comments: Str
        Comments on the taxon status
    references: List(Str)
        List of blibliographic references
    links: List(Str)
        List of internet links (URLs) for resources (usually datasets or pdf) associated with a bibliographic reference
    """
    try:
        res = manageInputTax(connection=connection, insert=False, **testEndemArgs)
        if res.get('alreadyInDb'):
            res.update(testEndemStatus(connection,res.get('cd_tax_acc')))
        else:
            res.update({'hasEndemStatus':False,'cd_status':None,'comments':None,'references':list(),'links':list()})
    except (MissingArgError, UncompatibilityGbifKeyCanonicalname) as e:
        return {'error':str(e)}
    except UnauthorizedValueError as e:
        if e.var=='gbifMatchMode':
           raise Abort500Error(str(e)) from e
        else:
            return {'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res


def testExotGet_err_hand(connection, **testExotArgs):
    """
    Description
		-----------
		Look for a species. If the found species has an exotic status, returns its status and associated references
		
    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    testExotArgs: dict
        Dictionary with the following elements:
		gbifkey: Int [optional]
			Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
		scientificname: Str [optional]
			Complete name of a taxon, with authorship
		canonicalname: Str [optional]
			Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format

    Returns
    -----------
    cd_tax: Int
        Identifier of a taxon in the API database
    cd_tax_acc: Int
        Identifier of the accepted taxon
    alreadyInDb: Bool
        Whether the taxon was already in the database when the endpoint was accessed
    foundGbif: Bool
        Whether the taxon was found in GBIF
    matchedname: Str
        Name of the taxon matched with the provided one, in the API database, or from the GBIF API
    acceptedname: Str
        Name of the accepted taxon
    gbifkey: Int
        Identifier of a taxon in the GBIF backbone
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
        res = manageInputTax(connection=connection, insert=False, **testExotArgs)
        if res.get('alreadyInDb'):
            res.update(testExotStatus(connection,res.get('cd_tax_acc')))
        else:
            res.update({'hasExotStatus':False,'is_alien':None,'is_invasive':None,'comments':None,'references':list(),'links':list()})
    except (MissingArgError, UncompatibilityGbifKeyCanonicalname) as e:
        return {'error':str(e)}
    except UnauthorizedValueError as e:
        if e.var=='gbifMatchMode':
           raise Abort500Error(str(e)) from e
        else:
            return {'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def testThreatGet_err_hand(connection, **testThreatArgs):
    """
    Description
		-----------
		Look for a species. If the found species has an threat status, returns its status and associated references
    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    testThreatArgs: dict
        Dictionary with the following elements:
		gbifkey: Int [optional]
			Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
		scientificname: Str [optional]
			Complete name of a taxon, with authorship
		canonicalname: Str [optional]
			Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format

    Returns
    -----------
    cd_tax: Int
        Identifier of a taxon in the API database
    alreadyInDb: Bool
        Whether the taxon was already in the database when the endpoint was accessed
    foundGbif: Bool
        Whether the taxon was found in GBIF
    matchedname: Str
        Name of the taxon matched with the provided one, in the API database, or from the GBIF API
    acceptedname: Str
        Name of the accepted taxon
    gbifkey: Int
        Identifier of a taxon in the GBIF backbone
    syno: Bool
        Whether a taxon is a synonym
    insertedTax: List(Int)
        List of inserted taxa
    hasThreatStatus: Bool
        Whether the taxon has a threat status in the database
    cd_status: Str
        Status of the species (IUCN threat statusl)
    comments: Str
        Comments on the taxon status
    references: List(Str)
        List of blibliographic references
    links: List(Str)
        List of internet links (URLs) for resources (usually datasets or pdf) associated with a bibliographic reference
    """
    try:
        res = manageInputTax(connection=connection, insert=False, **testThreatArgs)
        if res.get('alreadyInDb'):
            res.update(testThreatStatus(connection,res.get('cd_tax_acc')))
        else:
            res.update({'hasThreatStatus':False,'cd_status':None,'comments':None,'references':list(),'links':list()})
    except (MissingArgError, UncompatibilityGbifKeyCanonicalname) as e:
        return {'error':str(e)}
    except UnauthorizedValueError as e:
        if e.var=='gbifMatchMode':
           raise Abort500Error(str(e)) from e
        else:
            return {'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res


def ListEndem_err_hand(connection, **listEndemArgs):
    """
    Description
	-----------
	Returns of endemic taxa and associated reference. Without argument, returns the complete list. With the “childrenOf” argument, returns only the taxa from a taxonomic clade.  Export format may be JSON or CSV

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    listEndemArgs: dict
        Dictionary with the following elements:
        childrenOf: Str [optional]
            canonicalname or scientificname of the parent taxon for which we want to get the list of children taxa (and their statuses)
        format: Str [optional]
            JSON or CSV format in GET methods

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	scientificname: Str
		Name of a taxon, with associated authorship
	parentname: Str
		Name of the direct parent taxon
	tax_rank: Str
		Taxonomic level (from FORM to DOMAIN)
	gbifkey: Int
		Identifier of a taxon in the GBIF backbone
	synonyms: List(Str)
		List of synonyms associated with a taxon
	endemism: Str
		Endemism level (Spanish)
	endemism_en: Str
		Endemism level (English)
	comments: Str
		Comments on the taxon status
	references: List(Str)
		List of blibliographic references
	links: List(Str)
		List of internet links (URLs) for resources (usually datasets or pdf) associated with a bibliographic reference
    """
    try:
        if listEndemArgs.get('childrenOf'):
            parsed = get_gbif_parsed_from_sci_name(listEndemArgs.get('childrenOf'))
            if parsed.get('scientificName') and parsed.get('canonicalNameComplete') and parsed.get('scientificName')==parsed.get('canonicalNameComplete'):
                parent=manageInputTax(connection=connection, insert=False,canonicalname=listEndemArgs.get('childrenOf'))
            else:
                parent=manageInputTax(connection=connection, insert=False,scientificname=listEndemArgs.get('childrenOf'))
            if parent.get('alreadyInDb'):
                cursor=connection.cursor()
                listChildren=childrenList(cursor,parent.get('cd_tax_acc'))
                cursor.close()
                res=getListEndem(connection=connection, listChildren=listChildren, formatExport=listEndemArgs.get('format'))
            else:
                raise TaxonNotFoundDbError(tax=listEndemArgs.get('childrenOf'), message='\'childrenOf\' taxon not recognized')
                #raise Exception("childrenOfNotFound")
        else:
            res = getListEndem(connection=connection, listChildren=[], formatExport=listEndemArgs.get('format'))
    except (TaxonNotFoundDbError, MissingArgError) as e:
        return {'error':str(e)}
    except (DbIntegrityError, UnauthorizedValueError) as e:
        raise Abort500Error(str(e)) from e
    else:
        if listEndemArgs.get('format')=="CSV":
            response_stream = BytesIO(res.to_csv().encode())
            return send_file(response_stream, mimetype = "text/csv", attachment_filename = "endemic.csv")
        else:
            return res

def ListExot_err_hand(connection, **listExotArgs):
    """
    Description
	-----------
	Returns of exotic taxa and associated reference. Without argument, returns the complete list. With the “childrenOf” argument, returns only the taxa from a taxonomic clade.  Export format may be JSON or CSV

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    listExotArgs: dict
        Dictionary with the following elements:
        childrenOf: Str [optional]
            canonicalname or scientificname of the parent taxon for which we want to get the list of children taxa (and their statuses)
        format: Str [optional]
            JSON or CSV format in GET methods
	
	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	scientificname: Str
		Name of a taxon, with associated authorship
	parentname: Str
		Name of the direct parent taxon
	tax_rank: Str
		Taxonomic level (from FORM to DOMAIN)
	gbifkey: Int
		Identifier of a taxon in the GBIF backbone
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
        if listExotArgs.get('childrenOf'):
            parsed = get_gbif_parsed_from_sci_name(listExotArgs.get('childrenOf'))
            if parsed.get('scientificName') and parsed.get('canonicalNameComplete') and parsed.get('scientificName')==parsed.get('canonicalNameComplete'):
                parent=manageInputTax(connection=connection, insert=False,canonicalname=listExotArgs.get('childrenOf'))
            else:
                parent=manageInputTax(connection=connection, insert=False,scientificname=listExotArgs.get('childrenOf'))
            if parent.get('alreadyInDb'):
                cursor=connection.cursor()
                listChildren=childrenList(cursor,parent.get('cd_tax_acc'))
                cursor.close()
                res=getListExot(connection=connection, listChildren=listChildren, formatExport=listExotArgs.get('format'))
            else:
                raise TaxonNotFoundDbError(tax=listExotArgs.get('childrenOf'), message='\'childrenOf\' taxon not recognized')
                #raise Exception("childrenOfNotFound")
        else:
            res = getListExot(connection=connection, listChildren=[], formatExport=listExotArgs.get('format'))
    except (TaxonNotFoundDbError, MissingArgError) as e:
        return {'error':str(e)}
    except (DbIntegrityError, UnauthorizedValueError) as e:
        raise Abort500Error(str(e)) from e
    else:
        if listExotArgs.get('format')=="CSV":
            response_stream = BytesIO(res.to_csv().encode())
            return send_file(response_stream, mimetype = "text/csv", attachment_filename = "exot.csv")
        else:
            return res

def ListThreat_err_hand(connection, **listThreatArgs):
    """
    Description
	-----------
	Returns of threatened taxa and associated reference. Without argument, returns the complete list. With the “childrenOf” argument, returns only the taxa from a taxonomic clade.  Export format may be JSON or CSV

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    listThreatArgs: dict
        Dictionary with the following elements:
        childrenOf: Str [optional]
            canonicalname or scientificname of the parent taxon for which we want to get the list of children taxa (and their statuses)
        format: Str [optional]
            JSON or CSV format in GET methods

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	scientificname: Str
		Name of a taxon, with associated authorship
	parentname: Str
		Name of the direct parent taxon
	tax_rank: Str
		Taxonomic level (from FORM to DOMAIN)
	gbifkey: Int
		Identifier of a taxon in the GBIF backbone
	synonyms: List(Str)
		List of synonyms associated with a taxon
	cd_status: Str
		Status of the species (IUCN threat statusl)
	comments: Str
		Comments on the taxon status
	references: List(Str)
		List of blibliographic references
	links: List(Str)
		List of internet links (URLs) for resources (usually datasets or pdf) associated with a bibliographic reference
    """
    try:
        if listThreatArgs.get('childrenOf'):
            parsed = get_gbif_parsed_from_sci_name(listThreatArgs.get('childrenOf'))
            if parsed.get('scientificName') and parsed.get('canonicalNameComplete') and parsed.get('scientificName')==parsed.get('canonicalNameComplete'):
                parent=manageInputTax(connection=connection, insert=False,canonicalname=listThreatArgs.get('childrenOf'))
            else:
                parent=manageInputTax(connection=connection, insert=False,scientificname=listThreatArgs.get('childrenOf'))
            if parent.get('alreadyInDb'):
                cursor=connection.cursor()
                listChildren=childrenList(cursor,parent.get('cd_tax_acc'))
                cursor.close()
                res=getListThreat(connection=connection, listChildren=listChildren, formatExport=listThreatArgs.get('format'))
            else:
                raise TaxonNotFoundDbError(tax=listThreatArgs.get('childrenOf'), message='\'childrenOf\' taxon not recognized')
                #raise Exception("childrenOfNotFound")
        else:
            res = getListThreat(connection=connection, listChildren=[], formatExport=listThreatArgs.get('format'))
    except (TaxonNotFoundDbError, MissingArgError) as e:
        return {'error':str(e)}
    except (DbIntegrityError, UnauthorizedValueError) as e:
        raise Abort500Error(str(e)) from e
    else:
        if listThreatArgs.get('format')=="CSV":
            response_stream = BytesIO(res.to_csv().encode())
            return send_file(response_stream, mimetype = "text/csv", attachment_filename = "threat.csv")
        else:
            return res

def GetTaxon_err_hand(connection, **taxInput):
    """
    Description
	-----------
	Returns the information about one taxon.

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    taxInput: dict
        Dictionary with the following elements:
        cd_tax: Int [optional]
            Identificator of a taxon in the database
        gbifkey: Int [optional]
            Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
        scientificname: Str [optional]
            Complete name of a taxon, with authorship
        canonicalname: Str [optional]
            Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
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
		Identifier of the accepted taxon
	acceptedname: Str
		Name of the accepted taxon
	status: Str
		Taxonomic status of a taxon
	gbifkey: Int
		Identifier of a taxon in the GBIF backbone
	hasEndemStatus: Bool
		Whether the taxon has an endemism status in the database
	hasExotStatus: Bool
		Whether the taxon has an alien/invasive status in the database
	hasThreatStatus: Bool
		Whether the taxon has a threat status in the database
    """
    try:
        if not taxInput.get('cd_tax'):
            taxInput.update(manageInputTax(connection=connection,insert=False,**taxInput))
        taxOutput = getTax(connection,taxInput.get('cd_tax'))
    except (MissingArgError, UncompatibilityGbifKeyCanonicalname) as e:
        return {'error':str(e)}
    except (DbIntegrityError, UnauthorizedValueError) as e:
        raise Abort500Error(str(e)) from e
    else:
        return taxOutput


def ListTax_err_hand(connection, **listTaxArgs):
    """
    Description
	-----------
	Returns a list of tax integrated in the API database.  Without argument, returns the complete list. With the “childrenOf” argument, returns only the taxa from a taxonomic clade.  Export format may be JSON or CSV

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    listTaxArgs: dict
        Dictionary with the following elements:
        childrenOf: Str [optional]
            canonicalname or scientificname of the parent taxon for which we want to get the list of children taxa (and their statuses)
        format: Str [optional]
            JSON or CSV format in GET methods

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
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
		Identifier of the accepted taxon
	acceptedname: Str
		Name of the accepted taxon
	status: Str
		Taxonomic status of a taxon
	gbifkey: Int
		Identifier of a taxon in the GBIF backbone
	hasEndemStatus: Bool
		Whether the taxon has an endemism status in the database
	hasExotStatus: Bool
		Whether the taxon has an alien/invasive status in the database
	hasThreatStatus: Bool
		Whether the taxon has a threat status in the database
    """
    try:
        if listTaxArgs.get('childrenOf'):
            parsed = get_gbif_parsed_from_sci_name(listTaxArgs.get('childrenOf'))
            if parsed.get('scientificName') and parsed.get('canonicalNameComplete') and parsed.get('scientificName')==parsed.get('canonicalNameComplete'):
                parent=manageInputTax(connection=connection, insert=False,canonicalname=listTaxArgs.get('childrenOf'))
            else:
                parent=manageInputTax(connection=connection, insert=False,scientificname=listTaxArgs.get('childrenOf'))
            if parent.get('alreadyInDb'):
                cursor=connection.cursor()
                listChildren=childrenList(cursor,parent.get('cd_tax_acc'))
                cursor.close()
                res=getListTax(connection=connection, listChildren=listChildren, formatExport=listTaxArgs.get('format'))
            else:
                raise TaxonNotFoundDbError(tax=listTaxArgs.get('childrenOf'), message='\'childrenOf\' taxon not recognized')
                #raise Exception("childrenOfNotFound")
        else:
            res = getListTax(connection=connection, listChildren=[], formatExport=listTaxArgs.get('format'))
    except (TaxonNotFoundDbError, MissingArgError) as e:
        return {'error':str(e)}
    except (DbIntegrityError, UnauthorizedValueError) as e:
        raise Abort500Error(str(e)) from e
    else:
        if listTaxArgs.get('format')=="CSV":
            response_stream = BytesIO(res.to_csv().encode())
            return send_file(response_stream, mimetype = "text/csv", attachment_filename = "taxonomy.csv")
        else:
            return res

def ListRef_err_hand(connection, **listRefArgs):
    """
    Description
	-----------
	Returns a list of bibliographic references from the database, with the number of taxa with statuses (endemism, alien and threatened). Format may be JSON or CSV
	
    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    listRefArgs: dict
        Dictionary with the following elements:
        onlyExot: Bool [optional]
            Whether to returns only the exotic-related references
        onlyEndem: Bool [optional]
            Whether to returns only the endemism-related references
        onlyThreat: Bool [optional]
            Whether to returns only the threat-related references
        format: Str [optional]
            JSON or CSV format in GET methods

	Returns
	-----------
	cd_ref: Int
		Identifier of the bibliographic reference
	ref_citation: Str
		Bibliographic reference descriptor
	link: Str
		Internet link for resources (usually datasets or pdf) associated with a bibliographic reference
	nb_exot: Int
		Number of exotic taxa associated with a bibliographic reference
	nb_endem: Int
		Number of endemic taxa associated with a bibliographic reference
	nb_threat: Int
		Number of threatened taxa associated with a bibliographic reference
    """
    try:
        listRef = getListReferences(connection=connection, formatExport= listRefArgs.get('format'), onlyEndem= listRefArgs.get('onlyEndem'), onlyExot= listRefArgs.get('onlyExot'), onlyThreat= listRefArgs.get('onlyThreat'))
    except (MissingArgError) as e:
        return {'error':str(e)}
    except (DbIntegrityError, UnauthorizedValueError) as e:
        raise Abort500Error(str(e)) from e
    else:
        if listRefArgs.get('format')=="CSV":
            response_stream = BytesIO(listRef.to_csv().encode())
            return send_file(response_stream, mimetype = "text/csv", attachment_filename = "references.csv")
        else:
            return listRef

def cleanDbDel_err_hand(connection,**cdbArgs):
    """
    Description
	-----------
	Delete status without references, references without status nor taxa, synonyms without accepted tax, and/or taxa without statuses ( and which are not synonyms or parents of taxa with statuses)

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    cdbArgs: dict
        Dictionary with the following elements:
        status_no_ref: Bool [optional]
            Whether to delete statuses without associated bibliographic references
        ref_no_status: Bool [optional]
            Whether to delete references which are not associated with any status or taxon
        syno_no_tax: Bool [optional]
            Whether to delete synonym without accepted names
        tax_no_status: Bool [optional]
            Whether to delete taxa which have no status in the database (and are neither synonym or parents of a taxon with status)

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	cd_ref: Int
		Identifier of the bibliographic reference
	cd_st: List(Int)
		List of status Identifiers (since a taxon can only have only a status in each category, corresponds to the cd_tax)
    """
        try:
            cd_taxs=[]
            cd_refs=[]
            cd_status=[]
            if cdbArgs.get('status_no_ref'):
                cd_status+=delStatus_no_reference(connection)
            if cdbArgs.get('ref_no_status'):
                cd_refs+=delReference_no_status(connection)
            if cdbArgs.get('syno_no_tax'):
                cd_taxs+=delSyno_no_tax(connection)
            if cdbArgs.get('tax_no_status'):
                cd_taxs+=delTaxo_no_status(connection)
        except (MissingArgError,DeleteMissingElementDbError) as e:
            return {'error':str(e)}
        else:
            return {'cd_taxs': cd_taxs, 'cd_refs':cd_refs,'cd_status':cd_status}

def userPost_err_hand(connection, **userArgs):
    """
    Description
	-----------
	Creates a user without editing/admin rights
	
    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    userArgs: dict
        Dictionary with the following elements:
        username: Str [required]
            Name of a user
        password: Str [required]
            Password of a user for its creation

	Returns
	-----------
	uid: Int
		Identifier of a user
    """
    try:
        uid,username=new_user(connection,**userArgs)
    except (AlreadyExistsDbError) as e:
        return {'error':str(e)}
    else:
        return{'uid':uid, 'username':username}


def userPut_err_hand(connection,**userArgs):
    """
    Description
	-----------
	Change password for the autenticated user

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    userArgs: dict
        Dictionary with the following elements:
        newPassword: Str [required]
            New password of the user

	Returns
	-----------
	uid: Int
		Identifier of a user
    """
    try:
        user=g.get('user')
        user.update(**userArgs)
        cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        uid = change_password(cur,**user)
    except (UserNotFoundError,MissingArgError) as e:
        return {'error':str(e)}
    else:
        connection.commit()
        return {'uid':uid}
    finally: 
        cur.close()
    
def adminUserDel_err_hand(connection,**userArgs):
    """
    Description
	-----------
	Delete a user
	
    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    userArgs: dict
        Dictionary with the following elements:
        uid: Int [optional]
            Identificator of a user in the API database
        username: Str [optional]
            Name of a user

	Returns
	-----------
	uid: Int
		Identifier of a user
	username: Str
		User name
    """
    try:
        uid, delUsername = delete_user(connection,**userArgs)
    except (UserNotFoundError,MissingArgError,DeleteMissingElementDbError) as e:
        return {'error':str(e)}
    else:
        connection.commit()
        return{'uid':uid, 'username':delUsername}

def adminUserPut_err_hand(connection,**modifyArgs):
    """
    Description
	-----------
	Change permission and/or password of a user.

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    modifyArgs: dict
        Dictionary with the following elements:
        uid: Int [optional]
            Identificator of a user in the API database
        username: Str [optional]
            Name of a user
        grant_user: Bool [optional]
            Whether to grant or not the user basic permissions to the user
        revoke_user: Bool [optional]
            Whether to revoke basic rights of a user
        grant_edit: Bool [optional]
            Whether to grant or not the editing permission to the user
        revoke_edit: Bool [optional]
            Whether to revoke edition rights of a user
        grant_admin: Bool [optional]
            Whether to grant or not the administrative permission to the user
        revoke_admin: Bool [optional]
            Whether to revoke administrative rights of a user
        newPassword: Str [optional]
            New password of the user

	Returns
	-----------
	uid: Int
		Identifier of a user
	username: Str
		User name
    """
    try:
        res={'grant_edit':None,'grant_user':None,'grant_admin':None,'revoke_edit':None,'revoke_admin':None,'revoke_user':None,'newPassword':None}
        cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if modifyArgs.get('grant_user'):
            res['grant_user']=grant_user(cur,**modifyArgs)
        if modifyArgs.get('grant_edit'):
            res['grant_edit']=grant_edit(cur,**modifyArgs)
        if modifyArgs.get('grant_admin'):
            res['grant_admin']=grant_admin(cur,**modifyArgs)
        if modifyArgs.get('revoke_user'):
            res['revoke_user']=revoke_user(cur,**modifyArgs)
        if modifyArgs.get('revoke_edit'):
            res['revoke_edit']=revoke_edit(cur,**modifyArgs)
        if modifyArgs.get('revoke_admin'):
            res['revoke_admin']=revoke_admin(cur,**modifyArgs)
        if modifyArgs.get('newPassword'):
            res['newPassword']=change_password(cur,**modifyArgs)
    except (UserNotFoundError,GrantExistingRightError,RevokeUnexistingRightError,MissingArgError) as e:
        return {'error':str(e)}
    else:
        connection.commit()
        return res
    finally:
        cur.close()


def adminUserGet_err_hand(connection):
    """
    Description
	-----------
	Returns the list of users and their permissions. Format may be JSON or CSV
	
    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
	
	Returns
	-----------
	uid: Int
		Identifier of a user
	username: Str
		User name
	roles: List(Str)
		List of roles (permissions, rights) for a user
    """
    try:
        cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        user_list=get_user_list(cur)
        return user_list
    finally:
        cur.close()

def manageTaxPost_err_hand(connection, **inputTax):
    """
    Description
	-----------
	Insert a taxon in the datababase (with its accepted taxon, if synonym, and parent taxa)
	

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    inputTax: dict
        Dictionary with the following elements:
        gbifkey: Int [optional]
            Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
        scientificname: Str [optional]
            Complete name of a taxon, with authorship
        canonicalname: Str [optional]
            Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format
        authorship: Str [optional]
            Authorship of a taxon (usually corresponds to the difference between scientificname and canonicalname)
        syno: Bool [optional]
            Whether the taxon is a synonym
        parentgbifkey: Int [optional]
            gbifkey of the parent taxon
        parentcanonicalname: Str [optional]
            canonicalname of the parent taxon
        parentscientificname: Str [optional]
            scientificname of the parent taxon
        synogbifkey: Int [optional]
            Accepted taxon gbifkey (when the sent taxon is a synonym)
        synocanonicalname: Str [optional]
            Accepted taxon canonicalname (when the sent taxon is a synonym)
        synoscientificname: Str [optional]
            Accepted taxon scientificname (when the sent taxon is a synonym)
        rank: Str [optional]
            Taxonomic rank (level) of the provided taxon
        min_gbif_conf: Int [optional]
            Minimum value for the confidence in the GBIF matching: default value is 90, maximum is 100. Higher value means the taxon found in GBIF needs to have a closer spelling to the provided one in order to be accepted
        no_gbif: Bool [optional]
            Whether the provided taxon should be matched through the GBIF API. Note that even though ‘no_gbif’ is set to True, the parents taxa will be searched through the GBIF API if not found in the database

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	cd_tax_acc: Int
		Identifier of the accepted taxon
	alreadyInDb: Bool
		Whether the taxon was already in the database when the endpoint was accessed
	foundGbif: Bool
		Whether the taxon was found in GBIF
	matchedname: Str
		Name of the taxon matched with the provided one, in the API database, or from the GBIF API
	acceptedname: Str
		Name of the accepted taxon
	gbifkey: Int
		Identifier of a taxon in the GBIF backbone
	syno: Bool
		Whether a taxon is a synonym
	insertedTax: List(Int)
		List of inserted taxa
    """
    try:
        res = manageInputTax(connection=connection, insert=True,**inputTax)
    except (MissingArgError,UncompatibilityGbifKeyCanonicalname) as e:
        return{'error':str(e)}
    except (UnauthorizedValueError, DbIntegrityError) as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageTaxDel_err_hand(connection,**delTaxArgs):
    """
    Description
	-----------
	Delete a taxon and its statuses in the database. Note that if the taxon has synonyms and/or children taxa, it might cause problems in the app. Use carefully.
	

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    delTaxArgs: dict
        Dictionary with the following elements:
        cd_tax: Int [required]
            Identificator of a taxon in the database
        gbifkey: Int [optional]
            Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
        scientificname: Str [optional]
            Complete name of a taxon, with authorship
        canonicalname: Str [optional]
            Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	cd_children: List(Int)
		List of Identifiers of children taxa
	cd_synos: List(Int)
		List of synonym Identifiers
    """
    try:
        cd_tax = delTaxArgs.get('cd_tax')
        if delTaxArgs.get('canonicalname') or delTaxArgs.get('scientificname') or delTaxArgs.get('gbifkey'):
            if not checkCdTax(connection=connection, cd_tax=cd_tax, **delTaxArgs):
                raise UncompatibilityCdTaxInputTaxError(cd_tax=cd_tax,inputTax={key:value for (key,value) in delTaxArgs.items() if key in ('canonicalname','scientificname','gbifkey')})
        res = deleteTaxo(connection, cd_tax)
    except (MissingArgError,UncompatibilityGbifKeyCanonicalname,UncompatibilityCdTaxInputTaxError) as e:
        return{'error':str(e)}
    except (UnauthorizedValueError, DbIntegrityError) as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageTaxPut_err_hand(connection,**putTaxArgs):
    """
    Description
	-----------
	Modify a taxon in the database, if the arguments gbifkey, parentgbifkey, or synogbifkey are provided, information is extracted from GBIF. Otherwise the information concerning the taxon is extracted from provided arguments
	

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    putTaxArgs: dict
        Dictionary with the following elements:
        cd_tax: Int [required]
            Identificator of a taxon in the database
        gbifkey: Int [optional]
            Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
        scientificname: Str [optional]
            Complete name of a taxon, with authorship
        canonicalname: Str [optional]
            Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format
        authorship: Str [optional]
            Authorship of a taxon (usually corresponds to the difference between scientificname and canonicalname)
        syno: Bool [optional]
            Whether the taxon is a synonym
        parentgbifkey: Int [optional]
            gbifkey of the parent taxon
        parentcanonicalname: Str [optional]
            canonicalname of the parent taxon
        parentscientificname: Str [optional]
            scientificname of the parent taxon
        synogbifkey: Int [optional]
            Accepted taxon gbifkey (when the sent taxon is a synonym)
        synocanonicalname: Str [optional]
            Accepted taxon canonicalname (when the sent taxon is a synonym)
        synoscientificname: Str [optional]
            Accepted taxon scientificname (when the sent taxon is a synonym)
        status: Str [optional]
            Taxonomic status (ACCEPTED, DOUBTFUL or SYNONYM) Note: doubtful synonym are “SYNONYM”
        reference: Str [optional]
            Bibliographic references for the taxonomic status of a taxon
        link: List(Str) [optional]
            Link, or link list for the resources associated with a bibliographic reference which justify the status of a taxon (if provided, it needs to have the same length as ref_citation)
        cd_ref: Int [optional]
            Identificator of a bibliographic reference
        rank: Str [optional]
            Taxonomic rank (level) of the provided taxon
        no_gbif: Bool [optional]
            Whether the provided taxon should be matched through the GBIF API. Note that even though ‘no_gbif’ is set to True, the parents taxa will be searched through the GBIF API if not found in the database
        min_gbif_conf: Int [optional]
            Minimum value for the confidence in the GBIF matching: default value is 90, maximum is 100. Higher value means the taxon found in GBIF needs to have a closer spelling to the provided one in order to be accepted

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	insertedTax: List(Int)
		List of inserted taxa
    """
    try:
        res = modifyTaxo(connection=connection,**putTaxArgs)
    except (MissingArgError,UncompatibilityGbifKeyCanonicalname,AlreadyExistsDbError) as e:
        return{'error':str(e)}
    except (UnauthorizedValueError, DbIntegrityError) as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageEndemPost_err_hand(connection,**inputEndem):
    """
    Description
	-----------
	Add references to an endemic status, or insert references and status if the taxon has no status yet. If the taxon is not yet in the database, insert the taxon as well (by the same process as in the /manageTaxo endpoint). The optional parameter “priority” control the behavior of the function when the endemic status already exists in the database: if “high”, replace the preexisting status, if low, only add new references. If not provided, or null, and the status from the database is different from the provided status, returns an error and no modification is applied in the database.
	

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    inputEndem: dict
        Dictionary with the following elements:
        endemstatus: Str [required]
            Endemic status to insert or edit in the database
        ref_citation: List(Str) [required]
            Bibliographic references justifying the status of a taxon
        gbifkey: Int [optional]
            Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
        scientificname: Str [optional]
            Complete name of a taxon, with authorship
        canonicalname: Str [optional]
            Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format
        authorship: Str [optional]
            Authorship of a taxon (usually corresponds to the difference between scientificname and canonicalname)
        syno: Bool [optional]
            Whether the taxon is a synonym
        parentgbifkey: Int [optional]
            gbifkey of the parent taxon
        parentcanonicalname: Str [optional]
            canonicalname of the parent taxon
        parentscientificname: Str [optional]
            scientificname of the parent taxon
        synogbifkey: Int [optional]
            Accepted taxon gbifkey (when the sent taxon is a synonym)
        synocanonicalname: Str [optional]
            Accepted taxon canonicalname (when the sent taxon is a synonym)
        synoscientificname: Str [optional]
            Accepted taxon scientificname (when the sent taxon is a synonym)
        rank: Str [optional]
            Taxonomic rank (level) of the provided taxon
        min_gbif_conf: Int [optional]
            Minimum value for the confidence in the GBIF matching: default value is 90, maximum is 100. Higher value means the taxon found in GBIF needs to have a closer spelling to the provided one in order to be accepted
        no_gbif: Bool [optional]
            Whether the provided taxon should be matched through the GBIF API. Note that even though ‘no_gbif’ is set to True, the parents taxa will be searched through the GBIF API if not found in the database
        link: List(Str) [optional]
            Link, or link list for the resources associated with a bibliographic reference which justify the status of a taxon (if provided, it needs to have the same length as ref_citation)
        comments: Str [optional]
            Comments and supplementary information about a taxon status
        replace_comment: Bool [optional]
            Whether to delete the preexisting comment in a taxon status, before inserting the provided comments, when the status already exists.
        priority: Str [optional]
            “high” if the provided status is prioritary on (must replace) the preexisting status, “low” if the preexisting status should not be modified (in this case only the new references are added in the database)

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	alreadyInDb: Bool
		Whether the taxon was already in the database when the endpoint was accessed
	foundGbif: Bool
		Whether the taxon was found in GBIF
	matchedname: Str
		Name of the taxon matched with the provided one, in the API database, or from the GBIF API
	acceptedname: Str
		Name of the accepted taxon
	gbifkey: Int
		Identifier of a taxon in the GBIF backbone
	syno: Bool
		Whether a taxon is a synonym
	insertedTax: List(Int)
		List of inserted taxa
	cd_refs: List(Int)
		List of Identifiers of bibliographic references
	status_replaced: Bool
		Whether the status has been replaced in the application of the POST method
	status_created: Bool
		Whether the status has been created in the POST method
    """
    try:
        res = manageInputTax(connection=connection, insert=True,**inputEndem)
        res.update(manageInputEndem(res.get('cd_tax_acc'), connection = connection, **inputEndem))
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageEndemDel_err_hand(connection,**delEndemArgs):
    """
    Description
	-----------
	Delete a link between a taxon and its endemic status, or the status of a taxon.
	

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    delEndemArgs: dict
        Dictionary with the following elements:
        cd_tax: Int [required]
            Identificator of a taxon in the database
        cd_ref: Int [optional]
            Identificator of a bibliographic reference
        delete_status: Bool [optional]
            Whether to suppress the whole status of a taxon in the delete methods (if negative or null, only the association between a reference and a status is deleted)
        

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	cd_refs: List(Int)
		List of Identifiers of bibliographic references
    """
    try:
        cd_tax=delEndemArgs['cd_tax']
        delEndemArgs={k:v for (k,v) in delEndemArgs.items() if k!='cd_tax'}
        res= deleteEndem(cd_tax=cd_tax,connection=connection,**delEndemArgs)
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageEndemPut_err_hand(connection, **putEndemArgs):
    """
    Description
	-----------
	Modify the parameters of an endemic status of a species, and insert the references associated with the new endemic status
	

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    putEndemArgs: dict
        Dictionary with the following elements:
        cd_tax: Int [required]
            Identificator of a taxon in the database
        endemstatus: Str [required]
            Endemic status to insert or edit in the database
        ref_citation: List(Str) [required]
            Bibliographic references justifying the status of a taxon
        link: List(Str) [optional]
            Link, or link list for the resources associated with a bibliographic reference which justify the status of a taxon (if provided, it needs to have the same length as ref_citation)
        comments: Str [optional]
            Comments and supplementary information about a taxon status
        replace_comment: Bool [optional]
            Whether to delete the preexisting comment in a taxon status, before inserting the provided comments, when the status already exists.
	

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	cd_refs: List(Int)
		List of Identifiers of bibliographic references
    """
    try:
        cd_tax=putEndemArgs['cd_tax']
        putEndemArgs={k:v for (k,v) in putEndemArgs.items() if k!='cd_tax'}
        res= modifyEndem(cd_tax=cd_tax,connection=connection,**putEndemArgs)
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res


def manageExotPost_err_hand(connection,**inputExot):
    """
    Description
	-----------
	Add references to an exotic (alien/invasive) status, or insert references and status if the taxon has no status yet. If the taxon is not yet in the database, insert the taxon as well (by the same process as in the /manageTaxo endpoint). The optional parameter “priority” control the behavior of the function when the exotic status already exists in the database: if “high”, replace the preexisting status, if low, only add new references. If not provided, or null, and the status from the database is different from the provided status, returns an error and no modification is applied in the database.
	

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    inputExot: dict
        Dictionary with the following elements:
        is_alien: Bool [required]
            Part of the exotic status of a taxon: is it considered alien in Colombia?
        is_invasive: Bool [required]
            Part of the exotic status of a taxon: is it considered invasive in Colombia?
        ref_citation: List(Str) [required]
            Bibliographic references justifying the status of a taxon
        gbifkey: Int [optional]
            Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
        scientificname: Str [optional]
            Complete name of a taxon, with authorship
        canonicalname: Str [optional]
            Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format
        authorship: Str [optional]
            Authorship of a taxon (usually corresponds to the difference between scientificname and canonicalname)
        syno: Bool [optional]
            Whether the taxon is a synonym
        parentgbifkey: Int [optional]
            gbifkey of the parent taxon
        parentcanonicalname: Str [optional]
            canonicalname of the parent taxon
        parentscientificname: Str [optional]
            scientificname of the parent taxon
        synogbifkey: Int [optional]
            Accepted taxon gbifkey (when the sent taxon is a synonym)
        synocanonicalname: Str [optional]
            Accepted taxon canonicalname (when the sent taxon is a synonym)
        synoscientificname: Str [optional]
            Accepted taxon scientificname (when the sent taxon is a synonym)
        rank: Str [optional]
            Taxonomic rank (level) of the provided taxon
        min_gbif_conf: Int [optional]
            Minimum value for the confidence in the GBIF matching: default value is 90, maximum is 100. Higher value means the taxon found in GBIF needs to have a closer spelling to the provided one in order to be accepted
        no_gbif: Bool [optional]
            Whether the provided taxon should be matched through the GBIF API. Note that even though ‘no_gbif’ is set to True, the parents taxa will be searched through the GBIF API if not found in the database
        link: List(Str) [optional]
            Link, or link list for the resources associated with a bibliographic reference which justify the status of a taxon (if provided, it needs to have the same length as ref_citation)
        comments: Str [optional]
            Comments and supplementary information about a taxon status
        replace_comment: Bool [optional]
            Whether to delete the preexisting comment in a taxon status, before inserting the provided comments, when the status already exists.
        priority: Str [optional]
            “high” if the provided status is prioritary on (must replace) the preexisting status, “low” if the preexisting status should not be modified (in this case only the new references are added in the database)

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	alreadyInDb: Bool
		Whether the taxon was already in the database when the endpoint was accessed
	foundGbif: Bool
		Whether the taxon was found in GBIF
	matchedname: Str
		Name of the taxon matched with the provided one, in the API database, or from the GBIF API
	acceptedname: Str
		Name of the accepted taxon
	gbifkey: Int
		Identifier of a taxon in the GBIF backbone
	syno: Bool
		Whether a taxon is a synonym
	insertedTax: List(Int)
		List of inserted taxa
	cd_refs: List(Int)
		List of Identifiers of bibliographic references
	status_replaced: Bool
		Whether the status has been replaced in the application of the POST method
	status_created: Bool
		Whether the status has been created in the POST method
    """
    try:
        res = manageInputTax(connection=connection, insert=True,**inputExot)
        res.update(manageInputExot(res.get('cd_tax_acc'), connection = connection, **inputExot))
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageExotDel_err_hand(connection,**delExotArgs):
    """
    Description
	-----------
	Delete a link between a taxon and its exotic status, or the status of a taxon.
	

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
        delExotArgs: dict
            Dictionary with the following elements:
            cd_tax: Int [required]
                Identificator of a taxon in the database
            cd_ref: Int [optional]
                Identificator of a bibliographic reference
            delete_status: Bool [optional]
                Whether to suppress the whole status of a taxon in the delete methods (if negative or null, only the association between a reference and a status is deleted)

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	cd_refs: List(Int)
		List of Identifiers of bibliographic references
    """
    try:
        cd_tax=delExotArgs['cd_tax']
        delExotArgs={k:v for (k,v) in delExotArgs.items() if k!='cd_tax'}
        res= deleteExot(cd_tax=cd_tax,connection=connection,**delExotArgs)
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageExotPut_err_hand(connection, **putExotArgs):
    """
    Description
	-----------
	Modify the parameters of an exotic status of a species, and insert the references associated with the new exotic status

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    putExotArgs: dict
        Dictionary with the following elements:
        cd_tax: Int [required]
            Identificator of a taxon in the database
        is_alien: Bool [required]
            Part of the exotic status of a taxon: is it considered alien in Colombia?
        is_invasive: Bool [required]
            Part of the exotic status of a taxon: is it considered invasive in Colombia?
        ref_citation: List(Str) [required]
            Bibliographic references justifying the status of a taxon
        link: List(Str) [optional]
            Link, or link list for the resources associated with a bibliographic reference which justify the status of a taxon (if provided, it needs to have the same length as ref_citation)
        comments: Str [optional]
            Comments and supplementary information about a taxon status
        replace_comment: Bool [optional]
            Whether to delete the preexisting comment in a taxon status, before inserting the provided comments, when the status already exists.

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	cd_refs: List(Int)
		List of Identifiers of bibliographic references
    """
    try:
        cd_tax=putExotArgs['cd_tax']
        putExotArgs={k:v for (k,v) in putExotArgs.items() if k!='cd_tax'}
        res= modifyExot(cd_tax=cd_tax,connection=connection,**putExotArgs)
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res


def manageThreatPost_err_hand(connection,**inputThreat):
    """
    Description
	-----------
	Add references to a threat status, or insert references and status if the taxon has no status yet. If the taxon is not yet in the database, insert the taxon as well (by the same process as in the /manageTaxo endpoint). The optional parameter “priority” control the behavior of the function when the threat status already exists in the database: if “high”, replace the preexisting status, if low, only add new references. If not provided, or null, and the status from the database is different from the provided status, returns an error and no modification is applied in the database.
	
    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    inputThreat: dict
        Dictionary with the following elements:
        threatstatus: Str [required]
            IUCN threat status
        ref_citation: List(Str) [required]
            Bibliographic references justifying the status of a taxon
        gbifkey: Int [optional]
            Identificator of a taxon in the GBIF Backbone database (=specieskey, key, acceptedkey etc.)
        scientificname: Str [optional]
            Complete name of a taxon, with authorship
        canonicalname: Str [optional]
            Name of the taxon without authorship. Formally correspond to canonicalNameWithMarker in GBIF DarwinCore format
        authorship: Str [optional]
            Authorship of a taxon (usually corresponds to the difference between scientificname and canonicalname)
        syno: Bool [optional]
            Whether the taxon is a synonym
        parentgbifkey: Int [optional]
            gbifkey of the parent taxon
        parentcanonicalname: Str [optional]
            canonicalname of the parent taxon
        parentscientificname: Str [optional]
            scientificname of the parent taxon
        synogbifkey: Int [optional]
            Accepted taxon gbifkey (when the sent taxon is a synonym)
        synocanonicalname: Str [optional]
            Accepted taxon canonicalname (when the sent taxon is a synonym)
        synoscientificname: Str [optional]
            Accepted taxon scientificname (when the sent taxon is a synonym)
        rank: Str [optional]
            Taxonomic rank (level) of the provided taxon
        min_gbif_conf: Int [optional]
            Minimum value for the confidence in the GBIF matching: default value is 90, maximum is 100. Higher value means the taxon found in GBIF needs to have a closer spelling to the provided one in order to be accepted
        no_gbif: Bool [optional]
            Whether the provided taxon should be matched through the GBIF API. Note that even though ‘no_gbif’ is set to True, the parents taxa will be searched through the GBIF API if not found in the database
        link: List(Str) [optional]
            Link, or link list for the resources associated with a bibliographic reference which justify the status of a taxon (if provided, it needs to have the same length as ref_citation)
        comments: Str [optional]
            Comments and supplementary information about a taxon status
        replace_comment: Bool [optional]
            Whether to delete the preexisting comment in a taxon status, before inserting the provided comments, when the status already exists.
        priority: Str [optional]
            “high” if the provided status is prioritary on (must replace) the preexisting status, “low” if the preexisting status should not be modified (in this case only the new references are added in the database)

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	alreadyInDb: Bool
		Whether the taxon was already in the database when the endpoint was accessed
	foundGbif: Bool
		Whether the taxon was found in GBIF
	matchedname: Str
		Name of the taxon matched with the provided one, in the API database, or from the GBIF API
	acceptedname: Str
		Name of the accepted taxon
	gbifkey: Int
		Identifier of a taxon in the GBIF backbone
	syno: Bool
		Whether a taxon is a synonym
	insertedTax: List(Int)
		List of inserted taxa
	cd_refs: List(Int)
		List of Identifiers of bibliographic references
	status_replaced: Bool
		Whether the status has been replaced in the application of the POST method
	status_created: Bool
		Whether the status has been created in the POST method
    """
    try:
        res = manageInputTax(connection=connection, insert=True,**inputThreat)
        res.update(manageInputThreat(res.get('cd_tax_acc'), connection = connection, **inputThreat))
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageThreatDel_err_hand(connection,**delThreatArgs):
    """
    Description
	-----------
	Delete a link between a taxon and its threat status, or the status of a taxon.
	

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    delThreatArgs: dict
        Dictionary with the following elements:
        cd_tax: Int [required]
            Identificator of a taxon in the database
        cd_ref: Int [optional]
            Identificator of a bibliographic reference
        delete_status: Bool [optional]
            Whether to suppress the whole status of a taxon in the delete methods (if negative or null, only the association between a reference and a status is deleted)

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	cd_refs: List(Int)
		List of Identifiers of bibliographic references
    """
    try:
        cd_tax=delThreatArgs['cd_tax']
        delThreatArgs={k:v for (k,v) in delThreatArgs.items() if k!='cd_tax'}
        res= deleteThreat(cd_tax=cd_tax,connection=connection,**delThreatArgs)
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageThreatPut_err_hand(connection, **putThreatArgs):
    """
    Description
	-----------
	Modify the parameters of the threat status of a species, and insert the references associated with the new threat status
	

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    putThreatArgs: dict
        Dictionary with the following elements:
        cd_tax: Int [required]
            Identificator of a taxon in the database
        threatstatus: Str [required]
            IUCN threat status
        ref_citation: List(Str) [required]
            Bibliographic references justifying the status of a taxon
        link: List(Str) [optional]
            Link, or link list for the resources associated with a bibliographic reference which justify the status of a taxon (if provided, it needs to have the same length as ref_citation)
        comments: Str [optional]
            Comments and supplementary information about a taxon status
        replace_comment: Bool [optional]
            Whether to delete the preexisting comment in a taxon status, before inserting the provided comments, when the status already exists.

	Returns
	-----------
	cd_tax: Int
		Identifier of a taxon in the API database
	cd_refs: List(Int)
		List of Identifiers of bibliographic references
    """
    try:
        cd_tax=putThreatArgs['cd_tax']
        putThreatArgs={k:v for (k,v) in putThreatArgs.items() if k!='cd_tax'}
        res= modifyThreat(cd_tax=cd_tax,connection=connection,**putThreatArgs)
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageRefDel_err_hand(connection, **delRefArgs):
    """
    Description
	-----------
	Delete a reference, or join them. In the mergeInto parameter is provided, all references to cd_ref are replaced into references to mergeInto. Otherwise, references to cd_ref are deleted

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
    delRefArgs: dict
        Dictionary with the following elements:
        cd_ref: Int [required]
            Identificator of a bibliographic reference
        mergeInto: Int [optional]
            Identificator of the bibliographic reference which will be kept in the database in the case of merging references

	Returns
	-----------
	cd_ref_modif: Int
		Identifier of the modified bibliographic reference
	cd_ref_del: Int
		Identifier of the deleted bibliographic reference
    """
    try:
        res=dict()
        if delRefArgs.get('mergeInto'):
            res.update(mergeRefs(connection=connection,into_ref=delRefArgs.get('mergeInto'),from_ref=delRefArgs.get('cd_ref')))
        res.update(deleteRef(connection,delRefArgs.get('cd_ref')))
    except (UnauthorizedValueError,DeleteMissingElementDbError) as e:
        return {'error':str(e)}
    else:
        connection.commit()
        return(res)

def manageRefPut_err_hand(connection, **putRefArgs):
    """
    Description
	-----------
	Modify the references
	

    Parameters:
    ----------
    connection: psycopg2 Connection
        connection to the postgres database.
        putRefArgs: dict
            Dictionary with the following elements:
        cd_ref: Int [required]
            Identificator of a bibliographic reference
        reference: Str [optional]
            Bibliographic references for the taxonomic status of a taxon
        link: List(Str) [optional]
            Link, or link list for the resources associated with a bibliographic reference which justify the status of a taxon (if provided, it needs to have the same length as ref_citation)

	Returns
	-----------
	cd_ref_modif: Int
		Identifier of the modified bibliographic reference
	cd_ref_del: Int
		Identifier of the deleted bibliographic reference
    """
    try:
        res=modifyRef(connection, **putRefArgs)
    except ModifyMissingRefDbError as e:
        return {'error':str(e)}
    else:
        connection.commit()
        return res
