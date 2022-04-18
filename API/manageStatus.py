"""
Functions for status management (inserting, adding information etc)
"""
from flask_restful import Resource
import requests
import random
import re
import json
import os
import psycopg2
from psycopg2 import sql
import psycopg2.extras
from io import BytesIO
from flask import send_file
from fuzzywuzzy import fuzz
from getStatus import getThreatStatus
from getStatus import getExotStatus
from getStatus import getEndemStatus
from errors_def import ModifyMissingRefDbError, UnauthorizedValueError, DeleteMissingElementDbError, UncompatibleStatusError, MissingArgError, ModifyMissingStatusDbError

DATABASE_URL = os.environ['DATABASE_URL']
PYTHONIOENCODING="UTF-8"

def insertHabitos(connection,cd_tax, habitos):
    Pass

def manageSource(cursor, ref_citation, ref_link):
    """
    Testing whether one source and its associated link exist in the database, if not insert it in the database
    
    Parameters
    -----------
    cursor: psycopg2 cursor
        cursor for the current operations in the database
    ref_citation: str
        complete text describing the reference
    ref_link
        URL link to the reference ressources
    
    Returns
    ------------
    return the cd_ref to the reference
    """
    # Does the source exist
    if ref_link == ' ':
        ref_link = None
    SQL = "SELECT count(*) FROM refer WHERE citation = %s"
    cursor.execute(SQL, [ref_citation])
    nb, = cursor.fetchone()
    cit_exists = bool(nb)
    if cit_exists:
        SQL = "SELECT cd_ref FROM refer WHERE citation = %s"
        cursor.execute(SQL, [ref_citation])
        cdRef, = cursor.fetchone()
    else:
        # insertion of the source if it does not exist
        SQL = "INSERT INTO refer(citation,link) VALUES(%s,%s) RETURNING cd_ref"
        cursor.execute(SQL,[ref_citation, ref_link])
        cdRef, = cursor.fetchone()
    # it should return the id of the source in the database
    return cdRef

def modifyRef(connection,**refPutArgs):
    cd_ref=refPutArgs.get('cd_ref')
    cur=connection.cursor()
    SQL="SELECT count(cd_ref) FROM refer WHERE cd_ref=%s"
    cur.execute(SQL,[cd_ref])
    nb_cd_ref,=cur.fetchone()
    if not bool(nb_cd_ref):
        cur.close()
        raise ModifyMissingRefDbError(cd_ref=cd_ref)
    if refPutArgs.get('reference'):
        SQL="UPDATE refer SET citation=%s WHERE cd_ref=%s"
        cur.execute(SQL,[refPutArgs.get('reference'),cd_ref])
    if refPutArgs.get('link'):
        SQL="UPDATE refer SET link=%s WHERE cd_ref=%s"
        cur.execute(SQL,[refPutArgs.get('link'),cd_ref])
    cur.close()
    return {'cd_ref_modif':cd_ref}

def mergeRefs(connection, into_ref, from_ref):
    cur=connection.cursor()
    SQL= "SELECT count(cd_ref) FILTER (WHERE cd_ref=%s) nb_into_ref, count(cd_ref) FILTER (WHERE cd_ref=%s) nb_from_ref  FROM refer"
    cur.execute(SQL,[into_ref,from_ref])
    nb_into_ref,nb_from_ref=cur.fetchone()
    if not bool(nb_into_ref):
        cur.close()
        raise UnauthorizedValueError(value=into_ref,var='into_ref',acceptable='See endpoint /listRef')
    if not bool(nb_from_ref):
        cur.close()
        raise UnauthorizedValueError(value=from_ref,var='cd_ref',acceptable='See endpoint /listRef')
    SQL="UPDATE ref_endem SET cd_ref=%s WHERE cd_ref=%s -- RETURNING id"
    cur.execute(SQL,[into_ref,from_ref])
    SQL="UPDATE ref_threat SET cd_ref=%s WHERE cd_ref=%s -- RETURNING id"
    cur.execute(SQL,[into_ref,from_ref])
    SQL="UPDATE ref_exot SET cd_ref=%s WHERE cd_ref=%s -- RETURNING id"
    cur.execute(SQL,[into_ref,from_ref])
    SQL="UPDATE taxon SET source=%s WHERE source=%s -- RETURNING cd_tax"
    cur.execute(SQL,[into_ref,from_ref])
    cur.close()
    return {'cd_ref_modif':into_ref}

def deleteRef(connection, cd_ref):
    cur=connection.cursor()
    SQL="SELECT count(cd_ref) FROM refer WHERE cd_ref=%s"
    cur.execute(SQL,[cd_ref])
    nb_cd_ref,=cur.fetchone()
    if not bool(nb_cd_ref):
        cur.close()
        raise DeleteMissingElementDbError(value=cd_ref,field='cd_ref')
    SQL = "DELETE FROM refer WHERE cd_ref=%s"
    cur.execute(SQL,[cd_ref])
    cur.close()
    return {'cd_ref_del':cd_ref}



