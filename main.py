from flask_restful import Resource
import requests
import random
import re
import json
import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from io import BytesIO
from flask import send_file
from fuzzywuzzy import fuzz






def get_gbif_tax_from_id(gbifid: int):
    api = f"https://api.gbif.org/v1/species/{gbifid}"
    response = requests.get(api)
    content = response.json()
    return content

def get_gbif_tax_from_name(name: str):
    api = f"https://api.gbif.org/v1/species/match/?name={name}"
    response = requests.get(api)
    content = response.json()
    return content

def get_gbif_tax_from_sci_name(sci_name: str):
    api = f"https://api.gbif.org/v1/species/match/?name={sci_name},nameType=SCIENTIFIC"
    response = requests.get(api)
    content = response.json()
    return content

def get_gbif_parent(gbifkey: int):
    api= f"https://api.gbif.org/v1/species/{gbifkey}/parents"
    response = requests.get(api)
    content = pd.json_normalize(response.json())
    return content

def get_gbif_parsed_from_id(gbifkey: int):
    api= f"https://api.gbif.org/v1/species/{gbifkey}/name"
    response = requests.get(api)
    content = response.json()
    return content

def get_gbif_parsed_from_sci_name(sci_name: str):
    api= f"https://api.gbif.org/v1/parser/name?name={sci_name}"
    response = requests.get(api)
    content = response.json()
    return content


def get_gbif_synonyms(gbifkey: int):
    api= f"https://api.gbif.org/v1/species/{gbifkey}/synonyms"
    response = requests.get(api)
    content = response.json()
    return content

def test_taxInDb(**kwargs):
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    alreadyInDb = False
    gbifMatchMode = None
    idTax = None
    if (kwargs.get('gbifkey') is not None):
        SQL = "SELECT count(*) AS nb FROM taxon WHERE gbifkey = %s"
        cur.execute(SQL, [kwargs.get('gbifkey')])
        gbifKeyInDb_nb, = cur.fetchone()
        if (gbifKeyInDb_nb == 1):
            if(kwargs.get('canonicalname') is not None):
                SQL = "SELECT name FROM taxon WHERE gbifkey = %s"
                cur.execute(SQL,[kwargs.get('gbifkey')])
                nameTaxDb, = cur.fetchone()
                diffTaxName = fuzz.ratio(nameTaxDb,kwargs.get('canonicalname'))
                if (diffTaxName < 0.75):
                    raise Exception("Name of the taxon does not correspond to gbifkey")
                else:
                    alreadyInDb = True
                    SQL = "SELECT id_tax FROM taxon WHERE gbifkey = %s"
                    cur.execute(SQL,[kwargs.get('gbifkey')])
                    idTax,  = cur.fetchone()
        elif (gbifKeyInDb_nb == 0):
            gbifMatchMode = 'gbifkey'
        else :
            raise Exception("gbifkey more than once in the database, should not be possible!")
    elif (kwargs.get('scientificname') is not None):
        SQL = "SELECT count(*) AS nb FROM taxon WHERE name_auth = %s"
        cur.execute(SQL,[kwargs.get('scientificname')])
        gbifSciInDb_nb, = cur.fetchone()
        if (gbifSciInDb_nb == 1):
            alreadyInDb = True
            SQL = "SELECT id_tax FROM taxon WHERE gbifkey = %s"
            cur.execute(SQL,[kwargs.get('scientificname')])
            idTax,  = cur.fetchone()
        elif (gbifSciInDb_nb == 0):
            infoTax = get_gbif_tax_from_sci_name(kwargs.get('scientificname'))
            gbifMatchMode = 'scientificname'
        else:
            raise Exception("Name (with author) in the database more than once, should not be possible!")
    elif (kwargs.get('canonicalname') is not None):
        SQL = "SELECT count(*) AS nb FROM taxon WHERE name =%s"
        cur.execute(SQL,[kwargs.get('canonicalname')])
        gbifNameInDb_nb, = cur.fetchone()
        if (gbifNameInDb_nb == 1):
            alreadyInDb = True
            SQL = "SELECT id_tax FROM taxon WHERE name = %s"
            cur.execute(SQL, [kwargs.get('canonicalname')])
            idTax, = cur.fetchone()
        elif (gbifNameInDb_nb == 0):
            infoTax = get_gbif_tax_from_name(kwargs.get('canonicalname'))
            gbifMatchMode = 'canonicalname'
        else:
            raise Exception("Name (without author) exists more than once in the database, please provide scientificname or gbifkey instead, in order to be able to identify which taxon you are referring to")
    else:
        raise Exception("Either 'gbifkey', or 'scientificname', or 'canonicalname' should be included in the parameters in order to be able to identify the taxon")
    cur.close()
    conn.close()
    return {'alreadyInDb': alreadyInDb, 'gbifMatchMode': gbifMatchMode, 'idTax': idTax}

