import requests
from requests.auth import HTTPBasicAuth
from flask import jsonify
from pprint import pprint as pp
api_url="https://colsplist.herokuapp.com"

f=open("codeAdmin","r")
codeAdmin=f.readline().replace('\n','')
f.close()
authAdmin=HTTPBasicAuth('admin',codeAdmin)
requests.put(api_url+'/user',auth=authAdmin,json={'newPassword':'temporaryAdminCode'})
authAdmin=HTTPBasicAuth('admin','temporaryAdminCode')
resToken=requests.get(api_url+'/user',auth=authAdmin,json={'create_token':'True'})
content=resToken.json()
authTokenAdmin =HTTPBasicAuth(content.get('token'),'token')
# creation user with edit right
res = requests.post(api_url+'/user',json={'username':'editUser','password':'tempCode2'})
pp(res.json())
# grant edit to editUser
res=requests.put(api_url+'/admin/users',json={'username':'editUser','grant_edit':'True'},auth=authTokenAdmin)
pp(res.json())
# Getting the tokens for these new users:
authEditUser=HTTPBasicAuth('editUser','tempCode2')
res= requests.get(api_url+'/user',json={'create_token':'True'},auth=authEditUser)
content=res.json()
authTokenEditUser=HTTPBasicAuth(content.get('token'),'token')

endpoint="/manageTaxo"

newTax1={'canonicalname':'Abies grandis'}
res=requests.post(api_url+endpoint,json=newTax1,auth=authTokenEditUser)
pp(res.json())

newTax2={'canonicalname':'Vultur gryphus'}
res=requests.post(api_url+endpoint,json=newTax2,auth=authTokenEditUser)
pp(res.json())

newTax3={'gbifkey':7963890}
res=requests.post(api_url+endpoint,json=newTax3,auth=authTokenEditUser)
pp(res.json())
newTax4={'scientificname':'Juniperus thurifera'}
res=requests.post(api_url+endpoint,json=newTax4,auth=authTokenEditUser)
pp(res.json())

newTax5={'canonicalname':'Vultur fossilis'}
res=requests.post(api_url+endpoint,json=newTax5,auth=authTokenEditUser)
pp(res.json())

newTax5={'canonicalname':'Vultur fossilis','min_gbif_conf':98}
res=requests.post(api_url+endpoint,json=newTax5,auth=authTokenEditUser)
pp(res.json())

res=requests.get(api_url+'/tax',json={'canonicalname':'Vultur fossilis'})
pp(res.json())

newTax6={'canonicalname':'Juniperus communis','no_gbif':True}
res=requests.post(api_url+endpoint,json=newTax6,auth=authTokenEditUser)
pp(res.json())

newTax8 = {'canonicalname':'Invented species'}
res=requests.post(api_url+endpoint,json=newTax8,auth=authTokenEditUser)
pp(res.json())

newTax7={'canonicalname':'Invented','scientificname':'Invented (marius, 2022)','authorship':'(marius, 2022)','parentcanonicalname':'Fabaceae','syno':False,'rank':'GENUS','no_gbif':True}
res=requests.post(api_url+endpoint,json=newTax7,auth=authTokenEditUser)
pp(res.json())
parentId=res.json().get('cd_tax')

newTax8={'canonicalname':'Invented species','scientificname':'Invented species (marius, 2022)','authorship':'(marius, 2022)','parentcanonicalname':'Invented','syno':False,'rank':'SPECIES','no_gbif':True}
res=requests.post(api_url+endpoint,json=newTax8,auth=authTokenEditUser)
pp(res.json())
taxId=res.json().get('cd_tax')

res=requests.get(api_url+'/tax',json={'cd_tax':parentId})
pp(res.json())
res=requests.get(api_url+'/tax',json={'cd_tax':taxId})
pp(res.json())

res=requests.get(api_url+'/tax',json={'canonicalname':'Juniperus communis'})
pp(res.json())
modified1={'cd_tax':res.json().get('cd_tax')}

modified1['gbifkey']=2684709
res=requests.put(api_url+endpoint, json=modified1, auth=authTokenEditUser)

res=requests.get(api_url+'/tax',json={'canonicalname':'Juniperus communis'})
pp(res.json())

res=requests.get(api_url+'/tax',json={'canonicalname':'Invented species'})
pp(res.json())
modified2Id = res.json().get('cd_tax')