def manageInputThreat(cd_tax, connection, **inputThreat):
    """
    Test whether the status provided by the user is compatible with the current status of the taxon (if it has one), then if it is compatible, inserts the new references provided. If the taxon has no threat status, it inserts it in the database
    Parameters
    -----------
    cd_tax: int [mandatory]
        cd_tax of the taxon
    connyection: psycopg2 connection [mandatory]
        connection to the postgres database
    inputThreat: dict
        dictionary containing the user-provided information about the threat status and the associated references with the following elements:
        'threatstatus': str [mandatory]
            IUCN code for threat status
        'ref_citation': list(str) [mandatory]
            list of references for the status
        'link': list(str)
            list of URL links (should be the same length than ref_citation, with None elements where there are no URL links associated with the reference)
        'comments': str
            comments concerning the threat status (separated by "|")
        'priority': str
            If it is provided, avoid the errors when the status is different to preexisting status. If "low" and there is a preexisting status, the functions only add new references. If "high" and there is a preexisting status, replace the status in the database.
        replace_comment: Bool
            Whether to delete the preexisting comment in a taxon status, before inserting the provided comments, when the status already exists.

    Returns
    ------------
    dictionary with the following elements:
        cd_tax: int 
            database taxon identifier 
        cds_ref: list(int)
            list of reference identifiers
        status_replaced: Bool
            Whether the status has been replaced in the application of the POST method
        status_created: Bool
            Whether the status has been created in the POST method
            
    Error handling
    --------------
    Exception: UnauthorizedValueError
        case 1:
            If the cd_status is not one of the IUCN code, raises this error and stops the execution
        case 2:
            If the priority is not one of 'low' or 'high'
    Exception: UncompatibleStatusError
        If the taxon already has a threat status different to the one provided by the user and no priority is given, raises this exception and stops execution
    """
    # test whether status is compatible with the database specification
    resRet=dict()
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL="SELECT cd_status FROM threat_status"
    cur.execute(SQL)
    res=cur.fetchall()
    acceptableThreatStatus= [r['cd_status'] for r in res]
    compatible = (inputThreat.get('threatstatus') in acceptableThreatStatus)
    if (not compatible):
        raise UnauthorizedValueError(value=inputThreat.get('threatstatus'), var="threatstatus", acceptable=acceptableThreatStatus, message="The input threat status is not recognized")
        #raise Exception("The input threat status is not recognized")
    else:
        # find the threat status if it exists in the database
        SQL = "SELECT * FROM threat_list WHERE cd_tax=%s"
        cur.execute(SQL,[cd_tax])
        res=cur.fetchone()
        statusExists=res is not None
        if statusExists:
            oldStatus=dict(res)
            if inputThreat.get('priority'):
                if inputThreat.get('priority')=='high':
                    cur.close()
                    resRet.update(modifyThreat(cd_tax,connection,**inputThreat))
                    resRet.update({'status_replaced':True, 'status_created':False})
                    return resRet
                if inputThreat.get('priority')!='low':
                    raise UnauthorizedValueError(value=inputThreat.get('priority'), var='priority',acceptable=['low','high'])
                    #Exception('unrecognisedPriority')
            else:

                sameStatus = (oldStatus.get('cd_status') == inputThreat['threatstatus'])
                if(not sameStatus and  inputThreat.get('priority')!='low'):
                    raise UncompatibleStatusError(dbStatus=threatStatus.get('cd_status'), providedStatus=inputThreat.get('threatstatus'))
                    #Exception("The taxon already exists in the database with another threat status")
    cur.close()
    with connection:
        with connection.cursor() as cur:
            cdRefs = [manageSource(cur,inputThreat['ref_citation'][i],inputThreat.get('link')[i] if bool(inputThreat.get('link')) else None) for i in range(0,len(inputThreat['ref_citation']))]
            if not statusExists:
                resRet.update({'status_replaced':False, 'status_created':True})
                # if it is compatible with an existing status, insert the new source
                SQL = "INSERT INTO threat(cd_tax,cd_status,comments) VALUES (%s,%s,%s)"
                cur.execute(SQL, [cd_tax, inputThreat['threatstatus'],inputThreat.get('comments')])
            # if it does not exist insert the source, the status and make the links
            else:
                resRet.update({'status_replaced':False, 'status_created':False})
                if inputThreat.get('comments'):
                    if inputThreat.get('replace_comment'):
                        SQL = "UPDATE threat SET comments=%s WHERE cd_tax=%s"
                        cur.execute(SQL,[inputThreat.get('comments'),cd_tax])
                    else:
                        SQL = "WITH c0 AS (SELECT cd_tax,comments FROM threat WHERE cd_tax=%s), c1 AS (SELECT %s AS new_comment), c2 AS (SELECT cd_tax, CASE WHEN c0.comments IS NULL THEN c1.new_comment ELSE c0.comments || ' | ' || c1.new_comment END AS new FROM c0,c1) UPDATE threat SET comments=c2.new FROM c2 WHERE threat.cd_tax=c2.cd_tax"
                        cur.execute(SQL,[cd_tax,inputThreat.get('comments')])
            for i in range(len(cdRefs)):
                SQL = "WITH a AS (SELECT %s AS cd_ref, %s AS cd_tax), b AS(SELECT a.cd_ref,a.cd_tax,rt.id FROM a LEFT JOIN ref_threat AS rt USING (cd_ref,cd_tax)) INSERT INTO ref_threat(cd_ref, cd_tax) SELECT cd_ref,cd_tax FROM b WHERE id IS NULL"
                cur.execute(SQL,[cdRefs[i],cd_tax])
    resRet.update({'cd_tax': cd_tax,'cdRefs': cdRefs})
    return resRet