def get_infoTax(**kwargs):
    foundGbif = False
    if (kwargs.get('gbifMatchMode') == 'gbifkey'):
        infoTax = get_gbif_tax_from_id(kwargs.get('gbifkey'))
        foundGbif = True
    elif (kwargs.get('gbifMatchMode') == 'canonicalname'):
        infoTax = get_gbif_tax_from_name(kwargs.get('canonicalname'))
    elif (kwargs.get('gbifMatchMode') == 'scientificname'):
        infoTax = get_gbif_tax_from_sci_name(kwargs.get('scientificname'))
    else:
        raise Exception("No acceptable gbifMatchMode were provided")
    if(kwargs.get('gbifMatchMode') in ('scientificname','canonicalname')):
        if(infoTax.get("matchType") == "EXACT" or infoTax.get('confidence') >=90):
            foundGbif = True
            infoTax.update(get_gbif_tax_from_id(infoTax.get('usageKey')))
    # We need to update the information as well if the taxon is of a level lower than species, because canonicalnames are given without markers, which is not the way it is in the species lists
    if(foundGbif and infoTax.get('rank') in ('SUBSPECIES','VARIETY','FORM','SUBVARIETY','SUPERSPECIES','SUBGENUS','TRIBE')):
        infoTax.update(get_gbif_parsed_from_sci_name(infoTax.get('scientificName')))
    infoTax['foundGbif'] = foundGbif
    return infoTax
    
def format_infoTax()
    # Here we need to format the data from gbif from species matching ()into something that could feed the database
    None

def insert_tax(**kwargs):
    # Managing matchtype, precision and potential need to get all the informations if no confident match is found from gbif
    if (kwargs.get('gbifMatchMode') in ('scientificname','canonicalname') and ( infoTax.get('confidence') is None or infoTax.get('confidence') < 90)):
        None
    if (infoTax.get('matchType') == 'NONE'):
        # We are here in the cases where the information is not on gbif, the function should have been given sufficient information to populate the database "by hand"            
        
        # Managing synonyms: note in case of synonyms, we need to be sure all synonyms in the database will be attached to the same taxon status
        # Managing parents
        # In the process of parents and taxonomic level, it might be important to get the parsed names in case of underspecies taxa because canonicalnames in these cases come without markers, but most probably will come with it in the user lists. (I can't think of any case where this could happen in higher levels though)
        # final insertion
        return infoTax

def manageInputTax(**kwargs):
    syno = False
    kwargs.update(test_taxInDb(**kwargs))
    if (not kwargs.get('alreadyInDb')):
        infoTax = get_infoTax(**kwargs)
        # In case we did not find the taxon at first be it is indeed in the database
        recheck = test_taxInDb(gbifkey=infoTax('usageKey'))
        kwargs['alreadyInDb']=recheck['alreadyInDb']
        kwargs['idTax'] = recheck['idTax']
    if (not kwargs.get('alreadyInDb')):
        # synonyms
        if(infoTax.get('foundGbif') and infoTax.get('synonym')): # synonym found through gbif, note: all synonym info from the arguments (positive, negative, precise or not) in the function will not be considered... GBIF being our backbone here!
            syno = True
            synoArgs = {'gbifkey':infoTax.get('acceptedUsageKey')}
        if(not infoTax.get('foundGbif') and (kwargs.get('synogbifkey') is not None or kwargs.get('synoscientificname') is not None or kwargs.get('synocanonicalname') is not None)):
            syno = True
            synoArgs = {gbifkey: kwargs.get('synogbifkey'), scientificname: kwargs.get('synoscientificname'), canonicalname: kwargs.get('synocanonicalname')}
        if(syno): 
            synoArgs.update(test_taxInDb(**synoArgs))
            if(not synoArgs.get('alreadyInDb')):
                infoAccepted = get_infoTax(**synoArgs)
                recheckSyno = test_taxInDb(gbifkey=infoAccepted['usageKey'])
                synoArgs['alreadyInDb'] = recheckSyno['alreadyInDb']
                synoArgs['idTax'] = recheckSyno ['idTax']
                tmp_var = (infoTax,infoAccepted)
        else:
            tmp_var=(infoTax)
    return tmp_var

manageInputTax(scientificname='Acacia farnesiana (L.) Willd.')
kwargs={'scientificname':'Acacia farnesiana (L.) Willd.'}
