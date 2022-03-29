from flask import Flask,request,jsonify
from flask_restful import Api, Resource, abort
from webargs import fields, validate,missing
from webargs.flaskparser import parser
from webargs.flaskparser import use_args,use_kwargs
from endpoint_def import testEndem,testExot,testThreat,insertEndem,insertExot,insertThreat,insertTaxo,User,AdminUsers,listExot,listTax, listEndem, listThreat, listReferences, getTaxon
PYTHONIOENCODING="UTF-8"


app = Flask(__name__, static_folder='static', static_url_path='')
api = Api(app)


@app.route('/')
def mainPage():
    return(app.send_static_file("home.html"))

api.add_resource(User,'/user')
api.add_resource(insertTaxo, '/insertTaxo')
api.add_resource(testEndem, '/testEndem')
api.add_resource(testExot, '/testExot')
api.add_resource(testThreat, '/testThreat')
api.add_resource(insertEndem, '/insertEndem')
api.add_resource(insertExot, '/insertExot')
api.add_resource(insertThreat, '/insertThreat')
api.add_resource(AdminUsers,'/admin/users')
api.add_resource(listExot, '/listExot')
api.add_resource(listTax, '/listTax')
api.add_resource(listEndem, '/listEndem')
api.add_resource(listThreat, '/listThreat')
api.add_resource(listReferences, '/listReferences')
api.add_resource(getTaxon,'/tax')

if __name__ == "__main__":
    app.run()
