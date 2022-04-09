Functionality tests and examples for the colSpListAPI: data management
================

-   [1 Before starting](#before-starting)
-   [2 Endpoint /manageTaxo](#endpoint-managetaxo)
    -   [2.1 POST](#post)
    -   [2.2 PUT](#put)
        -   [2.2.1 With gbifkey](#with-gbifkey)
        -   [2.2.2 With provided parameters](#with-provided-parameters)
    -   [2.3 DELETE](#delete)
-   [3 Finally : getting back to the previous
    state](#finally--getting-back-to-the-previous-state)

In this document, we will test the endpoints of the colSpList API which
allow to manage users and some specific administrative tasks.

------------------------------------------------------------------------

**Note**:

This document was created from a Rmarkdown document, with the output
format “github_document”. In order to use this type of file, please
install the packages *knitr* and *rmarkdown* in R.

1.  If you want to compile the document as a markdown document for
    github, while applying all the code contained in the file
    -   use `rmarkdown::render("file.Rmd")`
2.  The python script is extracted from the Rmd document using (in R):
    -   \`\`\`source “../../extra/extractPythonRmd.R”;
        extractPythonRmd(“file.Rmd”)

------------------------------------------------------------------------

``` python
import requests
from requests.auth import HTTPBasicAuth
from flask import jsonify
api_url="http://localhost:5000"
```

# 1 Before starting

In order to apply the code of this document, we will need to have access
to user management and administrative right. Since I cannot share here
the code for the admin user, I created a file called “codeAdmin” which
contains the code of the admin user. This file has been excluded from
the gitHub folder. In order to be able to show all the possibilities of
data management in this document, I will:

-   change the admin code for ‘temporaryAdminCode’
-   create a user with edition rights

Note that the following code is not part of the functionality tests, but
actually uses the same endpoints.

``` python
f=open("codeAdmin","r")
codeAdmin=f.readline().replace('\n','')
f.close()
endpoint="/user"
authAdmin=HTTPBasicAuth('admin',codeAdmin)
requests.put(api_url+endpoint,auth=authAdmin,json={'newPassword':'temporaryAdminCode'})
```

    ## <Response [401]>

``` python
authAdmin=HTTPBasicAuth('admin','temporaryAdminCode')
resToken=requests.get(api_url+endpoint,auth=authAdmin,json={'create_token':'True'})
content=resToken.json()
authTokenAdmin =HTTPBasicAuth(content.get('token'),'token')
# creation user with edit right
res = requests.post(api_url+endpoint,json={'username':'editUser','password':'tempCode2'})
res.json()
# grant edit to editUser
```

    ## {'error': 'username editUser already exists in the database'}

``` python
endpoint = "/admin/users"
res=requests.put(api_url+endpoint,json={'username':'editUser','grant_edit':'True'},auth=authTokenAdmin)
res.json()
# Getting the tokens for these new users:
```

    ## {'error': 'Attempt to grant existing right: user editUser already has edit rights'}

``` python
endpoint="/user"
authEditUser=HTTPBasicAuth('editUser','tempCode2')
res= requests.get(api_url+endpoint,json={'create_token':'True'},auth=authEditUser)
content=res.json()
authTokenEditUser=HTTPBasicAuth(content.get('token'),'token')
```

# 2 Endpoint /manageTaxo

The endpoint ‘/manageTaxo’ allows to add (POST), suppress (DELETE) or
modify (PUT) taxonomic information in the database.

``` python
endpoint="/manageTaxo"
```

## 2.1 POST

In most of the case, sending only the canonical name of the taxa will be
sufficient to insert a new taxon:

``` python
newTax1={'canonicalname':'Abies grandis'}
res=requests.post(api_url+endpoint,json=newTax1,auth=authTokenEditUser)
res.json()
```

    ## {'cd_tax': 3771, 'cd_tax_acc': 3771, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Abies grandis', 'acceptedname': 'Abies grandis (Douglas ex D.Don) Lindl.', 'gbifkey': 2685361, 'syno': False, 'insertedTax': []}

The API send back all the informations from the database or the GBIF
API, and the “insertedTax” part of the results shows which taxa were
inserted.

It might be important to look at the “matchedname”, to be sure that the
inserted taxon is the one we wanted to insert.

If the species we want to insert already exists in the database, here
are what the results look like:

``` python
newTax2={'canonicalname':'Vultur gryphus'}
res=requests.post(api_url+endpoint,json=newTax2,auth=authTokenEditUser)
res.json()
```

    ## {'cd_tax': 3600, 'cd_tax_acc': 3600, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Vultur gryphus', 'acceptedname': 'Vultur gryphus Linnaeus, 1758', 'gbifkey': 2481907, 'syno': False, 'insertedTax': []}

You may also insert taxa from their key in the gbif database, or their
scientificName (with author):

``` python
newTax3={'gbifkey':7963890}
res=requests.post(api_url+endpoint,json=newTax3,auth=authTokenEditUser)
res.json()
```

    ## {'cd_tax': 3764, 'cd_tax_acc': 3764, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Juniperus sabina L.', 'acceptedname': 'Juniperus sabina L.', 'gbifkey': 7963890, 'syno': False, 'insertedTax': []}

``` python
newTax4={'scientificname':'Juniperus thurifera'}
res=requests.post(api_url+endpoint,json=newTax4,auth=authTokenEditUser)
res.json()
```

    ## {'cd_tax': 3766, 'cd_tax_acc': 3766, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Juniperus thurifera L.', 'acceptedname': 'Juniperus thurifera L.', 'gbifkey': 2684528, 'syno': False, 'insertedTax': []}

Sometimes, the taxa found by the gbif may be problematic:

``` python
newTax5={'canonicalname':'Vultur fossilis'}
res=requests.post(api_url+endpoint,json=newTax5,auth=authTokenEditUser)
res.json()
```

    ## {'cd_tax': 3767, 'cd_tax_acc': 3767, 'alreadyInDb': True, 'foundGbif': False, 'matchedname': 'Vultur fossilis', 'acceptedname': 'Vultur fossilis', 'gbifkey': None, 'syno': False, 'insertedTax': []}

As you can see the GBIF API does not find the species, which is a
doubtfuk synonym for the condor ‘Vultur gryphus’, hence, it matches it
with the genus. To avoid these problem, you might want to set the
‘min_conf_gbif’ parameter to a higher value:

``` python
newTax5={'canonicalname':'Vultur fossilis','min_gbif_conf':98}
res=requests.post(api_url+endpoint,json=newTax5,auth=authTokenEditUser)
res.json()
```

    ## {'cd_tax': 3767, 'cd_tax_acc': 3767, 'alreadyInDb': True, 'foundGbif': False, 'matchedname': 'Vultur fossilis', 'acceptedname': 'Vultur fossilis', 'gbifkey': None, 'syno': False, 'insertedTax': []}

The problem here is that it actually inserted the taxon without
extracting the information from gbif. Here is what looks ‘Vultur
fossilis’ in the database:

``` python
res=requests.get(api_url+'/tax',json={'canonicalname':'Vultur fossilis'})
res.json()
```

    ## {'cd_tax': 3767, 'scientificname': 'Vultur fossilis', 'canonicalname': 'Vultur fossilis', 'authorship': None, 'tax_rank': 'SP', 'cd_parent': 3599, 'parentname': 'Vultur Linnaeus, 1758', 'cd_accepted': 3767, 'acceptedname': 'Vultur fossilis', 'status': 'DOUBTFUL', 'gbifkey': None, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}

It inserted the taxon with the status ‘DOUBTFUL’, but it inserted it
anyway! A good practise would be to revise regularly the taxonomic data
(<https://colsplist.herokuapp.com/listTax?format=CSV>) and particularly
all the ‘DOUBTFUL’ taxa.

Another way to avoid matching in gbif is to use the parameter ‘no_gbif’
in the function.

``` python
newTax6={'canonicalname':'Juniperus communis','no_gbif':True}
res=requests.post(api_url+endpoint,json=newTax6,auth=authTokenEditUser)
res.json()
```

    ## {'cd_tax': 3765, 'cd_tax_acc': 3765, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Juniperus communis', 'acceptedname': 'Juniperus communis L.', 'gbifkey': 2684709, 'syno': False, 'insertedTax': []}

Until here we used the functions with very few parameters, but if you
want to insert a taxon which has no close parent in the database and is
not found in gbif, you might need to use more parameters.

Let’s imagine a virtual taxon that we invent for the current
demonstration:

The species ‘Invented species’ is from the genus ‘Invented’, which is
part of the family ‘Fabaceae’, already in the database:

If we simply send the ‘Invented species’ to the API, here is what
happens:

``` python
newTax8 = {'canonicalname':'Invented species'}
res=requests.post(api_url+endpoint,json=newTax8,auth=authTokenEditUser)
res.json()
```

    ## {'cd_tax': 3769, 'cd_tax_acc': 3769, 'alreadyInDb': True, 'foundGbif': False, 'matchedname': 'Invented species', 'acceptedname': 'Invented species (marius, 2022)', 'gbifkey': None, 'syno': False, 'insertedTax': []}

As you can see, the parent taxon is not found in the database, which is
what we would have expected… Therefore, we need to insert the parent
taxon first, and then to insert the taxon, which will automatically be
assigned to the right genus. In order to make things right, we should
give a maximum amount of informations to the API:

``` python
newTax7={'canonicalname':'Invented','scientificname':'Invented (marius, 2022)','authorship':'(marius, 2022)','parentcanonicalname':'Fabaceae','syno':False,'rank':'GENUS','no_gbif':True}
res=requests.post(api_url+endpoint,json=newTax7,auth=authTokenEditUser)
res.json()
```

    ## {'cd_tax': 3768, 'cd_tax_acc': 3768, 'alreadyInDb': True, 'foundGbif': False, 'matchedname': 'Invented (marius, 2022)', 'acceptedname': 'Invented (marius, 2022)', 'gbifkey': None, 'syno': False, 'insertedTax': []}

``` python
parentId=res.json().get('cd_tax')
```

Now we insert the taxon with:

``` python
newTax8={'canonicalname':'Invented species','scientificname':'Invented species (marius, 2022)','authorship':'(marius, 2022)','parentcanonicalname':'Invented','syno':False,'rank':'SPECIES','no_gbif':True}
res=requests.post(api_url+endpoint,json=newTax8,auth=authTokenEditUser)
res.json()
```

    ## {'cd_tax': 3769, 'cd_tax_acc': 3769, 'alreadyInDb': True, 'foundGbif': False, 'matchedname': 'Invented species (marius, 2022)', 'acceptedname': 'Invented species (marius, 2022)', 'gbifkey': None, 'syno': False, 'insertedTax': []}

``` python
taxId=res.json().get('cd_tax')
```

Now we can see what are these new taxa like in the database:

``` python
res=requests.get(api_url+'/tax',json={'cd_tax':parentId})
res.json()
```

    ## {'cd_tax': 3768, 'scientificname': 'Invented (marius, 2022)', 'canonicalname': 'Invented', 'authorship': '(marius, 2022)', 'tax_rank': 'GN', 'cd_parent': 5, 'parentname': 'Fabaceae', 'cd_accepted': 3768, 'acceptedname': 'Invented (marius, 2022)', 'status': 'DOUBTFUL', 'gbifkey': None, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}

``` python
res=requests.get(api_url+'/tax',json={'cd_tax':taxId})
res.json()
```

    ## {'cd_tax': 3769, 'scientificname': 'Invented species (marius, 2022)', 'canonicalname': 'Invented species', 'authorship': '(marius, 2022)', 'tax_rank': 'SP', 'cd_parent': 3768, 'parentname': 'Invented (marius, 2022)', 'cd_accepted': 3769, 'acceptedname': 'Invented species (marius, 2022)', 'status': 'DOUBTFUL', 'gbifkey': None, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}

## 2.2 PUT

The PUT method allows to modify a taxon which is already in the database

### 2.2.1 With gbifkey

The easiest way to use this method is to provide a gbifkey, so the taxon
designated by the cd_tax is modified to become exactly like the taxon
referred by the gbifkey.

For example, we inserted the taxon *Juniperus communis* without using
GBIF, with the no_gbif option. When we look at the taxon in the
database, here is what we obtain:

``` python
res=requests.get(api_url+'/tax',json={'canonicalname':'Juniperus communis'})
res.json()
```

    ## {'cd_tax': 3765, 'scientificname': 'Juniperus communis L.', 'canonicalname': 'Juniperus communis', 'authorship': 'L.', 'tax_rank': 'SP', 'cd_parent': 3763, 'parentname': 'Juniperus L.', 'cd_accepted': 3765, 'acceptedname': 'Juniperus communis L.', 'status': 'ACCEPTED', 'gbifkey': 2684709, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}

``` python
modified1={'cd_tax':res.json().get('cd_tax')}
```

But this taxon is actually present in GBIF with more accurate
information. In order to modify the taxon, you just have to use the
following code:

``` python
modified1['gbifkey']=2684709
res=requests.put(api_url+endpoint, json=modified1, auth=authTokenEditUser)
```

Now, the taxon has this information:

``` python
res=requests.get(api_url+'/tax',json={'canonicalname':'Juniperus communis'})
res.json()
```

    ## {'cd_tax': 3765, 'scientificname': 'Juniperus communis L.', 'canonicalname': 'Juniperus communis', 'authorship': 'L.', 'tax_rank': 'SP', 'cd_parent': 3763, 'parentname': 'Juniperus L.', 'cd_accepted': 3765, 'acceptedname': 'Juniperus communis L.', 'status': 'ACCEPTED', 'gbifkey': 2684709, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}

As you can see, the cd_tax is the same as before (which avoids problems
in case the taxon has a status, but the information is now more
complete)

### 2.2.2 With provided parameters

## 2.3 DELETE

The DELETE method allows the user to delete a taxon and all its statuses
in the database

If we want to delete, say the taxon ‘Abies grandis’ which we inserted
before it is done by first, finding its code in the database, and then
the DELETE method.

``` python
res=requests.get(api_url+'/tax',json={'canonicalname': 'Abies grandis'})
res.json()
```

    ## {'cd_tax': 3771, 'scientificname': 'Abies grandis (Douglas ex D.Don) Lindl.', 'canonicalname': 'Abies grandis', 'authorship': '(Douglas ex D.Don) Lindl.', 'tax_rank': 'SP', 'cd_parent': 3761, 'parentname': 'Abies Mill.', 'cd_accepted': 3771, 'acceptedname': 'Abies grandis (Douglas ex D.Don) Lindl.', 'status': 'ACCEPTED', 'gbifkey': 2685361, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}

``` python
del1={'cd_tax':res.json().get('cd_tax')}
res=requests.delete(api_url+endpoint,json=del1,auth=authTokenEditUser)
res.json()
```

    ## {'cd_tax': 3771, 'cd_children': [3771], 'cd_synos': []}

As you can see the API returns the synonyms and children cd_tax, so that
you can avoid problematic taxa kept in the database.

# 3 Finally : getting back to the previous state

Here, I will delete the users that were created for this document and
give back the previous password to the ‘admin’ user:

``` python
endpoint="/admin/users"
# Deleting the users created for this document
userToDel={'username':'editUser'}
res=requests.delete(api_url+endpoint,json=userToDel,auth=authAdmin)
res.json()
```

    ## {'uid': 43, 'username': 'editUser'}

``` python
endpoint="/user"
res=requests.put(api_url+endpoint,json={'newPassword':codeAdmin},auth=authTokenAdmin)
res.json()
```

    ## 3
