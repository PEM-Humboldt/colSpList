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

DATABASE_URL = os.environ['DATABASE_URL']
PYTHONIOENCODING="UTF-8"

def insertHabitos(connection,cd_tax, habitos):
    None

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

def manageInputThreat(cd_tax, connection, **inputThreat):
    """
    Test whether the status provided by the user is compatible with the current status of the taxon (if it has one), then if it is compatible, inserts the new references provided. If the taxon has no threat status, it inserts it in the database
    
    Parameters
    -----------
    cd_tax: int [mandatory]
        cd_tax of the taxon
    connection: psycopg2 connection [mandatory]
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
    Returns
    ------------
    dictionary with the following elements:
        cd_tax: int 
            database taxon identifier 
        cds_ref: list(int)
            list of reference identifiers
            
    Error handling
    --------------
    Exception: "The input threat status is not recognized"
        If the cd_status is not one of the IUCN code, raises this error and stops the execution
    Exception: "The taxon already exists in the database with another threat status"
        If the taxon already has a threat status different to the one provided by the user, raises this exception and stops execution
    """
    # test whether status is compatible with the database specification
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL = "SELECT count(*) FROM threat_status WHERE cd_status = %s"
    cur.execute(SQL, [inputThreat.get('threatstatus')])
    nb = cur.fetchone()['count']
    compatible = bool(nb)
    if (not compatible):
        raise Exception("The input threat status is not recognized")
    else:
        # find the threat status if it exists in the database
        SQL = "SELECT count(*) FROM threat WHERE cd_tax=%s"
        cur.execute(SQL,[cd_tax])
        nb = cur.fetchone()['count']
        statusExists = bool(nb)
        if statusExists:
            # if it exists, look whether it is compatible with the current status
            threatStatus = getThreatStatus(cur,cd_tax)
            sameStatus = (threatStatus.get('cd_status') == inputThreat['threatstatus'])
            if(not sameStatus):
                raise Exception("The taxon already exists in the database with another threat status")
    cur.close()
    with connection:
        with connection.cursor() as cur:
            cdRefs = [manageSource(cur,inputThreat['ref_citation'][i],inputThreat.get('link')[i] if bool(inputThreat.get('link')) else None) for i in range(0,len(inputThreat['ref_citation']))]
            if not statusExists:
                # if it is compatible with an existing status, insert the new source
                SQL = "INSERT INTO threat(cd_tax,cd_status,comments) VALUES (%s,%s,%s)"
                cur.execute(SQL, [cd_tax, inputThreat['threatstatus'],inputThreat.get('comments')])
            # if it does not exist insert the source, the status and make the links
            for i in range(len(cdRefs)):
                SQL = "WITH a AS (SELECT %s AS cd_ref, %s AS cd_tax), b AS(SELECT a.cd_ref,a.cd_tax,rt.id FROM a LEFT JOIN ref_threat AS rt USING (cd_ref,cd_tax)) INSERT INTO ref_threat(cd_ref, cd_tax) SELECT cd_ref,cd_tax FROM b WHERE id IS NULL"
                cur.execute(SQL,[cdRefs[i],cd_tax])
    return {'cd_tax': cd_tax,'cdRefs': cdRefs}