def deleteThreat(cd_tax,connection,**inputThreat):
    """
    Delete a link between a taxon and its threat status, or the status of a taxon.

    Parameters
    ----------
    cd_tax: Int
        Identificator of a taxon in the database
    connection: psycopg2 connection [mandatory]
        connection to the postgres database
    inputThreat: Dictionary
        See the definition of the endpoint for a complete list of the potential arguments
    returns
    -------
    cd_tax: Int
        Identifier of a taxon in the API database
    cd_refs: List(Int)
        List of Identifiers of bibliographic references
    """
    cur = connection.cursor()
    if inputThreat.get('delete_status'):
        SQL = "SELECT cd_ref FROM ref_threat WHERE cd_tax=%s"
        cur.execute(SQL,[cd_tax])
        res = cur.fetchall()
        cd_refs = [r[0] for r in res]
        SQL = "DELETE FROM threat WHERE cd_tax=%s"
        cur.execute(SQL, [cd_tax])
    elif inputThreat.get('cd_ref'):
        SQL = "DELETE FROM ref_threat WHERE cd_tax=%s AND cd_ref=%s"
        cur.execute(SQL,[cd_tax,inputThreat.get('cd_ref')])
        cd_refs = [inputThreat.get('cd_ref')]
    else:
        raise MissingArgError(missingArg="'cd_ref' or 'delete_status'",message='Do you want to suppress the status (\'delete_status\'=True) or just a reference associated with the status (provide \'cd_ref\')')
        #Exception('noCdRefNorDeletestatus')
    connection.commit()
    cur.close()
    return {'cd_tax': cd_tax, 'cd_refs': cd_refs}

def modifyThreat(cd_tax,connection,**inputThreat):
    """
     Modify the parameters of the threat status of a species, and insert the references associated with the new threat status

     Parameters
     ----------
    cd_tax: int [mandatory]
        cd_tax of the taxon
    connyection: psycopg2 connection [mandatory]
        connection to the postgres database
    inputThreat: dict
        dictionary containing the user-provided information about the threat status and the associated references (See definition of the endpoint for the list of possible elements: class ManageThreat, method put)

    Returns
    -----------
    cd_tax: Int
            Identifier of a taxon in the API database
    cd_refs: List(Int)
            List of Identifiers of bibliographic references

    """
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL = "SELECT count(*) FROM threat_status WHERE cd_status = %s"
    cur.execute(SQL, [inputThreat.get('threatstatus')])
    nb = cur.fetchone()['count']
    compatible = bool(nb)
    if (not compatible):
        SQL="SELECT cd_status FROM threat_status"
        cur.execute(SQL)
        res=cur.fetchall()
        acceptableThreatStatus= [r['cd_status'] for r in res]
        raise UnauthorizedValueError(value=inputThreat.get('threatstatus'), var="threatstatus", acceptable=acceptableThreatStatus)
        #Exception("The input threat status is not recognized")
    else:
        # find the threat status if it exists in the database
        SQL = "SELECT count(*) FROM threat WHERE cd_tax=%s"
        cur.execute(SQL,[cd_tax])
        nb = cur.fetchone()['count']
        statusExists = bool(nb)
        if not statusExists:
            raise ModifyMissingStatusDbError(cd_tax=cd_tax,statustype='threat')
            #Exception('noStatus')
    cur.close()
    with connection:
        with connection.cursor() as cur:
            cdRefs = [manageSource(cur,inputThreat['ref_citation'][i],inputThreat.get('link')[i] if bool(inputThreat.get('link')) else None) for i in range(0,len(inputThreat['ref_citation']))]
            SQL = "UPDATE threat SET cd_status=%s WHERE cd_tax=%s"
            cur.execute(SQL, [inputThreat['threatstatus'],cd_tax])
            if inputThreat.get('comments'):
                if inputThreat.get('replace_comment'):
                    SQL = "UPDATE threat SET comments=%s WHERE cd_tax=%s"
                    cur.execute(SQL,[inputThreat.get('comments'),cd_tax])
                else:
                    SQL = "WITH c0 AS (SELECT cd_tax,comments FROM threat WHERE cd_tax=%s), c1 AS (SELECT %s AS new_comment), c2 AS (SELECT cd_tax, CASE WHEN c0.comments IS NULL THEN c1.new_comment ELSE c0.comments || ' | ' || c1.new_comment END AS new FROM c0,c1) UPDATE threat SET comments=c2.new FROM c2 WHERE threat.cd_tax=c2.cd_tax"
                    cur.execute(SQL,[cd_tax,inputThreat.get('comments')])
            for i in range(len(cdRefs)):
                SQL = "WITH a AS (SELECT %s AS cd_ref, %s AS cd_tax), b AS(SELECT a.cd_ref,a.cd_tax,rt.id FROM a LEFT JOIN ref_threat AS rt USING (cd_ref,cd_tax)) INSERT INTO ref_threat(cd_ref, cd_tax) SELECT cd_ref,cd_tax FROM b WHERE id IS NULL"
                cur.execute(SQL,[cdRefs[i],cd_tax])
    return {'cd_tax': cd_tax,'cdRefs': cdRefs}

