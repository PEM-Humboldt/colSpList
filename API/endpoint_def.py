from flask import Flask, render_template, jsonify
from flask_restful import Resource, Api
from taxo import manageInputTax
from manageStatus import manageInputThreat
from manageStatus import manageInputEndem
from manageStatus import manageInputExot
from getStatus import testEndemStatus
from getStatus import testExotStatus
from getStatus import testThreatStatus
from webargs import fields, validate,missing
from webargs.flaskparser import parser
from webargs.flaskparser import use_args,use_kwargs,abort
import psycopg2
import os
DATABASE_URL = os.environ['DATABASE_URL']
PYTHONIOENCODING="UTF-8"

taxInputArgs = {'gbifkey':fields.Int(required=False), 'scientificname':fields.Str(required=False), 'canonicalname':fields.Str(required=False), 'authorship':fields.Str(required=False), 'syno':fields.Bool(required=False), 'rank': fields.Str(required=False), 'parentgbifkey':fields.Int(required=False), 'parentcanonicalname':fields.Str(required=False), 'parentscientificname':fields.Str(required=False), 'synogbifkey':fields.Int(required=False), 'synocanonicalname':fields.Str(required=False), 'synoscientificname':fields.Str(required=False) }

# TODO: check, for link, how to authorize some of the element of a list to be None and how to force the link and ref_citation to be of the same size

inputThreatArgs={'threatstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'link': fields.List(fields.Str(), required = False), 'comments': fields.Str(required=False)}
inputThreatArgs.update(taxInputArgs)


inputEndemArgs={'endemstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'link': fields.List(fields.Str(), required = False), 'comments': fields.Str(required=False)}
inputEndemArgs.update(taxInputArgs)

inputExotArgs={'is_alien':fields.Bool(required=True), 'is_invasive': fields.Bool(required=True), 'occ_observed': fields.Bool(required=False),'cryptogenic': fields.Bool(required=False), 'ref_citation':fields.List(fields.Str(),required=True), 'link': fields.List(fields.Str(),required=False), 'comments': fields.Str(required=False)}
inputExotArgs.update(taxInputArgs)

class testEnvVariable(Resource):
    def get(self):
        var=os.environ['TEST_ENV']
        return {'test_env':var}

class testEndem(Resource):
    @use_kwargs(taxInputArgs,location="query")
    @use_kwargs(taxInputArgs,location="json")
    def get(self, **inputArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cd_tax = manageInputTax(**inputArgs)
        res = testEndemStatus(conn,cd_tax)
        conn.close()
        return res
        
        
class testExot(Resource):
    @use_kwargs(taxInputArgs,location="query")
    @use_kwargs(taxInputArgs,location="json")
    def get(self, **inputArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cd_tax = manageInputTax(**inputArgs)
        res = testExotStatus(conn,cd_tax)
        conn.close()
        return res

class testThreat(Resource):
    @use_kwargs(taxInputArgs,location="query")
    @use_kwargs(taxInputArgs,location="json")
    def get(self, **inputArgs):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cd_tax = manageInputTax(**inputArgs)
        res = testThreatStatus(conn,cd_tax)
        conn.close()
        return res

class insertEndem(Resource):
    @use_kwargs(inputEndemArgs)
    def post(self,**inputEndem):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cd_tax = manageInputTax(**inputEndem)
        res = manageInputEndem(cd_tax, connection = conn, **inputEndem)
        return res

class insertExot(Resource):
    @use_kwargs(inputExotArgs)
    def post(self, **inputExot):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cd_tax = manageInputTax(**inputExot)
        res = manageInputExot(cd_tax, connection = conn, **inputExot)
        return res
    
class insertThreat(Resource):
    @use_kwargs(inputThreatArgs)
    def post(self, **inputThreat):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cd_tax = manageInputTax(**inputThreat)
        res = manageInputThreat(cd_tax, connection = conn, **inputThreat)
        conn.close()
        return res

class insertTaxo(Resource):
    @use_kwargs(taxInputArgs)
    def post(self,**dictInput):
        return manageInputTax(**dictInput)

    
# This error handler is necessary for usage with Flask-RESTful
@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(error_status_code, errors=err.messages)
