import requests
api_url="http://localhost:5000"

endpoint="/testEndem"

toSend1={'canonicalname':'Accipiter collaris'}
response = requests.get(api_url+endpoint, json=toSend1)
response.json()

toSend2={'scientificname':'Odontophorus strophium (Gould, 1844)'}
response = requests.get(api_url+endpoint, json=toSend2)
response.json()

toSend3={'gbifkey':2480593}
response = requests.get(api_url+endpoint, json=toSend3)
response.json()

toSend4 = {'canonicalname':'Anas andium'}
response = requests.get(api_url+endpoint, json=toSend4)
response.json()

toSend5 = {'canonicalname':'Accipiter colloris'}
response = requests.get(api_url+endpoint, json=toSend5)
response.json()

toSend6={'canonicalname':'Elaeis guineensis'}
response = requests.get(api_url+endpoint, json=toSend6)
response.json()

toSend7={'canonicalname':'Espeletia grandiflora'}
response = requests.get(api_url+endpoint, json=toSend7)
response.json()

toSend8={'canonicalname':'Asriwendosa machibibus'}
response = requests.get(api_url+endpoint, json=toSend8)
response.json()

toSend9={}
response = requests.get(api_url+endpoint, json=toSend9)
response.json()

endpoint="/testEndem/list"

ListToSend={'list':[toSend1,toSend2,toSend3,toSend4,toSend5,toSend6,toSend7,toSend8,toSend9]}
response = requests.post(api_url+endpoint, json=ListToSend)
response.json()

endpoint="/testExot"

toSend1={'canonicalname':'Gymnocorymbus ternetzi'}
response = requests.get(api_url+endpoint, json=toSend1)
response.json()

toSend2={'scientificname':'Rosa chinensis Jacq.'}
response = requests.get(api_url+endpoint, json=toSend2)
response.json()

toSend3={'gbifkey':5190769}
response = requests.get(api_url+endpoint, json=toSend3)
response.json()

toSend4 = {'canonicalname':'Cnidoscolus chayamansa'}
response = requests.get(api_url+endpoint, json=toSend4)
response.json()

toSend5 = {'canonicalname':'Rosa chinansis'}
response = requests.get(api_url+endpoint, json=toSend5)
response.json()

toSend6={'canonicalname':'Licania glauca'}
response = requests.get(api_url+endpoint, json=toSend6)
response.json()

toSend7={'canonicalname':'Espeletia grandiflora'}
response = requests.get(api_url+endpoint, json=toSend7)
response.json()

toSend8={'canonicalname':'Asriwendosa machibibus'}
response = requests.get(api_url+endpoint, json=toSend8)
response.json()

toSend9={}
response = requests.get(api_url+endpoint, json=toSend9)
response.json()

endpoint="/testExot/list"

ListToSend={'list':[toSend1,toSend2,toSend3,toSend4,toSend5,toSend6,toSend7,toSend8,toSend9]}
response = requests.post(api_url+endpoint, json=ListToSend)
response.json()

endpoint="/testThreat"

toSend1={'canonicalname':'Podocarpus guatemalensis'}
response = requests.get(api_url+endpoint, json=toSend1)
response.json()

toSend2={'scientificname':'Puya ochroleuca Betancur & Callejas'}
response = requests.get(api_url+endpoint, json=toSend2)
response.json()

toSend3={'gbifkey':5789077}
response = requests.get(api_url+endpoint, json=toSend3)
response.json()

toSend4 = {'canonicalname':'Ptychoglossus danieli'}
response = requests.get(api_url+endpoint, json=toSend4)
response.json()

toSend5 = {'canonicalname':'Espeletia paypana'}
response = requests.get(api_url+endpoint, json=toSend5)
response.json()

toSend6={'canonicalname':'Tangara johannae'}
response = requests.get(api_url+endpoint, json=toSend6)
response.json()

toSend7={'canonicalname':'Espeletia grandiflora'}
response = requests.get(api_url+endpoint, json=toSend7)
response.json()

toSend8={'canonicalname':'Asriwendosa machibibus'}
response = requests.get(api_url+endpoint, json=toSend8)
response.json()

toSend9={}
response = requests.get(api_url+endpoint, json=toSend9)
response.json()

endpoint="/testThreat/list"

ListToSend={'list':[toSend1,toSend2,toSend3,toSend4,toSend5,toSend6,toSend7,toSend8,toSend9]}
response = requests.post(api_url+endpoint, json=ListToSend)
response.json()

endpoint="/listEndem"

response = requests.get(api_url+endpoint)
content=response.json()
len(content)
content[0:4]

onlyPasserine={'childrenOf':'Passeriformes'}
response = requests.get(api_url+endpoint,json=onlyPasserine)
content=response.json()
len(content)
content[0:4]

onlyAbies={'childrenOf':'Abies'}
response = requests.get(api_url+endpoint,json=onlyAbies)
response.json()

endpoint="/listExot"

response = requests.get(api_url+endpoint)
content=response.json()
len(content)
content[0:4]

onlyPasserine={'childrenOf':'Passeriformes'}
response = requests.get(api_url+endpoint,json=onlyPasserine)
content=response.json()
len(content)
content[0:4]

onlyAbies={'childrenOf':'Abies'}
response = requests.get(api_url+endpoint,json=onlyAbies)
response.json()

endpoint="/listThreat"

response = requests.get(api_url+endpoint)
content=response.json()
len(content)
content[0:4]

onlyPasserine={'childrenOf':'Passeriformes'}
response = requests.get(api_url+endpoint,json=onlyPasserine)
content=response.json()
len(content)
content[0:4]

onlyAbies={'childrenOf':'Abies'}
response = requests.get(api_url+endpoint,json=onlyAbies)
response.json()

endpoint = "/tax"

toSend={'cd_tax':150}
response = requests.get(api_url+endpoint, json=toSend)
response.json()

toSend={'scientificname':"Urochloa brizantha (A.Rich.) R.D.Webster"}
response = requests.get(api_url+endpoint, json=toSend)
response.json()

toSend={'canonicalname':'Rottboellia cochinchinensis'}
response = requests.get(api_url+endpoint, json=toSend)
response.json()

toSend={'canonicalname':'Amanita caesarea'}
response = requests.get(api_url+endpoint, json=toSend)
response.json()

toSend={'canonicalname':'Inventadus inexistus'}
response = requests.get(api_url+endpoint, json=toSend)
response.json()

endpoint="/listTax"

response = requests.get(api_url+endpoint)
content=response.json()
len(content)
content[0:4]

onlyBivalve={'childrenOf':'Bivalvia'}
response = requests.get(api_url+endpoint,json=onlyBivalve)
content=response.json()
len(content)
content[0:9]

endpoint = "/listReferences"

response = requests.get(api_url+endpoint)
content=response.json()
len(content)
content[0:9]

onlyExot={'onlyExot':True}
response = requests.get(api_url+endpoint, json=onlyExot)
content=response.json()
len(content)
content[0:9]

onlyThreat={'onlyThreat':True}
response = requests.get(api_url+endpoint, json=onlyThreat)
content=response.json()
len(content)
content[0:9]

onlyEndem={'onlyEndem':True}
response = requests.get(api_url+endpoint, json=onlyEndem)
content=response.json()
len(content)
content[0:9]
