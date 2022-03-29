"""
Functions allowing to get status (alien/invasive, threats or endemisms) of the species in Colombia 
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
import pandas as pd
DATABASE_URL = os.environ['DATABASE_URL']
PYTHONIOENCODING="UTF-8"

def getThreatStatus(cursor, cd_tax):
    """
    Get the threat status of a taxon, with the associated references and links
    
    Parameters
    -----------
    cursor: psycopg2 cursor
        cursor of the current operations in the postgres database (need to be of psycopg2.extras.RealDictCursor type, in order to obtain query results as python dictionaries)
    cd_tax: cd_tax of the accepted taxon
    
    Returns
    ----------
    Dictionary with the following elements:
        cd_status: str
            IUCN code for the threat status of the taxon
        comments: str
            comments associated with the threat status of the species
        references: str 
            bibliographic references associated with the threat status of the species, separated with the "|" character (NOTE: If the status change through time, we keep the references corresponding to the previous threat statuses)
        links: str 
            URL links to ressources associated with the references in the "references" element        
    """
    SQL = "SELECT cd_status, comments, STRING_AGG(r.citation, ' | ' ORDER BY r.cd_ref) AS references, STRING_AGG(r.link, ' | ' ORDER BY r.cd_ref) AS links FROM threat t LEFT JOIN ref_threat rt ON t.cd_tax=rt.cd_tax   LEFT JOIN refer r ON rt.cd_ref=r.cd_ref WHERE t.cd_tax=%s GROUP BY cd_status,comments"
    cursor.execute(SQL,[cd_tax])
    res =dict(cursor.fetchone())
    return res

def getEndemStatus(cursor, cd_tax):
    """
    Get the endemism status of a taxon, with the associated references and links
    
    Parameters
    -----------
    cursor: psycopg2 cursor
        cursor of the current operations in the postgres database (need to be of psycopg2.extras.RealDictCursor type, in order to obtain query results as python dictionaries)
    cd_tax: cd_tax of the accepted taxon
    
    Returns
    ----------
    Dictionary with the following elements:
        cd_nivel: int
            database code for the endemism level (from 0 when the information is unsuficient, to 4 when the species is clearly endemic in Colombia)
        descr_endem_es : str 
            Endemic level description in spanish
        comments: str
            comments associated with the endemism status of the species
        references: str 
            bibliographic references associated with the endemism status of the species, separated with the "|" character (NOTE: If the status change through time, we keep the references corresponding to the previous endemism statuses)
        links: str 
            URL links to ressources associated with the references in the "references" element        
    """
    SQL = "SELECT ne.cd_nivel,ne.descr_endem_es endemism, comments, STRING_AGG(r.citation, ' | ' ORDER BY r.cd_ref) AS references, STRING_AGG(r.link, ' | ' ORDER BY r.cd_ref) AS links FROM endemic e LEFT JOIN nivel_endem ne ON e.cd_nivel=ne.cd_nivel LEFT JOIN ref_endem rt ON e.cd_tax=rt.cd_tax   LEFT JOIN refer r ON rt.cd_ref=r.cd_ref WHERE e.cd_tax=%s GROUP BY ne.cd_nivel, ne.descr_endem_es, comments"
    cursor.execute(SQL,[cd_tax])
    res = dict(cursor.fetchone())
    return res

def getExotStatus(cursor, id_tax):
    """
    Get the alien/invasive status of a taxon, with the associated references and links
    
    Parameters
    -----------
    cursor: psycopg2 cursor
        cursor of the current operations in the postgres database (need to be of psycopg2.extras.RealDictCursor type, in order to obtain query results as python dictionaries)
    cd_tax: cd_tax of the accepted taxon
    
    Returns
    ----------
    Dictionary with the following elements:
        is_alien: bool
            Whether the taxon is alien or not in Colombia
        is_invasive : bool 
            Whether the taxon is invasive or not
        comments: str
            comments associated with the alien/invasive status of the species
        references: str 
            bibliographic references associated with the alien/invasive status of the species, separated with the "|" character (NOTE: If the status change through time, we keep the references corresponding to the previous alien/invasive statuses)
        links: str 
            URL links to ressources associated with the references in the "references" element        
    """
    SQL = "SELECT e.is_alien, e.is_invasive,  e.comments, STRING_AGG(r.citation, ' | ' ORDER BY r.cd_ref) AS references, STRING_AGG(r.link, ' | ' ORDER BY r.cd_ref) AS links FROM exot e LEFT JOIN ref_exot re ON e.cd_tax=re.cd_tax   LEFT JOIN refer r ON re.cd_ref=r.cd_ref WHERE e.cd_tax=%s GROUP BY e.is_alien, e.is_invasive, e.comments"
    cursor.execute(SQL,[id_tax])
    res = dict(cursor.fetchone())
    return res

def testEndemStatus(connection,cd_tax):
    """
    Test whether the taxon associated with the provided cd_tax has an endemism status.
    
    Parameters
    -----------
    connection: psycopg2 connection
        connection to the postgres database
    cd_tax: cd_tax of the accepted taxon
    
    Returns
    ----------
    Dictionary with the following elements:
        hasEndemStatus: bool
            Whether there is information about an endemism status for the taxon associated with the cd_tax
        cd_nivel: int
            database code for the endemism level (from 0 when the information is unsuficient, to 4 when the species is clearly endemic in Colombia)
        descr_endem_es : str 
            Endemic level description in spanish
        comments: str
            comments associated with the endemism status of the species
        references: str 
            bibliographic references associated with the endemism status of the species, separated with the "|" character (NOTE: If the status change through time, we keep the references corresponding to the previous endemism statuses)
        links: str 
            URL links to ressources associated with the references in the "references" element        
    """
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL = "SELECT count(*) FROM endemic WHERE cd_tax = %s"
    cur.execute(SQL,[cd_tax])
    hasEndemStatus = bool(cur.fetchone()['count'])
    res = {'hasEndemStatus': hasEndemStatus}
    if hasEndemStatus:
        res.update(getEndemStatus(cur,cd_tax))
    else:
        res.update({'cd_nivel':None, 'descr_endem_es': None, 'comments': None, 'references': None, 'links': None})
    return res

def testExotStatus(connection,cd_tax):
    """
    Test whether a taxon has an alien/invasive status, and returns the status
    
    Parameters
    -----------
    connection: psycopg2 connection
        connection to the postgres database
    cd_tax: cd_tax of the accepted taxon
    
    Returns
    ----------
    Dictionary with the following elements:
        hasExotStatus: bool
            Whether the taxon has an invasive/alien status in Colombia
        is_alien: bool
            Whether the taxon is alien or not in Colombia
        is_invasive : bool 
            Whether the taxon is invasive or not
        comments: str
            comments associated with the alien/invasive status of the species
        references: str 
            bibliographic references associated with the alien/invasive status of the species, separated with the "|" character (NOTE: If the status change through time, we keep the references corresponding to the previous alien/invasive statuses)
        links: str 
            URL links to ressources associated with the references in the "references" element        
    """
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL = "SELECT count(*) FROM exot WHERE cd_tax = %s"
    cur.execute(SQL,[cd_tax])
    hasExotStatus = bool(cur.fetchone()['count'])
    res = {'hasExotStatus': hasExotStatus}
    if hasExotStatus:
        res.update(getExotStatus(cur,cd_tax))
    else:
        res.update({'cd_nivel':None, 'is_alien': None, 'is_invasive': None,'comments': None,'references': None, 'links': None})
    return res

def testThreatStatus(connection,cd_tax):
    """
    Test whether a taxon has a threat status, and returns the status
    
    Parameters
    -----------
    connection: psycopg2 connection
        connection to the postgres database
    cd_tax: cd_tax of the accepted taxon
    
    Returns
    ----------
    Dictionary with the following elements:
        hasThreatStatus: bool
            Whether the taxon has a threat status in Colombia
        cd_status: str
            IUCN code for the threat status of the taxon
        comments: str
            comments associated with the threat status of the species
        references: str 
            bibliographic references associated with the threat status of the species, separated with the "|" character (NOTE: If the status change through time, we keep the references corresponding to the previous threat statuses)
        links: str 
            URL links to ressources associated with the references in the "references" element        
    """
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL = "SELECT count(*) FROM threat WHERE cd_tax = %s"
    cur.execute(SQL,[cd_tax])
    hasThreatStatus = bool(cur.fetchone()['count'])
    res = {'hasThreatStatus': hasThreatStatus}
    if hasThreatStatus:
        res.update(getThreatStatus(cur,cd_tax))
    else:
        res.update({'cd_status':None, 'comments': None, 'references': None, 'links': None})
    return res

def getListExot(connection, listChildren, formatExport):
    if len(listChildren)==0:
        SQL="SELECT * FROM exot_list"
        if formatExport=="CSV":
             res = pd.read_sql_query(SQL, connection)
        else:
            cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(SQL)
            res = cur.fetchall()
            cur.close()
    else:
        SQL="SELECT * FROM exot_list WHERE cd_tax IN (SELECT UNNEST( %s ))"
        if formatExport=="CSV":
            cur=connection.cursor()
            query=cur.mogrify(SQL,[listChildren])
            cur.close()
            res=pd.read_sql_query(query,connection)
        else:
            cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(SQL,[listChildren])
            res = cur.fetchall()
            cur.close()
    return res
        

def getListEndem(connection, listChildren, formatExport):
    if len(listChildren)==0:
        SQL="SELECT * FROM endem"
        if formatExport=="CSV":
             res = pd.read_sql_query(SQL, connection)
        else:
            cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(SQL)
            res = cur.fetchall()
            cur.close()
    else:
        SQL="SELECT * FROM endem_list WHERE cd_tax IN (SELECT UNNEST( %s ))"
        if formatExport=="CSV":
            cur=connection.cursor()
            query=cur.mogrify(SQL,[listChildren])
            cur.close()
            res=pd.read_sql_query(query,connection)
        else:
            cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(SQL,[listChildren])
            res = cur.fetchall()
            cur.close()
    return res
        

def getListThreat(connection, listChildren, formatExport):
    if len(listChildren)==0:
        SQL="SELECT * FROM threat_list"
        if formatExport=="CSV":
             res = pd.read_sql_query(SQL, connection)
        else:
            cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(SQL)
            res = cur.fetchall()
            cur.close()
    else:
        SQL="SELECT * FROM threat_list WHERE cd_tax IN (SELECT UNNEST( %s ))"
        if formatExport=="CSV":
            cur=connection.cursor()
            query=cur.mogrify(SQL,[listChildren])
            cur.close()
            res=pd.read_sql_query(query,connection)
        else:
            cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(SQL,[listChildren])
            res = cur.fetchall()
            cur.close()
    return res
        
def getListTax(connection, listChildren, formatExport):
    if len(listChildren)==0:
        SQL="SELECT *  FROM tax_list"
        if formatExport=="CSV":
             res = pd.read_sql_query(SQL, connection)
        else:
            cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(SQL)
            res = cur.fetchall()
            cur.close()
    else:
        SQL="SELECT * FROM tax_list WHERE cd_tax IN (SELECT UNNEST( %s ))"
        if formatExport=="CSV":
            cur=connection.cursor()
            query=cur.mogrify(SQL,[listChildren])
            cur.close()
            res=pd.read_sql_query(query,connection)
        else:
            cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(SQL,[listChildren])
            res = cur.fetchall()
            cur.close()
    return res

def getTax(connection, cd_tax):
    cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL="SELECT *  FROM tax_list WHERE cd_tax = %s"
    cur.execute(SQL, [cd_tax])
    tax = cur.fetchone()
    return tax

def getListReferences(connection, formatExport="JSON",onlyEndem=False, onlyExot=False, onlyThreat=False):
    if not (onlyEndem or onlyExot or onlyThreat):
        SQL = "SELECT * FROM ref_list"
    else:
        SQL= "SELECT * FROM ref_list WHERE "
        if onlyExot:
            SQL += 'nb_exot>0 '
        else:
            SQL += 'TRUE '
        if onlyEndem:
            SQL += 'AND nb_endem>0 '
        else:
            SQL += 'AND TRUE '
        if onlyThreat:
            SQL += 'AND nb_threat>0'
        else:
            SQL+= 'AND TRUE'
    if formatExport=="CSV":
        listRef=pd.read_sql_query(SQL, connection)
    else:
        cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(SQL)
        listRef=cur.fetchall()
        cur.close()
    return listRef


