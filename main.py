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
    content = response.json()[0]
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
            SQL = "SELECT id_tax FROM taxon WHERE name_auth = %s"
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
    hasSup = inputTax.get('parentcanonicalname') is not None or inputTax.get('parentscientificname') is not None or inputTax.get('parentgbifkey') is not None
    hasRank = inputTax.get('rank')
    syno = inputTax.get('syno')
    parentTax = {'canonicalname':inputTax.get('parentcanonicalname'),'scientificname':inputTax.get('parentscientificname'),'gbifkey':inputTax.get('parentgbifkey')}
    # status: since this is the case where taxa are not found in gbif, the taxon will be noted as either synonym or doubtful
    if(syno):
        status = 'SYNONYM'
    else:
        status = 'DOUBTFUL'
    if(hasRank and hasCanoName and hasSciName and (hasSup or syno)):
        rank, level_rank = get_rank(connection,inputTax.get('rank'))
        #if (not syno):
        #    name_sup = inputTax.get('tax_sup')
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
        if(parentTax.get('canonicalname') is None):
            if(rank_level < 5):#infraspecies: the superior rank is the species which we can get by association between the genus and the epithet
                parentTax['canonicalName'] = parsed.get('genusOrAbove') + ' ' + parsed.get('specificEpithet')
            elif (rank_level == 5):
                parentTax['canonicalname'] = parsed.get('genusOrAbove')
            else:
                if(not hasSup and not syno):
                    raise Exception("No sure way to determine the superior taxon")
    if(not hasAuth and name in name_auth):
        extractAuth = name_auth.replace(name,'')
        auth = re.sub("^ *(.+) *$","\1",extractAuth)
        if(auth == ''):
            auth = None
    else:
        auth = inputTax.get('authorship')
    return {'name': name, 'name_auth': name_auth, 'auth': auth, 'tax_rank_name': rank, 'status': status, 'gbifkey': None, 'source': inputTax.get('source')}, parentTax

def format_gbif_tax(connection,**gbif_tax):
    rank, level_rank = get_rank(connection, gbif_tax.get('rank'))
    if(level_rank < 5):
        parsed = get_gbif_parsed_from_id(gbif_tax.get('key'))
        name = parsed.get('canonicalNameWithMarker')
        name_auth = parsed.get('scientificName')
    else:
        name = gbif_tax.get('canonicalName')
        name_auth = gbif_tax.get('scientificName')
    if(gbif_tax.get('syno')):
        status = 'SYNONYM'
    else:
        status = gbif_tax.get('status')
        if (status is None):
            status = gbif_tax.get('taxonomicStatus')
    parentTax = {'gbifkey': gbif_tax.get('parentKey'), 'canonicalname': gbif_tax.get('parent')}
    return {'name': name, 'name_auth': name_auth, 'auth': gbif_tax.get('authorship'), 'tax_rank_name': rank, 'status': status, 'gbifkey': gbif_tax.get('key'), 'source' : None}, parentTax

def format_parents(connection,parents):
    idParentInDb = None
    listFormatted = []
    for i in parents:
        i.update(test_taxInDb(connection,**{'gbifkey':i.get('key')}))
        if(i.get('alreadyInDb')):
            idParentInDb=i.get('idTax')
        else:
            listFormatted.append({'name':i.get('canonicalName'), 'name_auth': i.get('scientificName'),'auth':i.get('authorship'),'tax_rank_name': i.get('rank'), 'status': i.get('taxonomicStatus'), 'gbifkey':i.get('key'), 'source': None})
    return idParentInDb, listFormatted

def acceptedId(connection,id_tax:int):
    cur = connection.cursor()
    SQL = "SELECT COALESCE(cd_syno,id_tax) FROM taxon WHERE id_tax=%s"
    cur.execute(SQL,[id_tax])
    res, =cur.fetchone()
    cur.close()
    return res