def manageInputEndem(cd_tax,connection,**inputEndem):
    """
    Add references to an endemic status, or insert references and status if the taxon has no status yet. The optional parameter “priority” control the behavior of the function when the endemic status already exists in the database: if “high”, replace the preexisting status, if low, only add new references. If not provided, or null, and the status from the database is different from the provided status, returns an error and no modification is applied in the database.
    
    Parameters
    -----------
    cd_tax: int [mandatory]
        cd_tax of the taxon
    connection: psycopg2 connection [mandatory]
        connection to the postgres database
    inputThreat: dict
        dictionary containing the user-provided information about the threat status and the associated references with the following elements:
        'endemstatus': str [mandatory]
            Endemism level (one of: 'Información insuficiente','Especie de interés','Casi endémicas por área','Casi endémica','Endémica' in spanish, or their equivalent in english: 'Unsuficient information', 'Species of interest', 'Almost endemic by area', 'Almost endemic', 'Endemic', or a code going from 0 to 4 corresponding to these levels)
        'ref_citation': list(str) [mandatory]
            list of references for the status
        'link': list(str)
            list of URL links (should be the same length than ref_citation, with None elements where there are no URL links associated with the reference)
        'comments': str
            comments concerning the endemism status (separated by "|")
        'priority': str
            If it is provided, avoid the errors when the status is different to preexisting status. If "low" and there is a preexisting status, the functions only add new references. If "high" and there is a preexisting status, replace the status in the database.
        replace_comment: Bool
            Whether to delete the preexisting comment in a taxon status, before inserting the provided comments, when the status already exists.
        priority: Str
           “high” if the provided status is prioritary on (must replace) the preexisting status, “low” if the preexisting status should not be modified (in this case only the new references are added in the database)

    Returns
    ------------
    dictionary with the following elements:
        cd_tax: int 
            database taxon identifier 
        cds_ref: list(int)
            list of reference identifiers
        status_replaced: Bool
            Whether the status has been replaced in the application of the POST method
        status_created: Bool
            Whether the status has been created in the POST method
            
    Error handling
    --------------
    Exception: UnauthorizedValueError
        case 1:
            If the cd_status is not one of the authorized values to recognized endemism status (Spanish description English description, or value from 0 to 4), raises this error and stops the execution
        case 2:
            If the priority is not one of 'low' or 'high'
    Exception: UncompatibleStatusError
        If the taxon already has a threat status different to the one provided by the user and no priority is given, raises this exception and stops execution

    """
    # test whether status is compatible with the database specification
    resRet=dict()
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL="SELECT * FROM (SELECT descr_endem_es AS cd_status, 1 AS type_order, cd_nivel FROM nivel_endem UNION SELECT descr_endem_en AS cd_status,2,cd_nivel FROM nivel_endem UNION SELECT cd_nivel::text AS cd_status,3,cd_nivel FROM nivel_endem) AS foo ORDER BY type_order, cd_nivel"
    cur.execute(SQL)
    res=cur.fetchall()
    acceptableEndemStatus= [r['cd_status'] for r in res]
    compatible = (inputEndem.get('endemstatus') in acceptableEndemStatus)
    if (not compatible):
        raise UnauthorizedValueError(value=inputEndem.get('endemstatus'), var="endemstatus", acceptable=acceptableEndemStatus, message="The input endemic status is not recognized")
        #raise Exception("The input endemic status is not recognized")
    else:
        SQL="WITH a AS (SELECT %s AS input) SELECT cd_nivel FROM nivel_endem,a WHERE cd_nivel::text=a.input OR descr_endem_es=a.input OR descr_endem_en=a.input"
        cur.execute(SQL,[inputEndem.get('endemstatus')])
        nivInput=cur.fetchone()['cd_nivel']
        # find the endemism status if it exists in the database
        SQL = "SELECT el.*,ne.cd_nivel, ne.descr_endem_en FROM endem_list el LEFT JOIN nivel_endem ne ON el.cd_status=ne.descr_endem_es WHERE cd_tax=%s"
        cur.execute(SQL,[cd_tax])
        res=cur.fetchone()
        statusExists = res is not None
        if statusExists:
            oldStatus=dict(res)
            # if it exists, look whether it is compatible with the current status
            if inputEndem.get('priority'):
                if inputEndem.get('priority')=='high':
                    cur.close()
                    resRet.update(modifyEndem(cd_tax,connection,**inputEndem))
                    resRet.update({'status_replaced':True, 'status_created':False})
                    return resRet
                elif inputEndem.get('priority')=='low':
                    pass
                else:
                    raise UnauthorizedValueError(value=inputEndem.get('priority'), var='priority',acceptable=['low','high'])
            sameStatus = (oldStatus.get('cd_nivel') == nivInput)
            if not sameStatus and inputEndem.get('priority')!='low':
                raise UncompatibleStatusError(dbStatus=oldStatus.get('cd_status') + ' (english:' + oldStatus.get('descr_endem_en') +')', providedStatus=inputEndem.get('endemstatus'))
                #raise Exception("The taxon already exists in the database with another endemic status")
    cur.close()
    with connection:
        with connection.cursor() as cur:
            cdRefs = [manageSource(cur,inputEndem['ref_citation'][i],inputEndem.get('link')[i] if bool(inputEndem.get('link')) else None) for i in range(0,len(inputEndem['ref_citation']))]
            if not statusExists:
                resRet.update({'status_created':True,'status_replaced':False})
                # if it is compatible with an existing status, insert the new source
                SQL = "INSERT INTO endemic(cd_tax,cd_nivel,comments) VALUES (%s,%s,%s)"
                cur.execute(SQL, [cd_tax, nivInput,inputEndem.get('comments')])
            else:
                resRet.update({'status_created':False,'status_replaced':False})
                if inputEndem.get('comments'):
                    if inputEndem.get('replace_comment'):
                        SQL = "UPDATE endemic SET comments=%s WHERE cd_tax=%s"
                        cur.execute(SQL,[inputEndem.get('comments'),cd_tax])
                    else:
                        SQL = "WITH c0 AS (SELECT cd_tax,comments FROM endemic WHERE cd_tax=%s), c1 AS (SELECT %s AS new_comment), c2 AS (SELECT cd_tax, CASE WHEN c0.comments IS NULL THEN c1.new_comment ELSE c0.comments || ' | ' || c1.new_comment END AS new FROM c0,c1) UPDATE endemic SET comments=c2.new FROM c2 WHERE endemic.cd_tax=c2.cd_tax"
                    cur.execute(SQL,[cd_tax,inputEndem.get('comments')])
            # if it does not exist insert the source, the status and make the links
            for i in range(len(cdRefs)):
                SQL = "WITH a AS (SELECT %s AS cd_ref, %s AS cd_tax), b AS(SELECT a.cd_ref,a.cd_tax,rt.id FROM a LEFT JOIN ref_endem AS rt USING (cd_ref,cd_tax)) INSERT INTO ref_endem(cd_ref, cd_tax) SELECT cd_ref,cd_tax FROM b WHERE id IS NULL"
                cur.execute(SQL,[cdRefs[i],cd_tax])
    resRet.update({'cd_tax': cd_tax,'cdRefs': cdRefs})
    return resRet

