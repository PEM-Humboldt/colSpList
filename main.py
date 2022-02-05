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
    if (kwargs.get('gbifkey') is not None):
        SQL = "SELECT count(*) AS nb FROM taxon WHERE gbifkey = %s"
        cur.execute(SQL, [kwargs.get('gbifkey')])
        res, = cur.fetchone()
        if (res = 1):
            None
            elif (res = 0):
                get_gbif_tax_from_id(kwargs.get('gbifkey'))
        
        # yes: 
            # is the gbif key already in the db?
                # yes: check if there are other info on the species and if there are compatible with the tax in the db
                # no get the gbif taxon info from gbif key
    # has the species a scientificname?
        # yes:
            # is the scientificname already in the db
                # yes
            #
    