modified2={'cd_tax':modified2Id,'authorship':'(marius 2005)','scientificname':'Invented species (marius 2005)'}
res=requests.put(api_url+endpoint, json=modified2, auth=authTokenEditUser)
pp(res.json())

res=requests.get(api_url+'/tax',json={'canonicalname':'Invented species'})
pp(res.json())
modified2Id = res.json().get('cd_tax')

res=requests.get(api_url+'/tax',json={'canonicalname': 'Abies grandis'})
pp(res.json())
del1={'cd_tax':res.json().get('cd_tax')}
res=requests.delete(api_url+endpoint,json=del1,auth=authTokenEditUser)
pp(res.json())

res=requests.delete(api_url+'/cleanDb',json={'tax_no_status':True},auth=authTokenEditUser)
pp(res.json())
endpoint='/manageTaxo/list'

multiNewTax={'list':[newTax1,newTax2,newTax3,newTax4,newTax5,newTax6,newTax7,newTax8]}
pp(multiNewTax)

res=requests.post(api_url+endpoint,json=multiNewTax,auth=authTokenEditUser)
pp(res.json())

res=requests.post(api_url+'/tax/list',json={'list':[{'canonicalname':'Abies grandis'},{'canonicalname':'Juniperus thurifera'}]})
pp(res.json())
cdTaxToDel=[{'cd_tax':r['cd_tax']} for r in res.json()]
pp(cdTaxToDel)

res=requests.delete(api_url+endpoint, json={'list':cdTaxToDel},auth=authTokenEditUser)
pp(res.json())

res=requests.post(api_url+'/tax/list',json={'list':[{'canonicalname':'Juniperus communis'},{'canonicalname':'Invented species'}]})
pp(res.json())
ToModify=[{'cd_tax':r['cd_tax']} for r in res.json()]
ToModify[0]['gbifkey']=2684709
ToModify[1].update({'authorship':'(marius 2005)','scientificname':'Invented species (marius 2005)'})
pp(ToModify)

res=requests.put(api_url+endpoint,json={'list':ToModify},auth=authTokenEditUser)
res.text
res=requests.post(api_url+'/tax/list',json={'list':[{'canonicalname':'Juniperus communis'},{'canonicalname':'Invented species'}]})
pp(res.json())

endpoint='/manageEndem'



status1={'canonicalname':'Invented species',
  'endemstatus':'Información insuficiente',
  'ref_citation':['Bottin et al, 2022. False paper to show an example','A second reference just for fun!'],
  'link':['https://colsplist.herokuapp.com',' '],
  'comments':'This is a first comment | Feeding habits: Does not eat at all!'}
res=requests.post(api_url+endpoint,json=status1,auth= authTokenEditUser)
pp(res.json())

res=requests.get(api_url+'/testEndem',json={'canonicalname':'Invented species'})
pp(res.json())

status2={'canonicalname':'Newspecies nonexistens',
  'scientificname':'Newspecies nonexistens (marius 2022)',
  'authorship':'(marius 2022)',
  'parentcanonicalname':'Invented',
  'endemstatus':'Endemic',
  'ref_citation':['Bottin et al, 2022. False paper to show an example','A third reference just for fun!'],
  'link':['https://colsplist.herokuapp.com',' '],
  'comments':'random comment | repartition: nula'}
res=requests.post(api_url+endpoint,json=status2,auth= authTokenEditUser)
pp(res.json())


requests.get(api_url+'/testEndem',json={'canonicalname':'Juniperus communis'}).json()
status3={'canonicalname':'Juniperus communis',
  'endemstatus':'Almost endamic',
  'ref_citation':['Bottin et al, 2022. False paper to show an example'],
  'link':['https://colsplist.herokuapp.com'],
  'comments':'random comment | repartition: nula'}
res=requests.post(api_url+endpoint,json=status3,auth= authTokenEditUser)
pp(res.json())

res=requests.get(api_url+'/testEndem',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())

status4={'canonicalname':'Newspecies nonexistens',
  'endemstatus':'Almost endemic',
  'comments':'endemism evaluation methodology: None, this is only a fake species!',
  'ref_citation':['Bottin, 2025. New fake reference with a weird date'],
  'priority':'low',
  'replace_comment':False
}
pp(requests.post(api_url+'/manageEndem',json=status4,auth=authTokenEditUser).json())

res=requests.get(api_url+'/testEndem',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())