def insertTax(cursor,idParent,idSyno,**tax):
    SQL = "WITH a AS( SELECT %s AS name, %s AS name_auth, %s AS auth, %s AS name_rank, %s AS status, %s AS gbif_key, %s AS source, %s AS cd_sup, %s AS cd_syno), b AS (SELECT name, name_auth, CASE WHEN NOT auth ~ '^ *$' THEN auth ELSE NULL END AS auth, id_rank,cd_sup::int, cd_syno::int, status, gbif_key, source::int FROM a JOIN tax_rank t ON a.name_rank=t.rank_name)  INSERT INTO taxon(name,name_auth,auth,tax_rank,cd_sup,cd_syno,status, gbifkey, source) SELECT * FROM b RETURNING id_tax"
    cursor.execute(SQL,(tax.get('name'), tax.get('name_auth'), tax.get('auth'), tax.get('tax_rank_name'),tax.get('status'), tax.get('gbifkey'),tax.get('source'),idParent,idSyno))
    idInserted, = cursor.fetchone()
    return idInserted
    
    
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
        inputTax.update(get_infoTax(**inputTax))
        inputTax['syno'] = False
        # In case we did not find the taxon at first be it is indeed in the database
        recheck = test_taxInDb(connection=conn,gbifkey=inputTax.get('key'))
        inputTax['alreadyInDb']=recheck.get('alreadyInDb')
        inputTax['idTax'] = recheck.get('idTax')
    if (not inputTax.get('alreadyInDb')):
        # synonyms
        if(inputTax.get('foundGbif') and inputTax.get('synonym')): # synonym found through gbif, note: all synonym info from the arguments (positive, negative, precise or not) in the function will not be considered... GBIF being our backbone here!
            syno = True
            inputTax['syno'] = True
            acceptedTax = {'gbifkey':inputTax.get('acceptedUsageKey')}
        if(not inputTax.get('foundGbif') and (inputTax.get('synogbifkey') is not None or inputTax.get('synoscientificname') is not None or inputTax.get('synocanonicalname') is not None)):
            syno = True
            inputTax['syno'] = True
            acceptedTax = {gbifkey: inputTax.get('synogbifkey'), scientificname: inputTax.get('synoscientificname'), canonicalname: inputTax.get('synocanonicalname')}
        if(syno): 
            acceptedTax.update(test_taxInDb(connection=conn,**acceptedTax))
            if(not acceptedTax.get('alreadyInDb')):
                acceptedTax.update(get_infoTax(**acceptedTax))
                acceptedTax['syno'] = False
                recheckAccepted = test_taxInDb(connection=conn,gbifkey=acceptedTax.get('key'))
                acceptedTax['alreadyInDb'] = recheckAccepted.get('alreadyInDb')
                acceptedTax['idTax'] = recheckAccepted.get('idTax')
        # The smart  move I think would be to manage formats (taxa recognized or not by gbif) here in order to:
        # - get the ranks
        # - get the simplified versions of taxa before going to parents
        # - change the names of dictionaries in order to get the "accepted" taxon in one variable, synonyms or not, recognized by gbif or not
            if(not acceptedTax.get('alreadyInDb')):
                if(acceptedTax.get('foundGbif')):
                    accepted, parentTax = format_gbif_tax(connection=conn, **acceptedTax)
                else:
                    accepted, parentTax = format_inputTax(connection=conn, **acceptedTax)
            if(inputTax.get('foundGbif')):
                synonym, synoParent = format_gbif_tax(connection=conn, **inputTax)
            else:
                synonym, synoParent = format_inputTax(connection=conn, **inputTax)
        else:
            if(not inputTax.get('alreadyInDb')):
                if(inputTax.get('foundGbif')):
                    accepted, parentTax = format_gbif_tax(connection=conn, **inputTax)
                else:
                    accepted, parentTax = format_input_tax(connection=conn, acceptedName = None, acceptedId=None,**inputTax)
        
        parentTax.update(test_taxInDb(conn,**parentTax))
        if(not parentTax.get('alreadyInDb')):
            if(accepted.get('gbifkey') is None):
                parentTax.update(get_infoTax(**parentTax))
                if (not parentTax.get('foundGbif')):
                    raise Exception('Parent taxa not found')
                parents = get_gbif_parent(parentTax.get('key'))
                parents.append(parentTax)
            else:
                parents = get_gbif_parent(accepted.get('gbifkey'))
            idParentInDb, parentsFormatted = format_parents(conn,parents)
        with conn:
            with conn.cursor() as cur:
                if(not parentTax.get('alreadyInDb')):
                    for i in range(0,len(parentsFormatted)):
                        idParentInDb = insertTax(cur,idParentInDb,None,**parentsFormatted[i])
                else:
                    idParentInDb=parentTax.get('idTax')
                if(syno and acceptedTax.get('alreadyInDb')):
                    accId=accepted.get('idTax')
                else:
                    accId=insertTax(cur,idParentInDb,idSyno=None,**accepted)
                if(syno):
                    insertTax(cur, None, accId, **synonym)
        cur.close()
        conn.close()
    else:
        accId = acceptedId(connection=conn,id_tax=inputTax.get('idTax'))
        conn.close()
    return accId