def deleteEndem(cd_tax,connection,**inputEndem):
    """
    Delete a link between a taxon and its endemic status, or the status of a taxon.

    Parameters
    ----------
    cd_tax: Int
        Identificator of a taxon in the database
    connection: psycopg2 connection [mandatory]
        connection to the postgres database
    inputThreat: Dictionary
        See the definition of the endpoint for a complete list of the potential arguments
    returns
    -------
    cd_tax: Int
        Identifier of a taxon in the API database
    cd_refs: List(Int)
        List of Identifiers of bibliographic references
    """
    cur = connection.cursor()
    if inputThreat.get('delete_status'):
        SQL = "SELECT cd_ref FROM ref_threat WHERE cd_tax=%s"
        cur.execute(SQL,[cd_tax])
        res = cur.fetchall()
        cd_refs = [r[0] for r in res]
        SQL = "DELETE FROM threat WHERE cd_tax=%s"
        cur.execute(SQL, [cd_tax])
    elif inputThreat.get('cd_ref'):
        SQL = "DELETE FROM ref_threat WHERE cd_tax=%s AND cd_ref=%s"
        cur.execute(SQL,[cd_tax,inputThreat.get('cd_ref')])
        cd_refs = [inputThreat.get('cd_ref')]
    else:
        raise MissingArgError(missingArg="'cd_ref' or 'delete_status'",message='Do you want to suppress the status (\'delete_status\'=True) or just a reference associated with the status (provide \'cd_ref\')')
        #Exception('noCdRefNorDeletestatus')
    connection.commit()
    cur.close()
    return {'cd_tax': cd_tax, 'cd_refs': cd_refs}

