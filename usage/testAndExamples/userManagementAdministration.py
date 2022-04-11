import requests
from requests.auth import HTTPBasicAuth
from flask import jsonify
from pprint import pprint as pp
api_url="http://colsplist.herokuapp.com"

f=open("codeAdmin","r")
codeAdmin=f.readline().replace('\n','')
endpoint="/user"
authAdmin=HTTPBasicAuth('admin',codeAdmin)
requests.put(api_url+endpoint,auth=authAdmin,json={'newPassword':'temporaryAdminCode'})
authAdmin=HTTPBasicAuth('admin','temporaryAdminCode')
resToken=requests.get(api_url+endpoint,auth=authAdmin,json={'create_token':'True'})
content=resToken.json()
authTokenAdmin =HTTPBasicAuth(content.get('token'),'token')
# creation user with basic right
res = requests.post(api_url+endpoint,json={'username':'basicUser','password':'tempCode1'})
res.json()
# creation user with edit right
res = requests.post(api_url+endpoint,json={'username':'editUser','password':'tempCode2'})
res.json()
# grant edit to editUser
endpoint = "/admin/users"
res=requests.put(api_url+endpoint,json={'username':'editUser','grant_edit':'True'},auth=authTokenAdmin)
res.json()
# Getting the tokens for these new users:
endpoint="/user"
authBasicUser=HTTPBasicAuth('basicUser','tempCode1')
res= requests.get(api_url+endpoint,json={'create_token':'True'},auth=authBasicUser)
content=res.json()
authTokenBasicUser=HTTPBasicAuth(content.get('token'),'token')
authEditUser=HTTPBasicAuth('editUser','tempCode2')
res= requests.get(api_url+endpoint,json={'create_token':'True'},auth=authEditUser)
content=res.json()
authTokenEditUser=HTTPBasicAuth(content.get('token'),'token')

endpoint = "/admin/users"
res=requests.get(api_url+endpoint, auth=authTokenAdmin)
users=res.json()
pp(users)

usernames=[r['username'] for r in users]
pp(usernames)

res=requests.get(api_url+endpoint, auth=authTokenBasicUser)
pp(res.text)

requests.post(api_url+'/user',json={'username':'userToDel','password':'whatever'})
res=requests.get(api_url+endpoint, auth=authTokenAdmin)
users=res.json()
usernames=[r['username'] for r in users]
pp(usernames)

requests.delete(api_url+endpoint,json={'username':'userToDel'}, auth=authTokenAdmin)
res=requests.get(api_url+endpoint, auth=authTokenAdmin)
users=res.json()
usernames=[r['username'] for r in users]
pp(usernames)

requests.post(api_url+'/user',json={'username':'userToDel','password':'whatever'})

res=requests.get(api_url+endpoint, auth=authTokenAdmin)
users=res.json()
usernamesEdit=[r['username'] for r in users if r['edit']]
pp(usernamesEdit)

res=requests.put(api_url+endpoint, json={'username':'userToDel','grant_edit':True}, auth=authTokenAdmin)
res.text

res=requests.get(api_url+endpoint, auth=authTokenAdmin)
users=res.json()
usernamesEdit=[r['username'] for r in users if r['edit']]
pp(usernamesEdit)

res=requests.put(api_url+endpoint, json={'username':'userToDel','revoke_edit':True}, auth=authTokenAdmin)
res.text

res=requests.get(api_url+endpoint, auth=authTokenAdmin)
users=res.json()
usernamesEdit=[r['username'] for r in users if r['edit']]
pp(usernamesEdit)

userToDel,=[r for r in users if r['username']=='userToDel']
pp(userToDel)
requests.put(api_url+endpoint, json={'grant_admin':True,'username':'userToDel'}, auth=authTokenAdmin)
res=requests.get(api_url+endpoint, auth=authTokenAdmin)
users=res.json()
userToDel,=[r for r in users if r['username']=='userToDel']
pp(userToDel)
requests.put(api_url+endpoint, json={'revoke_admin':True,'username':'userToDel'}, auth=authTokenAdmin)
res=requests.get(api_url+endpoint, auth=authTokenAdmin)
users=res.json()
userToDel,=[r for r in users if r['username']=='userToDel']
pp(userToDel)
requests.put(api_url+endpoint, json={'revoke_user':True,'username':'userToDel'}, auth=authTokenAdmin)
res=requests.get(api_url+endpoint, auth=authTokenAdmin)
users=res.json()
userToDel,=[r for r in users if r['username']=='userToDel']
pp(userToDel)
requests.put(api_url+endpoint, json={'grant_user':True,'username':'userToDel'}, auth=authTokenAdmin)
res=requests.get(api_url+endpoint, auth=authTokenAdmin)
users=res.json()
userToDel,=[r for r in users if r['username']=='userToDel']
pp(userToDel)


res=requests.put(api_url+endpoint, json={'revoke_admin':True,'username':'basicUser'}, auth=authTokenAdmin)
res.json()

requests.put(api_url+endpoint, json={'newPassword':'newWhatever','username':'userToDel'}, auth=authTokenAdmin)

requests.delete(api_url+endpoint,json={'username':'userToDel'}, auth=authTokenAdmin)

endpoint="/user"
authBasicUser=HTTPBasicAuth('basicUser','tempCode1')
res = requests.get(api_url+endpoint, json={'create_token':True}, auth=authBasicUser)
res.json()

content=res.json()
token=content.get('token')
myAuth=HTTPBasicAuth(token,'token')
res= requests.get(api_url+endpoint, json={'create_token':False}, auth=myAuth)
res.json()

res=requests.put(api_url+endpoint, json={'newPassword':'tempCode3'}, auth=myAuth)

res = requests.get(api_url+endpoint, auth=HTTPBasicAuth('basicUser','tempCode1'))
res.text
res = requests.get(api_url+endpoint, auth=HTTPBasicAuth('basicUser','tempCode3'))
res.text

res=requests.get(api_url+'/admin/users', auth=authTokenAdmin)
users=res.json()
usernames=[r['username'] for r in users]
pp(usernames)

res = requests.delete(api_url+endpoint, auth=myAuth)

res=requests.get(api_url+'/admin/users', auth=authTokenAdmin)
users=res.json()
usernames=[r['username'] for r in users]
pp(usernames)

res = requests.post(api_url+endpoint, json={'username':'newUser','password':'whatever'})

res=requests.get(api_url+'/admin/users', auth=authTokenAdmin)
users=res.json()
usernames=[r['username'] for r in users]
pp(usernames)

endpoint="/performance"
res=requests.put(api_url+endpoint,json={'vacuum':True,'analysis':True},auth=authTokenAdmin)

endpoint="/manageTaxo"
res=requests.post(api_url+endpoint,json={'canonicalname':'Abies fraseri'},auth=authEditUser)
res.json()

endpoint="/cleanDb"
res=requests.delete(api_url+endpoint,auth=authEditUser,json={'ref_no_status':True,'status_no_ref':True,'syno_no_tax':True,'tax_no_status':True})
res.json()

endpoint="/admin/users"
# Deleting the users created for this document
userToDel={'username':'editUser'}
res=requests.delete(api_url+endpoint,json=userToDel,auth=authAdmin)
res.json()
userToDel={'username':'newUser'}
res=requests.delete(api_url+endpoint,json=userToDel,auth=authAdmin)
res.json()
endpoint="/user"
res=requests.put(api_url+endpoint,json={'newPassword':codeAdmin},auth=authTokenAdmin)
res.json()