def manageSource(cursor, ref_citation, ref_link):
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
    return(cdRef)

def getThreatStatus(cursor, id_tax):
    SQL = "SELECT cd_status, comments, STRING_AGG(r.citation, ' | ' ORDER BY r.cd_ref) AS references, STRING_AGG(r.link, ' | ' ORDER BY r.cd_ref) AS links FROM threat t LEFT JOIN ref_threat rt ON t.cd_tax=rt.cd_tax   LEFT JOIN refer r ON rt.cd_ref=r.cd_ref WHERE t.cd_tax=%s GROUP BY cd_status,comments"
    cursor.execute(SQL,[id_tax])
    res =dict(cursor.fetchone())
    return res

def manageInputThreat(id_tax, connection, **inputThreat):
    # test whether status is compatible with the database specification
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL = "SELECT count(*) FROM threat_status WHERE id_status = %s"
    cur.execute(SQL, [inputThreat.get('threatstatus')])
    nb = cur.fetchone()['count']
    compatible = bool(nb)
    if (not compatible):
        raise Exception("The input threat status is not recognized")
    else:
        # find the threat status if it exists in the database
        SQL = "SELECT count(*) FROM threat WHERE cd_tax=%s"
        cur.execute(SQL,[id_tax])
        nb = cur.fetchone()['count']
        statusExists = bool(nb)
        if statusExists:
            # if it exists, look whether it is compatible with the current status
            threatStatus = getThreatStatus(cur,id_tax)
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
                cur.execute(SQL, [id_tax, inputThreat['threatstatus'],inputThreat.get('comments')])
            # if it does not exist insert the source, the status and make the links
            for i in range(len(cdRefs)):
                SQL = "WITH a AS (SELECT %s AS cd_ref, %s AS cd_tax), b AS(SELECT a.cd_ref,a.cd_tax,rt.id FROM a LEFT JOIN ref_threat AS rt USING (cd_ref,cd_tax)) INSERT INTO ref_threat(cd_ref, cd_tax) SELECT cd_ref,cd_tax FROM b WHERE id IS NULL"
                cur.execute(SQL,[cdRefs[i],id_tax])
    return {'id_tax': id_tax,'cdRefs': cdRefs}


def insertHabito(id_tax,connection,**inputHabito):
    None

def getEndemStatus(cursor, id_tax):
    SQL = "SELECT ne.cd_nivel,ne.descr_endem_es endemism, comments, STRING_AGG(r.citation, ' | ' ORDER BY r.cd_ref) AS references, STRING_AGG(r.link, ' | ' ORDER BY r.cd_ref) AS links FROM endemic e LEFT JOIN nivel_endem ne ON e.cd_nivel=ne.cd_nivel LEFT JOIN ref_endem rt ON e.cd_tax=rt.cd_tax   LEFT JOIN refer r ON rt.cd_ref=r.cd_ref WHERE e.cd_tax=%s GROUP BY ne.cd_nivel, ne.descr_endem_es, comments"
    cursor.execute(SQL,[id_tax])
    res = dict(cursor.fetchone())
    return res

def manageInputEndem(id_tax,connection,**inputEndem):
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
        # find the threat status if it exists in the database
        SQL = "SELECT count(*) FROM endemic WHERE cd_tax=%s"
        cur.execute(SQL,[id_tax])
        nb = cur.fetchone()['count']
        statusExists = bool(nb)
        if statusExists:
            # if it exists, look whether it is compatible with the current status
            endemStatus = getEndemStatus(cur,id_tax)
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
                cur.execute(SQL, [id_tax, nivInput,inputEndem.get('comments')])
            # if it does not exist insert the source, the status and make the links
            for i in range(len(cdRefs)):
                SQL = "WITH a AS (SELECT %s AS cd_ref, %s AS cd_tax), b AS(SELECT a.cd_ref,a.cd_tax,rt.id FROM a LEFT JOIN ref_endem AS rt USING (cd_ref,cd_tax)) INSERT INTO ref_endem(cd_ref, cd_tax) SELECT cd_ref,cd_tax FROM b WHERE id IS NULL"
                cur.execute(SQL,[cdRefs[i],id_tax])
    return {'id_tax': id_tax,'cdRefs': cdRefs}

