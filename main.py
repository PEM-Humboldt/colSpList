from flask_restful import Resource
import requests
import random
import re
import json
import os
import psycopg2
from psycopg2 import sql
from io import BytesIO
from flask import send_file
from fuzzywuzzy import fuzz
DATABASE_URL = os.environ['DATABASE_URL']





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
    content = response.json()
    #content = pd.json_normalize(response.json())
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

def test_taxInDb(connection,**kwargs):
    cur = connection.cursor()
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
        if(infoTax.get("matchType") != "NONE" and(infoTax.get("matchType") == "EXACT" or infoTax.get('confidence') >=90)):
            foundGbif = True
            infoTax.update(get_gbif_tax_from_id(infoTax.get('usageKey')))
    # We need to update the information as well if the taxon is of a level lower than species, because canonicalnames are given without markers, which is not the way it is in the species lists
    if(foundGbif and infoTax.get('rank') in ('SUBSPECIES','VARIETY','FORM','SUBVARIETY','SUPERSPECIES','SUBGENUS','TRIBE')):
        infoTax.update(get_gbif_parsed_from_sci_name(infoTax.get('scientificName')))
    infoTax['foundGbif'] = foundGbif
    return infoTax

def get_rank(connection,rankInput):
    cur = connection.cursor()
    SQL = "WITH a as (SELECT %s AS input) SELECT rank_name,rank_level FROM tax_rank,A WHERE gbif_bb_marker = a.input OR rank_name = a.input OR id_rank= a.input"
    cur.execute(SQL,[rankInput])
    rank, level= cur.fetchone()
    cur.close()
    return rank, level
    

def format_inputTax(connection, acceptedName, acceptedId, **inputTax):
    hasSciName = inputTax.get('scientificname') is not None
    hasCanoName = inputTax.get('canonicalname') is not None
    hasAuth = inputTax.get('authorship')
    hasSup = inputTax.get('tax_sup') is not None
    hasRank = inputTax.get('rank')
    syno = inputTax.get('syno')
    # status: since this is the case where taxa are not found in gbif, the taxon will be noted as either synonym or doubtful
    if(syno):
        status = 'SYNONYM'
        name_sup = None
    else:
        status = 'DOUBTFUL'
    if(hasRank and hasCanoName and hasSciName and (hasSup or syno)):
        rank, level_rank = get_rank(connection,inputTax.get('rank'))
        if (not syno):
            name_sup = inputTax.get('tax_sup')
        name = inputTax.get('canonicalname')
        name_auth = inputTax.get('scientificname')
    else:
        if(hasSciName):
            parsed = get_gbif_parsed_from_sci_name(inputTax.get('scientificname'))[0]
        else:
            parsed = get_gbif_parsed_from_sci_name(inputTax.get('canonicalname'))[0]
        name=parsed.get('canonicalNameComplete')
        name_auth = parsed.get('scientificName')
        if(not hasRank):
            if(parsed.get('rankMarker') is not None):
                rank, level_rank = get_rank(connection,parsed.get('rankMarker'))
            else:
                raise Exception("No way to determine the taxon rank")
        else:
            rank, level_rank = get_rank(connection,inputTax.get('rank'))
        if(not hasSup):
            if(rank_level < 5):#infraspecies: the superior rank is the species which we can get by association between the genus and the epithet
                name_sup = parsed.get('genusOrAbove') + ' ' + parsed.get('specificEpithet')
            elif (rank_level == 5):
                name_sup = parsed.get('genusOrAbove')
            else:
                raise Exception("No sure way to determine the superior taxon")
    if(not hasAuth and name in name_auth):
        extractAuth = name_auth.replace(name,'')
        auth = re.sub("^ *(.+) *$","\1",extractAuth)
        if(auth == ''):
            auth = None
    else:
        auth = inputTax.get('authorship')
    return {'name': name, 'name_auth': name_auth, 'auth': auth, 'tax_rank_name': rank, 'name_sup': name_sup, 'sup_gbif_key': None, 'accepted_name': acceptedName, 'accepted_id': acceptedId,'status': status, 'gbifkey': None, 'source': inputTax.get('source')}

def format_gbif_tax(connection, acceptedId,**gbif_tax):
    rank, level_rank = get_rank(connection, gbif_tax.get('rank'))
    if(level_rank < 5):
        parsed = get_gbif_parsed_from_id(gbif_tax.get('key'))
        name = parsed.get('canonicalNameWithMarker')
        name_auth = parsed.get('scientificName')
    else:
        name = gbif_tax.get('canonicalName')
        name_auth
    if(gbif_tax.get('synonym')):
        name_sup = None
        sup_gbif_key = None
    else:
        name_sup = gbif_tax.get('parent')
        sup_gbif_key = gbif_tax.get('parentKey')
    return {'name': name, 'name_auth': name_auth, 'auth': gbif_tax.get('authorship'), 'tax_rank_name': rank, 'name_sup': name_sup, 'sup_gbif_key': sup_gbif_key, 'accepted_name': gbif_tax.get('accepted'), 'accepted_id': acceptedId, status: gbif_tax.get('status'), source : None}

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

