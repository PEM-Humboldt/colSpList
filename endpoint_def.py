from flask import Flask, render_template, jsonify
from flask_restful import Resource, Api
from main import manageInputTax
from webargs import fields, validate,missing
from webargs.flaskparser import parser
from webargs.flaskparser import use_args,use_kwargs
import psycopg2
import os

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
    def post(self):
        return None

class insertExot(Resource):
    def post(self):
        return None
    
class insertThreat(Resource):
    def post(self):
        return None

class insertTaxo(Resource):
    taxInputArgs = {'gbifkey':fields.Int(required=False),'scientificname':fields.Str(required=False),'canonicalname':fields.Str(required=False)}
    @use_kwargs(taxInputArgs)
    def post(self,**dictInput):
        return manageInputTax(**dictInput)

    
