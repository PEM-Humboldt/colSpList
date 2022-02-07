from flask_restful import Resource
import requests
import spacy
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



DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()


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


def insert_tax(**kwargs):
    # has the taxon a gbifkey?
    alreadyInDb = False
    if (kwargs.get('gbifkey') is not None):
        SQL = "SELECT count(*) AS nb FROM taxon WHERE gbifkey = %s"
        cur.execute(SQL, [kwargs.get('gbifkey')])
        gbifKeyInDb_nb, = cur.fetchone()
        if (gbifKeyInDb_nb = 1):
            if(kwargs.get('canonicalname') is not None):
                SQL = "SELECT name FROM taxon WHERE gbifkey = %s"
                cur.execute(SQL,[kwargs.get('gbifkey')])
                nameTaxDb, = cur.fetchone()
                diffTaxName = fuzz.ratio(nameTaxDb,kwargs.get('canonicalname'))
                if (diffTaxName <0.75):
                    raise Exception("Name of the taxon does not correspond to gbifkey")
                else:
                    alreadyInDb = True
        elif (gbifKeyInDb_nb = 0):
            infoTax = get_gbif_tax_from_id(kwargs.get('gbifkey'))
        else :
            raise Exception("gbifkey more than once in the database, should not be possible!")
    elif (kwargs.get('scientificname') is not None):
        SQL = "SELECT count(*) AS nb FROM taxon WHERE name_auth = %s"
        cur.execute(SQL,[kwargs.get('scientificname')])
        gbifSciInDb_nb, = cur.fetchone()
        if (gbifSciInDb_nb = 0):
            infoTax = get_gbif_tax_from_sci_name(kwargs.get('scientificname'))
            