def acceptedId(connection,id_tax:int):
    cur = connection.cursor()
    SQL = "SELECT COALESCE(cd_syno,id_tax) FROM taxon WHERE id_tax=%s"
    cur.execute(SQL,[id_tax])
    res, =cur.fetchone()
    cur.close()
    return res


# TODO : since panda does not simplify particularly the method to write a table in the postgres database, it would be better to remove all the panda dependency and keep only dictionaries...
# if the direct parent is not in the database
# testing its presence in gbif
# formatting in a way that keep only the parent which are not in the database
# inserting in the database one by one with a returning clause which gives the ID to be used in the following descendant...
# using the same kind of returning clause to get the accepted id from the thing
# in all the inserting into taxon clause, it would be possible as well to use a with clause in order to create a recursing with pseudo-table and avoid temporary table...

def manageInputTax(**inputTax):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    syno = False
    inputTax.update(test_taxInDb(connection=conn,**inputTax))
    if (not inputTax.get('alreadyInDb')):
        infoBaseTax = get_infoTax(**inputTax)
        infoBaseTax['syno'] = False
        # In case we did not find the taxon at first be it is indeed in the database
        recheck = test_taxInDb(connection=conn,gbifkey=infoBaseTax['key'])
        inputTax['alreadyInDb']=recheck.get('alreadyInDb')
        inputTax['idTax'] = recheck.get('idTax')
    if (not inputTax.get('alreadyInDb')):
        # synonyms
        if(infoBaseTax.get('foundGbif') and infoBaseTax.get('synonym')): # synonym found through gbif, note: all synonym info from the arguments (positive, negative, precise or not) in the function will not be considered... GBIF being our backbone here!
            syno = True
            infoBaseTax['syno'] = True
            infoSyno = infoBaseTax
            synoArgs = inputTax
            synoArgs['syno'] = True
            acceptedArgs = {'gbifkey':infoSyno.get('acceptedUsageKey')}
        if(not infoBaseTax.get('foundGbif') and (inputTax.get('synogbifkey') is not None or inputTax.get('synoscientificname') is not None or inputTax.get('synocanonicalname') is not None)):
            syno = True
            infoBaseTax['syno'] = True
            infoSyno = infoBaseTax
            synoArgs = inputTax
            synoArgs['syno'] = True
            acceptedArgs = {gbifkey: inputTax.get('synogbifkey'), scientificname: inputTax.get('synoscientificname'), canonicalname: inputTax.get('synocanonicalname')}
        if(syno): 
            acceptedArgs.update(test_taxInDb(connection=conn,**acceptedArgs))
            if(not synoArgs.get('alreadyInDb')):
                infoAccepted = get_infoTax(**synoArgs)
                acceptedArgs['syno'] = False
                recheckAccepted = test_taxInDb(connection=conn,gbifkey=infoAccepted.get('key'))
                acceptedArgs['alreadyInDb'] = recheckAccepted.get('alreadyInDb')
                acceptedArgs['idTax'] = recheckAccepted.get('idTax')
        # The smart  move I think would be to manage formats (taxa recognized or not by gbif) here in order to:
        # - get the ranks
        # - get the simplified versions of taxa before going to parents
        # - change the names of dictionaries in order to get the "accepted" taxon in one variable, synonyms or not, recognized by gbif or not
        insertDF = pd.DataFrame()
        if(not infoBaseTax.get('foundGbif')):
            if(syno):
                acc=format_inputTax(conn,**acceptedArgs)
                insertDF.append(acc)
            else:
                acc=format_inputTax(conn,**inputTax)
                insertDF.append(acc)
        else:
            if(syno)
                acc=format_gbif_tax(**infoAccepted)
                insertDF.append(acc)
            else:
                acc=format_gbif_tax(**infoBaseTax)
                insertDF.append(acc)
        if(syno and not synoArgs.get('alreadyInDb')):
            if(acceptedArgs.get('alreadyInDb')):
                synoArgs['dbaccepted_id'] = acceptedArgs['idTax']# Here we need to get the scientificname from the database, or change the functions in order to accept directly the id_syno in the table
            else:
                synoArgs['acceptedsciname']=acc[0,'name_auth']# Here it works only whether acc is created (which means the acceptedname is not alreadyInDb)
            if(synoArgs.get('foundGbif')):
                format_gbif_tax(conn,**infoSyno)
            else:
                synoDF = format_inputTax(conn,**synoArgs)
        conn.close()
    else:
        
        conn.close()
    # parents: note that for now we will take parents only for the accepted names, synonyms in the taxon table will be considered as not having parents. Note that if the 
    #3 cases:
    # Not syno and found in gbif -> look and search for parents 
    # syno and accepted found in gbif (it does not matter yet that the synomym is not found in gbif)
    # Not syno and not found in gbif -> parse name, verify parent name
    # syno and accepted not found in gbif -> parse 
    
    return accId

manageInputTax(scientificname='Acacia farnesiana (L.) Willd.')
inputTax={'scientificname':'Acacia farnesiana (L.) Willd.'}
