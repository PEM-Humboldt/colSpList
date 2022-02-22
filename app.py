from flask import Flask,request,jsonify
from flask_restful import Api, Resource, abort
from webargs import fields, validate,missing
from webargs.flaskparser import parser
from webargs.flaskparser import use_args,use_kwargs
from endpoint_def import testEndem
from endpoint_def import testExot
from endpoint_def import testThreat
from endpoint_def import insertEndem
from endpoint_def import insertExot
from endpoint_def import insertThreat
from endpoint_def import insertTaxo
PYTHONIOENCODING="UTF-8"

args_taxo_insert = {
    'gbifkey' : fields.Int(required=False),
    'canonicalname' : fields.Str(required=False),
    'scientificname': fields.Str(required=False)}

app = Flask(__name__, static_folder='static', static_url_path='')
api = Api(app)


@app.route('/')
def mainPage():
    return(app.send_static_file("home.html"))

api.add_resource(insertTaxo, '/insertTaxo')
api.add_resource(testEndem, '/testEndem')
api.add_resource(testExot, '/testExot')
api.add_resource(testThreat, '/testThreat')
api.add_resource(insertEndem, '/insertEndem')
api.add_resource(insertExot, '/insertExot')
api.add_resource(insertThreat, '/insertThreat')

if __name__ == "__main__":
    app.run()
