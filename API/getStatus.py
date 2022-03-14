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
DATABASE_URL = os.environ['DATABASE_URL']
PYTHONIOENCODING="UTF-8"

def getThreatStatus(cursor, cd_tax):
    SQL = "SELECT cd_status, comments, STRING_AGG(r.citation, ' | ' ORDER BY r.cd_ref) AS references, STRING_AGG(r.link, ' | ' ORDER BY r.cd_ref) AS links FROM threat t LEFT JOIN ref_threat rt ON t.cd_tax=rt.cd_tax   LEFT JOIN refer r ON rt.cd_ref=r.cd_ref WHERE t.cd_tax=%s GROUP BY cd_status,comments"
    cursor.execute(SQL,[cd_tax])
    res =dict(cursor.fetchone())
    return res

def getEndemStatus(cursor, cd_tax):
    SQL = "SELECT ne.cd_nivel,ne.descr_endem_es endemism, comments, STRING_AGG(r.citation, ' | ' ORDER BY r.cd_ref) AS references, STRING_AGG(r.link, ' | ' ORDER BY r.cd_ref) AS links FROM endemic e LEFT JOIN nivel_endem ne ON e.cd_nivel=ne.cd_nivel LEFT JOIN ref_endem rt ON e.cd_tax=rt.cd_tax   LEFT JOIN refer r ON rt.cd_ref=r.cd_ref WHERE e.cd_tax=%s GROUP BY ne.cd_nivel, ne.descr_endem_es, comments"
    cursor.execute(SQL,[cd_tax])
    res = dict(cursor.fetchone())
    return res

def getExotStatus(cursor, id_tax):
    SQL = "SELECT e.is_alien, e.is_invasive,  e.comments, STRING_AGG(r.citation, ' | ' ORDER BY r.cd_ref) AS references, STRING_AGG(r.link, ' | ' ORDER BY r.cd_ref) AS links FROM exot e LEFT JOIN ref_exot re ON e.cd_tax=re.cd_tax   LEFT JOIN refer r ON re.cd_ref=r.cd_ref WHERE e.cd_tax=%s GROUP BY e.is_alien, e.is_invasive, e.comments"
    cursor.execute(SQL,[id_tax])
    res = dict(cursor.fetchone())
    return res

def testEndemStatus(connection,cd_tax):
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

