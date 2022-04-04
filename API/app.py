from flask import Flask,request,jsonify
from flask_restful import Api, Resource, abort
from webargs import fields, validate,missing
from webargs.flaskparser import parser
from webargs.flaskparser import use_args,use_kwargs
from endpoint_def import CleanDb,Performance,User,AdminUsers,GetTaxon, TestEndem, TestThreat, TestExot, ListExot, ListEndem, ListThreat, ListTax, ListReferences, ManageEndem, ManageExot, ManageThreat, ManageTax, ManageRef
PYTHONIOENCODING="UTF-8"


app = Flask(__name__, static_folder='static', static_url_path='')
api = Api(app)

api.add_resource(TestEndem,'/testEndem')
api.add_resource(TestExot,'/testExot')
api.add_resource(TestThreat,'/testThreat')
api.add_resource(ListEndem,'/listEndem')
api.add_resource(ListExot,'/listExot')
api.add_resource(ListThreat,'/listThreat')
api.add_resource(ListTax,'/listTax')
api.add_resource(GetTaxon,'/tax')
api.add_resource(ListReferences,'/listReferences')
api.add_resource(ManageTax,'/manageTaxo')
api.add_resource(ManageEndem,'/manageEndem')
api.add_resource(ManageExot,'/manageExot')
api.add_resource(ManageThreat,'/manageThreat')
api.add_resource(ManageRef,'/manageRef')
api.add_resource(CleanDb,'/cleanDb')
api.add_resource(Performance,'/performance')
api.add_resource(User,'/user')
api.add_resource(AdminUsers,'/admin/users')

@app.route('/')
def mainPage():
    return(app.send_static_file("home.html"))


if __name__ == "__main__":
    app.run()