status5={'canonicalname':'Newspecies nonexistens',
  'endemstatus':'Almost endemic',
  'comments':'endemism evaluation methodology 2: None, this is still only a fake species!',
  'ref_citation':['Bottin, 2026. New fake reference with a weirder date'],
  'priority':'high',
  'replace_comment':True
}
pp(requests.post(api_url+'/manageEndem',json=status5,auth=authTokenEditUser).json())

res=requests.get(api_url+'/testEndem',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())

res=requests.get(api_url+'/testEndem',json={'canonicalname':'Invented species'})
pp(res.json())
cd_tax=res.json().get('cd_tax_acc')

status6={'cd_tax':cd_tax,
  'endemstatus':'Species of interest',
  'ref_citation':['Bottin, 2051. New fake reference with the weirdest date'],
}
pp(requests.put(api_url+'/manageEndem',json=status6,auth=authTokenEditUser).json())

res=requests.get(api_url+'/testEndem',json={'canonicalname':'Invented species'})
pp(res.json())

listRef=requests.get(api_url+'/listReferences').json()
cd_ref = [r['cd_ref'] for r in listRef if r['ref_citation']=='Bottin et al, 2022. False paper to show an example'][0]
pp(cd_ref)
cd_tax=requests.get(api_url+'/tax',json={'canonicalname':'Invented species'}).json()['cd_tax']
pp(cd_tax)

pp(requests.get(api_url+'/testEndem',json={'canonicalname':'Invented species'}).json())

res=requests.delete(api_url+'/manageEndem', json={'cd_tax':cd_tax,'cd_ref':cd_ref},auth=authTokenEditUser)
pp(res.json())

pp(requests.get(api_url+'/testEndem',json={'canonicalname':'Invented species'}).json())

pp(requests.delete(api_url + '/manageEndem',json={'cd_tax':cd_tax},auth=authTokenEditUser).json())

pp(requests.delete(api_url + '/manageEndem',json={'cd_tax':cd_tax,'delete_status':True},auth=authTokenEditUser).json())

pp(requests.get(api_url+'/testEndem',json={'canonicalname':'Invented species'}).json())

cd_tax_ToDel=requests.get(api_url + '/tax',json={'canonicalname':'Newspecies nonexistens'}).json().get('cd_tax')
requests.delete(api_url+'/manageTaxo',json={'cd_tax':cd_tax_ToDel},auth=authTokenEditUser)
cd_tax_StatusToDel=requests.get(api_url + '/testEndem',json={'canonicalname':'Invented species'}).json().get('cd_tax')
res=requests.delete(api_url+'/manageEndem',json={'cd_tax':cd_tax_StatusToDel, 'delete_status':True}, auth=authTokenEditUser)
res=requests.delete(api_url+'/cleanDb',json={'ref_no_status':True}, auth=authTokenEditUser)

statuses=[status1,status2,status3,status4,status5]
pp(statuses)
res=requests.post(api_url + '/manageEndem/list',json={'list':statuses},auth=authTokenEditUser)
pp(res.json())