def modifyEndem(cd_tax,connection,**inputEndem):
    """
     Modify the parameters of the endemism status of a species, and insert the references associated with the new endemism status

     Parameters
     ----------
    cd_tax: int [mandatory]
        cd_tax of the taxon
    connyection: psycopg2 connection [mandatory]
        connection to the postgres database
    inputendem: dict
        dictionary containing the user-provided information about the threat status and the associated references (See definition of the endpoint for the list of possible elements: class ManageEndem, method put)

    Returns
    -----------
    cd_tax: Int
            Identifier of a taxon in the API database
    cd_refs: List(Int)
            List of Identifiers of bibliographic references
    
    Error handling
    --------------
    Exception: UnauthorizedValueError
        If the provided value of endemstatus is not compatible with possible values (description in spanish and english or code from 0 to 4)
    Exception: ModifyMissingStatusDbError
        If the status of the species does not exist

    """
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL="SELECT * FROM (SELECT descr_endem_es AS cd_status, 1 AS type_order, cd_nivel FROM nivel_endem UNION SELECT descr_endem_en AS cd_status,2,cd_nivel FROM nivel_endem UNION SELECT cd_nivel::text AS cd_status,3,cd_nivel FROM nivel_endem) AS foo ORDER BY type_order, cd_nivel"
    cur.execute(SQL)
    res=cur.fetchall()
    acceptableEndemStatus= [r['cd_status'] for r in res]
    compatible = (inputEndem.get('endemstatus') in acceptableEndemStatus)
    if (not compatible):
        raise UnauthorizedValueError(value=inputEndem.get('endemstatus'), var="endemstatus", acceptable=acceptableEndemStatus, message="The input endemic status is not recognized")
    else:
        SQL = "WITH e AS (SELECT %s::text AS nivel) SELECT cd_nivel FROM nivel_endem,e WHERE descr_endem_es = e.nivel OR descr_endem_en = e.nivel OR cd_nivel::text=e.nivel"
        cur.execute(SQL,[inputEndem.get('endemstatus')])
        nivInput = cur.fetchone()['cd_nivel']
        # find the endem status if it exists in the database
        SQL = "SELECT count(*) FROM endemic WHERE cd_tax=%s"
        cur.execute(SQL,[cd_tax])
        nb = cur.fetchone()['count']
        statusExists = bool(nb)
        if not statusExists:
            raise ModifyMissingStatusDbError(cd_tax=cd_tax,statustype='endemic')
            #raise Exception('noStatus')
    cur.close()
    with connection:
        with connection.cursor() as cur:
            cdRefs = [manageSource(cur,inputEndem['ref_citation'][i],inputEndem.get('link')[i] if bool(inputEndem.get('link')) else None) for i in range(0,len(inputEndem['ref_citation']))]
            SQL = "UPDATE endemic SET cd_nivel=%s WHERE cd_tax=%s"
            cur.execute(SQL, [nivInput,cd_tax])
            if inputEndem.get('comments'):
                if inputEndem.get('replace_comment'):
                    SQL = "UPDATE endemic SET comments=%s WHERE cd_tax=%s"
                    cur.execute(SQL,[inputEndem.get('comments'),cd_tax])
                else:
                    SQL = "WITH c0 AS (SELECT cd_tax,comments FROM endemic WHERE cd_tax=%s), c1 AS (SELECT %s AS new_comment), c2 AS (SELECT cd_tax, CASE WHEN c0.comments IS NULL THEN c1.new_comment ELSE c0.comments || ' | ' || c1.new_comment END AS new FROM c0,c1) UPDATE endemic SET comments=c2.new FROM c2 WHERE endemic.cd_tax=c2.cd_tax"
                    cur.execute(SQL,[cd_tax,inputEndem.get('comments')])
            for i in range(len(cdRefs)):
                SQL = "WITH a AS (SELECT %s AS cd_ref, %s AS cd_tax), b AS(SELECT a.cd_ref,a.cd_tax,rt.id FROM a LEFT JOIN ref_endem AS rt USING (cd_ref,cd_tax)) INSERT INTO ref_endem(cd_ref, cd_tax) SELECT cd_ref,cd_tax FROM b WHERE id IS NULL"
                cur.execute(SQL,[cdRefs[i],cd_tax])
    return {'cd_tax': cd_tax,'cdRefs': cdRefs}

