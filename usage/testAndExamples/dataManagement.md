Functionality tests and examples for the colSpListAPI: data management
================

-   [Before starting](#before-starting)
-   [Endpoint /manageTaxo](#endpoint-managetaxo)
    -   [POST](#post)
    -   [PUT](#put)
        -   [With gbifkey](#with-gbifkey)
        -   [With provided parameters](#with-provided-parameters)
    -   [DELETE](#delete)
-   [endpoint /manageTaxo/list : for multiple
    taxa](#endpoint-managetaxolist--for-multiple-taxa)
    -   [POST](#post-1)
    -   [DELETE](#delete-1)
    -   [PUT](#put-1)
-   [Managing the statuses](#managing-the-statuses)
    -   [Endpoint /ManageEndem](#endpoint-manageendem)
        -   [POST: adding endemic species and/or the associated
            bibliographic
            references](#post-adding-endemic-species-andor-the-associated-bibliographic-references)
        -   [PUT: modify a status](#put-modify-a-status)
        -   [DELETE: suppress a reference associated with a status, or
            the status
            itself](#delete-suppress-a-reference-associated-with-a-status-or-the-status-itself)
        -   [Cleaning](#cleaning)
    -   [Endpoint /manageEndem/list](#endpoint-manageendemlist)
        -   [POST](#post-2)
        -   [PUT](#put-2)
        -   [DELETE](#delete-2)
        -   [Cleaning](#cleaning-1)
    -   [Endpoint /ManageThreat](#endpoint-managethreat)
        -   [POST: adding threatened species and/or the associated
            bibliographic
            references](#post-adding-threatened-species-andor-the-associated-bibliographic-references)
        -   [PUT: modify a status](#put-modify-a-status-1)
        -   [DELETE: suppress a reference associated with a status, or
            the status
            itself](#delete-suppress-a-reference-associated-with-a-status-or-the-status-itself-1)
        -   [Cleaning](#cleaning-2)
    -   [Endpoint /manageThreat/list](#endpoint-managethreatlist)
        -   [POST](#post-3)
        -   [PUT](#put-3)
        -   [DELETE](#delete-3)
        -   [Cleaning](#cleaning-3)
    -   [Endpoint /ManageExot](#endpoint-manageexot)
        -   [POST: adding alien-invasive species and/or the associated
            bibliographic
            references](#post-adding-alien-invasive-species-andor-the-associated-bibliographic-references)
        -   [PUT: modify a status](#put-modify-a-status-2)
        -   [DELETE: suppress a reference associated with a status, or
            the status
            itself](#delete-suppress-a-reference-associated-with-a-status-or-the-status-itself-2)
        -   [Cleaning](#cleaning-4)
    -   [Endpoint /manageExot/list](#endpoint-manageexotlist)
        -   [POST](#post-4)
        -   [PUT](#put-4)
        -   [DELETE](#delete-4)
        -   [Cleaning](#cleaning-5)
-   [Endpoint /manageRef : modifying and supressing
    references](#endpoint-manageref--modifying-and-supressing-references)
    -   [PUT:modifying the references](#putmodifying-the-references)
    -   [DELETE: merging and/or deleting the
        references](#delete-merging-andor-deleting-the-references)
-   [Finally : getting back to the previous
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
    -   \``source "../../extra/extractPythonRmd.R"; extractPythonRmd("file.Rmd")`

------------------------------------------------------------------------

``` python
import requests
from requests.auth import HTTPBasicAuth
from flask import jsonify
from pprint import pprint as pp
api_url="https://colsplist.herokuapp.com"
```

# Before starting

In order to apply the code of this document, we will need to have access
to user management and administrative right. Since I cannot share here
the code for the admin user, I created a file called “codeAdmin” which
contains the code of the admin user. This file has been excluded from
the gitHub folder. In order to be able to show all the possibilities of
data management in this document, I will:

-   change the admin code for ‘temporaryAdminCode’
-   create a user with edition rights

Note that the following code is not part of the functionality tests
concerning data management.

``` python
f=open("codeAdmin","r")
codeAdmin=f.readline().replace('\n','')
f.close()
authAdmin=HTTPBasicAuth('admin',codeAdmin)
requests.put(api_url+'/user',auth=authAdmin,json={'newPassword':'temporaryAdminCode'})
```

    ## <Response [200]>

``` python
authAdmin=HTTPBasicAuth('admin','temporaryAdminCode')
resToken=requests.get(api_url+'/user',auth=authAdmin,json={'create_token':'True'})
content=resToken.json()
authTokenAdmin =HTTPBasicAuth(content.get('token'),'token')
# creation user with edit right
res = requests.post(api_url+'/user',json={'username':'editUser','password':'tempCode2'})
pp(res.json())
# grant edit to editUser
```

    ## {'uid': 24, 'username': 'editUser'}

``` python
res=requests.put(api_url+'/admin/users',json={'username':'editUser','grant_edit':'True'},auth=authTokenAdmin)
pp(res.json())
# Getting the tokens for these new users:
```

    ## {'grant_admin': None,
    ##  'grant_edit': 24,
    ##  'grant_user': None,
    ##  'newPassword': None,
    ##  'revoke_admin': None,
    ##  'revoke_edit': None,
    ##  'revoke_user': None}

``` python
authEditUser=HTTPBasicAuth('editUser','tempCode2')
res= requests.get(api_url+'/user',json={'create_token':'True'},auth=authEditUser)
content=res.json()
authTokenEditUser=HTTPBasicAuth(content.get('token'),'token')
```

# Endpoint /manageTaxo

The endpoint ‘/manageTaxo’ allows to add (POST), suppress (DELETE) or
modify (PUT) taxonomic information in the database.

``` python
endpoint="/manageTaxo"
```

## POST

In most of the case, sending only the canonical name of the taxa will be
sufficient to insert a new taxon:

``` python
newTax1={'canonicalname':'Abies grandis'}
res=requests.post(api_url+endpoint,json=newTax1,auth=authTokenEditUser)
pp(res.json())
```

    ## {'acceptedname': 'Abies grandis (Douglas ex D.Don) Lindl.',
    ##  'alreadyInDb': False,
    ##  'cd_tax': 3816,
    ##  'cd_tax_acc': 3816,
    ##  'foundGbif': True,
    ##  'gbifkey': 2685361,
    ##  'insertedTax': [3815, 3816],
    ##  'matchedname': 'Abies grandis',
    ##  'syno': False}

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
pp(res.json())
```

    ## {'acceptedname': 'Vultur gryphus Linnaeus, 1758',
    ##  'alreadyInDb': True,
    ##  'cd_tax': 3600,
    ##  'cd_tax_acc': 3600,
    ##  'foundGbif': True,
    ##  'gbifkey': 2481907,
    ##  'insertedTax': [],
    ##  'matchedname': 'Vultur gryphus',
    ##  'syno': False}

You may also insert taxa from their key in the gbif database, or their
scientificName (with author):

``` python
newTax3={'gbifkey':7963890}
res=requests.post(api_url+endpoint,json=newTax3,auth=authTokenEditUser)
pp(res.json())
```

    ## {'acceptedname': 'Juniperus sabina L.',
    ##  'alreadyInDb': False,
    ##  'cd_tax': 3818,
    ##  'cd_tax_acc': 3818,
    ##  'foundGbif': True,
    ##  'gbifkey': 7963890,
    ##  'insertedTax': [3817, 3818],
    ##  'matchedname': 'Juniperus sabina L.',
    ##  'syno': False}

``` python
newTax4={'scientificname':'Juniperus thurifera'}
res=requests.post(api_url+endpoint,json=newTax4,auth=authTokenEditUser)
pp(res.json())
```

    ## {'acceptedname': 'Juniperus thurifera L.',
    ##  'alreadyInDb': False,
    ##  'cd_tax': 3819,
    ##  'cd_tax_acc': 3819,
    ##  'foundGbif': True,
    ##  'gbifkey': 2684528,
    ##  'insertedTax': [3819],
    ##  'matchedname': 'Juniperus thurifera L.',
    ##  'syno': False}

Sometimes, the taxa found through the gbif API may be problematic:

``` python
newTax5={'canonicalname':'Vultur fossilis'}
res=requests.post(api_url+endpoint,json=newTax5,auth=authTokenEditUser)
pp(res.json())
```

    ## {'acceptedname': 'Vultur Linnaeus, 1758',
    ##  'alreadyInDb': True,
    ##  'cd_tax': 3599,
    ##  'cd_tax_acc': 3599,
    ##  'foundGbif': True,
    ##  'gbifkey': 2481906,
    ##  'insertedTax': [],
    ##  'matchedname': 'Vultur',
    ##  'syno': False}

As you can see the GBIF API does not find the species, which is a
doubtful synonym for the condor ‘Vultur gryphus’, hence, it matches it
with the genus. To avoid these problem, you might want to set the
‘min_conf_gbif’ parameter to a higher value:

``` python
newTax5={'canonicalname':'Vultur fossilis','min_gbif_conf':98}
res=requests.post(api_url+endpoint,json=newTax5,auth=authTokenEditUser)
pp(res.json())
```

    ## {'acceptedname': None,
    ##  'alreadyInDb': False,
    ##  'cd_tax': 3820,
    ##  'cd_tax_acc': 3820,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [3820],
    ##  'matchedname': None,
    ##  'syno': False}

The problem here is that it actually inserted the taxon without
extracting the information from gbif. Here is what looks ‘Vultur
fossilis’ in the database:

``` python
res=requests.get(api_url+'/tax',json={'canonicalname':'Vultur fossilis'})
pp(res.json())
```

    ## {'acceptedname': 'Vultur fossilis',
    ##  'authorship': None,
    ##  'canonicalname': 'Vultur fossilis',
    ##  'cd_accepted': 3820,
    ##  'cd_parent': 3599,
    ##  'cd_tax': 3820,
    ##  'gbifkey': None,
    ##  'hasendemstatus': False,
    ##  'hasexotstatus': False,
    ##  'hasthreatstatus': False,
    ##  'parentname': 'Vultur Linnaeus, 1758',
    ##  'scientificname': 'Vultur fossilis',
    ##  'status': 'DOUBTFUL',
    ##  'synonyms': [None],
    ##  'tax_rank': 'SP'}

It inserted the taxon with the status ‘DOUBTFUL’, but it inserted it
anyway! A good practise would be to revise regularly the taxonomic data
(<https://colsplist.herokuapp.com/listTax?format=CSV>) and particularly
all the ‘DOUBTFUL’ taxa.

Another way to avoid matching in gbif is to use the parameter ‘no_gbif’
in the function.

``` python
newTax6={'canonicalname':'Juniperus communis','no_gbif':True}
res=requests.post(api_url+endpoint,json=newTax6,auth=authTokenEditUser)
pp(res.json())
```

    ## {'acceptedname': None,
    ##  'alreadyInDb': False,
    ##  'cd_tax': 3821,
    ##  'cd_tax_acc': 3821,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [3821],
    ##  'matchedname': None,
    ##  'syno': False}

Until now we used the functions with very few parameters, but if you
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
pp(res.json())
```

    ## {'error': 'Parent taxon not found in GBIF, missing argument: '
    ##           "'parentcanonicalname' or 'parentscientificname' or 'parentgbifkey'"}

As you can see, the parent taxon is not found which is what we would
have expected… Therefore, we need to insert the parent taxon first, and
then to insert the taxon, which will automatically be assigned to the
right genus. In order to make things right, we should give a maximum
amount of informations to the API:

``` python
newTax7={'canonicalname':'Invented','scientificname':'Invented (marius, 2022)','authorship':'(marius, 2022)','parentcanonicalname':'Fabaceae','syno':False,'rank':'GENUS','no_gbif':True}
res=requests.post(api_url+endpoint,json=newTax7,auth=authTokenEditUser)
pp(res.json())
```

    ## {'acceptedname': None,
    ##  'alreadyInDb': False,
    ##  'cd_tax': 3822,
    ##  'cd_tax_acc': 3822,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [3822],
    ##  'matchedname': None,
    ##  'syno': False}

``` python
parentId=res.json().get('cd_tax')
```

Now we insert the taxon with:

``` python
newTax8={'canonicalname':'Invented species','scientificname':'Invented species (marius, 2022)','authorship':'(marius, 2022)','parentcanonicalname':'Invented','syno':False,'rank':'SPECIES','no_gbif':True}
res=requests.post(api_url+endpoint,json=newTax8,auth=authTokenEditUser)
pp(res.json())
```

    ## {'acceptedname': None,
    ##  'alreadyInDb': False,
    ##  'cd_tax': 3823,
    ##  'cd_tax_acc': 3823,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [3823],
    ##  'matchedname': None,
    ##  'syno': False}

``` python
taxId=res.json().get('cd_tax')
```

Now we can see what are these new taxa like in the database:

``` python
res=requests.get(api_url+'/tax',json={'cd_tax':parentId})
pp(res.json())
```

    ## {'acceptedname': 'Invented (marius, 2022)',
    ##  'authorship': '(marius, 2022)',
    ##  'canonicalname': 'Invented',
    ##  'cd_accepted': 3822,
    ##  'cd_parent': 5,
    ##  'cd_tax': 3822,
    ##  'gbifkey': None,
    ##  'hasendemstatus': False,
    ##  'hasexotstatus': False,
    ##  'hasthreatstatus': False,
    ##  'parentname': 'Fabaceae',
    ##  'scientificname': 'Invented (marius, 2022)',
    ##  'status': 'DOUBTFUL',
    ##  'synonyms': [None],
    ##  'tax_rank': 'GN'}

``` python
res=requests.get(api_url+'/tax',json={'cd_tax':taxId})
pp(res.json())
```

    ## {'acceptedname': 'Invented species (marius, 2022)',
    ##  'authorship': '(marius, 2022)',
    ##  'canonicalname': 'Invented species',
    ##  'cd_accepted': 3823,
    ##  'cd_parent': 3822,
    ##  'cd_tax': 3823,
    ##  'gbifkey': None,
    ##  'hasendemstatus': False,
    ##  'hasexotstatus': False,
    ##  'hasthreatstatus': False,
    ##  'parentname': 'Invented (marius, 2022)',
    ##  'scientificname': 'Invented species (marius, 2022)',
    ##  'status': 'DOUBTFUL',
    ##  'synonyms': [None],
    ##  'tax_rank': 'SP'}

## PUT

The PUT method allows to modify a taxon which is already in the database

### With gbifkey

The easiest way to use this method is to provide a gbifkey, so the taxon
designated by the cd_tax is modified to become exactly like the taxon
referred by the gbifkey.

For example, we inserted the taxon *Juniperus communis* without using
GBIF, with the no_gbif option. When we look at the taxon in the
database, here is what we obtain:

``` python
res=requests.get(api_url+'/tax',json={'canonicalname':'Juniperus communis'})
pp(res.json())
```

    ## {'acceptedname': 'Juniperus communis',
    ##  'authorship': None,
    ##  'canonicalname': 'Juniperus communis',
    ##  'cd_accepted': 3821,
    ##  'cd_parent': 3817,
    ##  'cd_tax': 3821,
    ##  'gbifkey': None,
    ##  'hasendemstatus': False,
    ##  'hasexotstatus': False,
    ##  'hasthreatstatus': False,
    ##  'parentname': 'Juniperus L.',
    ##  'scientificname': 'Juniperus communis',
    ##  'status': 'DOUBTFUL',
    ##  'synonyms': [None],
    ##  'tax_rank': 'SP'}

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
pp(res.json())
```

    ## {'acceptedname': 'Juniperus communis L.',
    ##  'authorship': 'L.',
    ##  'canonicalname': 'Juniperus communis',
    ##  'cd_accepted': 3821,
    ##  'cd_parent': 3817,
    ##  'cd_tax': 3821,
    ##  'gbifkey': 2684709,
    ##  'hasendemstatus': False,
    ##  'hasexotstatus': False,
    ##  'hasthreatstatus': False,
    ##  'parentname': 'Juniperus L.',
    ##  'scientificname': 'Juniperus communis L.',
    ##  'status': 'ACCEPTED',
    ##  'synonyms': [None],
    ##  'tax_rank': 'SP'}

As you can see, the cd_tax is the same as before (which avoids problems
in case the taxon has a status, but the information is now more
complete)

### With provided parameters

Let’s go back to the taxon that we invented “Invented species”:

``` python
res=requests.get(api_url+'/tax',json={'canonicalname':'Invented species'})
pp(res.json())
```

    ## {'acceptedname': 'Invented species (marius, 2022)',
    ##  'authorship': '(marius, 2022)',
    ##  'canonicalname': 'Invented species',
    ##  'cd_accepted': 3823,
    ##  'cd_parent': 3822,
    ##  'cd_tax': 3823,
    ##  'gbifkey': None,
    ##  'hasendemstatus': False,
    ##  'hasexotstatus': False,
    ##  'hasthreatstatus': False,
    ##  'parentname': 'Invented (marius, 2022)',
    ##  'scientificname': 'Invented species (marius, 2022)',
    ##  'status': 'DOUBTFUL',
    ##  'synonyms': [None],
    ##  'tax_rank': 'SP'}

``` python
modified2Id = res.json().get('cd_tax')
```

Modifying its authorship and scientificname may be done by:

``` python
modified2={'cd_tax':modified2Id,'authorship':'(marius 2005)','scientificname':'Invented species (marius 2005)'}
res=requests.put(api_url+endpoint, json=modified2, auth=authTokenEditUser)
pp(res.json())
```

    ## {'cd_tax': 3823, 'insertedTax': []}

``` python
res=requests.get(api_url+'/tax',json={'canonicalname':'Invented species'})
pp(res.json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'authorship': '(marius 2005)',
    ##  'canonicalname': 'Invented species',
    ##  'cd_accepted': 3823,
    ##  'cd_parent': 3822,
    ##  'cd_tax': 3823,
    ##  'gbifkey': None,
    ##  'hasendemstatus': False,
    ##  'hasexotstatus': False,
    ##  'hasthreatstatus': False,
    ##  'parentname': 'Invented (marius, 2022)',
    ##  'scientificname': 'Invented species (marius 2005)',
    ##  'status': 'DOUBTFUL',
    ##  'synonyms': [None],
    ##  'tax_rank': 'SP'}

``` python
modified2Id = res.json().get('cd_tax')
```

As you can see the year associated with the authorship has been changed,
you may as well use the parameters:

-   canonicalname: changes the canonicalName of the taxon
-   syno: change the synonym status of the taxon
-   rank : change the rank of the taxon (the safest way to write the
    rank is “SPECIES”, “FAMILY”,“VARIETY” etc.)
-   parentgbifkey,parentcanonicalname, parentscientificname: change the
    parent taxon, if the taxon is not present in the database, search
    for it in the gbif API, and inserts it. Note that if you do not want
    to use GBIF for the parent taxa, you will have to modify or insert
    the parents (with POST) one by one
-   synogbifkey, synocanonicalname, and synoscientificname: search for
    the accepted name in the GBIF API if it does not exist in the
    database, inserts it and use it to consider cd_tax as a synonym to
    the acceptedname. Note that if you do not want to pass by the GBIF
    API, you will have to enter the accepted taxon with the POST method
    and the ‘no_gbif’ option

## DELETE

The DELETE method allows the user to delete a taxon and all its statuses
in the database

If we want to delete, say the taxon ‘Abies grandis’ which we inserted
before it is done by first, finding its code in the database, and then
the DELETE method.

``` python
res=requests.get(api_url+'/tax',json={'canonicalname': 'Abies grandis'})
pp(res.json())
```

    ## {'acceptedname': 'Abies grandis (Douglas ex D.Don) Lindl.',
    ##  'authorship': '(Douglas ex D.Don) Lindl.',
    ##  'canonicalname': 'Abies grandis',
    ##  'cd_accepted': 3816,
    ##  'cd_parent': 3815,
    ##  'cd_tax': 3816,
    ##  'gbifkey': 2685361,
    ##  'hasendemstatus': False,
    ##  'hasexotstatus': False,
    ##  'hasthreatstatus': False,
    ##  'parentname': 'Abies Mill.',
    ##  'scientificname': 'Abies grandis (Douglas ex D.Don) Lindl.',
    ##  'status': 'ACCEPTED',
    ##  'synonyms': [None],
    ##  'tax_rank': 'SP'}

``` python
del1={'cd_tax':res.json().get('cd_tax')}
res=requests.delete(api_url+endpoint,json=del1,auth=authTokenEditUser)
pp(res.json())
```

    ## {'cd_children': [3816], 'cd_synos': [], 'cd_tax': 3816}

As you can see the API returns the synonyms and children cd_tax, so that
you can avoid problematic taxa kept in the database.

Note that the statuses of the deleted species will also be deleted (as a
“ON DELETE CASCADE” process in the postgres database, so the information
will be lost… proceed with caution!)

# endpoint /manageTaxo/list : for multiple taxa

This endpoints work the same than the previous one, except that the json
dictionaries presented before as argument have to be encapsuled in a
“list” element of a JSON dictionary, which may contain many taxa.

In order to run the examples presented before again, I will first
supress the taxa using the “/cleanDb” endpoint. Since the inserted taxa
have no status, the ‘tax_no_status’ argument should be sufficient to get
rid of all the newly inserted taxa (More information on
<https://github.com/marbotte/colSpList/blob/main/usage/testAndExamples/userManagementAdministration.md#cleandb>)

``` python
res=requests.delete(api_url+'/cleanDb',json={'tax_no_status':True},auth=authTokenEditUser)
pp(res.json())
```

    ## {'cd_refs': [],
    ##  'cd_status': [],
    ##  'cd_taxs': [3817, 3815, 3822, 3818, 3819, 3823, 3820, 3821]}

``` python
endpoint='/manageTaxo/list'
```

## POST

You may send all the previous taxon in one only batch using the
following dictionary:

``` python
multiNewTax={'list':[newTax1,newTax2,newTax3,newTax4,newTax5,newTax6,newTax7,newTax8]}
pp(multiNewTax)
```

    ## {'list': [{'canonicalname': 'Abies grandis'},
    ##           {'canonicalname': 'Vultur gryphus'},
    ##           {'gbifkey': 7963890},
    ##           {'scientificname': 'Juniperus thurifera'},
    ##           {'canonicalname': 'Vultur fossilis', 'min_gbif_conf': 98},
    ##           {'canonicalname': 'Juniperus communis', 'no_gbif': True},
    ##           {'authorship': '(marius, 2022)',
    ##            'canonicalname': 'Invented',
    ##            'no_gbif': True,
    ##            'parentcanonicalname': 'Fabaceae',
    ##            'rank': 'GENUS',
    ##            'scientificname': 'Invented (marius, 2022)',
    ##            'syno': False},
    ##           {'authorship': '(marius, 2022)',
    ##            'canonicalname': 'Invented species',
    ##            'no_gbif': True,
    ##            'parentcanonicalname': 'Invented',
    ##            'rank': 'SPECIES',
    ##            'scientificname': 'Invented species (marius, 2022)',
    ##            'syno': False}]}

``` python
res=requests.post(api_url+endpoint,json=multiNewTax,auth=authTokenEditUser)
pp(res.json())
```

    ## [{'acceptedname': 'Abies grandis (Douglas ex D.Don) Lindl.',
    ##   'alreadyInDb': False,
    ##   'cd_tax': 3826,
    ##   'cd_tax_acc': 3826,
    ##   'foundGbif': True,
    ##   'gbifkey': 2685361,
    ##   'insertedTax': [3825, 3826],
    ##   'matchedname': 'Abies grandis',
    ##   'syno': False},
    ##  {'acceptedname': 'Vultur gryphus Linnaeus, 1758',
    ##   'alreadyInDb': True,
    ##   'cd_tax': 3600,
    ##   'cd_tax_acc': 3600,
    ##   'foundGbif': True,
    ##   'gbifkey': 2481907,
    ##   'insertedTax': [],
    ##   'matchedname': 'Vultur gryphus',
    ##   'syno': False},
    ##  {'acceptedname': 'Juniperus sabina L.',
    ##   'alreadyInDb': False,
    ##   'cd_tax': 3828,
    ##   'cd_tax_acc': 3828,
    ##   'foundGbif': True,
    ##   'gbifkey': 7963890,
    ##   'insertedTax': [3827, 3828],
    ##   'matchedname': 'Juniperus sabina L.',
    ##   'syno': False},
    ##  {'acceptedname': 'Juniperus thurifera L.',
    ##   'alreadyInDb': False,
    ##   'cd_tax': 3829,
    ##   'cd_tax_acc': 3829,
    ##   'foundGbif': True,
    ##   'gbifkey': 2684528,
    ##   'insertedTax': [3829],
    ##   'matchedname': 'Juniperus thurifera L.',
    ##   'syno': False},
    ##  {'acceptedname': None,
    ##   'alreadyInDb': False,
    ##   'cd_tax': 3830,
    ##   'cd_tax_acc': 3830,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [3830],
    ##   'matchedname': None,
    ##   'syno': False},
    ##  {'acceptedname': None,
    ##   'alreadyInDb': False,
    ##   'cd_tax': 3831,
    ##   'cd_tax_acc': 3831,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [3831],
    ##   'matchedname': None,
    ##   'syno': False},
    ##  {'acceptedname': None,
    ##   'alreadyInDb': False,
    ##   'cd_tax': 3832,
    ##   'cd_tax_acc': 3832,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [3832],
    ##   'matchedname': None,
    ##   'syno': False},
    ##  {'acceptedname': None,
    ##   'alreadyInDb': False,
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [3833],
    ##   'matchedname': None,
    ##   'syno': False}]

## DELETE

Let’s delete the ‘Abies grandis’ and ‘Juniperus thurifera’ taxa.

First we search their cd_tax:

``` python
res=requests.post(api_url+'/tax/list',json={'list':[{'canonicalname':'Abies grandis'},{'canonicalname':'Juniperus thurifera'}]})
pp(res.json())
```

    ## [{'acceptedname': 'Abies grandis (Douglas ex D.Don) Lindl.',
    ##   'authorship': '(Douglas ex D.Don) Lindl.',
    ##   'canonicalname': 'Abies grandis',
    ##   'cd_accepted': 3826,
    ##   'cd_parent': 3825,
    ##   'cd_tax': 3826,
    ##   'gbifkey': 2685361,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Abies Mill.',
    ##   'scientificname': 'Abies grandis (Douglas ex D.Don) Lindl.',
    ##   'status': 'ACCEPTED',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'acceptedname': 'Juniperus thurifera L.',
    ##   'authorship': 'L.',
    ##   'canonicalname': 'Juniperus thurifera',
    ##   'cd_accepted': 3829,
    ##   'cd_parent': 3827,
    ##   'cd_tax': 3829,
    ##   'gbifkey': 2684528,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Juniperus L.',
    ##   'scientificname': 'Juniperus thurifera L.',
    ##   'status': 'ACCEPTED',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'}]

``` python
cdTaxToDel=[{'cd_tax':r['cd_tax']} for r in res.json()]
pp(cdTaxToDel)
```

    ## [{'cd_tax': 3826}, {'cd_tax': 3829}]

Then we send them to the DELETE method of the endpoint

``` python
res=requests.delete(api_url+endpoint, json={'list':cdTaxToDel},auth=authTokenEditUser)
pp(res.json())
```

    ## [{'cd_children': [3826], 'cd_synos': [], 'cd_tax': 3826},
    ##  {'cd_children': [3829], 'cd_synos': [], 'cd_tax': 3829}]

## PUT

Again it is possible to send all the modification at once.

So here is the command to modify both the species we modified as well in
the simple version:

``` python
res=requests.post(api_url+'/tax/list',json={'list':[{'canonicalname':'Juniperus communis'},{'canonicalname':'Invented species'}]})
pp(res.json())
```

    ## [{'acceptedname': 'Juniperus communis',
    ##   'authorship': None,
    ##   'canonicalname': 'Juniperus communis',
    ##   'cd_accepted': 3831,
    ##   'cd_parent': 3827,
    ##   'cd_tax': 3831,
    ##   'gbifkey': None,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Juniperus L.',
    ##   'scientificname': 'Juniperus communis',
    ##   'status': 'DOUBTFUL',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'acceptedname': 'Invented species (marius, 2022)',
    ##   'authorship': '(marius, 2022)',
    ##   'canonicalname': 'Invented species',
    ##   'cd_accepted': 3833,
    ##   'cd_parent': 3832,
    ##   'cd_tax': 3833,
    ##   'gbifkey': None,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Invented (marius, 2022)',
    ##   'scientificname': 'Invented species (marius, 2022)',
    ##   'status': 'DOUBTFUL',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'}]

``` python
ToModify=[{'cd_tax':r['cd_tax']} for r in res.json()]
ToModify[0]['gbifkey']=2684709
ToModify[1].update({'authorship':'(marius 2005)','scientificname':'Invented species (marius 2005)'})
pp(ToModify)
```

    ## [{'cd_tax': 3831, 'gbifkey': 2684709},
    ##  {'authorship': '(marius 2005)',
    ##   'cd_tax': 3833,
    ##   'scientificname': 'Invented species (marius 2005)'}]

``` python
res=requests.put(api_url+endpoint,json={'list':ToModify},auth=authTokenEditUser)
res.text
```

    ## '[{"cd_tax": 3831, "insertedTax": [3834]}, {"cd_tax": 3833, "insertedTax": []}]\n'

``` python
res=requests.post(api_url+'/tax/list',json={'list':[{'canonicalname':'Juniperus communis'},{'canonicalname':'Invented species'}]})
pp(res.json())
```

    ## [{'acceptedname': 'Juniperus communis L.',
    ##   'authorship': 'L.',
    ##   'canonicalname': 'Juniperus communis',
    ##   'cd_accepted': 3831,
    ##   'cd_parent': 3827,
    ##   'cd_tax': 3831,
    ##   'gbifkey': 2684709,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Juniperus L.',
    ##   'scientificname': 'Juniperus communis L.',
    ##   'status': 'ACCEPTED',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'acceptedname': 'Invented species (marius 2005)',
    ##   'authorship': '(marius 2005)',
    ##   'canonicalname': 'Invented species',
    ##   'cd_accepted': 3833,
    ##   'cd_parent': 3832,
    ##   'cd_tax': 3833,
    ##   'gbifkey': None,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Invented (marius, 2022)',
    ##   'scientificname': 'Invented species (marius 2005)',
    ##   'status': 'DOUBTFUL',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'}]

# Managing the statuses

There are 6 endpoints for managing species statuses: */manageEndem* and
*/manageEndem/list* (endemic species), */manageExot* and
*/manageExot/list* (alien/invasive species) and */manageThreat* and
*/manageThreat/list*.

Important notes:

-   you can use directly these endpoint with the POST method to insert
    new taxa together with their statuses. In these cases the functions
    used are for taxon insertions are exactly the same than in the
    */manageTaxo* and */manageTaxo/list*. Therefore you can use exactly
    the same arguments and get exactly the same results as what I
    described previously in this document.
-   the status are always given to the **accepted taxon**, even though
    the taxon provided is the synonym

## Endpoint /ManageEndem

``` python
endpoint='/manageEndem'
```

### POST: adding endemic species and/or the associated bibliographic references

The formally required arguments to post an endemic status are:

-   **endemstatus** (see table ): the description of the endemism status
    for the taxon
-   **ref_citation**: A list of bibliographic references associated with
    the endemic status.

However, of course you will need at least one of ‘canonicalname’,
‘scientificname’ or ‘gbifkey’, for the API to know which taxon the
endemic status refer to…

    ## [1] TRUE

| cd_nivel | descr_endem_en          | descr_endem_es           |
|---------:|:------------------------|:-------------------------|
|        0 | Unsuficient information | Información insuficiente |
|        1 | Species of interest     | Especie de interés       |
|        2 | Almost endemic by area  | Casi endémicas por área  |
|        3 | Almost endemic          | Casi endémica            |
|        4 | Endemic                 | Endémica                 |

Table for endemic status description

#### Adding a status to an existing species

Let’s add an endemic status to the virtual species we invented
(‘Invented species’)

``` python
status1={'canonicalname':'Invented species',
  'endemstatus':'Información insuficiente',
  'ref_citation':['Bottin et al, 2022. False paper to show an example','A second reference just for fun!'],
  'link':['https://colsplist.herokuapp.com',' '],
  'comments':'This is a first comment | Feeding habits: Does not eat at all!'}
res=requests.post(api_url+endpoint,json=status1,auth= authTokenEditUser)
pp(res.json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cdRefs': [293, 294],
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [],
    ##  'matchedname': 'Invented species',
    ##  'syno': False}

Now, if we use the /testEndem endpoint for this species, we will obtain:

``` python
res=requests.get(api_url+'/testEndem',json={'canonicalname':'Invented species'})
pp(res.json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': 0,
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##  'endemism': 'Información insuficiente',
    ##  'endemism_en': 'Unsuficient information',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasEndemStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Invented species',
    ##  'references': 'Bottin et al, 2022. False paper to show an example | A second '
    ##                'reference just for fun!',
    ##  'syno': False}

#### Adding a status and a species in one command

Let’s invent a new species again : “Newspecies nonexistens”, it will
have an “Endemic”:

``` python
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
```

    ## {'acceptedname': None,
    ##  'alreadyInDb': False,
    ##  'cdRefs': [293, 295],
    ##  'cd_tax': 3835,
    ##  'cd_tax_acc': 3835,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [3835],
    ##  'matchedname': None,
    ##  'syno': False}

#### Error: endemic status not recognised

El argumento ‘endemstatus’ accepts any value shown in the previous
table. However, a simple orthographic results in an error.

For example: Let’s add the status ‘Almost end**a**mic’ to *Juniperus
communis*:

``` python
requests.get(api_url+'/testEndem',json={'canonicalname':'Juniperus communis'}).json()
```

    ## {'cd_tax': 3831, 'cd_tax_acc': 3831, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Juniperus communis', 'acceptedname': 'Juniperus communis L.', 'gbifkey': 2684709, 'syno': False, 'insertedTax': [], 'hasEndemStatus': False, 'cd_nivel': None, 'descr_endem_es': None, 'comments': None, 'references': None, 'links': None}

``` python
status3={'canonicalname':'Juniperus communis',
  'endemstatus':'Almost endamic',
  'ref_citation':['Bottin et al, 2022. False paper to show an example'],
  'link':['https://colsplist.herokuapp.com'],
  'comments':'random comment | repartition: nula'}
res=requests.post(api_url+endpoint,json=status3,auth= authTokenEditUser)
pp(res.json())
```

    ## {'error': 'The input endemic status is not recognized (variable: endemstatus, '
    ##           "value: Almost endamic, acceptable:['Información insuficiente', "
    ##           "'Especie de interés', 'Casi endémicas por área', 'Casi endémica', "
    ##           "'Endémica', 'Unsuficient information', 'Species of interest', "
    ##           "'Almost endemic by area', 'Almost endemic', 'Endemic', '0', '1', "
    ##           "'2', '3', '4'])"}

If the status provided is not recognized as one of the way to designate
the status (in english, in spanish or as a code from 0 to 4 in
character), the function send back this error.

#### What if the status already exists in the database

When the status already exists in the database, the behavior of the API
depends on 2 parameters:

-   priority: if ‘high’, the previous status is replaced, references are
    added (old references are kept anyway). I ‘low’ the previous status
    is kept, references are added.
-   replace_comment: if True, the comments provided replace the old
    comments, otherwise comments are added to the existing ones (with a
    ‘\|’ separator)

Note that:

-   the most logical cases are Priority:low + replace_comment:False or
    priority:high, replace_comment:True, but you might as well use
    priority and replace_comment independently to each other.
-   There is no way to avoid that comments are either added or replacing
    old ones. So if you want to avoid comments to be inserted when the
    status already exists you will have to first test whether the
    statuses exist before sending data to the post method (with the
    ‘/testEndem(/list)’ endpoint: see
    <https://github.com/marbotte/colSpList/blob/main/usage/testAndExamples/basic_getEndpoints_functionality.md#testendem>).
-   If priority is None (or is not provided by the user) and the status
    of the species is the same than in the database, the references and
    comment are added (with the method replace_comment or not) and no
    error is sent
-   If priority is None (or is not provided by the user) and the status
    of the species different, an error is sent and no modification is
    made in the database.

##### example 1: priority:low, replace_comment:False

Let’s say that we send again a status for the species *Newspecies
nonexistens*, this time “Almost endemic”, with the new reference:
“Bottin, 2025. New fake reference with a weird date”, and the comments.
“endemism evaluation methodology: None, this is only a fake species!”

As a reminder, here is the current status of the species:

``` python
res=requests.get(api_url+'/testEndem',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())
```

    ## {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': 4,
    ##  'cd_tax': 3835,
    ##  'cd_tax_acc': 3835,
    ##  'comments': 'random comment | repartition: nula',
    ##  'endemism': 'Endémica',
    ##  'endemism_en': 'Endemic',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasEndemStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Newspecies nonexistens',
    ##  'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                'reference just for fun!',
    ##  'syno': False}

Now we modify it with:

``` python
status4={'canonicalname':'Newspecies nonexistens',
  'endemstatus':'Almost endemic',
  'comments':'endemism evaluation methodology: None, this is only a fake species!',
  'ref_citation':['Bottin, 2025. New fake reference with a weird date'],
  'priority':'low',
  'replace_comment':False
}
pp(requests.post(api_url+'/manageEndem',json=status4,auth=authTokenEditUser).json())
```

    ## {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##  'alreadyInDb': True,
    ##  'cdRefs': [296],
    ##  'cd_tax': 3835,
    ##  'cd_tax_acc': 3835,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [],
    ##  'matchedname': 'Newspecies nonexistens',
    ##  'syno': False}

The new endemism status is:

``` python
res=requests.get(api_url+'/testEndem',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())
```

    ## {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': 4,
    ##  'cd_tax': 3835,
    ##  'cd_tax_acc': 3835,
    ##  'comments': 'random comment | repartition: nula | endemism evaluation '
    ##              'methodology: None, this is only a fake species!',
    ##  'endemism': 'Endémica',
    ##  'endemism_en': 'Endemic',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasEndemStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Newspecies nonexistens',
    ##  'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                'reference just for fun! | Bottin, 2025. New fake reference '
    ##                'with a weird date',
    ##  'syno': False}

As you can see:

-   new reference was added
-   new comment was added
-   endemism stayed the same

##### example 2: priority: high, replace_comment:True

``` python
status5={'canonicalname':'Newspecies nonexistens',
  'endemstatus':'Almost endemic',
  'comments':'endemism evaluation methodology 2: None, this is still only a fake species!',
  'ref_citation':['Bottin, 2026. New fake reference with a weirder date'],
  'priority':'high',
  'replace_comment':True
}
pp(requests.post(api_url+'/manageEndem',json=status5,auth=authTokenEditUser).json())
```

    ## {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##  'alreadyInDb': True,
    ##  'cdRefs': [297],
    ##  'cd_tax': 3835,
    ##  'cd_tax_acc': 3835,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [],
    ##  'matchedname': 'Newspecies nonexistens',
    ##  'syno': False}

``` python
res=requests.get(api_url+'/testEndem',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())
```

    ## {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': 3,
    ##  'cd_tax': 3835,
    ##  'cd_tax_acc': 3835,
    ##  'comments': 'endemism evaluation methodology 2: None, this is still only a '
    ##              'fake species!',
    ##  'endemism': 'Casi endémica',
    ##  'endemism_en': 'Almost endemic',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasEndemStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Newspecies nonexistens',
    ##  'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                'reference just for fun! | Bottin, 2025. New fake reference '
    ##                'with a weird date | Bottin, 2026. New fake reference with a '
    ##                'weirder date',
    ##  'syno': False}

As you can see:

-   new reference was added
-   comments were replaced
-   endemism changed into ‘Almost endemic’

### PUT: modify a status

The PUT method here is exactly the same than the POST method with
‘priority’:‘high’. The only difference is that it will send an error if
the status does not exist. The rationale is that they are used in
different context. The POST method is used when a new dataset is
available, and people want to update the information on the API, while
the PUT method is used when some errors or inconsistencies are found in
the API data…

Imagine that we found new data for ‘Invented species’: it is now
accepted in the literature as ‘Species of interest’

``` python
res=requests.get(api_url+'/testEndem',json={'canonicalname':'Invented species'})
pp(res.json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': 0,
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##  'endemism': 'Información insuficiente',
    ##  'endemism_en': 'Unsuficient information',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasEndemStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Invented species',
    ##  'references': 'Bottin et al, 2022. False paper to show an example | A second '
    ##                'reference just for fun!',
    ##  'syno': False}

``` python
cd_tax=res.json().get('cd_tax_acc')
```

``` python
status6={'cd_tax':cd_tax,
  'endemstatus':'Species of interest',
  'ref_citation':['Bottin, 2051. New fake reference with the weirdest date'],
}
pp(requests.put(api_url+'/manageEndem',json=status6,auth=authTokenEditUser).json())
```

    ## {'cdRefs': [298], 'cd_tax': 3833}

``` python
res=requests.get(api_url+'/testEndem',json={'canonicalname':'Invented species'})
pp(res.json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': 1,
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##  'endemism': 'Especie de interés',
    ##  'endemism_en': 'Species of interest',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasEndemStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Invented species',
    ##  'references': 'Bottin et al, 2022. False paper to show an example | A second '
    ##                'reference just for fun! | Bottin, 2051. New fake reference '
    ##                'with the weirdest date',
    ##  'syno': False}

### DELETE: suppress a reference associated with a status, or the status itself

The DELETE method, by default, concerns the references associated to a
status. If what you want to delete is the status, you have to use the
‘delete_status’ argument.

#### Deleting an association between a taxon status and a reference

The first thing to do is to search for the cd_ref and cd_tax
corresponding respectively to the reference and the taxon.

In order to suppress the association between the reference ‘Bottin et
al, 2022. False paper to show an example’ and the taxon ‘Invented
species’, here is the way to search for the codes automatically:

``` python
listRef=requests.get(api_url+'/listReferences').json()
cd_ref = [r['cd_ref'] for r in listRef if r['ref_citation']=='Bottin et al, 2022. False paper to show an example'][0]
pp(cd_ref)
```

    ## 293

``` python
cd_tax=requests.get(api_url+'/tax',json={'canonicalname':'Invented species'}).json()['cd_tax']
pp(cd_tax)
```

    ## 3833

Let’s take a look at the endemic status of *Invented species*.

``` python
pp(requests.get(api_url+'/testEndem',json={'canonicalname':'Invented species'}).json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': 1,
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##  'endemism': 'Especie de interés',
    ##  'endemism_en': 'Species of interest',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasEndemStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Invented species',
    ##  'references': 'Bottin et al, 2022. False paper to show an example | A second '
    ##                'reference just for fun! | Bottin, 2051. New fake reference '
    ##                'with the weirdest date',
    ##  'syno': False}

Here to suppress the association:

``` python
res=requests.delete(api_url+'/manageEndem', json={'cd_tax':cd_tax,'cd_ref':cd_ref},auth=authTokenEditUser)
pp(res.json())
```

    ## {'cd_refs': [293], 'cd_tax': 3833}

``` python
pp(requests.get(api_url+'/testEndem',json={'canonicalname':'Invented species'}).json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': 1,
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##  'endemism': 'Especie de interés',
    ##  'endemism_en': 'Species of interest',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasEndemStatus': True,
    ##  'insertedTax': [],
    ##  'links': None,
    ##  'matchedname': 'Invented species',
    ##  'references': 'A second reference just for fun! | Bottin, 2051. New fake '
    ##                'reference with the weirdest date',
    ##  'syno': False}

#### Deleting an association between a taxon status and a reference

If the delete method is called only with a cd_tax here is what happens:

``` python
pp(requests.delete(api_url + '/manageEndem',json={'cd_tax':cd_tax},auth=authTokenEditUser).json())
```

    ## {'error': "Do you want to suppress the status ('delete_status'=True) or just a "
    ##           "reference associated with the status (provide 'cd_ref')?, missing "
    ##           "argument: 'cd_ref' or 'delete_status'"}

As said, to delete the endemic status of ‘Invented species’, what should
be done is:

``` python
pp(requests.delete(api_url + '/manageEndem',json={'cd_tax':cd_tax,'delete_status':True},auth=authTokenEditUser).json())
```

    ## {'cd_refs': [294, 298], 'cd_tax': 3833}

``` python
pp(requests.get(api_url+'/testEndem',json={'canonicalname':'Invented species'}).json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': None,
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': None,
    ##  'descr_endem_es': None,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasEndemStatus': False,
    ##  'insertedTax': [],
    ##  'links': None,
    ##  'matchedname': 'Invented species',
    ##  'references': None,
    ##  'syno': False}

### Cleaning

**Species to suppress**:

‘Newspecies nonexistens’

**References to suppress**:

‘Bottin et al, 2022. False paper to show an example’,‘A second reference
just for fun!’,‘A third reference just for fun!’,‘Bottin, 2025. New fake
reference with a weird date’,‘Bottin, 2026. New fake reference with a
weirder date’,‘Bottin, 2051. New fake reference with the weirdest date’

``` python
cd_tax_ToDel=requests.get(api_url + '/tax',json={'canonicalname':'Newspecies nonexistens'}).json().get('cd_tax')
requests.delete(api_url+'/manageTaxo',json={'cd_tax':cd_tax_ToDel},auth=authTokenEditUser)
```

    ## <Response [200]>

``` python
cd_tax_StatusToDel=requests.get(api_url + '/testEndem',json={'canonicalname':'Invented species'}).json().get('cd_tax')
res=requests.delete(api_url+'/manageEndem',json={'cd_tax':cd_tax_StatusToDel, 'delete_status':True}, auth=authTokenEditUser)
res=requests.delete(api_url+'/cleanDb',json={'ref_no_status':True}, auth=authTokenEditUser)
```

## Endpoint /manageEndem/list

The endpoint /manageEndem/list works exactly like the endpoint
/manageEndem, except that all the insertions, modifications or deletions
may be done at once with a list.

### POST

See explanation in section POST of the /manageEndem endpoint.

We will show here how to post multiple statuses in a single call to the
API.

Of course, many of these statuses concern the species “Newspecies
nonexistens”, which is not the intended objective of the multiple
version in the endpoint /manageEndem/list, but the objective here is to
show a proof of concept…

``` python
statuses=[status1,status2,status3,status4,status5]
pp(statuses)
```

    ## [{'canonicalname': 'Invented species',
    ##   'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##   'endemstatus': 'Información insuficiente',
    ##   'link': ['https://colsplist.herokuapp.com', ' '],
    ##   'ref_citation': ['Bottin et al, 2022. False paper to show an example',
    ##                    'A second reference just for fun!']},
    ##  {'authorship': '(marius 2022)',
    ##   'canonicalname': 'Newspecies nonexistens',
    ##   'comments': 'random comment | repartition: nula',
    ##   'endemstatus': 'Endemic',
    ##   'link': ['https://colsplist.herokuapp.com', ' '],
    ##   'parentcanonicalname': 'Invented',
    ##   'ref_citation': ['Bottin et al, 2022. False paper to show an example',
    ##                    'A third reference just for fun!'],
    ##   'scientificname': 'Newspecies nonexistens (marius 2022)'},
    ##  {'canonicalname': 'Juniperus communis',
    ##   'comments': 'random comment | repartition: nula',
    ##   'endemstatus': 'Almost endamic',
    ##   'link': ['https://colsplist.herokuapp.com'],
    ##   'ref_citation': ['Bottin et al, 2022. False paper to show an example']},
    ##  {'canonicalname': 'Newspecies nonexistens',
    ##   'comments': 'endemism evaluation methodology: None, this is only a fake '
    ##               'species!',
    ##   'endemstatus': 'Almost endemic',
    ##   'priority': 'low',
    ##   'ref_citation': ['Bottin, 2025. New fake reference with a weird date'],
    ##   'replace_comment': False},
    ##  {'canonicalname': 'Newspecies nonexistens',
    ##   'comments': 'endemism evaluation methodology 2: None, this is still only a '
    ##               'fake species!',
    ##   'endemstatus': 'Almost endemic',
    ##   'priority': 'high',
    ##   'ref_citation': ['Bottin, 2026. New fake reference with a weirder date'],
    ##   'replace_comment': True}]

``` python
res=requests.post(api_url + '/manageEndem/list',json={'list':statuses},auth=authTokenEditUser)
pp(res.json())
```

    ## [{'acceptedname': 'Invented species (marius 2005)',
    ##   'alreadyInDb': True,
    ##   'cdRefs': [299, 300],
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [],
    ##   'matchedname': 'Invented species',
    ##   'syno': False},
    ##  {'acceptedname': None,
    ##   'alreadyInDb': False,
    ##   'cdRefs': [299, 301],
    ##   'cd_tax': 3836,
    ##   'cd_tax_acc': 3836,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [3836],
    ##   'matchedname': None,
    ##   'syno': False},
    ##  {'error': 'The input endemic status is not recognized (variable: endemstatus, '
    ##            "value: Almost endamic, acceptable:['Información insuficiente', "
    ##            "'Especie de interés', 'Casi endémicas por área', 'Casi endémica', "
    ##            "'Endémica', 'Unsuficient information', 'Species of interest', "
    ##            "'Almost endemic by area', 'Almost endemic', 'Endemic', '0', '1', "
    ##            "'2', '3', '4'])"},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cdRefs': [302],
    ##   'cd_tax': 3836,
    ##   'cd_tax_acc': 3836,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [],
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cdRefs': [303],
    ##   'cd_tax': 3836,
    ##   'cd_tax_acc': 3836,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [],
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'syno': False}]

### PUT

We will show here how to modify multiple statuses in a single call to
the API.

``` python
newSpecies=requests.post(api_url+'/testEndem/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json()
pp(newSpecies)
```

    ## [{'acceptedname': 'Invented species (marius 2005)',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': 0,
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##   'endemism': 'Información insuficiente',
    ##   'endemism_en': 'Unsuficient information',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasEndemStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://colsplist.herokuapp.com',
    ##   'matchedname': 'Invented species',
    ##   'references': 'Bottin et al, 2022. False paper to show an example | A second '
    ##                 'reference just for fun!',
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': 3,
    ##   'cd_tax': 3836,
    ##   'cd_tax_acc': 3836,
    ##   'comments': 'endemism evaluation methodology 2: None, this is still only a '
    ##               'fake species!',
    ##   'endemism': 'Casi endémica',
    ##   'endemism_en': 'Almost endemic',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasEndemStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://colsplist.herokuapp.com',
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                 'reference just for fun! | Bottin, 2025. New fake reference '
    ##                 'with a weird date | Bottin, 2026. New fake reference with a '
    ##                 'weirder date',
    ##   'syno': False}]

``` python
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
```

    ## {'list': [{'cd_tax': 3833,
    ##            'comments': 'a comment as replacement',
    ##            'endemstatus': 'Casi endémicas por área',
    ##            'link': ['https://www.afalsesiteasanexample.com'],
    ##            'ref_citation': ['Fake report to put Invented species as Almost '
    ##                             'endemic by area'],
    ##            'replace_comment': True},
    ##           {'cd_tax': 3836,
    ##            'comments': 'a comment to add',
    ##            'endemstatus': 'Endemic',
    ##            'ref_citation': ['Another fake report']}]}

``` python
modifs=requests.put(api_url + '/manageEndem/list',json=modifications,auth=authTokenEditUser).json()
pp(modifs)
```

    ## [{'cdRefs': [304], 'cd_tax': 3833}, {'cdRefs': [305], 'cd_tax': 3836}]

``` python
pp(requests.post(api_url+'/testEndem/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())
```

    ## [{'acceptedname': 'Invented species (marius 2005)',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': 2,
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'comments': 'a comment as replacement',
    ##   'endemism': 'Casi endémicas por área',
    ##   'endemism_en': 'Almost endemic by area',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasEndemStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://colsplist.herokuapp.com | '
    ##            'https://www.afalsesiteasanexample.com',
    ##   'matchedname': 'Invented species',
    ##   'references': 'Bottin et al, 2022. False paper to show an example | A second '
    ##                 'reference just for fun! | Fake report to put Invented species '
    ##                 'as Almost endemic by area',
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': 4,
    ##   'cd_tax': 3836,
    ##   'cd_tax_acc': 3836,
    ##   'comments': 'endemism evaluation methodology 2: None, this is still only a '
    ##               'fake species! | a comment to add',
    ##   'endemism': 'Endémica',
    ##   'endemism_en': 'Endemic',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasEndemStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://colsplist.herokuapp.com',
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                 'reference just for fun! | Bottin, 2025. New fake reference '
    ##                 'with a weird date | Bottin, 2026. New fake reference with a '
    ##                 'weirder date | Another fake report',
    ##   'syno': False}]

### DELETE

We will show here how to delete multiple references/statuses in a single
call to the API.

We will suppress the references ‘Bottin et al, 2022. False paper to show
an example’ and ‘Fake report to put Invented species as Almost endemic
by area’ as justifications for *Invented species*, and delete the
endemic status for *Newspecies nonExistens*

``` python
pp(requests.post(api_url+'/testEndem/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())
```

    ## [{'acceptedname': 'Invented species (marius 2005)',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': 2,
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'comments': 'a comment as replacement',
    ##   'endemism': 'Casi endémicas por área',
    ##   'endemism_en': 'Almost endemic by area',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasEndemStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://colsplist.herokuapp.com | '
    ##            'https://www.afalsesiteasanexample.com',
    ##   'matchedname': 'Invented species',
    ##   'references': 'Bottin et al, 2022. False paper to show an example | A second '
    ##                 'reference just for fun! | Fake report to put Invented species '
    ##                 'as Almost endemic by area',
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': 4,
    ##   'cd_tax': 3836,
    ##   'cd_tax_acc': 3836,
    ##   'comments': 'endemism evaluation methodology 2: None, this is still only a '
    ##               'fake species! | a comment to add',
    ##   'endemism': 'Endémica',
    ##   'endemism_en': 'Endemic',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasEndemStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://colsplist.herokuapp.com',
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                 'reference just for fun! | Bottin, 2025. New fake reference '
    ##                 'with a weird date | Bottin, 2026. New fake reference with a '
    ##                 'weirder date | Another fake report',
    ##   'syno': False}]

``` python
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
```

    ## [{'cd_ref': 299, 'cd_tax': 3833},
    ##  {'cd_ref': 304, 'cd_tax': 3833},
    ##  {'cd_tax': 3836, 'delete_status': True}]

``` python
pp(requests.delete(api_url + '/manageEndem/list',json={'list':deletions},auth=authTokenEditUser).json())
```

    ## [{'cd_refs': [299], 'cd_tax': 3833},
    ##  {'cd_refs': [304], 'cd_tax': 3833},
    ##  {'cd_refs': [299, 301, 302, 303, 305], 'cd_tax': 3836}]

``` python
pp(requests.post(api_url+'/testEndem/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())
```

    ## [{'acceptedname': 'Invented species (marius 2005)',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': 2,
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'comments': 'a comment as replacement',
    ##   'endemism': 'Casi endémicas por área',
    ##   'endemism_en': 'Almost endemic by area',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasEndemStatus': True,
    ##   'insertedTax': [],
    ##   'links': None,
    ##   'matchedname': 'Invented species',
    ##   'references': 'A second reference just for fun!',
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': None,
    ##   'cd_tax': 3836,
    ##   'cd_tax_acc': 3836,
    ##   'comments': None,
    ##   'descr_endem_es': None,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasEndemStatus': False,
    ##   'insertedTax': [],
    ##   'links': None,
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'references': None,
    ##   'syno': False}]

### Cleaning

``` python
pp(requests.delete(api_url + '/cleanDb',json={'status_no_ref':True,'ref_no_status':True},auth=authTokenEditUser).json())
```

    ## {'cd_refs': [299, 301, 302, 303, 304, 305], 'cd_status': [], 'cd_taxs': []}

``` python
pp(requests.delete(api_url + '/manageTaxo', json={'cd_tax':newSpecies_cd_tax[1]}, auth=authTokenEditUser).json())
```

    ## {'cd_children': [3836], 'cd_synos': [], 'cd_tax': 3836}

## Endpoint /ManageThreat

``` python
endpoint='/manageThreat'
```

### POST: adding threatened species and/or the associated bibliographic references

The formally required arguments to post a threatened status are:

-   **threatstatus** (see table ): IUCN code threat status for the taxon
-   **ref_citation**: A list of bibliographic references associated with
    the threat status.

However, of course you will need at least one of ‘canonicalname’,
‘scientificname’ or ‘gbifkey’, for the API to know which taxon the
threatened status refer to…

| cd_status | level | status_descr          |
|:----------|------:|:----------------------|
| NE        |     0 | Not Evaluated         |
| DD        |     1 | Data Deficient        |
| LC        |     2 | Least Concern         |
| NT        |     3 | Near Threatened       |
| VU        |     4 | Vulnerable            |
| EN        |     5 | Endangered            |
| CR        |     6 | Critically endangered |
| EW        |     7 | Extinct in the wild   |
| EX        |     8 | Extinct               |

Table for threatened status description

#### Adding a status to an existing species

Let’s add an threatened status to the virtual species we invented
(‘Invented species’)

``` python
status1={'canonicalname':'Invented species',
  'threatstatus':'DD',
  'ref_citation':['Bottin et al, 2022. False paper to show an example','A second reference just for fun!'],
  'link':['https://colsplist.herokuapp.com',' '],
  'comments':'This is a first comment | Feeding habits: Does not eat at all!'}
res=requests.post(api_url+endpoint,json=status1,auth= authTokenEditUser)
pp(res.json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cdRefs': [306, 300],
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [],
    ##  'matchedname': 'Invented species',
    ##  'syno': False}

Now, if we use the /testThreat endpoint for this species, we will
obtain:

``` python
res=requests.get(api_url+'/testThreat',json={'canonicalname':'Invented species'})
pp(res.json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_status': 'DD',
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasThreatStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Invented species',
    ##  'references': 'A second reference just for fun! | Bottin et al, 2022. False '
    ##                'paper to show an example',
    ##  'syno': False}

#### Adding a status and a species in one command

Let’s invent a new species again (it’s been deleted before) :
“Newspecies nonexistens”, it will have a “NT” status:

``` python
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
```

    ## {'acceptedname': None,
    ##  'alreadyInDb': False,
    ##  'cdRefs': [306, 307],
    ##  'cd_tax': 3837,
    ##  'cd_tax_acc': 3837,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [3837],
    ##  'matchedname': None,
    ##  'syno': False}

#### Error: threatened status not recognised

The argument ‘threatstatus’ accepts any value shown in the previous
table. However, a simple orthographic results in an error.

For example: Let’s add the status ‘E**M**’ to *Juniperus communis*:

``` python
requests.get(api_url+'/testThreat',json={'canonicalname':'Juniperus communis'}).json()
```

    ## {'cd_tax': 3831, 'cd_tax_acc': 3831, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Juniperus communis', 'acceptedname': 'Juniperus communis L.', 'gbifkey': 2684709, 'syno': False, 'insertedTax': [], 'hasThreatStatus': False, 'cd_status': None, 'comments': None, 'references': None, 'links': None}

``` python
status3={'canonicalname':'Juniperus communis',
  'threatstatus':'EM',
  'ref_citation':['Bottin et al, 2022. False paper to show an example'],
  'link':['https://colsplist.herokuapp.com'],
  'comments':'random comment | repartition: nula'}
res=requests.post(api_url+endpoint,json=status3,auth= authTokenEditUser)
pp(res.json())
```

    ## {'error': 'The input threat status is not recognized (variable: threatstatus, '
    ##           "value: EM, acceptable:['NE', 'DD', 'LC', 'NT', 'VU', 'EN', 'CR', "
    ##           "'EW', 'EX'])"}

If the status provided is not recognized as one of the way to designate
the status, the function send back this error.

#### What if the status already exists in the database

When the status already exists in the database, the behavior of the API
depends on 2 parameters:

-   priority: if ‘high’, the previous status is replaced, references are
    added (old references are kept anyway). I ‘low’ the previous status
    is kept, references are added.
-   replace_comment: if True, the comments provided replace the old
    comments, otherwise comments are added to the existing ones (with a
    ‘\|’ separator)

Note that:

-   the most logical cases are Priority:low + replace_comment:False or
    priority:high, replace_comment:True, but you might as well use
    priority and replace_comment independently to each other.
-   There is no way to avoid that comments are either added or replacing
    old ones. So if you want to avoid comments to be inserted when the
    status already exists you will have to first test whether the
    statuses exist before sending data to the post method (with the
    ‘/testThreat(/list)’ endpoint: see
    <https://github.com/marbotte/colSpList/blob/main/usage/testAndExamples/basic_getEndpoints_functionality.md#testthreat>).
-   If priority is None (or is not provided by the user) and the status
    of the species is the same than in the database, the references and
    comment are added (with the method replace_comment or not) and no
    error is sent
-   If priority is None (or is not provided by the user) and the status
    of the species different, an error is sent and no modification is
    made in the database.

##### example 1: priority:low, replace_comment:False

Let’s say that we send again a status for the species *Newspecies
nonexistens*, this time “EN”, with the new reference: “Bottin, 2025. New
fake reference with a weird date”, and the comments. “threat evaluation
methodology: None, this is only a fake species!”

As a reminder, here is the current status of the species:

``` python
res=requests.get(api_url+'/testThreat',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())
```

    ## {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##  'alreadyInDb': True,
    ##  'cd_status': 'NT',
    ##  'cd_tax': 3837,
    ##  'cd_tax_acc': 3837,
    ##  'comments': 'random comment | repartition: nula',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasThreatStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Newspecies nonexistens',
    ##  'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                'reference just for fun!',
    ##  'syno': False}

Now we modify it with:

``` python
status4={'canonicalname':'Newspecies nonexistens',
  'threatstatus':'EN',
  'comments':'threat evaluation methodology: None, this is only a fake species!',
  'ref_citation':['Bottin, 2025. New fake reference with a weird date'],
  'priority':'low',
  'replace_comment':False
}
pp(requests.post(api_url+'/manageThreat',json=status4,auth=authTokenEditUser).json())
```

    ## {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##  'alreadyInDb': True,
    ##  'cdRefs': [308],
    ##  'cd_tax': 3837,
    ##  'cd_tax_acc': 3837,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [],
    ##  'matchedname': 'Newspecies nonexistens',
    ##  'syno': False}

The new threat status is:

``` python
res=requests.get(api_url+'/testThreat',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())
```

    ## {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##  'alreadyInDb': True,
    ##  'cd_status': 'NT',
    ##  'cd_tax': 3837,
    ##  'cd_tax_acc': 3837,
    ##  'comments': 'random comment | repartition: nula | threat evaluation '
    ##              'methodology: None, this is only a fake species!',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasThreatStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Newspecies nonexistens',
    ##  'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                'reference just for fun! | Bottin, 2025. New fake reference '
    ##                'with a weird date',
    ##  'syno': False}

As you can see:

-   new reference was added
-   new comment was added
-   threat stayed the same

##### example 2: priority: high, replace_comment:True

``` python
status5={'canonicalname':'Newspecies nonexistens',
  'threatstatus':'EN',
  'comments':'threat evaluation methodology 2: None, this is still only a fake species!',
  'ref_citation':['Bottin, 2026. New fake reference with a weirder date'],
  'priority':'high',
  'replace_comment':True
}
pp(requests.post(api_url+'/manageThreat',json=status5,auth=authTokenEditUser).json())
```

    ## {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##  'alreadyInDb': True,
    ##  'cdRefs': [309],
    ##  'cd_tax': 3837,
    ##  'cd_tax_acc': 3837,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [],
    ##  'matchedname': 'Newspecies nonexistens',
    ##  'syno': False}

``` python
res=requests.get(api_url+'/testThreat',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())
```

    ## {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##  'alreadyInDb': True,
    ##  'cd_status': 'EN',
    ##  'cd_tax': 3837,
    ##  'cd_tax_acc': 3837,
    ##  'comments': 'threat evaluation methodology 2: None, this is still only a fake '
    ##              'species!',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasThreatStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Newspecies nonexistens',
    ##  'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                'reference just for fun! | Bottin, 2025. New fake reference '
    ##                'with a weird date | Bottin, 2026. New fake reference with a '
    ##                'weirder date',
    ##  'syno': False}

As you can see:

-   new reference was added
-   comments were replaced
-   threat changed into ‘EN’

### PUT: modify a status

The PUT method here is exactly the same than the POST method with
‘priority’:‘high’. The only difference is that it will send an error if
the status does not exist. The rationale is that they are used in
different context. The POST method is used when a new dataset is
available, and people want to update the information on the API, while
the PUT method is used when some errors or inconsistencies are found in
the API data…

Imagine that we found new data for ‘Invented species’: it is now
accepted in the literature as ‘VU’

``` python
res=requests.get(api_url+'/testThreat',json={'canonicalname':'Invented species'})
pp(res.json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_status': 'DD',
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasThreatStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Invented species',
    ##  'references': 'A second reference just for fun! | Bottin et al, 2022. False '
    ##                'paper to show an example',
    ##  'syno': False}

``` python
cd_tax=res.json().get('cd_tax_acc')
```

``` python
status6={'cd_tax':cd_tax,
  'threatstatus':'VU',
  'ref_citation':['Bottin, 2051. New fake reference with the weirdest date'],
}
pp(requests.put(api_url+'/manageThreat',json=status6,auth=authTokenEditUser).json())
```

    ## {'cdRefs': [310], 'cd_tax': 3833}

``` python
res=requests.get(api_url+'/testThreat',json={'canonicalname':'Invented species'})
pp(res.json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_status': 'VU',
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasThreatStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Invented species',
    ##  'references': 'A second reference just for fun! | Bottin et al, 2022. False '
    ##                'paper to show an example | Bottin, 2051. New fake reference '
    ##                'with the weirdest date',
    ##  'syno': False}

### DELETE: suppress a reference associated with a status, or the status itself

The DELETE method, by default, concerns the references associated to a
status. If what you want to delete is the status, you have to use the
‘delete_status’ argument.

#### Deleting an association between a taxon status and a reference

The first thing to do is to search for the cd_ref and cd_tax
corresponding respectively to the reference and the taxon.

In order to suppress the association between the reference ‘Bottin et
al, 2022. False paper to show an example’ and the taxon ‘Invented
species’, here is the way to search for the codes automatically:

``` python
listRef=requests.get(api_url+'/listReferences').json()
cd_ref = [r['cd_ref'] for r in listRef if r['ref_citation']=='Bottin et al, 2022. False paper to show an example'][0]
pp(cd_ref)
```

    ## 306

``` python
cd_tax=requests.get(api_url+'/tax',json={'canonicalname':'Invented species'}).json()['cd_tax']
pp(cd_tax)
```

    ## 3833

Let’s take a look at the threatened status of *Invented species*.

``` python
pp(requests.get(api_url+'/testThreat',json={'canonicalname':'Invented species'}).json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_status': 'VU',
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasThreatStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Invented species',
    ##  'references': 'A second reference just for fun! | Bottin et al, 2022. False '
    ##                'paper to show an example | Bottin, 2051. New fake reference '
    ##                'with the weirdest date',
    ##  'syno': False}

Here to suppress the association:

``` python
res=requests.delete(api_url+'/manageThreat', json={'cd_tax':cd_tax,'cd_ref':cd_ref},auth=authTokenEditUser)
pp(res.json())
```

    ## {'cd_refs': [306], 'cd_tax': 3833}

``` python
pp(requests.get(api_url+'/testThreat',json={'canonicalname':'Invented species'}).json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_status': 'VU',
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasThreatStatus': True,
    ##  'insertedTax': [],
    ##  'links': None,
    ##  'matchedname': 'Invented species',
    ##  'references': 'A second reference just for fun! | Bottin, 2051. New fake '
    ##                'reference with the weirdest date',
    ##  'syno': False}

#### Deleting an association between a taxon status and a reference

If the delete method is called only with a cd_tax here is what happens:

``` python
pp(requests.delete(api_url + '/manageThreat',json={'cd_tax':cd_tax},auth=authTokenEditUser).json())
```

    ## {'error': "Do you want to suppress the status ('delete_status'=True) or just a "
    ##           "reference associated with the status (provide 'cd_ref'), missing "
    ##           "argument: 'cd_ref' or 'delete_status'"}

As said, to delete the threatened status of ‘Invented species’, what
should be done is:

``` python
pp(requests.delete(api_url + '/manageThreat',json={'cd_tax':cd_tax,'delete_status':True},auth=authTokenEditUser).json())
```

    ## {'cd_refs': [300, 310], 'cd_tax': 3833}

``` python
pp(requests.get(api_url+'/testThreat',json={'canonicalname':'Invented species'}).json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_status': None,
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': None,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasThreatStatus': False,
    ##  'insertedTax': [],
    ##  'links': None,
    ##  'matchedname': 'Invented species',
    ##  'references': None,
    ##  'syno': False}

### Cleaning

**Species to suppress**:

‘Newspecies nonexistens’

**References to suppress**:

‘Bottin et al, 2022. False paper to show an example’,‘A second reference
just for fun!’,‘A third reference just for fun!’,‘Bottin, 2025. New fake
reference with a weird date’,‘Bottin, 2026. New fake reference with a
weirder date’,‘Bottin, 2051. New fake reference with the weirdest date’

``` python
cd_tax_ToDel=requests.get(api_url + '/tax',json={'canonicalname':'Newspecies nonexistens'}).json().get('cd_tax')
requests.delete(api_url+'/manageTaxo',json={'cd_tax':cd_tax_ToDel},auth=authTokenEditUser)
```

    ## <Response [200]>

``` python
cd_tax_StatusToDel=requests.get(api_url + '/testThreat',json={'canonicalname':'Invented species'}).json().get('cd_tax')
res=requests.delete(api_url+'/manageThreat',json={'cd_tax':cd_tax_StatusToDel, 'delete_status':True}, auth=authTokenEditUser)
res=requests.delete(api_url+'/cleanDb',json={'ref_no_status':True}, auth=authTokenEditUser)
```

## Endpoint /manageThreat/list

The endpoint /manageThreat/list works exactly like the endpoint
/manageThreat, except that all the insertions, modifications or
deletions may be done at once with a list.

### POST

See explanation in section POST of the /manageThreat endpoint.

We will show here how to post multiple statuses in a single call to the
API.

Of course, many of these statuses concern the species “Newspecies
nonexistens”, which is not the intended objective of the multiple
version in the endpoint /manageThreat/list, but the objective here is to
show a proof of concept…

``` python
statuses=[status1,status2,status3,status4,status5]
pp(statuses)
```

    ## [{'canonicalname': 'Invented species',
    ##   'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##   'link': ['https://colsplist.herokuapp.com', ' '],
    ##   'ref_citation': ['Bottin et al, 2022. False paper to show an example',
    ##                    'A second reference just for fun!'],
    ##   'threatstatus': 'DD'},
    ##  {'authorship': '(marius 2022)',
    ##   'canonicalname': 'Newspecies nonexistens',
    ##   'comments': 'random comment | repartition: nula',
    ##   'link': ['https://colsplist.herokuapp.com', ' '],
    ##   'parentcanonicalname': 'Invented',
    ##   'ref_citation': ['Bottin et al, 2022. False paper to show an example',
    ##                    'A third reference just for fun!'],
    ##   'scientificname': 'Newspecies nonexistens (marius 2022)',
    ##   'threatstatus': 'NT'},
    ##  {'canonicalname': 'Juniperus communis',
    ##   'comments': 'random comment | repartition: nula',
    ##   'link': ['https://colsplist.herokuapp.com'],
    ##   'ref_citation': ['Bottin et al, 2022. False paper to show an example'],
    ##   'threatstatus': 'EM'},
    ##  {'canonicalname': 'Newspecies nonexistens',
    ##   'comments': 'threat evaluation methodology: None, this is only a fake '
    ##               'species!',
    ##   'priority': 'low',
    ##   'ref_citation': ['Bottin, 2025. New fake reference with a weird date'],
    ##   'replace_comment': False,
    ##   'threatstatus': 'EN'},
    ##  {'canonicalname': 'Newspecies nonexistens',
    ##   'comments': 'threat evaluation methodology 2: None, this is still only a '
    ##               'fake species!',
    ##   'priority': 'high',
    ##   'ref_citation': ['Bottin, 2026. New fake reference with a weirder date'],
    ##   'replace_comment': True,
    ##   'threatstatus': 'EN'}]

``` python
res=requests.post(api_url + '/manageThreat/list',json={'list':statuses},auth=authTokenEditUser)
pp(res.json())
```

    ## [{'acceptedname': 'Invented species (marius 2005)',
    ##   'alreadyInDb': True,
    ##   'cdRefs': [311, 300],
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [],
    ##   'matchedname': 'Invented species',
    ##   'syno': False},
    ##  {'acceptedname': None,
    ##   'alreadyInDb': False,
    ##   'cdRefs': [311, 312],
    ##   'cd_tax': 3838,
    ##   'cd_tax_acc': 3838,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [3838],
    ##   'matchedname': None,
    ##   'syno': False},
    ##  {'error': 'The input threat status is not recognized (variable: threatstatus, '
    ##            "value: EM, acceptable:['NE', 'DD', 'LC', 'NT', 'VU', 'EN', 'CR', "
    ##            "'EW', 'EX'])"},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cdRefs': [313],
    ##   'cd_tax': 3838,
    ##   'cd_tax_acc': 3838,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [],
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cdRefs': [314],
    ##   'cd_tax': 3838,
    ##   'cd_tax_acc': 3838,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [],
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'syno': False}]

### PUT

We will show here how to modify multiple statuses in a single call to
the API.

``` python
newSpecies=requests.post(api_url+'/testThreat/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json()
pp(newSpecies)
```

    ## [{'acceptedname': 'Invented species (marius 2005)',
    ##   'alreadyInDb': True,
    ##   'cd_status': 'DD',
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasThreatStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://colsplist.herokuapp.com',
    ##   'matchedname': 'Invented species',
    ##   'references': 'A second reference just for fun! | Bottin et al, 2022. False '
    ##                 'paper to show an example',
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cd_status': 'EN',
    ##   'cd_tax': 3838,
    ##   'cd_tax_acc': 3838,
    ##   'comments': 'threat evaluation methodology 2: None, this is still only a '
    ##               'fake species!',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasThreatStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://colsplist.herokuapp.com',
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                 'reference just for fun! | Bottin, 2025. New fake reference '
    ##                 'with a weird date | Bottin, 2026. New fake reference with a '
    ##                 'weirder date',
    ##   'syno': False}]

``` python
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
```

    ## {'list': [{'cd_tax': 3833,
    ##            'comments': 'a comment as replacement',
    ##            'link': ['https://www.afalsesiteasanexample.com'],
    ##            'ref_citation': ['Fake report to put Invented species as LC'],
    ##            'replace_comment': True,
    ##            'threatstatus': 'LC'},
    ##           {'cd_tax': 3838,
    ##            'comments': 'a comment to add',
    ##            'ref_citation': ['Another fake report'],
    ##            'threatstatus': 'CR'}]}

``` python
modifs=requests.put(api_url + '/manageThreat/list',json=modifications,auth=authTokenEditUser).json()
pp(modifs)
```

    ## [{'cdRefs': [315], 'cd_tax': 3833}, {'cdRefs': [316], 'cd_tax': 3838}]

``` python
pp(requests.post(api_url+'/testThreat/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())
```

    ## [{'acceptedname': 'Invented species (marius 2005)',
    ##   'alreadyInDb': True,
    ##   'cd_status': 'LC',
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'comments': 'a comment as replacement',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasThreatStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://colsplist.herokuapp.com | '
    ##            'https://www.afalsesiteasanexample.com',
    ##   'matchedname': 'Invented species',
    ##   'references': 'A second reference just for fun! | Bottin et al, 2022. False '
    ##                 'paper to show an example | Fake report to put Invented '
    ##                 'species as LC',
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cd_status': 'CR',
    ##   'cd_tax': 3838,
    ##   'cd_tax_acc': 3838,
    ##   'comments': 'threat evaluation methodology 2: None, this is still only a '
    ##               'fake species! | a comment to add',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasThreatStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://colsplist.herokuapp.com',
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                 'reference just for fun! | Bottin, 2025. New fake reference '
    ##                 'with a weird date | Bottin, 2026. New fake reference with a '
    ##                 'weirder date | Another fake report',
    ##   'syno': False}]

### DELETE

We will show here how to delete multiple references/statuses in a single
call to the API.

We will suppress the references ‘Bottin et al, 2022. False paper to show
an example’ and ‘Fake report to put Invented species as LC’ as
justifications for *Invented species*, and delete the threatened status
for *Newspecies nonExistens*

``` python
pp(requests.post(api_url+'/testThreat/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())
```

    ## [{'acceptedname': 'Invented species (marius 2005)',
    ##   'alreadyInDb': True,
    ##   'cd_status': 'LC',
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'comments': 'a comment as replacement',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasThreatStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://colsplist.herokuapp.com | '
    ##            'https://www.afalsesiteasanexample.com',
    ##   'matchedname': 'Invented species',
    ##   'references': 'A second reference just for fun! | Bottin et al, 2022. False '
    ##                 'paper to show an example | Fake report to put Invented '
    ##                 'species as LC',
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cd_status': 'CR',
    ##   'cd_tax': 3838,
    ##   'cd_tax_acc': 3838,
    ##   'comments': 'threat evaluation methodology 2: None, this is still only a '
    ##               'fake species! | a comment to add',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasThreatStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://colsplist.herokuapp.com',
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                 'reference just for fun! | Bottin, 2025. New fake reference '
    ##                 'with a weird date | Bottin, 2026. New fake reference with a '
    ##                 'weirder date | Another fake report',
    ##   'syno': False}]

``` python
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
```

    ## [{'cd_ref': 311, 'cd_tax': 3833},
    ##  {'cd_ref': 315, 'cd_tax': 3833},
    ##  {'cd_tax': 3838, 'delete_status': True}]

``` python
pp(requests.delete(api_url + '/manageThreat/list',json={'list':deletions},auth=authTokenEditUser).json())
```

    ## [{'cd_refs': [311], 'cd_tax': 3833},
    ##  {'cd_refs': [315], 'cd_tax': 3833},
    ##  {'cd_refs': [311, 312, 313, 314, 316], 'cd_tax': 3838}]

``` python
pp(requests.post(api_url+'/testThreat/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())
```

    ## [{'acceptedname': 'Invented species (marius 2005)',
    ##   'alreadyInDb': True,
    ##   'cd_status': 'LC',
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'comments': 'a comment as replacement',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasThreatStatus': True,
    ##   'insertedTax': [],
    ##   'links': None,
    ##   'matchedname': 'Invented species',
    ##   'references': 'A second reference just for fun!',
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cd_status': None,
    ##   'cd_tax': 3838,
    ##   'cd_tax_acc': 3838,
    ##   'comments': None,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasThreatStatus': False,
    ##   'insertedTax': [],
    ##   'links': None,
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'references': None,
    ##   'syno': False}]

### Cleaning

``` python
pp(requests.delete(api_url + '/cleanDb',json={'status_no_ref':True,'ref_no_status':True},auth=authTokenEditUser).json())
```

    ## {'cd_refs': [313, 311, 312, 314, 315, 316], 'cd_status': [], 'cd_taxs': []}

``` python
pp(requests.delete(api_url + '/manageTaxo', json={'cd_tax':newSpecies_cd_tax[1]}, auth=authTokenEditUser).json())
```

    ## {'cd_children': [3838], 'cd_synos': [], 'cd_tax': 3838}

## Endpoint /ManageExot

``` python
endpoint='/manageExot'
```

### POST: adding alien-invasive species and/or the associated bibliographic references

The formally required arguments to post an alien-invasive status are:

-   **is_alien**: a boolean(verdadero/falso) decribing the alien
    character of the species for Colombia
-   **is_invasive**: a boolean(verdadero/falso) decribing the invasive
    character of the species for Colombia
-   **ref_citation**: A list of bibliographic references associated with
    the alien-invasive status.

However, of course you will need at least one of ‘canonicalname’,
‘scientificname’ or ‘gbifkey’, for the API to know which taxon the
alien-invasive status refer to…

#### Adding a status to an existing species

Let’s add an alien-invasive status to the virtual species we invented
(‘Invented species’)

``` python
status1={'canonicalname':'Invented species',
  'is_alien': True,
  'is_invasive': False,
  'ref_citation':['Bottin et al, 2022. False paper to show an example','A second reference just for fun!'],
  'link':['https://colsplist.herokuapp.com',' '],
  'comments':'This is a first comment | Feeding habits: Does not eat at all!'}
res=requests.post(api_url+endpoint,json=status1,auth= authTokenEditUser)
pp(res.json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cdRefs': [317, 300],
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [],
    ##  'matchedname': 'Invented species',
    ##  'syno': False}

Now, if we use the /testExot endpoint for this species, we will obtain:

``` python
res=requests.get(api_url+'/testExot',json={'canonicalname':'Invented species'})
pp(res.json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasExotStatus': True,
    ##  'insertedTax': [],
    ##  'is_alien': True,
    ##  'is_invasive': False,
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Invented species',
    ##  'references': 'A second reference just for fun! | Bottin et al, 2022. False '
    ##                'paper to show an example',
    ##  'syno': False}

#### Adding a status and a species in one command

Let’s invent a new species again : “Newspecies nonexistens”, it will
have an “Exotic”:

``` python
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
```

    ## {'acceptedname': None,
    ##  'alreadyInDb': False,
    ##  'cdRefs': [317, 318],
    ##  'cd_tax': 3839,
    ##  'cd_tax_acc': 3839,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [3839],
    ##  'matchedname': None,
    ##  'syno': False}

#### What if the status already exists in the database

When the status already exists in the database, the behavior of the API
depends on 2 parameters:

-   priority: if ‘high’, the previous status is replaced, references are
    added (old references are kept anyway). I ‘low’ the previous status
    is kept, references are added.
-   replace_comment: if True, the comments provided replace the old
    comments, otherwise comments are added to the existing ones (with a
    ‘\|’ separator)

Note that:

-   the most logical cases are Priority:low + replace_comment:False or
    priority:high, replace_comment:True, but you might as well use
    priority and replace_comment independently to each other.
-   There is no way to avoid that comments are either added or replacing
    old ones. So if you want to avoid comments to be inserted when the
    status already exists you will have to first test whether the
    statuses exist before sending data to the post method (with the
    ‘/testExot(/list)’ endpoint: see
    <https://github.com/marbotte/colSpList/blob/main/usage/testAndExamples/basic_getEndpoints_functionality.md#testthreat>).
-   If priority is None (or is not provided by the user) and the status
    of the species is the same than in the database, the references and
    comment are added (with the method replace_comment or not) and no
    error is sent
-   If priority is None (or is not provided by the user) and the status
    of the species different, an error is sent and no modification is
    made in the database.

##### example 1: priority:low, replace_comment:False

Let’s say that we send again a status for the species *Newspecies
nonexistens*, this time “Almost endemic”, with the new reference:
“Bottin, 2025. New fake reference with a weird date”, and the comments.
“endemism evaluation methodology: None, this is only a fake species!”

As a reminder, here is the current status of the species:

``` python
res=requests.get(api_url+'/testExot',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())
```

    ## {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##  'alreadyInDb': True,
    ##  'cd_tax': 3839,
    ##  'cd_tax_acc': 3839,
    ##  'comments': 'random comment | repartition: nula',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasExotStatus': True,
    ##  'insertedTax': [],
    ##  'is_alien': False,
    ##  'is_invasive': True,
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Newspecies nonexistens',
    ##  'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                'reference just for fun!',
    ##  'syno': False}

Now we modify it with:

``` python
status4={'canonicalname':'Newspecies nonexistens',
  'is_alien':False,
  'is_invasive':False,
  'comments':'invasive evaluation methodology: None, this is only a fake species!',
  'ref_citation':['Bottin, 2025. New fake reference with a weird date'],
  'priority':'low',
  'replace_comment':False
}
pp(requests.post(api_url+'/manageExot',json=status4,auth=authTokenEditUser).json())
```

    ## {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##  'alreadyInDb': True,
    ##  'cdRefs': [319],
    ##  'cd_tax': 3839,
    ##  'cd_tax_acc': 3839,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [],
    ##  'matchedname': 'Newspecies nonexistens',
    ##  'syno': False}

The new endemism status is:

``` python
res=requests.get(api_url+'/testExot',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())
```

    ## {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##  'alreadyInDb': True,
    ##  'cd_tax': 3839,
    ##  'cd_tax_acc': 3839,
    ##  'comments': 'random comment | repartition: nula | invasive evaluation '
    ##              'methodology: None, this is only a fake species!',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasExotStatus': True,
    ##  'insertedTax': [],
    ##  'is_alien': False,
    ##  'is_invasive': True,
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Newspecies nonexistens',
    ##  'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                'reference just for fun! | Bottin, 2025. New fake reference '
    ##                'with a weird date',
    ##  'syno': False}

As you can see:

-   new reference was added
-   new comment was added
-   invasive status stayed the same

##### example 2: priority: high, replace_comment:True

``` python
status5={'canonicalname':'Newspecies nonexistens',
  'is_alien':False,
  'is_invasive':False,
  'comments':'invasive evaluation methodology 2: None, this is still only a fake species!',
  'ref_citation':['Bottin, 2026. New fake reference with a weirder date'],
  'priority':'high',
  'replace_comment':True
}
pp(requests.post(api_url+'/manageExot',json=status5,auth=authTokenEditUser).json())
```

    ## {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##  'alreadyInDb': True,
    ##  'cdRefs': [320],
    ##  'cd_tax': 3839,
    ##  'cd_tax_acc': 3839,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'insertedTax': [],
    ##  'matchedname': 'Newspecies nonexistens',
    ##  'syno': False}

``` python
res=requests.get(api_url+'/testExot',json={'canonicalname':'Newspecies nonexistens'})
pp(res.json())
```

    ## {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##  'alreadyInDb': True,
    ##  'cd_tax': 3839,
    ##  'cd_tax_acc': 3839,
    ##  'comments': 'invasive evaluation methodology 2: None, this is still only a '
    ##              'fake species!',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasExotStatus': True,
    ##  'insertedTax': [],
    ##  'is_alien': False,
    ##  'is_invasive': False,
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Newspecies nonexistens',
    ##  'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                'reference just for fun! | Bottin, 2025. New fake reference '
    ##                'with a weird date | Bottin, 2026. New fake reference with a '
    ##                'weirder date',
    ##  'syno': False}

As you can see:

-   new reference was added
-   comments were replaced
-   invasive status changed into False

### PUT: modify a status

The PUT method here is exactly the same than the POST method with
‘priority’:‘high’. The only difference is that it will send an error if
the status does not exist. The rationale is that they are used in
different context. The POST method is used when a new dataset is
available, and people want to update the information on the API, while
the PUT method is used when some errors or inconsistencies are found in
the API data…

Imagine that we found new data for ‘Invented species’: it is now
accepted in the literature as invasive

``` python
res=requests.get(api_url+'/testExot',json={'canonicalname':'Invented species'})
pp(res.json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasExotStatus': True,
    ##  'insertedTax': [],
    ##  'is_alien': True,
    ##  'is_invasive': False,
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Invented species',
    ##  'references': 'A second reference just for fun! | Bottin et al, 2022. False '
    ##                'paper to show an example',
    ##  'syno': False}

``` python
cd_tax=res.json().get('cd_tax_acc')
```

``` python
status6={'cd_tax':cd_tax,
  'is_alien':True,
  'is_invasive':True,
  'ref_citation':['Bottin, 2051. New fake reference with the weirdest date'],
}
pp(requests.put(api_url+'/manageExot',json=status6,auth=authTokenEditUser).json())
```

    ## {'cdRefs': [321], 'cd_tax': 3833}

``` python
res=requests.get(api_url+'/testExot',json={'canonicalname':'Invented species'})
pp(res.json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasExotStatus': True,
    ##  'insertedTax': [],
    ##  'is_alien': True,
    ##  'is_invasive': True,
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Invented species',
    ##  'references': 'A second reference just for fun! | Bottin et al, 2022. False '
    ##                'paper to show an example | Bottin, 2051. New fake reference '
    ##                'with the weirdest date',
    ##  'syno': False}

### DELETE: suppress a reference associated with a status, or the status itself

The DELETE method, by default, concerns the references associated to a
status. If what you want to delete is the status, you have to use the
‘delete_status’ argument.

#### Deleting an association between a taxon status and a reference

The first thing to do is to search for the cd_ref and cd_tax
corresponding respectively to the reference and the taxon.

In order to suppress the association between the reference ‘Bottin et
al, 2022. False paper to show an example’ and the taxon ‘Invented
species’, here is the way to search for the codes automatically:

``` python
listRef=requests.get(api_url+'/listReferences').json()
cd_ref = [r['cd_ref'] for r in listRef if r['ref_citation']=='Bottin et al, 2022. False paper to show an example'][0]
pp(cd_ref)
```

    ## 317

``` python
cd_tax=requests.get(api_url+'/tax',json={'canonicalname':'Invented species'}).json()['cd_tax']
pp(cd_tax)
```

    ## 3833

Let’s take a look at the alien-invasive status of *Invented species*.

``` python
pp(requests.get(api_url+'/testExot',json={'canonicalname':'Invented species'}).json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasExotStatus': True,
    ##  'insertedTax': [],
    ##  'is_alien': True,
    ##  'is_invasive': True,
    ##  'links': 'https://colsplist.herokuapp.com',
    ##  'matchedname': 'Invented species',
    ##  'references': 'A second reference just for fun! | Bottin et al, 2022. False '
    ##                'paper to show an example | Bottin, 2051. New fake reference '
    ##                'with the weirdest date',
    ##  'syno': False}

Here to suppress the association:

``` python
res=requests.delete(api_url+'/manageExot', json={'cd_tax':cd_tax,'cd_ref':cd_ref},auth=authTokenEditUser)
pp(res.json())
```

    ## {'cd_refs': [317], 'cd_tax': 3833}

``` python
pp(requests.get(api_url+'/testExot',json={'canonicalname':'Invented species'}).json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasExotStatus': True,
    ##  'insertedTax': [],
    ##  'is_alien': True,
    ##  'is_invasive': True,
    ##  'links': None,
    ##  'matchedname': 'Invented species',
    ##  'references': 'A second reference just for fun! | Bottin, 2051. New fake '
    ##                'reference with the weirdest date',
    ##  'syno': False}

#### Deleting an association between a taxon status and a reference

If the delete method is called only with a cd_tax here is what happens:

``` python
pp(requests.delete(api_url + '/manageExot',json={'cd_tax':cd_tax},auth=authTokenEditUser).json())
```

    ## {'error': "Do you want to suppress the status ('delete_status'=True) or just a "
    ##           "reference associated with the status (provide 'cd_ref')?, missing "
    ##           "argument: 'cd_ref' or 'delete_status'"}

As said, to delete the endemic status of ‘Invented species’, what should
be done is:

``` python
pp(requests.delete(api_url + '/manageExot',json={'cd_tax':cd_tax,'delete_status':True},auth=authTokenEditUser).json())
```

    ## {'cd_refs': [300, 321], 'cd_tax': 3833}

``` python
pp(requests.get(api_url+'/testExot',json={'canonicalname':'Invented species'}).json())
```

    ## {'acceptedname': 'Invented species (marius 2005)',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': None,
    ##  'cd_tax': 3833,
    ##  'cd_tax_acc': 3833,
    ##  'comments': None,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasExotStatus': False,
    ##  'insertedTax': [],
    ##  'is_alien': None,
    ##  'is_invasive': None,
    ##  'links': None,
    ##  'matchedname': 'Invented species',
    ##  'references': None,
    ##  'syno': False}

### Cleaning

**Species to suppress**:

‘Newspecies nonexistens’

**References to suppress**:

‘Bottin et al, 2022. False paper to show an example’,‘A second reference
just for fun!’,‘A third reference just for fun!’,‘Bottin, 2025. New fake
reference with a weird date’,‘Bottin, 2026. New fake reference with a
weirder date’,‘Bottin, 2051. New fake reference with the weirdest date’

``` python
cd_tax_ToDel=requests.get(api_url + '/tax',json={'canonicalname':'Newspecies nonexistens'}).json().get('cd_tax')
requests.delete(api_url+'/manageTaxo',json={'cd_tax':cd_tax_ToDel},auth=authTokenEditUser)
```

    ## <Response [200]>

``` python
cd_tax_StatusToDel=requests.get(api_url + '/testExot',json={'canonicalname':'Invented species'}).json().get('cd_tax')
res=requests.delete(api_url+'/manageExot',json={'cd_tax':cd_tax_StatusToDel, 'delete_status':True}, auth=authTokenEditUser)
res=requests.delete(api_url+'/cleanDb',json={'ref_no_status':True}, auth=authTokenEditUser)
```

## Endpoint /manageExot/list

The endpoint /manageExot/list works exactly like the endpoint
/manageExot, except that all the insertions, modifications or deletions
may be done at once with a list.

### POST

See explanation in section POST of the /manageExot endpoint.

We will show here how to post multiple statuses in a single call to the
API.

Of course, many of these statuses concern the species “Newspecies
nonexistens”, which is not the intended objective of the multiple
version in the endpoint /manageExot/list, but the objective here is to
show a proof of concept…

``` python
statuses=[status1,status2,status4,status5]
pp(statuses)
```

    ## [{'canonicalname': 'Invented species',
    ##   'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##   'is_alien': True,
    ##   'is_invasive': False,
    ##   'link': ['https://colsplist.herokuapp.com', ' '],
    ##   'ref_citation': ['Bottin et al, 2022. False paper to show an example',
    ##                    'A second reference just for fun!']},
    ##  {'authorship': '(marius 2022)',
    ##   'canonicalname': 'Newspecies nonexistens',
    ##   'comments': 'random comment | repartition: nula',
    ##   'is_alien': False,
    ##   'is_invasive': True,
    ##   'link': ['https://colsplist.herokuapp.com', ' '],
    ##   'parentcanonicalname': 'Invented',
    ##   'ref_citation': ['Bottin et al, 2022. False paper to show an example',
    ##                    'A third reference just for fun!'],
    ##   'scientificname': 'Newspecies nonexistens (marius 2022)'},
    ##  {'canonicalname': 'Newspecies nonexistens',
    ##   'comments': 'invasive evaluation methodology: None, this is only a fake '
    ##               'species!',
    ##   'is_alien': False,
    ##   'is_invasive': False,
    ##   'priority': 'low',
    ##   'ref_citation': ['Bottin, 2025. New fake reference with a weird date'],
    ##   'replace_comment': False},
    ##  {'canonicalname': 'Newspecies nonexistens',
    ##   'comments': 'invasive evaluation methodology 2: None, this is still only a '
    ##               'fake species!',
    ##   'is_alien': False,
    ##   'is_invasive': False,
    ##   'priority': 'high',
    ##   'ref_citation': ['Bottin, 2026. New fake reference with a weirder date'],
    ##   'replace_comment': True}]

``` python
res=requests.post(api_url + '/manageExot/list',json={'list':statuses},auth=authTokenEditUser)
pp(res.json())
```

    ## [{'acceptedname': 'Invented species (marius 2005)',
    ##   'alreadyInDb': True,
    ##   'cdRefs': [322, 300],
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [],
    ##   'matchedname': 'Invented species',
    ##   'syno': False},
    ##  {'acceptedname': None,
    ##   'alreadyInDb': False,
    ##   'cdRefs': [322, 323],
    ##   'cd_tax': 3840,
    ##   'cd_tax_acc': 3840,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [3840],
    ##   'matchedname': None,
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cdRefs': [324],
    ##   'cd_tax': 3840,
    ##   'cd_tax_acc': 3840,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [],
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cdRefs': [325],
    ##   'cd_tax': 3840,
    ##   'cd_tax_acc': 3840,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'insertedTax': [],
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'syno': False}]

### PUT

We will show here how to modify multiple statuses in a single call to
the API.

``` python
newSpecies=requests.post(api_url+'/testExot/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json()
pp(newSpecies)
```

    ## [{'acceptedname': 'Invented species (marius 2005)',
    ##   'alreadyInDb': True,
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'comments': 'This is a first comment | Feeding habits: Does not eat at all!',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasExotStatus': True,
    ##   'insertedTax': [],
    ##   'is_alien': True,
    ##   'is_invasive': False,
    ##   'links': 'https://colsplist.herokuapp.com',
    ##   'matchedname': 'Invented species',
    ##   'references': 'A second reference just for fun! | Bottin et al, 2022. False '
    ##                 'paper to show an example',
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cd_tax': 3840,
    ##   'cd_tax_acc': 3840,
    ##   'comments': 'invasive evaluation methodology 2: None, this is still only a '
    ##               'fake species!',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasExotStatus': True,
    ##   'insertedTax': [],
    ##   'is_alien': False,
    ##   'is_invasive': False,
    ##   'links': 'https://colsplist.herokuapp.com',
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                 'reference just for fun! | Bottin, 2025. New fake reference '
    ##                 'with a weird date | Bottin, 2026. New fake reference with a '
    ##                 'weirder date',
    ##   'syno': False}]

``` python
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
```

    ## {'list': [{'cd_tax': 3833,
    ##            'comments': 'a comment as replacement',
    ##            'is_alien': True,
    ##            'is_invasive': True,
    ##            'link': ['https://www.afalsesiteasanexample.com'],
    ##            'ref_citation': ['Fake report to put Invented species as invasive'],
    ##            'replace_comment': True},
    ##           {'cd_tax': 3840,
    ##            'comments': 'a comment to add',
    ##            'is_alien': True,
    ##            'is_invasive': False,
    ##            'ref_citation': ['Another fake report']}]}

``` python
modifs=requests.put(api_url + '/manageExot/list',json=modifications,auth=authTokenEditUser).json()
pp(modifs)
```

    ## [{'cdRefs': [326], 'cd_tax': 3833}, {'cdRefs': [327], 'cd_tax': 3840}]

``` python
pp(requests.post(api_url+'/testExot/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())
```

    ## [{'acceptedname': 'Invented species (marius 2005)',
    ##   'alreadyInDb': True,
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'comments': 'a comment as replacement',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasExotStatus': True,
    ##   'insertedTax': [],
    ##   'is_alien': True,
    ##   'is_invasive': True,
    ##   'links': 'https://colsplist.herokuapp.com | '
    ##            'https://www.afalsesiteasanexample.com',
    ##   'matchedname': 'Invented species',
    ##   'references': 'A second reference just for fun! | Bottin et al, 2022. False '
    ##                 'paper to show an example | Fake report to put Invented '
    ##                 'species as invasive',
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cd_tax': 3840,
    ##   'cd_tax_acc': 3840,
    ##   'comments': 'invasive evaluation methodology 2: None, this is still only a '
    ##               'fake species! | a comment to add',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasExotStatus': True,
    ##   'insertedTax': [],
    ##   'is_alien': True,
    ##   'is_invasive': False,
    ##   'links': 'https://colsplist.herokuapp.com',
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                 'reference just for fun! | Bottin, 2025. New fake reference '
    ##                 'with a weird date | Bottin, 2026. New fake reference with a '
    ##                 'weirder date | Another fake report',
    ##   'syno': False}]

### DELETE

We will show here how to delete multiple references/statuses in a single
call to the API.

We will suppress the references ‘Bottin et al, 2022. False paper to show
an example’ and ‘Fake report to put Invented species as invasive’ as
justifications for *Invented species*, and delete the endemic status for
*Newspecies nonexistens*

``` python
pp(requests.post(api_url+'/testExot/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())
```

    ## [{'acceptedname': 'Invented species (marius 2005)',
    ##   'alreadyInDb': True,
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'comments': 'a comment as replacement',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasExotStatus': True,
    ##   'insertedTax': [],
    ##   'is_alien': True,
    ##   'is_invasive': True,
    ##   'links': 'https://colsplist.herokuapp.com | '
    ##            'https://www.afalsesiteasanexample.com',
    ##   'matchedname': 'Invented species',
    ##   'references': 'A second reference just for fun! | Bottin et al, 2022. False '
    ##                 'paper to show an example | Fake report to put Invented '
    ##                 'species as invasive',
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cd_tax': 3840,
    ##   'cd_tax_acc': 3840,
    ##   'comments': 'invasive evaluation methodology 2: None, this is still only a '
    ##               'fake species! | a comment to add',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasExotStatus': True,
    ##   'insertedTax': [],
    ##   'is_alien': True,
    ##   'is_invasive': False,
    ##   'links': 'https://colsplist.herokuapp.com',
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'references': 'Bottin et al, 2022. False paper to show an example | A third '
    ##                 'reference just for fun! | Bottin, 2025. New fake reference '
    ##                 'with a weird date | Bottin, 2026. New fake reference with a '
    ##                 'weirder date | Another fake report',
    ##   'syno': False}]

``` python
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
```

    ## [{'cd_ref': 322, 'cd_tax': 3833},
    ##  {'cd_ref': 326, 'cd_tax': 3833},
    ##  {'cd_tax': 3840, 'delete_status': True}]

``` python
pp(requests.delete(api_url + '/manageExot/list',json={'list':deletions},auth=authTokenEditUser).json())
```

    ## [{'cd_refs': [322], 'cd_tax': 3833},
    ##  {'cd_refs': [326], 'cd_tax': 3833},
    ##  {'cd_refs': [322, 323, 324, 325, 327], 'cd_tax': 3840}]

``` python
pp(requests.post(api_url+'/testExot/list',json={'list':[{'canonicalname':'Invented species'},{'canonicalname':'Newspecies nonexistens'}]}).json())
```

    ## [{'acceptedname': 'Invented species (marius 2005)',
    ##   'alreadyInDb': True,
    ##   'cd_tax': 3833,
    ##   'cd_tax_acc': 3833,
    ##   'comments': 'a comment as replacement',
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasExotStatus': True,
    ##   'insertedTax': [],
    ##   'is_alien': True,
    ##   'is_invasive': True,
    ##   'links': None,
    ##   'matchedname': 'Invented species',
    ##   'references': 'A second reference just for fun!',
    ##   'syno': False},
    ##  {'acceptedname': 'Newspecies nonexistens (marius 2022)',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': None,
    ##   'cd_tax': 3840,
    ##   'cd_tax_acc': 3840,
    ##   'comments': None,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasExotStatus': False,
    ##   'insertedTax': [],
    ##   'is_alien': None,
    ##   'is_invasive': None,
    ##   'links': None,
    ##   'matchedname': 'Newspecies nonexistens',
    ##   'references': None,
    ##   'syno': False}]

### Cleaning

``` python
pp(requests.delete(api_url + '/cleanDb',json={'status_no_ref':True},auth=authTokenEditUser).json())
```

    ## {'cd_refs': [], 'cd_status': [], 'cd_taxs': []}

``` python
pp(requests.delete(api_url + '/manageTaxo', json={'cd_tax':newSpecies_cd_tax[1]}, auth=authTokenEditUser).json())
```

    ## {'cd_children': [3840], 'cd_synos': [], 'cd_tax': 3840}

# Endpoint /manageRef : modifying and supressing references

## PUT:modifying the references

Here are the references ‘A second reference just for fun!’, ‘A third
reference just for fun!’ and ‘Bottin et al, 2022. False paper to show an
example’:

``` python
listRef=requests.get(api_url+'/listReferences').json()
refToModify=[r for r in listRef if r['ref_citation'] in ['A second reference just for fun!', 'A third reference just for fun!', 'Bottin et al, 2022. False paper to show an example']]
pp(refToModify)
```

    ## [{'cd_ref': 300,
    ##   'link': None,
    ##   'nb_endem': 1,
    ##   'nb_exot': 1,
    ##   'nb_threat': 1,
    ##   'ref_citation': 'A second reference just for fun!'},
    ##  {'cd_ref': 322,
    ##   'link': 'https://colsplist.herokuapp.com',
    ##   'nb_endem': 0,
    ##   'nb_exot': 0,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Bottin et al, 2022. False paper to show an example'},
    ##  {'cd_ref': 323,
    ##   'link': None,
    ##   'nb_endem': 0,
    ##   'nb_exot': 0,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'A third reference just for fun!'}]

We can modify by changing the description:

``` python
pp(requests.put(api_url + '/manageRef', json={'cd_ref':refToModify[0]['cd_ref'],'reference':'New text for the ref'}, auth=authTokenEditUser).json())
```

    ## None

We can modify by changing the link:

``` python
pp(requests.put(api_url + '/manageRef', json={'cd_ref':refToModify[1]['cd_ref'],'link':'http://justanotherwebsite.com'}, auth=authTokenEditUser).json())
```

    ## None

``` python
listRef=requests.get(api_url+'/listReferences').json()
cds_ref=[r['cd_ref'] for r in refToModify]
refModified=[r for r in listRef if r['cd_ref'] in cds_ref]
pp(refModified)
```

    ## [{'cd_ref': 300,
    ##   'link': None,
    ##   'nb_endem': 1,
    ##   'nb_exot': 1,
    ##   'nb_threat': 1,
    ##   'ref_citation': 'New text for the ref'},
    ##  {'cd_ref': 322,
    ##   'link': 'http://justanotherwebsite.com',
    ##   'nb_endem': 0,
    ##   'nb_exot': 0,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Bottin et al, 2022. False paper to show an example'},
    ##  {'cd_ref': 323,
    ##   'link': None,
    ##   'nb_endem': 0,
    ##   'nb_exot': 0,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'A third reference just for fun!'}]

## DELETE: merging and/or deleting the references

Let’s imagine that we inserted the references ‘New text for the ref’ and
‘A third reference just for fun!’, but they are indeed the same
references. Then we need to delete ‘New text for the ref’, but we want
first to transfer all the status into ‘A third reference just for fun!’.
This can be done by using the following code:

``` python
cd_ref=[r['cd_ref'] for r in refModified if r['ref_citation']=='New text for the ref'][0]
mergeInto=[r['cd_ref'] for r in refModified if r['ref_citation']=='A third reference just for fun!'][0]
pp(requests.delete(api_url + '/manageRef', json={'cd_ref':cd_ref,'mergeInto':mergeInto}, auth=authTokenEditUser).json())
```

    ## None

``` python
listRef=requests.get(api_url+'/listReferences').json()
refModified=[r for r in listRef if r['cd_ref'] in cds_ref]
pp(refModified)
```

    ## [{'cd_ref': 322,
    ##   'link': 'http://justanotherwebsite.com',
    ##   'nb_endem': 0,
    ##   'nb_exot': 0,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Bottin et al, 2022. False paper to show an example'},
    ##  {'cd_ref': 323,
    ##   'link': None,
    ##   'nb_endem': 1,
    ##   'nb_exot': 1,
    ##   'nb_threat': 1,
    ##   'ref_citation': 'A third reference just for fun!'}]

You may see that all the statuses have been transfered from ‘New text
for the ref’ to ‘A third reference just for fun!’ before deleting ‘New
text for the ref’!

Now, a simple deletion without transfer may be done by:

``` python
cd_ref=[r['cd_ref'] for r in refModified if r['ref_citation']=='Bottin et al, 2022. False paper to show an example'][0]
pp(requests.delete(api_url + '/manageRef', json={'cd_ref':cd_ref}, auth=authTokenEditUser).json())
```

    ## None

``` python
listRef=requests.get(api_url+'/listReferences').json()
refModified=[r for r in listRef if r['cd_ref'] in cds_ref]
pp(refModified)
```

    ## [{'cd_ref': 323,
    ##   'link': None,
    ##   'nb_endem': 1,
    ##   'nb_exot': 1,
    ##   'nb_threat': 1,
    ##   'ref_citation': 'A third reference just for fun!'}]

# Finally : getting back to the previous state

Let’s clean the database from all the modifications:

``` python
taxToSuppList=['Invented species','Juniperus communis','Vultur fossilis','Juniperus sabina']
taxToSupp=[{'canonicalname':r} for r in taxToSuppList]
res=requests.post(api_url+'/tax/list',json={'list':taxToSupp}).json()
cd_tax_supp=[{k:v for (k,v) in r.items() if k=='cd_tax'} for r in res]
pp(requests.delete(api_url+'/manageTaxo/list',json={'list':cd_tax_supp},auth=authTokenEditUser).json())
```

    ## [{'cd_children': [3833], 'cd_synos': [], 'cd_tax': 3833},
    ##  {'cd_children': [3831], 'cd_synos': [], 'cd_tax': 3831},
    ##  {'cd_children': [3830], 'cd_synos': [], 'cd_tax': 3830},
    ##  {'cd_children': [3828], 'cd_synos': [], 'cd_tax': 3828}]

``` python
pp(requests.delete(api_url+'/cleanDb',json={'status_no_ref':True,'ref_no_status':True,
'syno_no_tax':True,'tax_no_status':True},auth=authTokenEditUser).json())
```

    ## {'cd_refs': [323, 324, 325, 326, 327],
    ##  'cd_status': [],
    ##  'cd_taxs': [3825, 3827, 3832]}

Here, I will delete the users that were created for this document and
give back the previous password to the ‘admin’ user:

``` python
endpoint="/admin/users"
# Deleting the users created for this document
userToDel={'username':'editUser'}
res=requests.delete(api_url+endpoint,json=userToDel,auth=authAdmin)
pp(res.json())
```

    ## {'uid': 24, 'username': 'editUser'}

``` python
endpoint="/user"
res=requests.put(api_url+endpoint,json={'newPassword':codeAdmin},auth=authTokenAdmin)
pp(res.json())
```

    ## 1
