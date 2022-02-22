from flask import Flask, render_template, jsonify
from flask_restful import Resource, Api
from main import manageInputTax
from main import manageInputThreat
from webargs import fields, validate,missing
from webargs.flaskparser import parser
from webargs.flaskparser import use_args,use_kwargs
import psycopg2
import os
DATABASE_URL = os.environ['DATABASE_URL']
PYTHONIOENCODING="UTF-8"

inputExotArgs = inputEndemArgs = inputThreatArgs = taxInputArgs = {'gbifkey':fields.Int(required=False), 'scientificname':fields.Str(required=False), 'canonicalname':fields.Str(required=False)}

inputThreatArgs.update({'threatstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'link': fields.List(fields.Str(), required = False), 'comments': fields.Str(required=False)})

inputEndemArgs.update({'endemstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'link': fields.List(fields.Str(), required = False), 'comments': fields.Str(required=False)})


class testEndem(Resource):
    def get(self, name):
        return None
        
class testExot(Resource):
    def get(self):
        return None

class testThreat(Resource):
    def get(self):
        return None

class insertEndem(Resource):
    @use_kwargs(inputEndemArgs)
    def post(self,**inputEndem):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        id_tax = manageInputTax(**inputEndem)
        res = manageInputEndem(id_tax, connection = conn, **inputEndem)
        return res

class insertExot(Resource):
    def post(self):
        return None
    
class insertThreat(Resource):
    @use_kwargs(inputThreatArgs)
    def post(self, **inputThreat):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        id_tax = manageInputTax(**inputThreat)
        res = manageInputThreat(id_tax, connection = conn, **inputThreat)
        conn.close()
        return res

class insertTaxo(Resource):
    taxInputArgs = {'gbifkey':fields.Int(required=False), 'scientificname':fields.Str(required=False), 'canonicalname':fields.Str(required=False)}
    @use_kwargs(taxInputArgs)
    def post(self,**dictInput):
        return manageInputTax(**dictInput)

    