def manageInputExot(cd_tax,connection,**inputExot):
    """
    Test whether the status provided by the user is compatible with the current status of the taxon (if it has one), then if it is compatible, inserts the new references provided. If the taxon has no alien/invasive status, it inserts it in the database
    
    TODO
    -----
    Add the parameter add_comment for case where we want the commentary to be added when the status already exists
    
    Parameters
    -----------
    cd_tax: int [mandatory]
        cd_tax of the taxon
    connection: psycopg2 connection [mandatory]
        connection to the postgres database
    inputThreat: dict
        dictionary containing the user-provided information about the alien/invasive status and the associated references with the following elements:
        'is_alien': bool [mandatory]
            Whether thr species is an alien species for Colombia
        'is_invasive': bool [mandatory]
            Whether the species is invasive in Colombia
        'ref_citation': list(str) [mandatory]
            list of references for the status
        'link': list(str)
            list of URL links (should be the same length than ref_citation, with None elements where there are no URL links associated with the reference)
        'comments': str
            comments concerning the alien/invasive status (separated by "|")
        'priority': str
            If it is provided, avoid the errors when the status is different to preexisting status. If "low" and there is a preexisting status, the functions only add new references. If "high" and there is a preexisting status, replace the status in the database.
    Returns
    ------------
    dictionary with the following elements:
        cd_tax: int 
            database taxon identifier 
        cds_ref: list(int)
            list of reference identifiers
        status_replaced: Bool
            Whether the status has been replaced in the application of the POST method
        status_created: Bool
            Whether the status has been created in the POST method

            
    Error handling
    --------------
    Exception: UnauthorizedValueError
        if priority is not one of 'high' or 'low'
    Exception: UncompatibleStatusError
        If the taxon already has a alien/invasive status different to the one provided by the user,and no priority is given, raises this exception and stops execution
    """
    resRet=dict()
    # test whether status is compatible with the database specification
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # find the  status if it exists in the database
    SQL = "SELECT * FROM exot_list WHERE cd_tax=%s"
    cur.execute(SQL,[cd_tax])
    res=cur.fetchone()
    statusExists = res is not None
    if statusExists:
        oldStatus=dict(res)
        # if it exists, look whether it is compatible with the current status
        if inputExot.get('priority'):
            if inputExot.get('priority')=='high':
                cur.close()
                resRet.update(modifyExot(cd_tax,connection,**inputExot))
                resRet.update({'status_replaced':True, 'status_created':False})
                return resRet
            if inputExot.get('priority')!='low':
                raise UnauthorizedValueError(value=inputExot.get('priority'), var='priority',acceptable=['low','high'])
                #raise Exception('unrecognisedPriority')
        else:
            sameStatus = (inputExot.get('is_alien') == oldStatus['is_alien']) and (inputExot.get('is_invasive') == oldStatus['is_invasive'])   
            if(not sameStatus and inputExot.get('priority')!='low'):
                raise UncompatibleStatusError(dbStatus={'is_alien': oldStatus['is_alien'], 'is_invasive': oldStatus['is_invasive']}, providedStatus={'is_alien': inputExot['is_alien'], 'is_invasive': inputExot['is_invasive']})
                #raise Exception("The taxon already exists in the database with another threat status")    
    cur.close()
    with connection:
        with connection.cursor() as cur:
            cdRefs = [manageSource(cur,inputExot['ref_citation'][i],inputExot.get('link')[i] if bool(inputExot.get('link')) else None) for i in range(0,len(inputExot['ref_citation']))]
            if not statusExists:
                resRet.update({'status_created':True,'status_replaced':False})
                # if it is compatible with an existing status, insert the new source
                SQL = "INSERT INTO exot(cd_tax,is_alien,is_invasive,comments) VALUES (%s,%s,%s,%s)"
                cur.execute(SQL, [cd_tax,inputExot.get('is_alien'),inputExot.get('is_invasive'),inputExot.get('comments')])
            else:
                resRet.update({'status_created':False,'status_replaced':False})
                if inputExot.get('comments'):
                    if inputExot.get('replace_comment'):
                        SQL = "UPDATE exot SET comments=%s WHERE cd_tax=%s"
                        cur.execute(SQL,[inputExot.get('comments'),cd_tax])
                    else:
                        SQL = "WITH c0 AS (SELECT cd_tax,comments FROM exot WHERE cd_tax=%s), c1 AS (SELECT %s AS new_comment), c2 AS (SELECT cd_tax, CASE WHEN c0.comments IS NULL THEN c1.new_comment ELSE c0.comments || ' | ' || c1.new_comment END AS new FROM c0,c1) UPDATE exot SET comments=c2.new FROM c2 WHERE exot.cd_tax=c2.cd_tax"
                        cur.execute(SQL,[cd_tax,inputExot.get('comments')])
            # if it does not exist insert the source, the status and make the links
            for i in range(len(cdRefs)):
                SQL = "WITH a AS (SELECT %s AS cd_ref, %s AS cd_tax), b AS(SELECT a.cd_ref,a.cd_tax,rt.id FROM a LEFT JOIN ref_exot AS rt USING (cd_ref,cd_tax)) INSERT INTO ref_exot(cd_ref, cd_tax) SELECT cd_ref,cd_tax FROM b WHERE id IS NULL"
                cur.execute(SQL,[cdRefs[i],cd_tax])
    resRet.update({'cd_tax': cd_tax,'cdRefs': cdRefs})
    return resRet

