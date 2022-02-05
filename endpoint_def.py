from flask import Flask, render_template, jsonify
from flask_restful import Resource, Api
from main import exp_act_joke
from main import act_joke
from main import export_log
from main import export_log_complete
import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


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
    def post(self):
        return None

    
