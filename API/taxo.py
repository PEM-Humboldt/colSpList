"""
Functions for taxonomic management
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
from manageStatus import manageSource
DATABASE_URL = os.environ['DATABASE_URL']
PYTHONIOENCODING="UTF-8"


def get_gbif_tax_from_id(gbifid: int):
    """
    Obtaining extensive taxonomic information from the gbif API, when we have the taxonKey of the gbif backbone
    
    Parameters
    ----------
    gbifid: int
        taxonKey (speciesKey, parentKey etc.) of the taxon
    
    Returns
    ----------
    Dictionary containing all the information of the taxon available in the API. Note: the information here is more complete than when we search the taxon through its name
    """
    api = f"https://api.gbif.org/v1/species/{gbifid}"
    response = requests.get(api)
    content = response.json()
    return content

def get_gbif_tax_from_name(name: str):
    """
    Obtaining basic taxonomic information from the gbif API, by running a fuzzy match of the name
    
    Parameters
    ----------
    name: str
        canonical name of the taxon (note: fuzzy matching will be done in order to find the closest name)
    
    Returns
    ----------
    Dictionary containing basic information about the taxon (note: less precise than search through gbifkey
    """
    api = f"https://api.gbif.org/v1/species/match/?name={name}"
    response = requests.get(api)
    content = response.json()
    return content

def get_gbif_tax_from_sci_name(sci_name: str):
    """
    Obtaining basic taxonomic information from the gbif API, by running a fuzzy match of the name
    
    Parameters
    ----------
    name: str
        Scientific name (with authorship) of the taxon (note: fuzzy matching will be done in order to find the closest name)
    
    Returns
    ----------
    Dictionary containing basic information about the taxon (note: less precise than search through gbifkey
    """
    api = f"https://api.gbif.org/v1/species/match/?name={sci_name},nameType=SCIENTIFIC"
    response = requests.get(api)
    content = response.json()
    return content

def get_gbif_parent(gbifkey: int):
    """
    Obtaining basic information about the parents of a taxon through the gbif API
    
    Parameters
    ----------
    gbifkey: int
        taxonKey (speciesKey, parentKey etc.) of the taxon in the gbif backbone
    
    Returns
    ----------
    List of dictionaries with information concerning the parent taxa
    """
    api= f"https://api.gbif.org/v1/species/{gbifkey}/parents"
    response = requests.get(api)
    content = response.json()
    #content = pd.json_normalize(response.json())
    return content

def get_gbif_parsed_from_id(gbifkey: int):
    """
    Obtaining supplementary information about the taxa (in particular it allows to retrieve the canonicalNameWithMarker which is the basic name used as "name" in our database)
    
    Parameters
    ----------
    gbifkey: int
        taxonKey (speciesKey, parentKey etc.) of the taxon in the gbif backbone
    Returns
    ----------
    Dictionary with supplementary fields concerning the name of the taxon
    """
    api= f"https://api.gbif.org/v1/species/{gbifkey}/name"
    response = requests.get(api)
    content = response.json()
    return content

def get_gbif_parsed_from_sci_name(sci_name: str):
    """
    Perform an analysis of a scientific name through the gbif API and gives all the information it can from a scientific name (note: this also works with taxa which are not in the gbif backbone
    
    Parameters
    ----------
    sci_name: str
        scientific name (with authorship) or canonical name of a taxon
        
    Returns
    ----------
    Dictionary with supplementary fields concerning the name of the taxon
    """
    api= f"https://api.gbif.org/v1/parser/name?name={sci_name}"
    response = requests.get(api)
    content = response.json()[0]
    return content


def get_gbif_synonyms(gbifkey: int):
    """
    Retrieve the synonyms of a name through the gbif API
    
    Parameters
    ----------
    gbifkey: int
        taxonKey (speciesKey, parentKey etc.) of the taxon in the gbif backbone
    
    Returns
    ----------
    List of dictionaries with basic information about the synonyms of the taxon
    """
    api= f"https://api.gbif.org/v1/species/{gbifkey}/synonyms"
    response = requests.get(api)
    content = response.json()
    return content

def get_db_directParent(connection,cd_tax):
    """
    Retrieve direct parent information in the database
    
    Parameters
    -----------
    connection: postgres connection
        connection to the postgres database
    cd_tax: int
        identificador de la especie en la base de datos
    Returns
    -----------
    parent: dict
        dictionary with the following elements:
        cd_tax: int 
            Identificator of the parent taxon
        scientificname
            Scientific name (with authorship) of the parent taxon
    """
    cur=connection.cursor()
    SQL = "WITH parent AS(SELECT cd_sup FROM taxon WHERE cd_tax=%s) SELECT cd_tax,name_auth FROM taxon WHERE cd_tax = (SELECT cd_sup FROM parent)"
    cur.execute(SQL,[cd_tax])
    res = cur.fetchone()
    cur.close()
    return {'cd_tax':res[0], 'scientificname':res[1]}

def get_db_tax(connection, cd_tax):
    """
    Retrieve taxon information in the database
    
    Parameters
    -----------
    connection: postgres connection
        connection to the postgres database
    cd_tax: int
        identificador de la especie en la base de datos
    Returns
    -----------
    taxon: dict
        dictionary with the following elements:
        cd_tax: int 
            Identificator of the parent taxon
        scientificname
            Scientific name (with authorship) of the taxon
        canonicalname
            Canonical name (without authorship) of the taxon
        syno: Bool
            Is the taxon a synonym?
        gbifkey: Int 
            Identificator of the taxon in GBIF
    """
    cur= connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL = "SELECT cd_tax, name_auth AS scientificname, name AS canonicalname, status = 'SYNONYM' AS syno, gbifkey FROM taxon WHERE cd_tax=%s"
    cur.execute(SQL,[cd_tax])
    taxon=dict(cur.fetchone())
    cur.close()
    return taxon

def test_taxInDb(connection,**kwargs):
    """
    Test whether a taxon is already in the database. It is done first by looking for a gbifkey of the taxon, then by looking for its scientific name (if there is no gbifkey supplied) and finally the canonical name of the taxon (if no gbifkey or scientificname are supplied
    
    Parameters
    ----------
    connection: postgres connection
        connection to the postgres database
    kwargs: dict
        Dictionary, must contain at least one of the following parameters to work:
        gbifkey: int
            taxonKey (speciesKey, parentKey etc.) of the taxon in the gbif backbone
        scientificname: str
            scientific name (with authorship) of the taxon
        canonicalname: str
            canonical name of the taxon (we expect canonicalNameWithMarker)
    
    Returns
    ---------
    Dictionary with the following parameters:
        alreadyInDb: bool
            whether the taxon is matched with a taxon in the database
        gbifmatchmode: str
            One of 'gbifkey', 'scientificname' or 'canonicalname' showing which should be the method to retrieve the taxon in the gbif API, depending on the information available in the input
        cd_tax: int
            if the taxon already exists in the database, its cd_tax, otherwise None
        
    Error handling
    --------------
    Exception:
        "Name of the taxon does not correspond to gbifkey"
        If both canonical name and gbifkey are given, a partial match is performed between the "name" of the taxon corresponding to the gbifkey and the name given as "canonicalname" in kwargs. If we do not find a match between these two names, the exception is raised
    Exception:
        "gbifkey more than once in the database, should not be possible"
        gbifkey corresponds to more than one taxon in the database. In the current data model, gbifkey has an UNIQUE constraint, so we should not ever find this error, but it might be safer to keep it in case we have problems of concurrent INSERT in the database, or if we change the database motor, or data model in the future
    Exception: 
        "Name (with author) in the database more than once, should not be possible!"
        scientificname correspond to more than one taxon in the database (field name_auth in the taxon table). In the current data model, name_auth has an UNIQUE constraint, so we should not ever find this error, but it might be safer to keep it in case we have problems of concurrent INSERT in the database, or if we change the database motor, or data model in the future
    Exception:
        "Name (without author) exists more than once in the database, please provide scientificname or gbifkey instead, in order to be able to identify which taxon you are referring to"
        Since there is no UNIQUE constraint on the "name" field of the taxon table in the database, it is potentially possible that 2 taxa from the database share the same canonical name (with 2 different authorships though). In that case it is impossible to know which of the taxa is referred to, and the function stop, raising this error
    Exception:
        "Either 'gbifkey', or 'scientificname', or 'canonicalname' should be included in the parameters in order to be able to identify the taxon"
        If none of the parameters necessary to identify the taxon are given as parameters in the kwargs dictionary the function stops and raises this exception
    """
    cur = connection.cursor()
    alreadyInDb = False
    gbifMatchMode = None
    cdTax = None
    if (kwargs.get('gbifkey') is not None):
        SQL = "SELECT count(*) AS nb FROM taxon WHERE gbifkey = %s"
        cur.execute(SQL, [kwargs.get('gbifkey')])
        gbifKeyInDb_nb, = cur.fetchone()
        gbifMatchMode = 'gbifkey'
        if (gbifKeyInDb_nb == 1):
            if(kwargs.get('canonicalname') is not None):
                SQL = "SELECT name FROM taxon WHERE gbifkey = %s"
                cur.execute(SQL,[kwargs.get('gbifkey')])
                nameTaxDb, = cur.fetchone()
                diffTaxName = fuzz.ratio(nameTaxDb,kwargs.get('canonicalname'))
                if (diffTaxName < 0.75):
                    raise UncompatibilityGbifKeyCanonicalname(gbifkey = kwargs.get('gbifkey'), canonicalname = kwargs.get('canonicalname'), name_gbifkey = nameTaxDb)
                    #raise Exception("Name of the taxon does not correspond to gbifkey")
            alreadyInDb = True
            SQL = "SELECT cd_tax FROM taxon WHERE gbifkey = %s"
            cur.execute(SQL,[kwargs.get('gbifkey')])
            cdTax,  = cur.fetchone()
        elif (gbifKeyInDb_nb == 0):
            pass
        else :
            raise DbIntegrityError(value=kwargs.get('gbifkey'), field="'gbifkey'", message='gbifkey present more than once in the database')
            #raise Exception("gbifkey more than once in the database, should not be possible!")
    elif (kwargs.get('scientificname') is not None):
        SQL = "SELECT count(*) AS nb FROM taxon WHERE name_auth = %s"
        cur.execute(SQL,[kwargs.get('scientificname')])
        gbifSciInDb_nb, = cur.fetchone()
        gbifMatchMode = 'scientificname'
        if (gbifSciInDb_nb == 1):
            alreadyInDb = True
            SQL = "SELECT cd_tax FROM taxon WHERE name_auth = %s"
            cur.execute(SQL,[kwargs.get('scientificname')])
            cdTax,  = cur.fetchone()
        elif (gbifSciInDb_nb == 0):
            infoTax = get_gbif_tax_from_sci_name(kwargs.get('scientificname'))
        else:
            raise dbIntegrityError(value=kwargs.get('scientificname'), field="'name_auth'", message='name_auth (scientificname) present more than once in the database')
            #raise Exception("Name (with author) in the database more than once, should not be possible!")
    elif (kwargs.get('canonicalname') is not None):
        SQL = "SELECT count(*) AS nb FROM taxon WHERE name =%s"
        cur.execute(SQL,[kwargs.get('canonicalname')])
        gbifNameInDb_nb, = cur.fetchone()
        gbifMatchMode = 'canonicalname'
        if (gbifNameInDb_nb == 1):
            alreadyInDb = True
            SQL = "SELECT cd_tax FROM taxon WHERE name = %s"
            cur.execute(SQL, [kwargs.get('canonicalname')])
            cdTax, = cur.fetchone()
        elif (gbifNameInDb_nb == 0):
            infoTax = get_gbif_tax_from_name(kwargs.get('canonicalname'))
        else:
            raise MissingArgError(missingArg="'scientificname' or 'gbifkey'", message="The name without authorship (canonicalname) corresponds to various taxa in the database, please provide scientific name or gbif taxon key"
            #Exception("Name (without author) exists more than once in the database, please provide scientificname or gbifkey instead, in order to be able to identify which taxon you are referring to")
    else:
        raise MissingArgError(missingArg="'scientificname', 'canonicalname' or 'gbifkey'", message= "You did not provide GBIF taxon key nor name with nor without authorship")
        #Exception("Either 'gbifkey', or 'scientificname', or 'canonicalname' should be included in the parameters in order to be able to identify the taxon")
    cur.close()
    return {'alreadyInDb': alreadyInDb, 'gbifMatchMode': gbifMatchMode, 'cdTax': cdTax}

def get_infoTax(**kwargs):
    """
    Retrieve information about a taxon from GBIF, depending on the available information
    
    Parameters
    ----------
    kwargs: dict
        Dictionary consisting on the input given by the users about the taxon, together with the results of the function test_taxInDb. The important parameters in this dictionary is:
        gbifMatchMode [mandatory]: str
            Optimal match mode in GBIF ("gbifkey" > "scientificname" > "canonicalname")
        gbifkey: int
            taxonkey from gbif
        canonicalname: str
            canonical name of the taxon
        scientificname: str
            scientific name of the taxon
        
    Returns
    ---------
    Returns a dictionary with all the parameters retrieved from gbif, and additional parameters such as:
        foundGbif: bool
            Whether the taxon is found in gbif
    
    Error handling
    --------------
    Exception: "No acceptable gbifMatchMode were provided"
        If gbifMatchMode is not one of 'gbifkey', 'canonicalname' or 'scientificname' the function cannot know how to query the GBIF API, therefore it sends this exception and stops
    """
    foundGbif = False
    if (kwargs.get('gbifMatchMode') == 'gbifkey'):
        infoTax = get_gbif_tax_from_id(kwargs.get('gbifkey'))
        foundGbif = True
    elif (kwargs.get('gbifMatchMode') == 'canonicalname'):
        infoTax = get_gbif_tax_from_name(kwargs.get('canonicalname'))
    elif (kwargs.get('gbifMatchMode') == 'scientificname'):
        infoTax = get_gbif_tax_from_sci_name(kwargs.get('scientificname'))
    else:
        raise UnauthorizedValueError(value=kwargs.get(gbifMatchMode), var='gbifMatchMode', acceptable=['gbifkey','scientificname','canonicalname'])
        #raise Exception("No acceptable gbifMatchMode were provided")
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
    """
    Translate a rank, written in various format into the rank and level (number corresponding to the rank) as codificated in the database
    
    parameters
    -----------
    connection: postgres connection
        connection to the database
    rankInput: str
        rank name in uppercase ("SUBSPECIES", "GENUS", "SPECIES", "FAMILY" etc.), gbif backbone marker ("subsp.", "gn.", "sp.", "fam." etc.) or cd_rank ("SUBSP", "GN", "SP", "FAM")
    returns
    -----------
    rank: str
        rank(as a rank name in uppercase) 
    level: integer
        rank level (from 1 for the FORM to 29 for DOMAIN, levels lower than 5 are underspecies levels)
    """
    cur = connection.cursor()
    SQL = "WITH a as (SELECT %s AS input) SELECT rank_name,rank_level FROM tax_rank,A WHERE gbif_bb_marker = a.input OR rank_name = a.input OR cd_rank= a.input"
    cur.execute(SQL,[rankInput])
    rank, level= cur.fetchone()
    cur.close()
    return rank, level
    

def format_inputTax(connection, acceptedName, acceptedId, **inputTax):
    """
    Format taxon for insertion in the database, case of taxa which are extracted from information given by the user (another function format information extracted from GBIF, so this is mostly for the case where the taxon is not found in GBIF). The function returns also basic information about the direct parent taxon 
    
    TODO: it seems that some parameters are useless (connection, acceptedName and acceptedId and are just a legacy from previous versions of the function, check whether we can get rid of them
    
    parameters
    -----------
    connection: psycopg2 connection
        connection to the database
    acceptedName: str
        In case of synonyms: name of the accepted taxon, otherwise None
    acceptedId: int 
        In case of synonyms: cd_tax of the accepted taxon, otherwise None
    inputTax: dict
        Dictionary containing all the information available about the taxon (canonicalname, scientificname, authorship, parentscientificname, parentgbifkey, parentcanonicalname, rank, syno [mandatory]
    
    Returns
    --------
    2 dictionaries:
        dict1: dict
        dictionary concerning the taxon with the following parameters:
            name: str
                canonical name of the taxon (corresponding to the GBIF canonicalNameWithMarker
            name_auth : str
                scientific name of the taxon, with authorship if available
            auth : str
                authorship associated with the name of the taxon
            tax_rank_name: str
                name of the rank in uppercase
            status : str
                taxonomic status (here either SYNONYM or DOUBTFUL, because it is not found in GBIF)
            gbifkey : str
                None because the taxa are not found in GBIF
            source : int
                bibliographic reference of the taxon, not really implemented yet so: None
        parentTax : dict
        dictionary with the following parameters:
            canonicalname: str
                canonical name of the parent taxon
            scientificname: str
                scientific name of the parent taxon
            gbifkey: int 
                Gbif key of the parent taxon
    Error handling
    --------------
    Exception: "Name not found in GBIF and information insufficient to integrate in the database"
        If there are some mandatory information which are not found in the input from the user, potentially causing disfunctioning of the database, the function raises this exception and stop
    Exception: "No way to determine the taxon rank"
        If the rank is not provided and impossible to determine through GBIF API name analysis, the function raises this exception and stops
    Exception: "No sure way to determine the superior taxon"
        If there is no sufficient information about the parent taxon and it cannot be retrieved from the analysis of the name of the taxon, the function raises this exception and stops
    """
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
            parsed = get_gbif_parsed_from_sci_name(inputTax.get('scientificname'))
            if(not parsed.get('parsed')):
                raise MissingArgError(MissingArg="'scientificname' and 'authorship'", message="Name not found in GBIF API and parsing method from GBIF API does not allow to extract sufficient information")
                #raise Exception("Name not found in GBIF and information insufficient to integrate in the database")
        else:
            parsed = get_gbif_parsed_from_sci_name(inputTax.get('canonicalname'))
        name=parsed.get('canonicalNameComplete')
        name_auth = parsed.get('scientificName')
        if(not hasRank):
            if(parsed.get('rankMarker') is not None):
                rank, level_rank = get_rank(connection,parsed.get('rankMarker'))
            else:
                raise MissingArgError(missingArg="'tax_rank'", message="Rank was not provided, taxon not found in GBIF and extraction from name was impossible from the GBIF API parsing method")
                #raise Exception("No way to determine the taxon rank")
        else:
            rank, level_rank = get_rank(connection,inputTax.get('rank'))
        if(parentTax.get('canonicalname') is None):
            if(rank_level < 5):#infraspecies: the superior rank is the species which we can get by association between the genus and the epithet
                parentTax['canonicalName'] = parsed.get('genusOrAbove') + ' ' + parsed.get('specificEpithet')
            elif (rank_level == 5):
                parentTax['canonicalname'] = parsed.get('genusOrAbove')
            else:
                if(not hasSup and not syno):
                    raise MissingArgError(missingArg="'parentcanonicalname' or 'parentscientificname' or 'parentgbifkey'",message="Taxon not found in GBIF, no parent information provided and parent is not guessable from name provided")
                    #raise Exception("No sure way to determine the superior taxon")
    if(not hasAuth and name in name_auth):
        extractAuth = name_auth.replace(name,'')
        auth = re.sub("^ *(.+) *$","\1",extractAuth)
        if(auth == ''):
            auth = None
    else:
        auth = inputTax.get('authorship')
    return {'name': name, 'name_auth': name_auth, 'auth': auth, 'tax_rank_name': rank, 'status': status, 'gbifkey': None, 'source': inputTax.get('source')}, parentTax

def format_gbif_tax(connection,**gbif_tax):
    """
    Format the information retrieved from Gbif, in order to insert them in the taxon table of the database
    
    Parameters
    ----------
    connection: psycopg2 connection
        connection to the database
    gbif_tax: dict
        dictionary with all the information retrieved from GBIF during the different steps of taxon recognition. The dictionary needs to have at least the following parameters:
            rank: str
                taxonomic rank of the taxon
            key: int 
                key of the taxon in the gbif backbone
            scientificName: str
                scientific name of the taxon as it is in GBIF (different from scientificname, given by the user)
            parentkey : int
                gbifkey of the parent taxon
            parent: str
                canonical name of the parent taxon
            authorship: str
                authorship associated included in the scientific name of the taxon
            syno: bool
                whether the taxon is a synonym
            taxonomicStatus: str
                status of the taxon in the gbif taxon (ACCEPTED, SYNONYM or DOUBTFUL
    Returns
    ------------
    2 dictionaries:
        dict1: dict
        dictionary concerning the taxon with the following parameters:
            name: str
                canonical name of the taxon (corresponding to the GBIF canonicalNameWithMarker)
            name_auth : str
                scientific name of the taxon, with authorship if available
            auth : str
                authorship associated with the name of the taxon
            tax_rank_name: str
                name of the rank in uppercase
            status : str
                taxonomic status (ACCEPTED, SYNONYM or DOUBTFUL)
            gbifkey : str
                None because the taxa are not found in GBIF
            source : int
                bibliographic reference of the taxon, not really implemented yet so: None
        parentTax : dict
        dictionary with the following parameters:
            canonicalname: str
                canonical name of the parent taxon
            gbifkey: int 
                Gbif key of the parent taxon
    """
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
    """
    Look whether the parent taxa (as retrieved from GBIF by the function get_gbif_parent) are already in the database, if not format them in order to insert them later in the database
    
    Parameters
    -----------
    connection: psycopg2 connection
        connection to the postgres database
    parents: list(dict)
        List of parent taxon information (consisting of dictionaries concerning all the parent taxa) retrieved from the get_gbif_parent function
    
    Returns
    --------
    idParentInDb: int 
        cd_tax of the taxon of lower rank which is already in the database (para poder utilizar este cd_tax as the cd_sup of its direct child taxon)
    listFormatted: list(dict)
        list of dictionaries concerning all the parent taxa which are not already in the database 
    """
    idParentInDb = None
    listFormatted = []
    for i in parents:
        i.update(test_taxInDb(connection,**{'gbifkey':i.get('key')}))
        if(i.get('alreadyInDb')):
            idParentInDb=i.get('cdTax')
        else:
            listFormatted.append({'name':i.get('canonicalName'), 'name_auth': i.get('scientificName'),'auth':i.get('authorship'),'tax_rank_name': i.get('rank'), 'status': i.get('taxonomicStatus'), 'gbifkey':i.get('key'), 'source': None})
    return idParentInDb, listFormatted

def acceptedId(connection,cd_tax:int):
    """
    Returns the cd_tax of the accepted taxon corresponding to the cd_tax given in parameter (either returns the same cd_tax if the taxon is accepted, or its cd_syno if the taxon is a synonym)
    
    Parameters
    ----------
    connection: psycopg2 connection
        connection to the postgres database
    cd_tax: int
        cd_tax of the taxon
    Returns
    -----------
    cd_tax of the accepted corresponding taxon
    """
    cur = connection.cursor()
    SQL = "SELECT COALESCE(cd_syno,cd_tax) FROM taxon WHERE cd_tax=%s"
    cur.execute(SQL,[cd_tax])
    res, =cur.fetchone()
    cur.close()
    return res

def insertTax(cursor,idParent,idSyno,**tax):
    """
    Insert formatted information from a taxon in the database and returns the new cd_tax created in the database
    
    Parameters
    -----------
    cursor : psycopg2 cursor
        cursor corresponding to current operations in the postgres database
    idParent: int 
        cd_tax of the parent taxon (None if the taxon is a synonym or if the taxon is of the higher rank in the database)
    idSyno: int 
        cd_tax of the accepted taxon in the database (None if the taxon to insert is the accepted taxon)
    tax: dict
        dictionary containing the formatted information about the taxon (name, name_auth, tax_rank_name, status, gbifkey, source)
        
    Returns
    -----------
    cd_tax of the newly inserted taxon 
    """
    SQL = "WITH a AS( SELECT %s AS name, %s AS name_auth, %s AS auth, %s AS name_rank, %s AS status, %s AS gbif_key, %s AS source, %s AS cd_sup, %s AS cd_syno), b AS (SELECT name, name_auth, CASE WHEN NOT auth ~ '^ *$' THEN auth ELSE NULL END AS auth, cd_rank,cd_sup::int, cd_syno::int, status, gbif_key, source::int FROM a JOIN tax_rank t ON a.name_rank=t.rank_name)  INSERT INTO taxon(name,name_auth,auth,tax_rank,cd_sup,cd_syno,status, gbifkey, source) SELECT * FROM b RETURNING cd_tax"
    cursor.execute(SQL,(tax.get('name'), tax.get('name_auth'), tax.get('auth'), tax.get('tax_rank_name'),tax.get('status'), tax.get('gbifkey'),tax.get('source'),idParent,idSyno))
    idInserted, = cursor.fetchone()
    return idInserted
    
def manageInputTax(connection, insert, **inputTax):
    """
    Master function which organizes all the other functions running for recognizing, and inserting taxa in the databases (with their corresponding accepted and parent taxa)
    
    Parameters
    ------------
    connection: psycopg2 connection
        connection to the postgres database
    insert: Bool
        Whether the insertion of taxa which are not in the database should be done or not
    inputTax: dict
        dictionary containing all the information provided by the user about the taxon
    
    Returns
    ------------
    taxon: Dict
        Dictonary with the following elements:
            cd_tax: int
                identificator of the taxon in the database
            cd_tax_acc: int 
                identificator of the accepted taxon in the datase
            alreadyInDb: Bool
                ¿Was the taxon already in the database?
            foundGbif: Bool
                ¿ Is the taxon found in GBIF?
            matchedname: Str 
                Name of the taxon which has been matched against (in Gbif or the local database) input information (canonicalname if the taxon was retrieved by canonicalname, scientificname otherwise)
            acceptedname: Str
                Accepted scientificname (different to matchedname if the input taxon is a synonym)
            gbifkey: int
                identificator of the taxon in the gbif backbone
            syno: Bool
                Is the taxon a synonynm
            insertedTax: List(Int):
                List of inserted taxon (the accepted taxon itself, but also the parents and synonyms if needed)
    """
    insertedTax = list()
    res = {'cd_tax': 0, 'cd_tax_acc': 0 ,'alreadyInDb':False, 'foundGbif': False, 'matchedname': None, 'acceptedname':None, 'gbifkey':None,'syno':None, 'insertedTax': insertedTax}
    
    """
    -------------Searching for the information-------------------------
    """
    syno = False
    # First check : is the taxon in the database
    inputTax.update(test_taxInDb(connection=connection,**inputTax))
    if (not inputTax.get('alreadyInDb')):
        inputTax.update(get_infoTax(**inputTax))
        inputTax['syno'] = False
        # In case we did not find the taxon at first be it is indeed in the database
        if(inputTax.get('foundGbif')):
            recheck = test_taxInDb(connection=connection,gbifkey=inputTax.get('key'))
            inputTax['alreadyInDb']=recheck.get('alreadyInDb')
            inputTax['cdTax'] = recheck.get('cdTax')
    # Not in the database
    if (not inputTax.get('alreadyInDb')):
        # synonyms from GBIF
        if(inputTax.get('foundGbif') and inputTax.get('synonym')): # synonym found through gbif, note: all synonym and/or parent information from the arguments (positive, negative, precise or not) in the function will be overrided: GBIF takes priority
            syno = True
            inputTax['syno'] = True
            acceptedTax = {'gbifkey':inputTax.get('acceptedUsageKey'),'scientificname': inputTax.get('accepted')}
            if acceptedTax.get('gbifkey') is None:
                acceptedTax['gbifkey']=inputTax.get('acceptedKey')
        # synonyms for taxa not found in GBIF
        if(not inputTax.get('foundGbif') and (inputTax.get('synogbifkey') is not None or inputTax.get('synoscientificname') is not None or inputTax.get('synocanonicalname') is not None)):
            syno = True
            inputTax['syno'] = True
            acceptedTax = {'gbifkey': inputTax.get('synogbifkey'), 'scientificname': inputTax.get('synoscientificname'), 'canonicalname': inputTax.get('synocanonicalname')}
        # 
        if(syno): 
            acceptedTax.update(test_taxInDb(connection=connection,**acceptedTax))
            if(not acceptedTax.get('alreadyInDb')):
                acceptedTax.update(get_infoTax(**acceptedTax))
                acceptedTax['syno'] = False
                recheckAccepted = test_taxInDb(connection=connection,gbifkey=acceptedTax.get('key'))
                acceptedTax['alreadyInDb'] = recheckAccepted.get('alreadyInDb')
                acceptedTax['cdTax'] = recheckAccepted.get('cdTax')
    """
    ----------------Formatting the taxon information for insertion-------------------------------
    """
    if insert and not inputTax.get('alreadyInDb'):
        if syno:
            if not acceptedTax.get('alreadyInDb'):
                if acceptedTax.get('foundGbif'):
                    accepted, parentTax = format_gbif_tax(connection=connection, **acceptedTax)
                else:
                    accepted, parentTax = format_inputTax(connection=connection, **acceptedTax)
            if(inputTax.get('foundGbif')):
                synonym, synoParent = format_gbif_tax(connection=connection, **inputTax)
            else:
                synonym, synoParent = format_inputTax(connection=connection, **inputTax)
        else:
            if(not inputTax.get('alreadyInDb')):
                if(inputTax.get('foundGbif')):
                    accepted, parentTax = format_gbif_tax(connection=connection, **inputTax)
                else:
                    accepted, parentTax = format_inputTax(connection=connection, acceptedName = None, acceptedId=None,**inputTax)
        if syno and acceptedTax.get('alreadyInDb'):
            parentTax = {'alreadyInDb': True}
        else:
            parentTax.update(test_taxInDb(connection,**parentTax))
        if(not parentTax.get('alreadyInDb')):
            if(accepted.get('gbifkey') is None):
                parentTax.update(get_infoTax(**parentTax))
                if (not parentTax.get('foundGbif')):
                    raise MissingArgError(missingArg="'parentcanonicalname' or 'parentscientificname' or 'parentgbifkey'", message="Parent taxon not found in GBIF")
                parents = get_gbif_parent(parentTax.get('key'))
                parents.append(parentTax)
            else:
                parents = get_gbif_parent(accepted.get('gbifkey'))
            idParentInDb, parentsFormatted = format_parents(connection,parents)
        """
        ---------------------- Inserting the information in the database ---------------------------------
        """
        with connection:
            with connection.cursor() as cur:
                if(not parentTax.get('alreadyInDb')):
                    for i in range(0,len(parentsFormatted)):
                        idParentInDb = insertTax(cur,idParentInDb,None,**parentsFormatted[i])
                        insertedTax.append(idParentInDb)
                else:
                    idParentInDb=parentTax.get('cdTax')
                if(syno and acceptedTax.get('alreadyInDb')):
                    accId=acceptedTax.get('cdTax')
                else:
                    accId=insertTax(cur,idParentInDb,idSyno=None,**accepted)
                    insertedTax.append(accId)
                if(syno):
                    synoId=insertTax(cur, None, accId, **synonym)
                    insertedTax.append(synoId)
        cur.close()
    """
    --------------------------Final formatting of the returned information ------------------------------
    """
    if inputTax.get('alreadyInDb'):
        infoDb = get_db_tax(connection,inputTax.get('cdTax'))
        if inputTax.get('gbifMatchMode') == 'canonicalname':
            matchedname=infoDb.get('canonicalname')
        else:
            matchedname=infoDb.get('scientificname')
        if infoDb.get('syno'):
            infoDbAccepted = get_db_tax(connection,acceptedId(connection,inputTax.get('cdTax')))
            res.update({'cd_tax': infoDb.get('cd_tax'), 'cd_tax_acc': infoDbAccepted.get('cd_tax') ,'alreadyInDb':True, 'foundGbif': bool(infoDb.get('gbifkey')), 'matchedname': matchedname, 'acceptedname':infoDbAccepted.get('scientificname'), 'gbifkey':infoDb.get('gbifkey'),'syno':True, 'insertedTax': insertedTax})
        else:
            res.update({'cd_tax': infoDb.get('cd_tax'), 'cd_tax_acc': infoDb.get('cd_tax'), 'alreadyInDb':True, 'foundGbif': bool(infoDb.get('gbifkey')), 'matchedname': matchedname, 'acceptedname':infoDb.get('scientificname'), 'gbifkey':infoDb.get('gbifkey'),'syno':False, 'insertedTax':insertedTax})
    else:
        if insert and syno:
            res.update({'cd_tax':synoId, 'cd_tax_acc': accId})
        if insert and not syno:
            res.update({'cd_tax':accId, 'cd_tax_acc': accId})
        if inputTax.get('foundGbif'):
            if inputTax.get('gbifMatchMode') == 'canonicalname':
                matchedname = inputTax.get('canonicalName')
            else:
                matchedname = inputTax.get('scientificName')
        res.update({'alreadyInDb': False, 'foundGbif':inputTax.get('foundGbif'), 'matchedname':matchedname,'syno':syno,'gbifkey':inputTax.get('key'),'insertedTax':insertedTax})
        if syno:
            if acceptedTax.get('alreadyInDb'):
                infoDbAccepted = get_db_tax(connection,acceptedTax.get('cdTax'))
                res.update({'acceptedname':infoDbAccepted.get('scientificname')})
            else:
                if acceptedTax.get('foundGbif'):
                    res.update({'acceptedname': acceptedTax.get('scientificName')})
                else:
                    if acceptedTax.get('scientificname'):
                        res.update({'acceptedname':acceptedTax.get('scientificname')})
                    else:
                        res.update({'acceptedname':acceptedTax.get('canonicalname')})
        else:
            if inputTax.get('scientificName'):
                res.update({'acceptedname':acceptedTax.get('scientificName')})
            elif inputTax.get('scientificname'):
                res.update({'acceptedname':acceptedTax.get('scientificname')})
            else:
                res.update({'acceptedname':acceptedTax.get('canonicalname')})
                    
    return res

def childrenList(cursor,cd_tax):
    foundMore = True
    all_children=[cd_tax]
    new_children = [cd_tax]
    SQL = "SELECT cd_tax FROM taxon WHERE cd_sup IN (SELECT UNNEST( %s ))"
    while foundMore:
        cursor.execute(SQL,[new_children])
        res=cursor.fetchall()
        new_children = [r[0] for r in res]
        all_children=all_children+new_children
        if(len(new_children)==0):
            foundMore=False
    all_children.sort()
    return all_children

def parentList(cursor, cd_tax, includeBaseTax=True):
    foundMore = True
    all_parents = []
    currentTax = [cd_tax]
    if includeBaseTax:
        all_parents += [cd_tax]
    SQL = "SELECT tp.cd_tax FROM taxon t JOIN taxon tp ON t.cd_sup=tp.cd_tax WHERE t.cd_tax=%s"
    while foundMore:
        cursor.execute(SQL,currentTax)
        currentTax = cursor.fetchone()
        if not currentTax:
            foundMore= False
        else:
            all_parents += currentTax
    all_parents.sort()
    return all_parents

def synoList(cursor, cd_tax):
    SQL = "SELECT ts.cd_tax FROM taxon t JOIN taxon ts ON ts.cd_syno=t.cd_tax WHERE t.cd_tax=%s"
    cursor.execute(SQL,[cd_tax])
    res = cursor.fetchall()
    cds_syno = [r[0] for r in res]
    cds_syno.sort()
    return cds_syno

def synosAndParents(cursor,cd_taxs):
    all_parents=[]
    current=cd_taxs
    foundMore = True
    SQL_par = "SELECT tp.cd_tax FROM taxon t JOIN taxon tp ON t.cd_sup=tp.cd_tax WHERE t.cd_tax IN (SELECT(UNNEST(%s)))"
    while foundMore:
        cursor.execute(SQL_par,[current])
        res = cursor.fetchall()
        current = [r[0] for r in res if r[0] not in all_parents and r[0] not in cd_taxs]
        current = list(set(current))
        all_parents+=current
        if len(current)==0:
            foundMore = False
    all_parents.sort()
    SQL_syno = "WITH a AS (SELECT UNNEST(%s) AS cd_tax) SELECT ts.cd_tax FROM a JOIN taxon t USING (cd_tax) JOIN taxon ts ON t.cd_tax=ts.cd_syno"
    cursor.execute(SQL_syno,[all_parents+cd_taxs])
    res = cursor.fetchall()
    cds_syno = [r[0] for r in res]
    return {'cd_taxs':cd_taxs,'cd_parents': all_parents,'cd_synos':cds_syno,'all':cd_taxs+all_parents+cds_syno}

def checkCdTax(connection, cd_tax, **taxArgs):
    retrievedInfo = manageInputTax(connection=connection, insert = F, **taxArgs)
    return retrievedInfo.get('cd_tax') == cd_tax
    
def deleteTaxo(connection, cd_tax):
    cur=connection.cursor()
    children = childrenList(cur,cd_tax)
    SQL = "SELECT cd_tax FROM taxon WHERE cd_syno = %s"
    cur.execute(SQL,[cd_tax])
    res = cur.fetchall()
    cds_syno = [r[0] for r in res]
    SQL = "DELETE FROM taxon WHERE cd_tax =%s RETURNING cd_tax"
    cursor.execute(SQL,[cd_tax])
    cd_tax, =cursor.fetchone()
    connection.commit()
    cur.close()
    return {'cd_tax': cd_tax, 'cd_children':children, 'cd_synos':cds_syno}

def modifyTaxo(connection, cd_tax, **putTaxArgs):
    inserted=[]
    cur= connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    SQL = "SELECT * FROM taxon WHERE cd.tax=%s"
    cur.execute(SQL,[cd_tax])
    oldTax=dict(cur.fetchone)
    cur.close()
    cur=connection.cursor()
    children = childrenList(cur,cd_tax)
    SQL = "SELECT cd_tax FROM taxon WHERE cd_syno = %s"
    cur.execute(SQL[cd_tax])
    res = cur.fetchall()
    cds_syno = [r[0] for r in res]
    cur.close()
    if putTaxArgs.get('gbifkey'):
        insert=manageInputTax(connection=connection,insert=T,**{'gbifkey':putTaxArgs.get('gbifkey')})
        inserted+=insert.get('insertedTax')
        if insert.get('alreadyInDb'):
            raise AlreadyExistsDbError(value=putTaxArgs.get('gbifkey'),field="gbifkey")
            #raise Exception('NewGbifkeyAlreadypresent')
        else:
            cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            SQL = "SELECT * FROM taxon WHERE cd.tax=%s"
            cur.execute(SQL, [insert.get('cd_tax')])
            newTax=dict(cur.fetchone())
            cur.close()
            deleteTaxo(connection,newTax.get('cd_tax'))
            cur=connection.cursor()
            SQL = "UPDATE taxon SET name=%s, name_auth=%s, auth=%s, tax_rank=%s, cd_sup=%s, cd_syno=%s, status=%s, gbifkey=%s WHERE cd_tax=%s"
            cur.execute(SQL,[newTax.get('name'), newTax.get('name_auth'),newTax.get('auth'),newTax.get('tax_rank'),newTax.get('cd_sup'),newTax.get('cd_syno'),newTax.get('status'),newTax.get('gbifkey'),cd_tax])
            connection.commit()
            cur.close()
    else:
        if putTaxArgs.get('parentgbifkey') or putTaxArgs.get('parentcanonicalname') or putTaxArgs('parentscientificname'):
            parentInsert = manageInputTax(connection=connection,insert=True, **{'gbifkey':putTaxArgs.get('parentgbifkey'),'canonicalname':putTaxArgs.get('parentcanonicalname'),'scientificname':putTaxArgs('parentscientificname')})
            if oldTax.get('cd_sup') != parentInsert.get('cd_tax_acc'):
                cur = connection.cursor()
                SQL = "UPDATE taxon SET cd_sup=%s, gbifkey=NULL WHERE cd_tax=%s"
                cur.execute(SQL,[parentInsert.get('cd_tax_acc'),cd_tax])
                connection.commit()
                cur.close()
            inserted+=parentInsert.get('insertedtax')
        if putTaxArgs.get('synogbifkey') or putTaxArgs.get('synocanonicalname') or putTaxArgs('synoscientificname'):
            synoInsert = manageInputTax(connection=connection,insert=True, **{'gbifkey':putTaxArgs.get('synogbifkey'),'canonicalname':putTaxArgs.get('synocanonicalname'),'scientificname':putTaxArgs('synoscientificname')})
            if oldTax.get('cd_syno') != synoInsert.get('cd_tax_acc'):
                cur = connection.cursor()
                SQL = "UPDATE taxon SET cd_syno=%s, gbifkey=NULL WHERE cd_tax=%s"
                cur.execute(SQL,[synoInsert.get('cd_tax_acc'),cd_tax])
                connection.commit()
                cur.close()
            inserted+=synoInsert.get('insertedtax')
        cur = connection.cursor()
        if putTaxArgs.get('scientificname') and putTaxArgs.get('scientificname') != oldTax.get('name_auth'):
            SQL="UPDATE taxon SET name_auth=%s, gbifkey=NULL WHERE cd_tax=%s"# We suppress the gbifkey because the new version of the taxon might lose compatibility with gbif...
            cur.execute(SQL,[putTaxArgs.get('scientificname'),cd_tax])
        if putTaxArgs.get('canonicalname') and putTaxArgs.get('canonicalname') != oldTax.get('name'):
            SQL="UPDATE taxon SET name=%s, gbifkey=NULL WHERE cd_tax=%s"# We suppress the gbifkey because the new version of the taxon might lose compatibility with gbif...
            cur.execute(SQL,[putTaxArgs.get('canonicalname'),cd_tax])
        if putTaxArgs.get('authorship') and putTaxArgs.get('authorship') != oldTax.get('name'):
            SQL="UPDATE taxon SET auth=%s, gbifkey=NULL WHERE cd_tax=%s"# We suppress the gbifkey because the new version of the taxon might lose compatibility with gbif...
            cur.execute(SQL,[putTaxArgs.get('authorship'),cd_tax])
        if putTaxArgs.get('syno') is not None and putTaxArgs.get('syno') != (oldTax.get('status')=='SYNONYM'):
            if putTaxArgs.get('syno'):
                status='SYNONYM'
            else:
                status='DOUBTFUL'
            SQL="UPDATE taxon SET status=%s, gbifkey=NULL WHERE cd_tax=%s"# We suppress the gbifkey because the new version of the taxon might lose compatibility with gbif...
            cur.execute(SQL,[putTaxArgs.get('syno'),cd_tax])
        if putTaxArgs.get('status') and putTaxArgs.get('status') != oldTax.get('status'):
            SQL="UPDATE taxon SET status=%s, gbifkey=NULL WHERE cd_tax=%s"# We suppress the gbifkey because the new version of the taxon might lose compatibility with gbif...
            cur.execute(SQL,[putTaxArgs.get('status'),cd_tax])
        cur.close()
    if putTaxArgs.get('reference') or putTaxArgs.get('cd_ref'):
        cur=connection.cursor()
        cd_ref=putTaxArgs.get('cd_ref')
        if putTaxArgs.get('reference'):
            cd_ref = manageSource(cur, putTaxArgs.get('reference'), putTaxArgs.get('link'))
        SQL = "UPDATE taxon SET source=%s WHERE cd_tax=%s"
        cur.execute(SQL,[cd_ref,cd_tax])
        cur.close()
    connection.commit()
    return {'cd_tax':cd_tax, 'insertedTax':inserted}