def getExotStatus(cursor, id_tax):
    SQL = "SELECT e.is_alien, e.is_invasive, e.occ_observed, e.cryptogenic, e.comments, STRING_AGG(r.citation, ' | ' ORDER BY r.cd_ref) AS references, STRING_AGG(r.link, ' | ' ORDER BY r.cd_ref) AS links FROM exot e LEFT JOIN ref_exot re ON e.cd_tax=re.cd_tax   LEFT JOIN refer r ON re.cd_ref=r.cd_ref WHERE e.cd_tax=%s GROUP BY e.is_alien, e.is_invasive, e.occ_observed,e.cryptogenic, e.comments"
    cursor.execute(SQL,[id_tax])
    res = dict(cursor.fetchone())
    return res

def manageInputExot(id_tax,connection,**inputExot):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # find the  status if it exists in the database
    SQL = "SELECT count(*) FROM exot WHERE cd_tax=%s"
    cur.execute(SQL,[id_tax])
    nb = cur.fetchone()['count']
    statusExists = bool(nb)
    if statusExists:
        # if it exists, look whether it is compatible with the current status
        exotStatus = getExotStatus(cur,id_tax)
        sameStatus = (inputExot.get('is_alien') == exotStatus['is_alien']) and (inputExot.get('is_invasive') == exotStatus['is_invasive']) and (inputExot.get('occ_observed') == exotStatus['occ_observed']) and (inputExot.get('cryptogenic') == exotStatus['cryptogenic']) 
        if(not sameStatus):
            raise Exception("The taxon already exists in the database with another alien/invasive status")
    cur.close()
    with connection:
        with connection.cursor() as cur:
            cdRefs = [manageSource(cur,inputExot['ref_citation'][i],inputExot.get('link')[i] if bool(inputExot.get('link')) else None) for i in range(0,len(inputExot['ref_citation']))]
            if not statusExists:
                # if it is compatible with an existing status, insert the new source
                SQL = "INSERT INTO exot(cd_tax,is_alien,is_invasive,occ_observed,cryptogenic,comments) VALUES (%s,%s,%s,%s,%s,%s)"
                cur.execute(SQL, [id_tax,inputExot.get('is_alien'),inputExot.get('is_invasive'),inputExot.get('occ_observed'),inputExot.get('cryptogenic'),inputExot.get('comments')])
            # if it does not exist insert the source, the status and make the links
            for i in range(len(cdRefs)):
                SQL = "WITH a AS (SELECT %s AS cd_ref, %s AS cd_tax), b AS(SELECT a.cd_ref,a.cd_tax,rt.id FROM a LEFT JOIN ref_exot AS rt USING (cd_ref,cd_tax)) INSERT INTO ref_exot(cd_ref, cd_tax) SELECT cd_ref,cd_tax FROM b WHERE id IS NULL"
                cur.execute(SQL,[cdRefs[i],id_tax])
    return {'id_tax': id_tax,'cdRefs': cdRefs}

def testEndemStatus(connection,id_tax):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL = "SELECT count(*) FROM endemic WHERE cd_tax = %s"
    cur.execute(SQL,[id_tax])
    hasEndemStatus = bool(cur.fetchone()['count'])
    res = {'hasEndemStatus': hasEndemStatus}
    if hasEndemStatus:
        res.update(getEndemStatus(cur,id_tax))
    else:
        res.update({'cd_nivel':None, 'descr_endem_es': None, 'comments': None, 'references': None, 'links': None})
    return res

def testExotStatus(connection,id_tax):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL = "SELECT count(*) FROM exot WHERE cd_tax = %s"
    cur.execute(SQL,[id_tax])
    hasExotStatus = bool(cur.fetchone()['count'])
    res = {'hasExotStatus': hasExotStatus}
    if hasExotStatus:
        res.update(getExotStatus(cur,id_tax))
    else:
        res.update({'cd_nivel':None, 'is_alien': None, 'is_invasive': None, 'occ_observed': None, 'cryptogenic': None ,'comments': None,'references': None, 'links': None})
    return res

def testThreatStatus(connection,id_tax):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL = "SELECT count(*) FROM threat WHERE cd_tax = %s"
    cur.execute(SQL,[id_tax])
    hasThreatStatus = bool(cur.fetchone()['count'])
    res = {'hasThreatStatus': hasThreatStatus}
    if hasThreatStatus:
        res.update(getThreatStatus(cur,id_tax))
    else:
        res.update({'cd_status':None, 'comments': None, 'references': None, 'links': None})
    return res