newSpecies=requests.post(api_url+'/testEndem/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json()
pp(newSpecies)
newSpecies_cd_tax=[n['cd_tax_acc'] for n in newSpecies]
modifications={'list':
  [
    {
      'cd_tax': newSpecies_cd_tax[0],
      'endemstatus':'Casi endémicas por área',
      'ref_citation':['Fake report to put Invented species as Almost endemic by area'],
      'link':['https://www.afalsesiteasanexample.com'],
      'comments': 'a comment as replacement',
      'replace_comment':True
    },
    {
      'cd_tax': newSpecies_cd_tax[1],
      'endemstatus':'Endemic',
      'ref_citation':['Another fake report'],
      'comments': 'a comment to add',
    }
  ]
}
pp(modifications)
modifs=requests.put(api_url + '/manageEndem/list',json=modifications,auth=authTokenEditUser).json()
pp(modifs)
pp(requests.post(api_url+'/testEndem/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())

pp(requests.post(api_url+'/testEndem/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())
listRef=requests.get(api_url+'/listReferences').json()
cd_ref1 = [r['cd_ref'] for r in listRef if r['ref_citation']=='Bottin et al, 2022. False paper to show an example'][0]
cd_ref2 = [r['cd_ref'] for r in listRef if r['ref_citation']=='Fake report to put Invented species as Almost endemic by area'][0]
deletions=[
  {'cd_tax':newSpecies_cd_tax[0],
  'cd_ref':cd_ref1},
  {'cd_tax':newSpecies_cd_tax[0],
  'cd_ref':cd_ref2},
  {'cd_tax':newSpecies_cd_tax[1],
  'delete_status':True}
]
pp(deletions)
pp(requests.delete(api_url + '/manageEndem/list',json={'list':deletions},auth=authTokenEditUser).json())
pp(requests.post(api_url+'/testEndem/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())

pp(requests.delete(api_url + '/cleanDb',json={'status_no_ref':True,'ref_no_status':True},auth=authTokenEditUser).json())
pp(requests.delete(api_url + '/manageTaxo', json={'cd_tax':newSpecies_cd_tax[1]}, auth=authTokenEditUser).json())

endpoint='/manageThreat'



status1={'canonicalname':'Invented species',
  'threatstatus':'DD',
  'ref_citation':['Bottin et al, 2022. False paper to show an example','A second reference just for fun!'],
  'link':['https://colsplist.herokuapp.com',' '],
  'comments':'This is a first comment | Feeding habits: Does not eat at all!'}
res=requests.post(api_url+endpoint,json=status1,auth= authTokenEditUser)
pp(res.json())

res=requests.get(api_url+'/testThreat',json={'canonicalname':'Invented species'})
pp(res.json())

status2={'canonicalname':'Newspecies nonexistens',
  'scientificname':'Newspecies nonexistens (marius 2022)',
  'authorship':'(marius 2022)',
  'parentcanonicalname':'Invented',
  'threatstatus':'NT',
  'ref_citation':['Bottin et al, 2022. False paper to show an example','A third reference just for fun!'],
  'link':['https://colsplist.herokuapp.com',' '],
  'comments':'random comment | repartition: nula'}
res=requests.post(api_url+endpoint,json=status2,auth= authTokenEditUser)
pp(res.json())


requests.get(api_url+'/testThreat',json={'canonicalname':'Juniperus communis'}).json()
status3={'canonicalname':'Juniperus communis',
  'threatstatus':'EM',
  'ref_citation':['Bottin et al, 2022. False paper to show an example'],
  'link':['https://colsplist.herokuapp.com'],
  'comments':'random comment | repartition: nula'}
res=requests.post(api_url+endpoint,json=status3,auth= authTokenEditUser)
pp(res.json())

res=requests.get(api_url+'/testThreat',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())

status4={'canonicalname':'Newspecies nonexistens',
  'threatstatus':'EN',
  'comments':'threat evaluation methodology: None, this is only a fake species!',
  'ref_citation':['Bottin, 2025. New fake reference with a weird date'],
  'priority':'low',
  'replace_comment':False
}
pp(requests.post(api_url+'/manageThreat',json=status4,auth=authTokenEditUser).json())

res=requests.get(api_url+'/testThreat',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())

status5={'canonicalname':'Newspecies nonexistens',
  'threatstatus':'EN',
  'comments':'threat evaluation methodology 2: None, this is still only a fake species!',
  'ref_citation':['Bottin, 2026. New fake reference with a weirder date'],
  'priority':'high',
  'replace_comment':True
}
pp(requests.post(api_url+'/manageThreat',json=status5,auth=authTokenEditUser).json())

res=requests.get(api_url+'/testThreat',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())

res=requests.get(api_url+'/testThreat',json={'canonicalname':'Invented species'})
pp(res.json())
cd_tax=res.json().get('cd_tax_acc')

status6={'cd_tax':cd_tax,
  'threatstatus':'VU',
  'ref_citation':['Bottin, 2051. New fake reference with the weirdest date'],
}
pp(requests.put(api_url+'/manageThreat',json=status6,auth=authTokenEditUser).json())

res=requests.get(api_url+'/testThreat',json={'canonicalname':'Invented species'})
pp(res.json())

listRef=requests.get(api_url+'/listReferences').json()
cd_ref = [r['cd_ref'] for r in listRef if r['ref_citation']=='Bottin et al, 2022. False paper to show an example'][0]
pp(cd_ref)
cd_tax=requests.get(api_url+'/tax',json={'canonicalname':'Invented species'}).json()['cd_tax']
pp(cd_tax)

pp(requests.get(api_url+'/testThreat',json={'canonicalname':'Invented species'}).json())

res=requests.delete(api_url+'/manageThreat', json={'cd_tax':cd_tax,'cd_ref':cd_ref},auth=authTokenEditUser)
pp(res.json())

pp(requests.get(api_url+'/testThreat',json={'canonicalname':'Invented species'}).json())

pp(requests.delete(api_url + '/manageThreat',json={'cd_tax':cd_tax},auth=authTokenEditUser).json())

pp(requests.delete(api_url + '/manageThreat',json={'cd_tax':cd_tax,'delete_status':True},auth=authTokenEditUser).json())

pp(requests.get(api_url+'/testThreat',json={'canonicalname':'Invented species'}).json())

cd_tax_ToDel=requests.get(api_url + '/tax',json={'canonicalname':'Newspecies nonexistens'}).json().get('cd_tax')
requests.delete(api_url+'/manageTaxo',json={'cd_tax':cd_tax_ToDel},auth=authTokenEditUser)
cd_tax_StatusToDel=requests.get(api_url + '/testThreat',json={'canonicalname':'Invented species'}).json().get('cd_tax')
res=requests.delete(api_url+'/manageThreat',json={'cd_tax':cd_tax_StatusToDel, 'delete_status':True}, auth=authTokenEditUser)
res=requests.delete(api_url+'/cleanDb',json={'ref_no_status':True}, auth=authTokenEditUser)

statuses=[status1,status2,status3,status4,status5]
pp(statuses)
res=requests.post(api_url + '/manageThreat/list',json={'list':statuses},auth=authTokenEditUser)
pp(res.json())

newSpecies=requests.post(api_url+'/testThreat/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json()
pp(newSpecies)
newSpecies_cd_tax=[n['cd_tax_acc'] for n in newSpecies]
modifications={'list':
  [
    {
      'cd_tax': newSpecies_cd_tax[0],
      'threatstatus':'LC',
      'ref_citation':['Fake report to put Invented species as LC'],
      'link':['https://www.afalsesiteasanexample.com'],
      'comments': 'a comment as replacement',
      'replace_comment':True
    },
    {
      'cd_tax': newSpecies_cd_tax[1],
      'threatstatus':'CR',
      'ref_citation':['Another fake report'],
      'comments': 'a comment to add',
    }
  ]
}
pp(modifications)
modifs=requests.put(api_url + '/manageThreat/list',json=modifications,auth=authTokenEditUser).json()
pp(modifs)
pp(requests.post(api_url+'/testThreat/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())

pp(requests.post(api_url+'/testThreat/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())
listRef=requests.get(api_url+'/listReferences').json()
cd_ref1 = [r['cd_ref'] for r in listRef if r['ref_citation']=='Bottin et al, 2022. False paper to show an example'][0]
cd_ref2 = [r['cd_ref'] for r in listRef if r['ref_citation']=='Fake report to put Invented species as LC'][0]
deletions=[
  {'cd_tax':newSpecies_cd_tax[0],
  'cd_ref':cd_ref1},
  {'cd_tax':newSpecies_cd_tax[0],
  'cd_ref':cd_ref2},
  {'cd_tax':newSpecies_cd_tax[1],
  'delete_status':True}
]
pp(deletions)
pp(requests.delete(api_url + '/manageThreat/list',json={'list':deletions},auth=authTokenEditUser).json())
pp(requests.post(api_url+'/testThreat/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())

pp(requests.delete(api_url + '/cleanDb',json={'status_no_ref':True,'ref_no_status':True},auth=authTokenEditUser).json())
pp(requests.delete(api_url + '/manageTaxo', json={'cd_tax':newSpecies_cd_tax[1]}, auth=authTokenEditUser).json())

endpoint='/manageExot'

status1={'canonicalname':'Invented species',
  'is_alien': True,
  'is_invasive': False,
  'ref_citation':['Bottin et al, 2022. False paper to show an example','A second reference just for fun!'],
  'link':['https://colsplist.herokuapp.com',' '],
  'comments':'This is a first comment | Feeding habits: Does not eat at all!'}
res=requests.post(api_url+endpoint,json=status1,auth= authTokenEditUser)
pp(res.json())

res=requests.get(api_url+'/testExot',json={'canonicalname':'Invented species'})
pp(res.json())

status2={'canonicalname':'Newspecies nonexistens',
  'scientificname':'Newspecies nonexistens (marius 2022)',
  'authorship':'(marius 2022)',
  'parentcanonicalname':'Invented',
  'is_alien':False,
  'is_invasive':True,
  'ref_citation':['Bottin et al, 2022. False paper to show an example','A third reference just for fun!'],
  'link':['https://colsplist.herokuapp.com',' '],
  'comments':'random comment | repartition: nula'}
res=requests.post(api_url+endpoint,json=status2,auth= authTokenEditUser)
pp(res.json())


res=requests.get(api_url+'/testExot',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())

status4={'canonicalname':'Newspecies nonexistens',
  'is_alien':False,
  'is_invasive':False,
  'comments':'invasive evaluation methodology: None, this is only a fake species!',
  'ref_citation':['Bottin, 2025. New fake reference with a weird date'],
  'priority':'low',
  'replace_comment':False
}
pp(requests.post(api_url+'/manageExot',json=status4,auth=authTokenEditUser).json())

res=requests.get(api_url+'/testExot',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())

status5={'canonicalname':'Newspecies nonexistens',
  'is_alien':False,
  'is_invasive':False,
  'comments':'invasive evaluation methodology 2: None, this is still only a fake species!',
  'ref_citation':['Bottin, 2026. New fake reference with a weirder date'],
  'priority':'high',
  'replace_comment':True
}
pp(requests.post(api_url+'/manageExot',json=status5,auth=authTokenEditUser).json())

res=requests.get(api_url+'/testExot',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())

res=requests.get(api_url+'/testExot',json={'canonicalname':'Invented species'})
pp(res.json())
cd_tax=res.json().get('cd_tax_acc')

status6={'cd_tax':cd_tax,
  'is_alien':True,
  'is_invasive':True,
  'ref_citation':['Bottin, 2051. New fake reference with the weirdest date'],
}
pp(requests.put(api_url+'/manageExot',json=status6,auth=authTokenEditUser).json())

res=requests.get(api_url+'/testExot',json={'canonicalname':'Invented species'})
pp(res.json())

listRef=requests.get(api_url+'/listReferences').json()
cd_ref = [r['cd_ref'] for r in listRef if r['ref_citation']=='Bottin et al, 2022. False paper to show an example'][0]
pp(cd_ref)
cd_tax=requests.get(api_url+'/tax',json={'canonicalname':'Invented species'}).json()['cd_tax']
pp(cd_tax)

pp(requests.get(api_url+'/testExot',json={'canonicalname':'Invented species'}).json())

res=requests.delete(api_url+'/manageExot', json={'cd_tax':cd_tax,'cd_ref':cd_ref},auth=authTokenEditUser)
pp(res.json())

pp(requests.get(api_url+'/testExot',json={'canonicalname':'Invented species'}).json())

pp(requests.delete(api_url + '/manageExot',json={'cd_tax':cd_tax},auth=authTokenEditUser).json())

pp(requests.delete(api_url + '/manageExot',json={'cd_tax':cd_tax,'delete_status':True},auth=authTokenEditUser).json())

pp(requests.get(api_url+'/testExot',json={'canonicalname':'Invented species'}).json())

cd_tax_ToDel=requests.get(api_url + '/tax',json={'canonicalname':'Newspecies nonexistens'}).json().get('cd_tax')
requests.delete(api_url+'/manageTaxo',json={'cd_tax':cd_tax_ToDel},auth=authTokenEditUser)
cd_tax_StatusToDel=requests.get(api_url + '/testExot',json={'canonicalname':'Invented species'}).json().get('cd_tax')
res=requests.delete(api_url+'/manageExot',json={'cd_tax':cd_tax_StatusToDel, 'delete_status':True}, auth=authTokenEditUser)
res=requests.delete(api_url+'/cleanDb',json={'ref_no_status':True}, auth=authTokenEditUser)

statuses=[status1,status2,status4,status5]
pp(statuses)
res=requests.post(api_url + '/manageExot/list',json={'list':statuses},auth=authTokenEditUser)
pp(res.json())

newSpecies=requests.post(api_url+'/testExot/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json()
pp(newSpecies)
newSpecies_cd_tax=[n['cd_tax_acc'] for n in newSpecies]
modifications={'list':
  [
    {
      'cd_tax': newSpecies_cd_tax[0],
      'is_invasive':True,
      'is_alien':True,
      'ref_citation':['Fake report to put Invented species as invasive'],
      'link':['https://www.afalsesiteasanexample.com'],
      'comments': 'a comment as replacement',
      'replace_comment':True
    },
    {
      'cd_tax': newSpecies_cd_tax[1],
      'is_alien':True,
      'is_invasive': False,
      'ref_citation':['Another fake report'],
      'comments': 'a comment to add'
    }
  ]
}
pp(modifications)
modifs=requests.put(api_url + '/manageExot/list',json=modifications,auth=authTokenEditUser).json()
pp(modifs)
pp(requests.post(api_url+'/testExot/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())

pp(requests.post(api_url+'/testExot/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())
listRef=requests.get(api_url+'/listReferences').json()
cd_ref1 = [r['cd_ref'] for r in listRef if r['ref_citation']=='Bottin et al, 2022. False paper to show an example'][0]
cd_ref2 = [r['cd_ref'] for r in listRef if r['ref_citation']=='Fake report to put Invented species as invasive'][0]
deletions=[
  {'cd_tax':newSpecies_cd_tax[0],
  'cd_ref':cd_ref1},
  {'cd_tax':newSpecies_cd_tax[0],
  'cd_ref':cd_ref2},
  {'cd_tax':newSpecies_cd_tax[1],
  'delete_status':True}
]
pp(deletions)
pp(requests.delete(api_url + '/manageExot/list',json={'list':deletions},auth=authTokenEditUser).json())
pp(requests.post(api_url+'/testExot/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())

pp(requests.delete(api_url + '/cleanDb',json={'status_no_ref':True},auth=authTokenEditUser).json())
pp(requests.delete(api_url + '/manageTaxo', json={'cd_tax':newSpecies_cd_tax[1]}, auth=authTokenEditUser).json())

listRef=requests.get(api_url+'/listReferences').json()
refToModify=[r for r in listRef if r['ref_citation'] in ['A second reference just for fun!', 'A third reference just for fun!', 'Bottin et al, 2022. False paper to show an example']]
pp(refToModify)

pp(requests.put(api_url + '/manageRef', json={'cd_ref':refToModify[0]['cd_ref'],'reference':'New text for the ref'}, auth=authTokenEditUser).json())

pp(requests.put(api_url + '/manageRef', json={'cd_ref':refToModify[1]['cd_ref'],'link':'http://justanotherwebsite.com'}, auth=authTokenEditUser).json())

listRef=requests.get(api_url+'/listReferences').json()
cds_ref=[r['cd_ref'] for r in refToModify]
refModified=[r for r in listRef if r['cd_ref'] in cds_ref]
pp(refModified)

cd_ref=[r['cd_ref'] for r in refModified if r['ref_citation']=='New text for the ref'][0]
mergeInto=[r['cd_ref'] for r in refModified if r['ref_citation']=='A third reference just for fun!'][0]
pp(requests.delete(api_url + '/manageRef', json={'cd_ref':cd_ref,'mergeInto':mergeInto}, auth=authTokenEditUser).json())
listRef=requests.get(api_url+'/listReferences').json()
refModified=[r for r in listRef if r['cd_ref'] in cds_ref]
pp(refModified)

cd_ref=[r['cd_ref'] for r in refModified if r['ref_citation']=='Bottin et al, 2022. False paper to show an example'][0]
pp(requests.delete(api_url + '/manageRef', json={'cd_ref':cd_ref}, auth=authTokenEditUser).json())
listRef=requests.get(api_url+'/listReferences').json()
refModified=[r for r in listRef if r['cd_ref'] in cds_ref]
pp(refModified)

taxToSuppList=['Invented species','Juniperus communis','Vultur fossilis','Juniperus sabina']
taxToSupp=[{'canonicalname':r} for r in taxToSuppList]
res=requests.post(api_url+'/tax/list',json={'list':taxToSupp}).json()
cd_tax_supp=[{k:v for (k,v) in r.items() if k=='cd_tax'} for r in res]
pp(requests.delete(api_url+'/manageTaxo/list',json={'list':cd_tax_supp},auth=authTokenEditUser).json())
pp(requests.delete(api_url+'/cleanDb',json={'status_no_ref':True,'ref_no_status':True,
'syno_no_tax':True,'tax_no_status':True},auth=authTokenEditUser).json())

endpoint="/admin/users"
# Deleting the users created for this document
userToDel={'username':'editUser'}
res=requests.delete(api_url+endpoint,json=userToDel,auth=authAdmin)
pp(res.json())
endpoint="/user"
res=requests.put(api_url+endpoint,json={'newPassword':codeAdmin},auth=authTokenAdmin)
pp(res.json())

