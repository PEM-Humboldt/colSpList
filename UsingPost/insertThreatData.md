Inserting threatened species with the colSpList API
================

In order to show how to work with the colSpList API and the threatened
species, we will use the species list from the official “Resolución 1912
de 2017, from the Colombian ministry of environment (publicly available
at
<https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads>)

# 1 Basic usage : example of one only species

The first species of the list is *Philonotis striatula* Jaeger, 1875 and
has the “VU” (vulnerable) status.

In order to send the status to the database, we use a json “dictionary”
with the following elements:

-   the identification of the species, with either:
    -   *gbifkey* : integer corresponding to the taxonKey used in GBIF
    -   *scientificname* : string corresponding to the scientificName in
        the GBIF backbone
    -   *canonicalname* : string corresponding to the canonicalName in
        the GBIF backbone (formally, it is better to use the
        canonicalNameWithMarker) used by the name parser of the GBIF
        backbone)
-   *threatstatus* : the status level as defined by the IUCN
-   *ref_citation* : a list of the references on which are based the
    inclusion of the taxon and its threatened status in the API
-   *link* : a list of the url links (corresponding in length and order
    to the *ref_citation*)
-   *comments* : comment on the threatened status of the taxon

## 1.1 In R

``` r
require(httr)
```

    ## Loading required package: httr

``` r
require(jsonify)
```

    ## Loading required package: jsonify

``` r
sendJson <- to_json(list(gbifkey = as.integer(2676236), threatstatus = "VU", ref_citation = list("Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz"),link =list( "https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads" )),unbox=T)
baseURL <- 'http://localhost:5000'
baseResource <- "insertThreat"
POST(paste(baseURL,baseResource,sep="/"),body=sendJson, content_type("application/json"))
```

    ## Response [http://localhost:5000/insertThreat]
    ##   Date: 2022-02-24 17:32
    ##   Status: 200
    ##   Content-Type: application/json
    ##   Size: 34 B
    ## {"id_tax": 1862, "cdRefs": [216]}

## 1.2 In python

``` python
import requests
import json
from flask import jsonify
url = 'http://localhost:5000/insertThreat'
dictTosend = {"gbifkey": 2676236, "threatstatus": "VU", "ref_citation":["Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz"],"link": ["https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads"]}
x = requests.post(url, json = dictTosend)
x.json()
```

    ## {'id_tax': 1862, 'cdRefs': [216]}

# 2 A list of species and their status

In order to insert all the taxa in one script, using the same POST
endpoint of the API (another endpoint will come later, allowing to post
directly a list of species and their statuses), we may use the following
codes.

Note that since the “distribution.txt” file included in the dataset
includes the gbif codes, we do not need to use the “taxon.txt” file

In the examples here, we will simply exclude the 2 taxa which are
referenced from EOL

## 2.1 In R

``` r
file = "../../data/dwca-resolucion1912-2017mads-v2.5/distribution.txt"
listSpThreat <- read.csv(file,sep="\t")
regexExtractGbifkey <- "^gbif\\.org/species/([0-9]+)$"
listSpThreat <- listSpThreat [grepl(regexExtractGbifkey,listSpThreat$id),]
tabToSend <- data.frame(gbifkey = as.integer(sub(regexExtractGbifkey,"\\1",listSpThreat$id)), threatstatus= listSpThreat$threatStatus)
res = apply(tabToSend,1,function(x,bU,bR,ref,link)
  {sendJson = to_json(list(gbifkey=x[1],threatstatus=x[2],ref_citation = list(ref),link = list(link)),unbox = T)
  return(POST(paste(bU,bR,sep="/"),body=sendJson, content_type("application/json")))
  },
  bU=baseURL,
  bR=baseResource,
  ref="Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz",
  link = "https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads" )
```

<!--
## In python

```python
import csv
import pandas as pd
import re
file = "../data/dwca-resolucion1912-2017mads-v2.5/distribution.txt"
def readAndInsertApi()
listSpStatus = pd.read_csv(file, sep='\t')

  
```

-->

# 3 problems

``` r
pbs <- !sapply(res,function(x)"id_tax"%in%names(content(x)))
sum(pbs)
```

    ## [1] 0