def deleteExot(cd_tax,connection,**inputExot):
    """
    Delete a link between a taxon and its alien-invasive status, or the status of a taxon.

    Parameters
    ----------
    cd_tax: Int
        Identificator of a taxon in the database
    connection: psycopg2 connection [mandatory]
        connection to the postgres database
    inputExot: Dictionary
        See the definition of the endpoint for a complete list of the potential arguments
    returns
    -------
    cd_tax: Int
        Identifier of a taxon in the API database
    cd_refs: List(Int)
        List of Identifiers of bibliographic references
    """
    cur = connection.cursor()
    if inputExot.get('delete_status'):
        SQL = "SELECT cd_ref FROM ref_exot WHERE cd_tax=%s"
        cur.execute(SQL,[cd_tax])
        res = cur.fetchall()
        cd_refs = [r[0] for r in res]
        SQL = "DELETE FROM exot WHERE cd_tax=%s"
        cur.execute(SQL, [cd_tax])
    elif inputExot.get('cd_ref'):
        SQL = "DELETE FROM ref_exot WHERE cd_tax=%s AND cd_ref=%s"
        cur.execute(SQL,[cd_tax,inputExot.get('cd_ref')])
        cd_refs = [inputExot.get('cd_ref')]
    else:
        raise MissingArgError(missingArg="'cd_ref' or 'delete_status'",message='Do you want to suppress the status (\'delete_status\'=True) or just a reference associated with the status (provide \'cd_ref\')?')
        #raise Exception('noCdRefNorDeletestatus')
    connection.commit()
    cur.close()
    return {'cd_tax': cd_tax, 'cd_refs': cd_refs}

def modifyExot(cd_tax,connection,**inputExot):
    """
     Modify the parameters of the endemism status of a species, and insert the references associated with the new endemism status

     Parameters
     ----------
    cd_tax: int [mandatory]
        cd_tax of the taxon
    connection: psycopg2 connection [mandatory]
        connection to the postgres database
    inputendem: dict
        dictionary containing the user-provided information about the threat status and the associated references (See definition of the endpoint for the list of possible elements: class ManageExot, method put)

    Returns
    -----------
    cd_tax: Int
            Identifier of a taxon in the API database
    cd_refs: List(Int)
            List of Identifiers of bibliographic references
    
    Error handling
    --------------
    Exception: ModifyMissingStatusDbError
        If the status of the species does not exist

    """
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # find the  status if it exists in the database
    SQL = "SELECT count(*) FROM exot WHERE cd_tax=%s"
    cur.execute(SQL,[cd_tax])
    nb = cur.fetchone()['count']
    statusExists = bool(nb)
    if not statusExists:
        raise ModifyMissingStatusDbError(cd_tax=cd_tax,statustype='exotic')
        #raise Exception('noStatus')
    cur.close()
    with connection:
        with connection.cursor() as cur:
            cdRefs = [manageSource(cur,inputExot['ref_citation'][i],inputExot.get('link')[i] if bool(inputExot.get('link')) else None) for i in range(0,len(inputExot['ref_citation']))]
            SQL = "UPDATE exot SET is_invasive=%s, is_alien=%s WHERE cd_tax=%s"
            cur.execute(SQL, [inputExot.get('is_invasive'),inputExot.get('is_alien'),cd_tax])
            if inputExot.get('comments'):
                if inputExot.get('replace_comment'):
                    SQL = "UPDATE exot SET comments=%s WHERE cd_tax=%s"
                    cur.execute(SQL,[inputExot.get('comments'),cd_tax])
                else:
                    SQL = "WITH c0 AS (SELECT cd_tax,comments FROM exot WHERE cd_tax=%s), c1 AS (SELECT %s AS new_comment), c2 AS (SELECT cd_tax, CASE WHEN c0.comments IS NULL THEN c1.new_comment ELSE c0.comments || ' | ' || c1.new_comment END AS new FROM c0,c1) UPDATE exot SET comments=c2.new FROM c2 WHERE exot.cd_tax=c2.cd_tax"
                    cur.execute(SQL,[cd_tax,inputExot.get('comments')])
            for i in range(len(cdRefs)):
                SQL = "WITH a AS (SELECT %s AS cd_ref, %s AS cd_tax), b AS(SELECT a.cd_ref,a.cd_tax,rt.id FROM a LEFT JOIN ref_exot AS rt USING (cd_ref,cd_tax)) INSERT INTO ref_exot(cd_ref, cd_tax) SELECT cd_ref,cd_tax FROM b WHERE id IS NULL"
                cur.execute(SQL,[cdRefs[i],cd_tax])
    return {'cd_tax': cd_tax,'cdRefs': cdRefs}