def manageInputEndem(cd_tax,connection,**inputEndem):
    """
    Test whether the status provided by the user is compatible with the current status of the taxon (if it has one), then if it is compatible, inserts the new references provided. If the taxon has no endemic status, it inserts it in the database
    
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
    Returns
    ------------
    dictionary with the following elements:
        cd_tax: int 
            database taxon identifier 
        cds_ref: list(int)
            list of reference identifiers
            
    Error handling
    --------------
    Exception: "The input endemic status is not recognized"
        If the cd_status is not one of the IUCN code, raises this error and stops the execution
    Exception: "The taxon already exists in the database with another endemic status"
        If the taxon already has a endemism status different to the one provided by the user, raises this exception and stops execution
    """
    # test whether status is compatible with the database specification
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL = "WITH e AS (SELECT %s::text AS nivel) SELECT count(*) FROM nivel_endem,e WHERE descr_endem_es = e.nivel OR descr_endem_en = e.nivel OR cd_nivel::text=e.nivel"
    cur.execute(SQL, [inputEndem.get('endemstatus')])
    nb = cur.fetchone()['count']
    compatible = bool(nb)
    if (not compatible):
        raise Exception("The input endemic status is not recognized")
    else:
        # Getting status code
        SQL = "WITH e AS (SELECT %s::text AS nivel) SELECT cd_nivel FROM nivel_endem,e WHERE descr_endem_es = e.nivel OR descr_endem_en = e.nivel OR cd_nivel::text=e.nivel"
        cur.execute(SQL,[inputEndem.get('endemstatus')])
        nivInput = cur.fetchone()['cd_nivel']
        # find the endemism status if it exists in the database
        SQL = "SELECT count(*) FROM endemic WHERE cd_tax=%s"
        cur.execute(SQL,[cd_tax])
        nb = cur.fetchone()['count']
        statusExists = bool(nb)
        if statusExists:
            # if it exists, look whether it is compatible with the current status
            endemStatus = getEndemStatus(cur,cd_tax)
            sameStatus = (nivInput == endemStatus['cd_nivel'])
            if(not sameStatus):
                raise Exception("The taxon already exists in the database with another endemic status")
    cur.close()
    with connection:
        with connection.cursor() as cur:
            cdRefs = [manageSource(cur,inputEndem['ref_citation'][i],inputEndem.get('link')[i] if bool(inputEndem.get('link')) else None) for i in range(0,len(inputEndem['ref_citation']))]
            if not statusExists:
                # if it is compatible with an existing status, insert the new source
                SQL = "INSERT INTO endemic(cd_tax,cd_nivel,comments) VALUES (%s,%s,%s)"
                cur.execute(SQL, [cd_tax, nivInput,inputEndem.get('comments')])
            # if it does not exist insert the source, the status and make the links
            for i in range(len(cdRefs)):
                SQL = "WITH a AS (SELECT %s AS cd_ref, %s AS cd_tax), b AS(SELECT a.cd_ref,a.cd_tax,rt.id FROM a LEFT JOIN ref_endem AS rt USING (cd_ref,cd_tax)) INSERT INTO ref_endem(cd_ref, cd_tax) SELECT cd_ref,cd_tax FROM b WHERE id IS NULL"
                cur.execute(SQL,[cdRefs[i],cd_tax])
    return {'cd_tax': cd_tax,'cdRefs': cdRefs}

def manageInputExot(cd_tax,connection,**inputExot):
    """
    Test whether the status provided by the user is compatible with the current status of the taxon (if it has one), then if it is compatible, inserts the new references provided. If the taxon has no alien/invasive status, it inserts it in the database
    
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
    Returns
    ------------
    dictionary with the following elements:
        cd_tax: int 
            database taxon identifier 
        cds_ref: list(int)
            list of reference identifiers
            
    Error handling
    --------------
    Exception: "The input alien/invasive status is not recognized"
        If the cd_status is not one of the IUCN code, raises this error and stops the execution
    Exception: "The taxon already exists in the database with another alien/invasive status"
        If the taxon already has a alien/invasive status different to the one provided by the user, raises this exception and stops execution
    """
    # test whether status is compatible with the database specification
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # find the  status if it exists in the database
    SQL = "SELECT count(*) FROM exot WHERE cd_tax=%s"
    cur.execute(SQL,[cd_tax])
    nb = cur.fetchone()['count']
    statusExists = bool(nb)
    if statusExists:
        # if it exists, look whether it is compatible with the current status
        exotStatus = getExotStatus(cur,cd_tax)
        sameStatus = (inputExot.get('is_alien') == exotStatus['is_alien']) and (inputExot.get('is_invasive') == exotStatus['is_invasive'])   
        if(not sameStatus):
            raise Exception("The taxon already exists in the database with another alien/invasive status")
    cur.close()
    with connection:
        with connection.cursor() as cur:
            cdRefs = [manageSource(cur,inputExot['ref_citation'][i],inputExot.get('link')[i] if bool(inputExot.get('link')) else None) for i in range(0,len(inputExot['ref_citation']))]
            if not statusExists:
                # if it is compatible with an existing status, insert the new source
                SQL = "INSERT INTO exot(cd_tax,is_alien,is_invasive,comments) VALUES (%s,%s,%s,%s)"
                cur.execute(SQL, [cd_tax,inputExot.get('is_alien'),inputExot.get('is_invasive'),inputExot.get('comments')])
            # if it does not exist insert the source, the status and make the links
            for i in range(len(cdRefs)):
                SQL = "WITH a AS (SELECT %s AS cd_ref, %s AS cd_tax), b AS(SELECT a.cd_ref,a.cd_tax,rt.id FROM a LEFT JOIN ref_exot AS rt USING (cd_ref,cd_tax)) INSERT INTO ref_exot(cd_ref, cd_tax) SELECT cd_ref,cd_tax FROM b WHERE id IS NULL"
                cur.execute(SQL,[cdRefs[i],cd_tax])
    return {'cd_tax': cd_tax,'cdRefs': cdRefs}


