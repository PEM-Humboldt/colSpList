Functionality tests and examples for the colSpListAPI: basic query
endpoints
================

-   [1 /testEndem](#testendem)
    -   [1.1 GET](#get)
        -   [1.1.1 Species with an endemic
            status](#species-with-an-endemic-status)
        -   [1.1.2 Species without an endemic
            status](#species-without-an-endemic-status)
        -   [1.1.3 Error: no sufficient information
            given](#error-no-sufficient-information-given)
-   [2 /testEndem/list](#testendemlist)
    -   [2.1 POST](#post)
-   [3 /testExot](#testexot)
    -   [3.1 GET](#get-1)
        -   [3.1.1 Species with an exotic
            status](#species-with-an-exotic-status)
        -   [3.1.2 Species without an exotic
            status](#species-without-an-exotic-status)
        -   [3.1.3 Error: no sufficient information
            given](#error-no-sufficient-information-given-1)
-   [4 /testExot/list](#testexotlist)
    -   [4.1 POST](#post-1)
-   [5 /testThreat](#testthreat)
    -   [5.1 GET](#get-2)
        -   [5.1.1 Species with an threatened
            status](#species-with-an-threatened-status)
        -   [5.1.2 Species without an threatened
            status](#species-without-an-threatened-status)
        -   [5.1.3 Error: no sufficient information
            given](#error-no-sufficient-information-given-2)
-   [6 /testThreat/list](#testthreatlist)
    -   [6.1 POST](#post-2)
-   [7 /listEndem](#listendem)
    -   [7.1 GET](#get-3)
        -   [7.1.1 Comprehensive list](#comprehensive-list)
        -   [7.1.2 Only the passerine birds](#only-the-passerine-birds)
        -   [7.1.3 Error: asking for an unknown
            group](#error-asking-for-an-unknown-group)
-   [8 /listExot](#listexot)
    -   [8.1 GET](#get-4)
        -   [8.1.1 Comprehensive list](#comprehensive-list-1)
        -   [8.1.2 Only the passerine
            birds](#only-the-passerine-birds-1)
        -   [8.1.3 Error: asking for an unknown
            group](#error-asking-for-an-unknown-group-1)
-   [9 /listThreat](#listthreat)
    -   [9.1 GET](#get-5)
        -   [9.1.1 Comprehensive list](#comprehensive-list-2)
        -   [9.1.2 Only the passerine
            birds](#only-the-passerine-birds-2)
        -   [9.1.3 Error: asking for an unknown
            group](#error-asking-for-an-unknown-group-2)
-   [10 /tax](#tax)
    -   [10.1 GET](#get-6)
        -   [10.1.1 From the cd_tax](#from-the-cd_tax)
        -   [10.1.2 From a scientific name](#from-a-scientific-name)
        -   [10.1.3 From a canonical name](#from-a-canonical-name)
        -   [10.1.4 Species which is not in
            database](#species-which-is-not-in-database)
        -   [10.1.5 Species which does not
            exist](#species-which-does-not-exist)
-   [11 /listTax](#listtax)
    -   [11.1 GET](#get-7)
        -   [11.1.1 Comprehensive list](#comprehensive-list-3)
        -   [11.1.2 Only the Bivalve](#only-the-bivalve)
-   [12 /listReferences](#listreferences)
    -   [12.1 GET](#get-8)
        -   [12.1.1 Comprehensive list](#comprehensive-list-4)
        -   [12.1.2 Only the references concerning exotic
            species](#only-the-references-concerning-exotic-species)
        -   [12.1.3 Only the references concerning threatened
            species](#only-the-references-concerning-threatened-species)
        -   [12.1.4 Only the references concerning endemic
            species](#only-the-references-concerning-endemic-species)

In this document, we will test the base endpoints of the colSpList API
(the endpoints which allow to query the API database).

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
api_url="http://colsplist.herokuapp.com"
```

# 1 /testEndem

## 1.1 GET

``` python
endpoint="/testEndem"
```

The /testEndem endpoint allows to search a taxon in the API database and
returns its endemism status if it has one.

### 1.1.1 Species with an endemic status

#### 1.1.1.1 From canonical name

``` python
toSend1={'canonicalname':'Accipiter collaris'}
response = requests.get(api_url+endpoint, json=toSend1)
response.json()
```

    ## {'cd_tax': 1281, 'cd_tax_acc': 1281, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Accipiter collaris', 'acceptedname': 'Accipiter collaris P.L.Sclater, 1860', 'gbifkey': 2480593, 'syno': False, 'insertedTax': [], 'hasEndemStatus': True, 'cd_nivel': 3, 'endemism': 'Casi endémica', 'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | Vertiente oriental hacia Amazonía | Perú: Amazonas (desde divisoria de aguas y principales drenajes al río Amazonas) | occurrenceRemarks: Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el Golfo de Urabá hasta la Península de La Guajira, incluyendo las estribaciones de la Sierra Nevada de Santa Marta y la Serranía de Perijá en el norte de Cesar, y como subregión |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas más al norte de la cordillera Occidental y de la cordillera Central y la ladera nororiental de la Central hacia el sur hasta aproximadamente el límite sur de Caldas |Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. cordillera Central | ', 'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue | Arbeláez-Cortés et al. 2011b | Cuervo et al. 2008a | Cuervo et al. 2008b | Merkord 2010 | Rodríguez y Rojas-Suárez 2008', 'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09'}

#### 1.1.1.2 From scientific name

``` python
toSend2={'scientificname':'Odontophorus strophium (Gould, 1844)'}
response = requests.get(api_url+endpoint, json=toSend2)
response.json()
```

    ## {'cd_tax': 1678, 'cd_tax_acc': 1678, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Odontophorus strophium (Gould, 1844)', 'acceptedname': 'Odontophorus strophium (Gould, 1844)', 'gbifkey': 5228041, 'syno': False, 'insertedTax': [], 'hasEndemStatus': True, 'cd_nivel': 4, 'endemism': 'Endémica', 'comments': 'occurrenceRemarks: Franja y región: Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Vertiente occidental de la cordillera Oriental, desde el sur de Cesar hasta Cundinamarca | ', 'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue', 'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09'}

#### 1.1.1.3 From gbifkey

``` python
toSend3={'gbifkey':2480593}
response = requests.get(api_url+endpoint, json=toSend3)
response.json()
```

    ## {'cd_tax': 1281, 'cd_tax_acc': 1281, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Accipiter collaris P.L.Sclater, 1860', 'acceptedname': 'Accipiter collaris P.L.Sclater, 1860', 'gbifkey': 2480593, 'syno': False, 'insertedTax': [], 'hasEndemStatus': True, 'cd_nivel': 3, 'endemism': 'Casi endémica', 'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | Vertiente oriental hacia Amazonía | Perú: Amazonas (desde divisoria de aguas y principales drenajes al río Amazonas) | occurrenceRemarks: Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el Golfo de Urabá hasta la Península de La Guajira, incluyendo las estribaciones de la Sierra Nevada de Santa Marta y la Serranía de Perijá en el norte de Cesar, y como subregión |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas más al norte de la cordillera Occidental y de la cordillera Central y la ladera nororiental de la Central hacia el sur hasta aproximadamente el límite sur de Caldas |Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. cordillera Central | ', 'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue | Arbeláez-Cortés et al. 2011b | Cuervo et al. 2008a | Cuervo et al. 2008b | Merkord 2010 | Rodríguez y Rojas-Suárez 2008', 'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09'}

#### 1.1.1.4 synonym of a species with an endemic status

``` python
toSend4 = {'canonicalname':'Anas andium'}
response = requests.get(api_url+endpoint, json=toSend4)
response.json()
```

    ## {'cd_tax': 1303, 'cd_tax_acc': 1302, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Anas andium', 'acceptedname': 'Anas flavirostris andium (P.L.Sclater & Salvin, 1873)', 'gbifkey': 2498068, 'syno': True, 'insertedTax': [], 'hasEndemStatus': True, 'cd_nivel': 3, 'endemism': 'Casi endémica', 'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | Perú: Andes (incluido valles interandinos) | occurrenceRemarks: Franja y región: Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. cordillera Central |Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. altiplano Cundiboyacense. | ', 'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue | Parra-Hernández et al. 2007', 'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09'}

#### 1.1.1.5 spelling error

(Accipiter coll**O**ris en lugat de Accipiter coll**A**ris)

``` python
toSend5 = {'canonicalname':'Accipiter colloris'}
response = requests.get(api_url+endpoint, json=toSend5)
response.json()
```

    ## {'cd_tax': 1281, 'cd_tax_acc': 1281, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Accipiter collaris', 'acceptedname': 'Accipiter collaris P.L.Sclater, 1860', 'gbifkey': 2480593, 'syno': False, 'insertedTax': [], 'hasEndemStatus': True, 'cd_nivel': 3, 'endemism': 'Casi endémica', 'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | Vertiente oriental hacia Amazonía | Perú: Amazonas (desde divisoria de aguas y principales drenajes al río Amazonas) | occurrenceRemarks: Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el Golfo de Urabá hasta la Península de La Guajira, incluyendo las estribaciones de la Sierra Nevada de Santa Marta y la Serranía de Perijá en el norte de Cesar, y como subregión |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas más al norte de la cordillera Occidental y de la cordillera Central y la ladera nororiental de la Central hacia el sur hasta aproximadamente el límite sur de Caldas |Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. cordillera Central | ', 'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue | Arbeláez-Cortés et al. 2011b | Cuervo et al. 2008a | Cuervo et al. 2008b | Merkord 2010 | Rodríguez y Rojas-Suárez 2008', 'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09'}

### 1.1.2 Species without an endemic status

#### 1.1.2.1 Species which is in the database but has no endemic status

``` python
toSend6={'canonicalname':'Elaeis guineensis'}
response = requests.get(api_url+endpoint, json=toSend6)
response.json()
```

    ## {'cd_tax': 62, 'cd_tax_acc': 62, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Elaeis guineensis', 'acceptedname': 'Elaeis guineensis Jacq.', 'gbifkey': 2731882, 'syno': False, 'insertedTax': [], 'hasEndemStatus': False, 'cd_nivel': None, 'descr_endem_es': None, 'comments': None, 'references': None, 'links': None}

#### 1.1.2.2 Species which is not in the database

``` python
toSend7={'canonicalname':'Espeletia grandiflora'}
response = requests.get(api_url+endpoint, json=toSend7)
response.json()
```

    ## {'cd_tax': 0, 'cd_tax_acc': 0, 'alreadyInDb': False, 'foundGbif': True, 'matchedname': 'Espeletia grandiflora', 'acceptedname': 'Espeletia grandiflora Humb. & Bonpl.', 'gbifkey': 3105059, 'syno': False, 'insertedTax': [], 'hasEndemStatus': False, 'cd_status': None, 'comments': None, 'references': [], 'links': []}

#### 1.1.2.3 Species which does not exists

``` python
toSend8={'canonicalname':'Asriwendosa machibibus'}
response = requests.get(api_url+endpoint, json=toSend8)
response.json()
```

    ## {'cd_tax': 0, 'cd_tax_acc': 0, 'alreadyInDb': False, 'foundGbif': False, 'matchedname': None, 'acceptedname': None, 'gbifkey': None, 'syno': False, 'insertedTax': [], 'hasEndemStatus': False, 'cd_status': None, 'comments': None, 'references': [], 'links': []}

### 1.1.3 Error: no sufficient information given

``` python
toSend9={}
response = requests.get(api_url+endpoint, json=toSend9)
response.json()
```

    ## {'error': "You did not provide GBIF taxon key nor name with nor without authorship, missing argument: 'scientificname', 'canonicalname' or 'gbifkey'"}

# 2 /testEndem/list

## 2.1 POST

``` python
endpoint="/testEndem/list"
```

``` python
ListToSend={'list':[toSend1,toSend2,toSend3,toSend4,toSend5,toSend6,toSend7,toSend8,toSend9]}
response = requests.post(api_url+endpoint, json=ListToSend)
response.json()
```

    ## [{'cd_tax': 1281, 'cd_tax_acc': 1281, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Accipiter collaris', 'acceptedname': 'Accipiter collaris P.L.Sclater, 1860', 'gbifkey': 2480593, 'syno': False, 'insertedTax': [], 'hasEndemStatus': True, 'cd_nivel': 3, 'endemism': 'Casi endémica', 'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | Vertiente oriental hacia Amazonía | Perú: Amazonas (desde divisoria de aguas y principales drenajes al río Amazonas) | occurrenceRemarks: Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el Golfo de Urabá hasta la Península de La Guajira, incluyendo las estribaciones de la Sierra Nevada de Santa Marta y la Serranía de Perijá en el norte de Cesar, y como subregión |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas más al norte de la cordillera Occidental y de la cordillera Central y la ladera nororiental de la Central hacia el sur hasta aproximadamente el límite sur de Caldas |Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. cordillera Central | ', 'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue | Arbeláez-Cortés et al. 2011b | Cuervo et al. 2008a | Cuervo et al. 2008b | Merkord 2010 | Rodríguez y Rojas-Suárez 2008', 'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09'}, {'cd_tax': 1678, 'cd_tax_acc': 1678, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Odontophorus strophium (Gould, 1844)', 'acceptedname': 'Odontophorus strophium (Gould, 1844)', 'gbifkey': 5228041, 'syno': False, 'insertedTax': [], 'hasEndemStatus': True, 'cd_nivel': 4, 'endemism': 'Endémica', 'comments': 'occurrenceRemarks: Franja y región: Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Vertiente occidental de la cordillera Oriental, desde el sur de Cesar hasta Cundinamarca | ', 'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue', 'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09'}, {'cd_tax': 1281, 'cd_tax_acc': 1281, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Accipiter collaris P.L.Sclater, 1860', 'acceptedname': 'Accipiter collaris P.L.Sclater, 1860', 'gbifkey': 2480593, 'syno': False, 'insertedTax': [], 'hasEndemStatus': True, 'cd_nivel': 3, 'endemism': 'Casi endémica', 'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | Vertiente oriental hacia Amazonía | Perú: Amazonas (desde divisoria de aguas y principales drenajes al río Amazonas) | occurrenceRemarks: Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el Golfo de Urabá hasta la Península de La Guajira, incluyendo las estribaciones de la Sierra Nevada de Santa Marta y la Serranía de Perijá en el norte de Cesar, y como subregión |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas más al norte de la cordillera Occidental y de la cordillera Central y la ladera nororiental de la Central hacia el sur hasta aproximadamente el límite sur de Caldas |Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. cordillera Central | ', 'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue | Arbeláez-Cortés et al. 2011b | Cuervo et al. 2008a | Cuervo et al. 2008b | Merkord 2010 | Rodríguez y Rojas-Suárez 2008', 'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09'}, {'cd_tax': 1303, 'cd_tax_acc': 1302, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Anas andium', 'acceptedname': 'Anas flavirostris andium (P.L.Sclater & Salvin, 1873)', 'gbifkey': 2498068, 'syno': True, 'insertedTax': [], 'hasEndemStatus': True, 'cd_nivel': 3, 'endemism': 'Casi endémica', 'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | Perú: Andes (incluido valles interandinos) | occurrenceRemarks: Franja y región: Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. cordillera Central |Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. altiplano Cundiboyacense. | ', 'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue | Parra-Hernández et al. 2007', 'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09'}, {'cd_tax': 1281, 'cd_tax_acc': 1281, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Accipiter collaris', 'acceptedname': 'Accipiter collaris P.L.Sclater, 1860', 'gbifkey': 2480593, 'syno': False, 'insertedTax': [], 'hasEndemStatus': True, 'cd_nivel': 3, 'endemism': 'Casi endémica', 'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | Vertiente oriental hacia Amazonía | Perú: Amazonas (desde divisoria de aguas y principales drenajes al río Amazonas) | occurrenceRemarks: Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el Golfo de Urabá hasta la Península de La Guajira, incluyendo las estribaciones de la Sierra Nevada de Santa Marta y la Serranía de Perijá en el norte de Cesar, y como subregión |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas más al norte de la cordillera Occidental y de la cordillera Central y la ladera nororiental de la Central hacia el sur hasta aproximadamente el límite sur de Caldas |Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. cordillera Central | ', 'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue | Arbeláez-Cortés et al. 2011b | Cuervo et al. 2008a | Cuervo et al. 2008b | Merkord 2010 | Rodríguez y Rojas-Suárez 2008', 'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09'}, {'cd_tax': 62, 'cd_tax_acc': 62, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Elaeis guineensis', 'acceptedname': 'Elaeis guineensis Jacq.', 'gbifkey': 2731882, 'syno': False, 'insertedTax': [], 'hasEndemStatus': False, 'cd_nivel': None, 'descr_endem_es': None, 'comments': None, 'references': None, 'links': None}, {'cd_tax': 0, 'cd_tax_acc': 0, 'alreadyInDb': False, 'foundGbif': True, 'matchedname': 'Espeletia grandiflora', 'acceptedname': 'Espeletia grandiflora Humb. & Bonpl.', 'gbifkey': 3105059, 'syno': False, 'insertedTax': [], 'hasEndemStatus': False, 'cd_status': None, 'comments': None, 'references': [], 'links': []}, {'cd_tax': 0, 'cd_tax_acc': 0, 'alreadyInDb': False, 'foundGbif': False, 'matchedname': None, 'acceptedname': None, 'gbifkey': None, 'syno': False, 'insertedTax': [], 'hasEndemStatus': False, 'cd_status': None, 'comments': None, 'references': [], 'links': []}, {'error': "You did not provide GBIF taxon key nor name with nor without authorship, missing argument: 'scientificname', 'canonicalname' or 'gbifkey'"}]

# 3 /testExot

## 3.1 GET

``` python
endpoint="/testExot"
```

The /testExot endpoint allows to search a taxon in the API database and
returns its exotic status if it has one.

### 3.1.1 Species with an exotic status

#### 3.1.1.1 From canonical name

``` python
toSend1={'canonicalname':'Gymnocorymbus ternetzi'}
response = requests.get(api_url+endpoint, json=toSend1)
response.json()
```

    ## {'cd_tax': 690, 'cd_tax_acc': 690, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Gymnocorymbus ternetzi', 'acceptedname': 'Gymnocorymbus ternetzi (Boulenger, 1895)', 'gbifkey': 2353920, 'syno': False, 'insertedTax': [], 'hasExotStatus': True, 'is_alien': True, 'is_invasive': False, 'comments': None, 'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.', 'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'}

#### 3.1.1.2 From scientific name

``` python
toSend2={'scientificname':'Rosa chinensis Jacq.'}
response = requests.get(api_url+endpoint, json=toSend2)
response.json()
```

    ## {'cd_tax': 1133, 'cd_tax_acc': 1133, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Rosa chinensis Jacq.', 'acceptedname': 'Rosa chinensis Jacq.', 'gbifkey': 3005039, 'syno': False, 'insertedTax': [], 'hasExotStatus': True, 'is_alien': True, 'is_invasive': False, 'comments': None, 'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.', 'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'}

#### 3.1.1.3 From gbifkey

``` python
toSend3={'gbifkey':5190769}
response = requests.get(api_url+endpoint, json=toSend3)
response.json()
```

    ## {'cd_tax': 959, 'cd_tax_acc': 959, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Oxychilus alliarius (J.S.Miller, 1822)', 'acceptedname': 'Oxychilus alliarius (J.S.Miller, 1822)', 'gbifkey': 5190769, 'syno': False, 'insertedTax': [], 'hasExotStatus': True, 'is_alien': True, 'is_invasive': False, 'comments': None, 'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.', 'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'}

#### 3.1.1.4 synonym of a species with an exotic status

``` python
toSend4 = {'canonicalname':'Cnidoscolus chayamansa'}
response = requests.get(api_url+endpoint, json=toSend4)
response.json()
```

    ## {'cd_tax': 479, 'cd_tax_acc': 478, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Cnidoscolus chayamansa', 'acceptedname': 'Cnidoscolus aconitifolius subsp. aconitifolius', 'gbifkey': 3073521, 'syno': True, 'insertedTax': [], 'hasExotStatus': True, 'is_alien': True, 'is_invasive': False, 'comments': None, 'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.', 'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'}

#### 3.1.1.5 spelling error

(Accipiter Rosa chin**A**nsis en lugar de Rosa chin**E**nsis)

``` python
toSend5 = {'canonicalname':'Rosa chinansis'}
response = requests.get(api_url+endpoint, json=toSend5)
response.json()
```

    ## {'cd_tax': 1133, 'cd_tax_acc': 1133, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Rosa chinensis', 'acceptedname': 'Rosa chinensis Jacq.', 'gbifkey': 3005039, 'syno': False, 'insertedTax': [], 'hasExotStatus': True, 'is_alien': True, 'is_invasive': False, 'comments': None, 'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.', 'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'}

### 3.1.2 Species without an exotic status

#### 3.1.2.1 Species which is in the database but has no exotic status

``` python
toSend6={'canonicalname':'Licania glauca'}
response = requests.get(api_url+endpoint, json=toSend6)
response.json()
```

    ## {'cd_tax': 2810, 'cd_tax_acc': 2810, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Licania glauca', 'acceptedname': 'Licania glauca Cuatrec.', 'gbifkey': 2985428, 'syno': False, 'insertedTax': [], 'hasExotStatus': False, 'cd_nivel': None, 'is_alien': None, 'is_invasive': None, 'comments': None, 'references': None, 'links': None}

#### 3.1.2.2 Species which is not in the database

``` python
toSend7={'canonicalname':'Espeletia grandiflora'}
response = requests.get(api_url+endpoint, json=toSend7)
response.json()
```

    ## {'cd_tax': 0, 'cd_tax_acc': 0, 'alreadyInDb': False, 'foundGbif': True, 'matchedname': 'Espeletia grandiflora', 'acceptedname': 'Espeletia grandiflora Humb. & Bonpl.', 'gbifkey': 3105059, 'syno': False, 'insertedTax': [], 'hasExotStatus': False, 'is_alien': None, 'is_invasive': None, 'comments': None, 'references': [], 'links': []}

#### 3.1.2.3 Species which does not exists

``` python
toSend8={'canonicalname':'Asriwendosa machibibus'}
response = requests.get(api_url+endpoint, json=toSend8)
response.json()
```

    ## {'cd_tax': 0, 'cd_tax_acc': 0, 'alreadyInDb': False, 'foundGbif': False, 'matchedname': None, 'acceptedname': None, 'gbifkey': None, 'syno': False, 'insertedTax': [], 'hasExotStatus': False, 'is_alien': None, 'is_invasive': None, 'comments': None, 'references': [], 'links': []}

### 3.1.3 Error: no sufficient information given

``` python
toSend9={}
response = requests.get(api_url+endpoint, json=toSend9)
response.json()
```

    ## {'error': "You did not provide GBIF taxon key nor name with nor without authorship, missing argument: 'scientificname', 'canonicalname' or 'gbifkey'"}

# 4 /testExot/list

## 4.1 POST

``` python
endpoint="/testExot/list"
```

``` python
ListToSend={'list':[toSend1,toSend2,toSend3,toSend4,toSend5,toSend6,toSend7,toSend8,toSend9]}
response = requests.post(api_url+endpoint, json=ListToSend)
response.json()
```

    ## [{'cd_tax': 690, 'cd_tax_acc': 690, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Gymnocorymbus ternetzi', 'acceptedname': 'Gymnocorymbus ternetzi (Boulenger, 1895)', 'gbifkey': 2353920, 'syno': False, 'insertedTax': [], 'hasExotStatus': True, 'is_alien': True, 'is_invasive': False, 'comments': None, 'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.', 'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'}, {'cd_tax': 1133, 'cd_tax_acc': 1133, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Rosa chinensis Jacq.', 'acceptedname': 'Rosa chinensis Jacq.', 'gbifkey': 3005039, 'syno': False, 'insertedTax': [], 'hasExotStatus': True, 'is_alien': True, 'is_invasive': False, 'comments': None, 'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.', 'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'}, {'cd_tax': 959, 'cd_tax_acc': 959, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Oxychilus alliarius (J.S.Miller, 1822)', 'acceptedname': 'Oxychilus alliarius (J.S.Miller, 1822)', 'gbifkey': 5190769, 'syno': False, 'insertedTax': [], 'hasExotStatus': True, 'is_alien': True, 'is_invasive': False, 'comments': None, 'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.', 'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'}, {'cd_tax': 479, 'cd_tax_acc': 478, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Cnidoscolus chayamansa', 'acceptedname': 'Cnidoscolus aconitifolius subsp. aconitifolius', 'gbifkey': 3073521, 'syno': True, 'insertedTax': [], 'hasExotStatus': True, 'is_alien': True, 'is_invasive': False, 'comments': None, 'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.', 'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'}, {'cd_tax': 1133, 'cd_tax_acc': 1133, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Rosa chinensis', 'acceptedname': 'Rosa chinensis Jacq.', 'gbifkey': 3005039, 'syno': False, 'insertedTax': [], 'hasExotStatus': True, 'is_alien': True, 'is_invasive': False, 'comments': None, 'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.', 'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'}, {'cd_tax': 2810, 'cd_tax_acc': 2810, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Licania glauca', 'acceptedname': 'Licania glauca Cuatrec.', 'gbifkey': 2985428, 'syno': False, 'insertedTax': [], 'hasExotStatus': False, 'cd_nivel': None, 'is_alien': None, 'is_invasive': None, 'comments': None, 'references': None, 'links': None}, {'cd_tax': 0, 'cd_tax_acc': 0, 'alreadyInDb': False, 'foundGbif': True, 'matchedname': 'Espeletia grandiflora', 'acceptedname': 'Espeletia grandiflora Humb. & Bonpl.', 'gbifkey': 3105059, 'syno': False, 'insertedTax': [], 'hasExotStatus': False, 'is_alien': None, 'is_invasive': None, 'comments': None, 'references': [], 'links': []}, {'cd_tax': 0, 'cd_tax_acc': 0, 'alreadyInDb': False, 'foundGbif': False, 'matchedname': None, 'acceptedname': None, 'gbifkey': None, 'syno': False, 'insertedTax': [], 'hasExotStatus': False, 'is_alien': None, 'is_invasive': None, 'comments': None, 'references': [], 'links': []}, {'error': "You did not provide GBIF taxon key nor name with nor without authorship, missing argument: 'scientificname', 'canonicalname' or 'gbifkey'"}]

# 5 /testThreat

## 5.1 GET

``` python
endpoint="/testThreat"
```

The /testThreat endpoint allows to search a taxon in the API database
and returns its threat status if it has one.

### 5.1.1 Species with an threatened status

#### 5.1.1.1 From canonical name

``` python
toSend1={'canonicalname':'Podocarpus guatemalensis'}
response = requests.get(api_url+endpoint, json=toSend1)
response.json()
```

    ## {'cd_tax': 2099, 'cd_tax_acc': 2099, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Podocarpus guatemalensis', 'acceptedname': 'Podocarpus guatemalensis Standl.', 'gbifkey': 5285893, 'syno': False, 'insertedTax': [], 'hasThreatStatus': True, 'cd_status': 'VU', 'comments': None, 'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz', 'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'}

#### 5.1.1.2 From scientific name

``` python
toSend2={'scientificname':'Puya ochroleuca Betancur & Callejas'}
response = requests.get(api_url+endpoint, json=toSend2)
response.json()
```

    ## {'cd_tax': 2503, 'cd_tax_acc': 2503, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Puya ochroleuca Betancur & Callejas', 'acceptedname': 'Puya ochroleuca Betancur & Callejas', 'gbifkey': 2696064, 'syno': False, 'insertedTax': [], 'hasThreatStatus': True, 'cd_status': 'EN', 'comments': None, 'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz', 'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'}

#### 5.1.1.3 From gbifkey

``` python
toSend3={'gbifkey':5789077}
response = requests.get(api_url+endpoint, json=toSend3)
response.json()
```

    ## {'cd_tax': 1777, 'cd_tax_acc': 1777, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Scytalopus rodriguezi Krabbe, P.G.W.Salaman, A.Cortes, A.Quevedo, L.A.Ortega & C.D.Cadena, 2005', 'acceptedname': 'Scytalopus rodriguezi Krabbe, P.G.W.Salaman, A.Cortes, A.Quevedo, L.A.Ortega & C.D.Cadena, 2005', 'gbifkey': 5789077, 'syno': False, 'insertedTax': [], 'hasThreatStatus': True, 'cd_status': 'VU', 'comments': None, 'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz', 'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'}

#### 5.1.1.4 synonym of a species with an threatened status

``` python
toSend4 = {'canonicalname':'Ptychoglossus danieli'}
response = requests.get(api_url+endpoint, json=toSend4)
response.json()
```

    ## {'cd_tax': 3515, 'cd_tax_acc': 3514, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Ptychoglossus danieli', 'acceptedname': 'Alopoglossus danieli (Harris, 1994)', 'gbifkey': 2450617, 'syno': True, 'insertedTax': [], 'hasThreatStatus': True, 'cd_status': 'CR', 'comments': None, 'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz', 'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'}

#### 5.1.1.5 spelling error

(Espeletia pa**y**pana en lugat de Espeletia pa**i**pana)

``` python
toSend5 = {'canonicalname':'Espeletia paypana'}
response = requests.get(api_url+endpoint, json=toSend5)
response.json()
```

    ## {'cd_tax': 2831, 'cd_tax_acc': 2831, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Espeletia paipana', 'acceptedname': 'Espeletia paipana S.Díaz & Pedraza', 'gbifkey': 3105080, 'syno': False, 'insertedTax': [], 'hasThreatStatus': True, 'cd_status': 'CR', 'comments': None, 'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz', 'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'}

### 5.1.2 Species without an threatened status

#### 5.1.2.1 Species which is in the database but has no threatened status

``` python
toSend6={'canonicalname':'Tangara johannae'}
response = requests.get(api_url+endpoint, json=toSend6)
response.json()
```

    ## {'cd_tax': 1797, 'cd_tax_acc': 1797, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Tangara johannae', 'acceptedname': 'Tangara johannae (Dalmas, 1900)', 'gbifkey': 2488153, 'syno': False, 'insertedTax': [], 'hasThreatStatus': False, 'cd_status': None, 'comments': None, 'references': None, 'links': None}

#### 5.1.2.2 Species which is not in the database

``` python
toSend7={'canonicalname':'Espeletia grandiflora'}
response = requests.get(api_url+endpoint, json=toSend7)
response.json()
```

    ## {'cd_tax': 0, 'cd_tax_acc': 0, 'alreadyInDb': False, 'foundGbif': True, 'matchedname': 'Espeletia grandiflora', 'acceptedname': 'Espeletia grandiflora Humb. & Bonpl.', 'gbifkey': 3105059, 'syno': False, 'insertedTax': [], 'hasThreatStatus': False, 'cd_status': None, 'comments': None, 'references': [], 'links': []}

#### 5.1.2.3 Species which does not exists

``` python
toSend8={'canonicalname':'Asriwendosa machibibus'}
response = requests.get(api_url+endpoint, json=toSend8)
response.json()
```

    ## {'cd_tax': 0, 'cd_tax_acc': 0, 'alreadyInDb': False, 'foundGbif': False, 'matchedname': None, 'acceptedname': None, 'gbifkey': None, 'syno': False, 'insertedTax': [], 'hasThreatStatus': False, 'cd_status': None, 'comments': None, 'references': [], 'links': []}

### 5.1.3 Error: no sufficient information given

``` python
toSend9={}
response = requests.get(api_url+endpoint, json=toSend9)
response.json()
```

    ## {'error': "You did not provide GBIF taxon key nor name with nor without authorship, missing argument: 'scientificname', 'canonicalname' or 'gbifkey'"}

# 6 /testThreat/list

## 6.1 POST

``` python
endpoint="/testThreat/list"
```

``` python
ListToSend={'list':[toSend1,toSend2,toSend3,toSend4,toSend5,toSend6,toSend7,toSend8,toSend9]}
response = requests.post(api_url+endpoint, json=ListToSend)
response.json()
```

    ## [{'cd_tax': 2099, 'cd_tax_acc': 2099, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Podocarpus guatemalensis', 'acceptedname': 'Podocarpus guatemalensis Standl.', 'gbifkey': 5285893, 'syno': False, 'insertedTax': [], 'hasThreatStatus': True, 'cd_status': 'VU', 'comments': None, 'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz', 'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'}, {'cd_tax': 2503, 'cd_tax_acc': 2503, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Puya ochroleuca Betancur & Callejas', 'acceptedname': 'Puya ochroleuca Betancur & Callejas', 'gbifkey': 2696064, 'syno': False, 'insertedTax': [], 'hasThreatStatus': True, 'cd_status': 'EN', 'comments': None, 'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz', 'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'}, {'cd_tax': 1777, 'cd_tax_acc': 1777, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Scytalopus rodriguezi Krabbe, P.G.W.Salaman, A.Cortes, A.Quevedo, L.A.Ortega & C.D.Cadena, 2005', 'acceptedname': 'Scytalopus rodriguezi Krabbe, P.G.W.Salaman, A.Cortes, A.Quevedo, L.A.Ortega & C.D.Cadena, 2005', 'gbifkey': 5789077, 'syno': False, 'insertedTax': [], 'hasThreatStatus': True, 'cd_status': 'VU', 'comments': None, 'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz', 'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'}, {'cd_tax': 3515, 'cd_tax_acc': 3514, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Ptychoglossus danieli', 'acceptedname': 'Alopoglossus danieli (Harris, 1994)', 'gbifkey': 2450617, 'syno': True, 'insertedTax': [], 'hasThreatStatus': True, 'cd_status': 'CR', 'comments': None, 'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz', 'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'}, {'cd_tax': 2831, 'cd_tax_acc': 2831, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Espeletia paipana', 'acceptedname': 'Espeletia paipana S.Díaz & Pedraza', 'gbifkey': 3105080, 'syno': False, 'insertedTax': [], 'hasThreatStatus': True, 'cd_status': 'CR', 'comments': None, 'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz', 'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'}, {'cd_tax': 1797, 'cd_tax_acc': 1797, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Tangara johannae', 'acceptedname': 'Tangara johannae (Dalmas, 1900)', 'gbifkey': 2488153, 'syno': False, 'insertedTax': [], 'hasThreatStatus': False, 'cd_status': None, 'comments': None, 'references': None, 'links': None}, {'cd_tax': 0, 'cd_tax_acc': 0, 'alreadyInDb': False, 'foundGbif': True, 'matchedname': 'Espeletia grandiflora', 'acceptedname': 'Espeletia grandiflora Humb. & Bonpl.', 'gbifkey': 3105059, 'syno': False, 'insertedTax': [], 'hasThreatStatus': False, 'cd_status': None, 'comments': None, 'references': [], 'links': []}, {'cd_tax': 0, 'cd_tax_acc': 0, 'alreadyInDb': False, 'foundGbif': False, 'matchedname': None, 'acceptedname': None, 'gbifkey': None, 'syno': False, 'insertedTax': [], 'hasThreatStatus': False, 'cd_status': None, 'comments': None, 'references': [], 'links': []}, {'error': "You did not provide GBIF taxon key nor name with nor without authorship, missing argument: 'scientificname', 'canonicalname' or 'gbifkey'"}]

# 7 /listEndem

## 7.1 GET

``` python
endpoint="/listEndem"
```

### 7.1.1 Comprehensive list

We will download the list and show the 5 first taxa:

``` python
response = requests.get(api_url+endpoint)
content=response.json()
len(content)
```

    ## 308

``` python
content[0:4]
```

    ## [{'cd_tax': 976, 'scientificname': 'Paroaria nigrogenis (Lafresnaye, 1846)', 'parentname': 'Paroaria Bonaparte, 1832', 'tax_rank': 'SP', 'gbifkey': 5845551, 'synonyms': [None], 'cd_status': 'Especie de interés', 'comments': 'occurrenceRemarks: Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Llanos Orientales desde el norte de la Serranía de la Macarena aproximadamente siguiendo el curso del río Ariari y luego el río Guaviare hasta el río Orinoco | ', 'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue', '194: Davalos y Porzecanski 2009'], 'links': ['91: http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09', None]}, {'cd_tax': 1281, 'scientificname': 'Accipiter collaris P.L.Sclater, 1860', 'parentname': 'Accipiter Brisson, 1760', 'tax_rank': 'SP', 'gbifkey': 2480593, 'synonyms': [None], 'cd_status': 'Casi endémica', 'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | Vertiente oriental hacia Amazonía | Perú: Amazonas (desde divisoria de aguas y principales drenajes al río Amazonas) | occurrenceRemarks: Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el Golfo de Urabá hasta la Península de La Guajira, incluyendo las estribaciones de la Sierra Nevada de Santa Marta y la Serranía de Perijá en el norte de Cesar, y como subregión |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas más al norte de la cordillera Occidental y de la cordillera Central y la ladera nororiental de la Central hacia el sur hasta aproximadamente el límite sur de Caldas |Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. cordillera Central | ', 'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue', '92: Arbeláez-Cortés et al. 2011b', '93: Cuervo et al. 2008a', '94: Cuervo et al. 2008b', '95: Merkord 2010', '96: Rodríguez y Rojas-Suárez 2008'], 'links': ['91: http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09', None, None, None, None, None]}, {'cd_tax': 1285, 'scientificname': 'Aglaiocercus coelestis (Gould, 1861)', 'parentname': 'Aglaiocercus J.T.Zimmer, 1930', 'tax_rank': 'SP', 'gbifkey': 2476385, 'synonyms': [None], 'cd_status': 'Casi endémica', 'comments': 'locality: Ecuador: Vertiente pacífica del Ecuador | occurrenceRemarks: Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Andén del Pacífico, desde la zona media del Darién en límites con Panamá, al lado izquierdo del bajo río Atrato, hasta el Ecuador |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Vertiente occidental de la cordillera Occidental que incluye | ', 'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue'], 'links': ['91: http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09']}, {'cd_tax': 1287, 'scientificname': 'Polyerata amabilis (Gould, 1853)', 'parentname': 'Polyerata Heine, 1863', 'tax_rank': 'SP', 'gbifkey': 5788536, 'synonyms': ['Amazilia amabilis (Gould, 1853)'], 'cd_status': 'Especie de interés', 'comments': 'locality: Ecuador: Vertiente pacífica del Ecuador | occurrenceRemarks: Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Región más húmeda inmediatamente al sur de la región 1, desde el bajo río Atrato hasta la parte media del valle del río Magdalena, incluyendo el alto río Sinú y alto río Nechí |Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Andén del Pacífico, desde la zona media del Darién en límites con Panamá, al lado izquierdo del bajo río Atrato, hasta el Ecuador |Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Alto valle del río Magdalena, principalmente en Tolima y Huila |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas más al norte de la cordillera Occidental y de la cordillera Central y la ladera nororiental de la Central hacia el sur hasta aproximadamente el límite sur de Caldas |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas del alto valle del río Magdalena principalmente en Tolima y Huila |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Vertiente occidental de la cordillera Oriental, desde el sur de Cesar hasta Cundinamarca | ', 'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue', '97: Corpocaldas 2010', '98: Donegan et al. 2010', '99: Laverde-R. Et al. 2005b', '100: Parra-Hernández et al. 2007'], 'links': ['91: http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09', None, None, None, None]}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listEndem?format=CSV>

------------------------------------------------------------------------

### 7.1.2 Only the passerine birds

The five first passerine birds of the endemic list:

``` python
onlyPasserine={'childrenOf':'Passeriformes'}
response = requests.get(api_url+endpoint,json=onlyPasserine)
content=response.json()
len(content)
```

    ## 167

``` python
content[0:4]
```

    ## [{'cd_tax': 976, 'scientificname': 'Paroaria nigrogenis (Lafresnaye, 1846)', 'parentname': 'Paroaria Bonaparte, 1832', 'tax_rank': 'SP', 'gbifkey': 5845551, 'synonyms': [None], 'cd_status': 'Especie de interés', 'comments': 'occurrenceRemarks: Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Llanos Orientales desde el norte de la Serranía de la Macarena aproximadamente siguiendo el curso del río Ariari y luego el río Guaviare hasta el río Orinoco | ', 'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue', '194: Davalos y Porzecanski 2009'], 'links': ['91: http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09', None]}, {'cd_tax': 1300, 'scientificname': 'Anairetes agilis (P.L.Sclater, 1856)', 'parentname': 'Anairetes Reichenbach, 1850', 'tax_rank': 'SP', 'gbifkey': 2482692, 'synonyms': [None], 'cd_status': 'Casi endémica', 'comments': 'locality: Ecuador: Los Andes | Venezuela: Andes venezolanos | occurrenceRemarks: Franja y región: Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. cordillera Central |Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. cordillera Oriental con | ', 'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue', '92: Arbeláez-Cortés et al. 2011b', '97: Corpocaldas 2010', '100: Parra-Hernández et al. 2007', '103: Ayerbe-Quiñones et al. 2008', '107: López-Guzmán y Gómez-Botero 2005'], 'links': ['91: http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09', None, None, None, None, None]}, {'cd_tax': 1311, 'scientificname': 'Anisognathus melanogenys (Salvin & Godman, 1880)', 'parentname': 'Anisognathus Reichenbach, 1850', 'tax_rank': 'SP', 'gbifkey': 5230546, 'synonyms': [None], 'cd_status': 'Endémica', 'comments': 'occurrenceRemarks: Franja y región: Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. Sierra Nevada de Santa Marta | ', 'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue'], 'links': ['91: http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09']}, {'cd_tax': 1312, 'scientificname': 'Anisognathus notabilis (P.L.Sclater, 1855)', 'parentname': 'Anisognathus Reichenbach, 1850', 'tax_rank': 'SP', 'gbifkey': 5230540, 'synonyms': [None], 'cd_status': 'Casi endémica', 'comments': 'locality: Ecuador: Vertiente pacífica del Ecuador | occurrenceRemarks: Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Andén del Pacífico, desde la zona media del Darién en límites con Panamá, al lado izquierdo del bajo río Atrato, hasta el Ecuador |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Vertiente occidental de la cordillera Occidental que incluye | ', 'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue'], 'links': ['91: http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09']}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listEndem?childrenOf=Passeriformes&format=CSV>

------------------------------------------------------------------------

### 7.1.3 Error: asking for an unknown group

We will ask for all the children of the genus Abies (Fir genus)

``` python
onlyAbies={'childrenOf':'Abies'}
response = requests.get(api_url+endpoint,json=onlyAbies)
response.json()
```

    ## {'error': "'childrenOf' taxon not recognized: taxon Abies was not found in the database"}

# 8 /listExot

## 8.1 GET

``` python
endpoint="/listExot"
```

### 8.1.1 Comprehensive list

We will download the list and show the 5 first taxa:

``` python
response = requests.get(api_url+endpoint)
content=response.json()
len(content)
```

    ## 511

``` python
content[0:4]
```

    ## [{'cd_tax': 7, 'scientificname': 'Acacia decurrens (J.C.Wendl.) Willd.', 'parentname': 'Acacia Mill.', 'tax_rank': 'SP', 'gbifkey': 2979778, 'synonyms': [None], 'is_alien': True, 'is_invasive': True, 'comments': 'Altitud máxima: 3200 | Altitud máxima Unit: m.s.n.m. | Altitud mínima: 1600 | Altitud mínima Unit: m.s.n.m. | Asociación invasiva: No se encontraron datos | Aspectos generales de invasividad: Producción abundante de semillas, rápida germinación, alta viabilidad, resistencia a inundaciones y fuego, alta producción vegetativa, sustancias alelopáticas | Causas de introducción: Usos ornamentales | Distribución como exótica: Cosmopólita | Distribución nativa: ARG , AUS , NZL , URY , ZAF | Estatus: Exótica | Translocada | Factores limitantes para el establecimiento: Heladas, no tiene éxito por debajo de los 1000 msnm, zonas húmedas y secas tropicales | Hábito: Terrestre | Impactos de introducción: Migración de zonas de cultivos a espacios naturales, aumento regímenes de incendio, restricción en la regeneración natural de especies nativas, impedimento en el movimiento de fauna | Introducida después de (año): 1963 | Medidas de manejo y control: En África se ha evidenciado el control biológico sobre semillas con la especie Melanterius maculatus (Curculionidae) y en Nueva Zelanda con Bruchophagus acaciae (Hymenoptera) | Observaciones de ocurrencia: Frecuentemente en zonas de incendios y áreas perturbadas | pH: 7 | Precipitación máxima: 1200 | Precipitación máxima Unit: mm | Precipitación mínima: 750 | Precipitación mínima Unit: mm | Puntaje Riesgo de Invasión: 5 | Puntaje Riesgo de Invasión Remarks: Fuente: I3N | Riesgo de invasión: Alto riesgo | Temperatura máxima: 18 | Temperatura máxima Unit: °C | Temperatura mínima: 14 | Temperatura mínima Unit: °C | Tipo de dispersión: Anemocoría, zoocoría | Tipo de introducción: Intencional | Tipo de reproducción: Semillas | Tipo de suelo: Arenosos-arcillosos | Vías de introducción: Sembrada', 'references': ['1:  Instituto de Investigación de Recursos Biológicos Alexander von Humboldt (2020). Base de datos de información ecológica e invasividad de especies exóticas prioritarias de flora y fauna de Colombia. 43 registros.', '2: Cárdenas D., Baptiste M.P., Castaño N. (2017). Plantas exóticas con alto potencial de invasión en Colombia. Instituto de Investigación de Recursos Biológicos Alexander von Humboldt. Bogotá, D. C., Colombia. 295 p.', '3: Mora, M. F., Rubio J., Ocampo R. & Barrera J.I. (2015). Catálogo de especies invasoras del territorio CAR. Publicado por Pontificia Universidad Javeriana & Corporación Autónoma Regional de Cundinamarca – CAR, 238 pp.', '90: Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.'], 'links': ['1: http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020', None, None, '90: https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91']}, {'cd_tax': 14, 'scientificname': 'Achatina fulica (Férussac, 1821)', 'parentname': 'Achatina Lamarck, 1799', 'tax_rank': 'SP', 'gbifkey': 2295966, 'synonyms': [None], 'is_alien': True, 'is_invasive': True, 'comments': 'Altitud máxima: 1233 | Altitud máxima Unit: m.s.n.m. | Altitud mínima: 0 | Altitud mínima Unit: m.s.n.m. | Asociación invasiva: Hospedero intermediario de Angyostrongylus Cantonensis (causante de la meningoencefalitis eosinofílica) y Angyostrongylus costaricensis (causante de angiostrongilosis abdominal) | Aspectos generales de invasividad: Dieta generalista que le permite alimentarse de hongos, plantas, materia orgánica en descomposición, papel y paredes estucadas. Ausencia de depredadores naturales en ambientes antrópicos. Comienzan a reproducirse desde los 5 o 6 meses, llegando a poner hasta 1000 huevos en condiciones óptimas. En condiciones climáticas adversas es capaz de estivar. | Causas de introducción: Propósitos estéticos, alimenticios y medicinales | Distribución como exótica: AIA , ASM , BGD , BRA , BRB , CHN , COK , COL , ECU , ETH , GHA , GLP , GNQ , GUF , GUM , GUY , HKG , IDN , IND , JPN , KEN , KIR , LCA , LKA , MAF , MAR , MDG , MHL , MNP , MOZ , MTQ , MUS , MYS , MYT , NCL , NPL , NZL , PER , PHL , PLW , PNG , PRY , PYF , SGP , SLB , SOM , STP , SUR , SYC , THA , TTO , TUV , TWN , UMI , VEN , VUT , WLF , WSM , ZAF | Distribución nativa: ETH , KEN , TZA | Estatus: Exótica | Factores limitantes para el establecimiento: Temperaturas de 0°C producen la congelación del agua de los tejidos y las superiores a 30°C puede soportarlas siempre y cuando haya suficiente humedad. | Hábito: Terrestre | Impactos de introducción: Impactos a la agricultura ya que puede alimentarse de más de 200 especies vegetales | Introducida después de (año): 2008 | Medidas de manejo y control: Restricción del uso de la especie para cualquier fin. Control físico y control químico con disposición final controlada | Observaciones de ocurrencia: Áreas de baja a mediana elevación en clima tropical con calentamiento constante, aunque ya se han adaptado a climas templados. Abunda en zonas agrícolas, zonas costeras, humedales, áreas perturbadas, bosques, zonas urbanas y zonas de ribera | pH: No aplica | Precipitación máxima: 7650 | Precipitación máxima Unit: mm | Precipitación mínima: 900 | Precipitación mínima Unit: mm | Puntaje Riesgo de Invasión: No evaluada | Puntaje Riesgo de Invasión Remarks: No evaluada | Riesgo de invasión: No evaluada | Temperatura máxima: 29 | Temperatura máxima Unit: °C | Temperatura mínima: 9 | Temperatura mínima Unit: °C | Tipo de dispersión: Antropocoría y medios propios | Tipo de introducción: Intencional y no intencional | Tipo de reproducción: sexual | Tipo de suelo: No aplica | Vías de introducción: Intencional por propósitos estéticos, alimenticios y medicinales y no intencional a través del transporte de carga.', 'references': ['1:  Instituto de Investigación de Recursos Biológicos Alexander von Humboldt (2020). Base de datos de información ecológica e invasividad de especies exóticas prioritarias de flora y fauna de Colombia. 43 registros.', '4: Corporación Autónoma Regional (2018). Plan de Prevención, Control y Manejo (PPCM) de Caracol Gigante Africano (Achatina fulica) en la jurisdicción CAR. Dirección de Recursos Naturales. 61 pp.', '5: Invasive Species Specialist Group (2020). Achatina fulica.', '6: Garcés M., Patiño A., Gómez M., Giraldo A. & Bolívar G. (2016). Sustancias alternativas para el control del caracol africano (Achatina fulica) en el Valle del Cauca. Biota Colombiana. Vol. 17(1), 44 - 52 pp.', '90: Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.'], 'links': ['1: http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020', '4: https://www.car.gov.co/uploads/files/5b9033f095d34.pdf', '5: http://www.iucngisd.org/gisd/speciesname/Achatina+fulica', None, '90: https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91']}, {'cd_tax': 19, 'scientificname': 'Anthoxanthum odoratum L.', 'parentname': 'Anthoxanthum L.', 'tax_rank': 'SP', 'gbifkey': 2705975, 'synonyms': [None], 'is_alien': True, 'is_invasive': True, 'comments': 'Altitud máxima: 4500 | Altitud máxima Unit: m.s.n.m. | Altitud mínima: 1500 | Altitud mínima Unit: m.s.n.m. | Asociación invasiva: Holcus lanatus | Aspectos generales de invasividad: Florecimiento en todo el año, producción de gran cantidad de semillas, alta viabilidad de semillas | Causas de introducción: Constitución de céspedes, especie forrajera para el incremento de producción de leche de ganado vacuno, arreglos florales | Distribución como exótica: América , AUS , ZAF | Distribución nativa: BEL , CHN , ESP , FRA , GRB , GRC , IRN , PRT , RUS | Estatus: Exótica | Factores limitantes para el establecimiento: No se encontraron datos | Hábito: Terrestre | Impactos de introducción: Desplazamiento de especies nativas | Introducida después de (año): No se encontraron datos | Medidas de manejo y control: Actividades de siega antes de que las semillas hayan madurado | Observaciones de ocurrencia: Áreas abiertas con sombrío parcial entre media y alta montaña, sustratos arenosos, rocosos, arcillosos | pH: 3,7 - 7,5 | Precipitación máxima: No se encontraron datos | Precipitación máxima Unit: mm | Precipitación mínima: No se encontraron datos | Precipitación mínima Unit: mm | Puntaje Riesgo de Invasión: 6.14 | Puntaje Riesgo de Invasión Remarks: Fuente: I3N | Riesgo de invasión: Alto riesgo | Temperatura máxima: 18 | Temperatura máxima Unit: °C | Temperatura mínima: 0 | Temperatura mínima Unit: °C | Tipo de dispersión: Antropocoría | Tipo de introducción: Intencional | Tipo de reproducción: Vegetativa | Tipo de suelo: Arenoso-arcilloso | Vías de introducción: Sembrada', 'references': ['1:  Instituto de Investigación de Recursos Biológicos Alexander von Humboldt (2020). Base de datos de información ecológica e invasividad de especies exóticas prioritarias de flora y fauna de Colombia. 43 registros.', '2: Cárdenas D., Baptiste M.P., Castaño N. (2017). Plantas exóticas con alto potencial de invasión en Colombia. Instituto de Investigación de Recursos Biológicos Alexander von Humboldt. Bogotá, D. C., Colombia. 295 p.', '7: Invasive Species Compendium (2019). Anthoxanthum odoratum (sweet vernal grass).'], 'links': ['1: http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020', None, '7: https://www.cabi.org/isc/datasheet/93023']}, {'cd_tax': 21, 'scientificname': 'Arundo donax L.', 'parentname': 'Arundo L.', 'tax_rank': 'SP', 'gbifkey': 2703041, 'synonyms': [None], 'is_alien': True, 'is_invasive': True, 'comments': 'Altitud máxima: 3000 | Altitud máxima Unit: m.s.n.m. | Altitud mínima: 500 | Altitud mínima Unit: m.s.n.m. | Asociación invasiva: No se encontraron datos | Aspectos generales de invasividad: Tolerancia a altos niveles de salinidad | Causas de introducción: Usos de cestería, elaboración de utensilios de cocina, instrumentos musicales, muebles, juguetes, papel artesanal, protección de cuencas, estabilización y/o recuperación de suelos y taludes, establecimiento de cercas vivas y rompevientos | Distribución como exótica: América del Sur , AUS , USA , ZEF | Distribución nativa: AFG , CHN , IDN , IND , IRN , IRQ , JPN , KHM , NPL | Estatus: Exótica | Factores limitantes para el establecimiento: Requiere de fotoperíodos prolongados que no encuentra en países como Colombia | Hábito: Terrestre | Impactos de introducción: Fuerte competidora de especies nativas, absorbe gran cantidad de agua del suelo, alteraciones de hidrología, en el control de inundaciones, en el ciclo de nutrientes y el régimen de incendios | Introducida después de (año): No se encontraron datos | Medidas de manejo y control: Control mecánico especialmente de plantas jóvenes, prestando atención a la eliminación del rizoma. Control químico con glifosato. Se ha reportado control biológico usando orugas de Phothedes dulcis en Francia, larvas de Zyginidia manaliensis en Pakistán y las de Diatraea sacchararalis en Barbados | Observaciones de ocurrencia: Ambientes abiertos y de suelos con humedad permanente, orillas de diferentes corrientes hídricas | pH: 5,0 - 8,7 | Precipitación máxima: 4000 | Precipitación máxima Unit: mm | Precipitación mínima: 300 | Precipitación mínima Unit: mm | Puntaje Riesgo de Invasión: 5.35 | Puntaje Riesgo de Invasión Remarks: Fuente: I3N | Riesgo de invasión: Alto riesgo | Temperatura máxima: 29 | Temperatura máxima Unit: °C | Temperatura mínima: 9 | Temperatura mínima Unit: °C | Tipo de dispersión: Vegetación flotante | Tipo de introducción: No intencional | Tipo de reproducción: Vegetativa por rizomas | Tipo de suelo: Arenas de partícula gruesa, grava, arcillas pesadas y sedimentos de ríos | Vías de introducción: Dispersión voluntaria', 'references': ['1:  Instituto de Investigación de Recursos Biológicos Alexander von Humboldt (2020). Base de datos de información ecológica e invasividad de especies exóticas prioritarias de flora y fauna de Colombia. 43 registros.', '2: Cárdenas D., Baptiste M.P., Castaño N. (2017). Plantas exóticas con alto potencial de invasión en Colombia. Instituto de Investigación de Recursos Biológicos Alexander von Humboldt. Bogotá, D. C., Colombia. 295 p.', '8: Invasive Species Compendium (2019). Arundo donax (giant reed).'], 'links': ['1: http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020', None, '8: https://www.cabi.org/isc/datasheet/1940']}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listExot?format=CSV>

------------------------------------------------------------------------

### 8.1.2 Only the passerine birds

The five first passerine birds of the endemic list:

``` python
onlyPasserine={'childrenOf':'Passeriformes'}
response = requests.get(api_url+endpoint,json=onlyPasserine)
content=response.json()
len(content)
```

    ## 10

``` python
content[0:4]
```

    ## [{'cd_tax': 99, 'scientificname': 'Lonchura malacca (Linnaeus, 1766)', 'parentname': 'Lonchura Sykes, 1832', 'tax_rank': 'SP', 'gbifkey': 2493626, 'synonyms': [None], 'is_alien': True, 'is_invasive': True, 'comments': 'Altitud máxima: 2500 | Altitud máxima Unit: m.s.n.m. | Altitud mínima: 550 | Altitud mínima Unit: m.s.n.m. | Asociación invasiva: Se alimenta principalmente de arroz (Oryza sativa) y sorgo (sorghum bicolor). Abunda en corredores de pasto donde predomina Urochloa maxima e Hyparrhenia rufa para desplazarse y como sitio de descanso. | Aspectos generales de invasividad: Forman grandes bandadas, comúnmente entre 10 y 30 individuos. Grupos pequeñas tienden a unirse a otros para alimentación y desplazamiento | Causas de introducción: Importadas como aves ornamentales | Distribución como exótica: AUS , BLZ , CHN , COL , CRI , CUB , DOM , HND , JPN , MEX , PRI , SLV , USA , VEN | Distribución nativa: IDN , IND , KHM , LKA , MYS , PHL , SGP , TWN , VNM | Estatus: Exótica | Factores limitantes para el establecimiento: No se encontraron datos | Hábito: Terrestre | Impactos de introducción: Se desconoce su impacto en la biodiversidad nativa en Colombia, pero se reporta como plaga de cultivos en países vecinos. | Introducida después de (año): 2005 | Medidas de manejo y control: No se cuenta en el momento con planes de manejo y control debido a la falta de información de esta especie en el Neotrópico | Observaciones de ocurrencia: Registrada en pastos naturales y artificiales en zonas urbanas y suburbanas, y recientemente en cañaduzales. En otros países se registra como colonizador de ecosistemas de humedales | pH: No aplica | Precipitación máxima: No se encontraron datos | Precipitación máxima Unit: mm | Precipitación mínima: No se encontraron datos | Precipitación mínima Unit: mm | Puntaje Riesgo de Invasión: 3.6 | Puntaje Riesgo de Invasión Remarks: Fuente: AR - Vertebrados Terrestres | Riesgo de invasión: Alto riesgo | Temperatura máxima: 28 | Temperatura máxima Unit: °C | Temperatura mínima: 17 | Temperatura mínima Unit: °C | Tipo de dispersión: Antropocoría y dispersión natural | Tipo de introducción: Intencional | Tipo de reproducción: Sexual | Tipo de suelo: No aplica | Vías de introducción: Escape accidental', 'references': ['1:  Instituto de Investigación de Recursos Biológicos Alexander von Humboldt (2020). Base de datos de información ecológica e invasividad de especies exóticas prioritarias de flora y fauna de Colombia. 43 registros.', '18: Baptiste M.P., Castaño N., Cárdenas D., Gutiérrez F.P., Gil D. & Lasso C.A. (eds). (2010). Análisis de riesgo y propuesta de categorización de especies introducidas para Colombia. Instituto de Investigación de Recursos Biológicos Alexander von Humboldt. Bogotá, D. C., Colombia. 200 pp.', '19: Instituto de Investigación de Recursos Biológicos Alexander von Humboldt. (2011). Fauna exótica e invasora de Colombia. Bogotá, D. C., Colombia. 71 pp.', '56: Parra R., Tolosa Y. & Figueroa W. (2015). Nuevos registros y estado actual de las especies introducidas en el municipio de Ibagué. Revista Tumbaga, Vol. 10(1), 58 - 75 pp.', '57: CONABIO (2014). Método de Evaluación Rápida de Invasividad (MERI) para especies exóticas en México - Lonchura malacca, 1766, 9 pp. Gobierno de México.', '58: Carantón D., Certuche K., Díaz C., Parra R., Sanabria J. & Moreno M. (2008). Aspectos biológicos de una nueva población del Capuchino de cabeza negra (Lonchura malacca, Estrildidae) en el alto valle del Magdalena, Boletín SAO, Vol. 18(2), 54 - 63 pp.', '90: Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.'], 'links': ['1: http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020', None, None, None, '57: https://www.gob.mx/cms/uploads/attachment/file/222403/Lonchura_malacca.pdf', None, '90: https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91']}, {'cd_tax': 455, 'scientificname': 'Erythrura gouldiae (Gould, 1844)', 'parentname': 'Erythrura Swainson, 1837', 'tax_rank': 'SP', 'gbifkey': 5789080, 'synonyms': ['Chloebia gouldiae (Gould, 1844)'], 'is_alien': True, 'is_invasive': False, 'comments': None, 'references': ['90: Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.'], 'links': ['90: https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91']}, {'cd_tax': 812, 'scientificname': 'Lonchura atricapilla (Vieillot, 1807)', 'parentname': 'Lonchura Sykes, 1832', 'tax_rank': 'SP', 'gbifkey': 2493623, 'synonyms': [None], 'is_alien': True, 'is_invasive': False, 'comments': None, 'references': ['90: Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.'], 'links': ['90: https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91']}, {'cd_tax': 813, 'scientificname': 'Lonchura oryzivora (Linnaeus, 1758)', 'parentname': 'Lonchura Sykes, 1832', 'tax_rank': 'SP', 'gbifkey': 4845776, 'synonyms': [None], 'is_alien': True, 'is_invasive': False, 'comments': None, 'references': ['90: Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.'], 'links': ['90: https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91']}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listExot?childrenOf=Passeriformes&format=CSV>

------------------------------------------------------------------------

### 8.1.3 Error: asking for an unknown group

We will ask for all the children of the genus Abies (Fir genus)

``` python
onlyAbies={'childrenOf':'Abies'}
response = requests.get(api_url+endpoint,json=onlyAbies)
response.json()
```

    ## {'error': "'childrenOf' taxon not recognized: taxon Abies was not found in the database"}

# 9 /listThreat

## 9.1 GET

``` python
endpoint="/listThreat"
```

### 9.1.1 Comprehensive list

We will download the list and show the 5 first taxa:

``` python
response = requests.get(api_url+endpoint)
content=response.json()
len(content)
```

    ## 1299

``` python
content[0:4]
```

    ## [{'cd_tax': 274, 'scientificname': 'Arapaima gigas (Schinz, 1822)', 'parentname': 'Arapaima Müller, 1843', 'tax_rank': 'SP', 'gbifkey': 5212877, 'synonyms': [None], 'cd_status': 'VU', 'comments': None, 'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz'], 'links': ['222: https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads']}, {'cd_tax': 641, 'scientificname': 'Eremophilus mutisii Humboldt, 1805', 'parentname': 'Eremophilus Humboldt, 1805', 'tax_rank': 'SP', 'gbifkey': 5202895, 'synonyms': [None], 'cd_status': 'VU', 'comments': None, 'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz'], 'links': ['222: https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads']}, {'cd_tax': 1059, 'scientificname': 'Podocnemis expansa (Schweigger, 1812)', 'parentname': 'Podocnemis Wagler, 1830', 'tax_rank': 'SP', 'gbifkey': 2442795, 'synonyms': [None], 'cd_status': 'CR', 'comments': None, 'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz'], 'links': ['222: https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads']}, {'cd_tax': 1060, 'scientificname': 'Podocnemis unifilis Troschel, 1848', 'parentname': 'Podocnemis Wagler, 1830', 'tax_rank': 'SP', 'gbifkey': 2442782, 'synonyms': [None], 'cd_status': 'EN', 'comments': None, 'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz'], 'links': ['222: https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads']}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listThreat?format=CSV>

------------------------------------------------------------------------

### 9.1.2 Only the passerine birds

The five first passerine birds of the endemic list:

``` python
onlyPasserine={'childrenOf':'Passeriformes'}
response = requests.get(api_url+endpoint,json=onlyPasserine)
content=response.json()
len(content)
```

    ## 71

``` python
content[0:4]
```

    ## [{'cd_tax': 1327, 'scientificname': 'Arremon schlegeli Bonaparte, 1850', 'parentname': 'Arremon Vieillot, 1816', 'tax_rank': 'SP', 'gbifkey': 2491624, 'synonyms': [None], 'cd_status': 'VU', 'comments': None, 'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz'], 'links': ['222: https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads']}, {'cd_tax': 1332, 'scientificname': 'Asthenes perijana (Phelps, 1977)', 'parentname': 'Asthenes Reichenbach, 1853', 'tax_rank': 'SP', 'gbifkey': 6088359, 'synonyms': [None], 'cd_status': 'EN', 'comments': None, 'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz'], 'links': ['222: https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads']}, {'cd_tax': 1335, 'scientificname': 'Atlapetes blancae Donegan, 2007', 'parentname': 'Atlapetes Wagler, 1831', 'tax_rank': 'SP', 'gbifkey': 5788834, 'synonyms': [None], 'cd_status': 'CR', 'comments': None, 'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz'], 'links': ['222: https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads']}, {'cd_tax': 1336, 'scientificname': 'Atlapetes flaviceps Chapman, 1912', 'parentname': 'Atlapetes Wagler, 1831', 'tax_rank': 'SP', 'gbifkey': 2491438, 'synonyms': [None], 'cd_status': 'VU', 'comments': None, 'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz'], 'links': ['222: https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads']}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listThreat?childrenOf=Passeriformes&format=CSV>

------------------------------------------------------------------------

### 9.1.3 Error: asking for an unknown group

We will ask for all the children of the genus Abies (Fir genus)

``` python
onlyAbies={'childrenOf':'Abies'}
response = requests.get(api_url+endpoint,json=onlyAbies)
response.json()
```

    ## {'error': "'childrenOf' taxon not recognized: taxon Abies was not found in the database"}

# 10 /tax

## 10.1 GET

``` python
endpoint = "/tax"
```

The /tax endpoints allows to query the API database for a taxon.

### 10.1.1 From the cd_tax

cd_tax is the identificator of the taxon in the database and is returned
from many API endpoints. Therefore it might be useful to download the
information from this cd_tax

``` python
toSend={'cd_tax':150}
response = requests.get(api_url+endpoint, json=toSend)
response.json()
```

    ## {'cd_tax': 150, 'scientificname': 'Brachiaria eminii (Mez) Robyns', 'canonicalname': 'Brachiaria eminii', 'authorship': '(Mez) Robyns', 'tax_rank': 'SP', 'cd_parent': 147, 'parentname': 'Brachiaria (Trin.) Griseb.', 'cd_accepted': 150, 'acceptedname': 'Brachiaria eminii (Mez) Robyns', 'status': 'ACCEPTED', 'gbifkey': 4933082, 'synonyms': ['Brachiaria decumbens Stapf', 'Urochloa decumbens (Stapf) R.D.Webster'], 'hasendemstatus': False, 'hasexotstatus': True, 'hasthreatstatus': False}

### 10.1.2 From a scientific name

``` python
toSend={'scientificname':"Urochloa brizantha (A.Rich.) R.D.Webster"}
response = requests.get(api_url+endpoint, json=toSend)
response.json()
```

    ## {'cd_tax': 149, 'scientificname': 'Urochloa brizantha (A.Rich.) R.D.Webster', 'canonicalname': 'Urochloa brizantha', 'authorship': '(A.Rich.) R.D.Webster', 'tax_rank': 'SP', 'cd_parent': None, 'parentname': None, 'cd_accepted': 148, 'acceptedname': 'Brachiaria brizantha (A.Rich.) Stapf', 'status': 'SYNONYM', 'gbifkey': 2705862, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}

### 10.1.3 From a canonical name

``` python
toSend={'canonicalname':'Rottboellia cochinchinensis'}
response = requests.get(api_url+endpoint, json=toSend)
response.json()
```

    ## {'cd_tax': 135, 'scientificname': 'Rottboellia cochinchinensis (Lour.) Clayton', 'canonicalname': 'Rottboellia cochinchinensis', 'authorship': '(Lour.) Clayton', 'tax_rank': 'SP', 'cd_parent': 134, 'parentname': 'Rottboellia L.f.', 'cd_accepted': 135, 'acceptedname': 'Rottboellia cochinchinensis (Lour.) Clayton', 'status': 'ACCEPTED', 'gbifkey': 2704075, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': True, 'hasthreatstatus': False}

### 10.1.4 Species which is not in database

The API send back an empty JSON variable

``` python
toSend={'canonicalname':'Amanita caesarea'}
response = requests.get(api_url+endpoint, json=toSend)
response.json()
```

### 10.1.5 Species which does not exist

The API send back an empty JSON variable

``` python
toSend={'canonicalname':'Inventadus inexistus'}
response = requests.get(api_url+endpoint, json=toSend)
response.json()
```

# 11 /listTax

## 11.1 GET

The “/listTax” endpoints allows to query the taxonomic table of the
database API.

``` python
endpoint="/listTax"
```

### 11.1.1 Comprehensive list

Here is the code to download the complete list of taxa in the database
and show the 5 first taxa.

``` python
response = requests.get(api_url+endpoint)
content=response.json()
len(content)
```

    ## 3756

``` python
content[0:4]
```

    ## [{'cd_tax': 1, 'scientificname': 'Plantae', 'canonicalname': 'Plantae', 'authorship': None, 'tax_rank': 'KG', 'cd_parent': None, 'parentname': None, 'cd_accepted': 1, 'acceptedname': 'Plantae', 'status': 'ACCEPTED', 'gbifkey': 6, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}, {'cd_tax': 2, 'scientificname': 'Tracheophyta', 'canonicalname': 'Tracheophyta', 'authorship': None, 'tax_rank': 'PHY', 'cd_parent': 1, 'parentname': 'Plantae', 'cd_accepted': 2, 'acceptedname': 'Tracheophyta', 'status': 'ACCEPTED', 'gbifkey': 7707728, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}, {'cd_tax': 3, 'scientificname': 'Magnoliopsida', 'canonicalname': 'Magnoliopsida', 'authorship': None, 'tax_rank': 'CL', 'cd_parent': 2, 'parentname': 'Tracheophyta', 'cd_accepted': 3, 'acceptedname': 'Magnoliopsida', 'status': 'ACCEPTED', 'gbifkey': 220, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}, {'cd_tax': 4, 'scientificname': 'Fabales', 'canonicalname': 'Fabales', 'authorship': None, 'tax_rank': 'OR', 'cd_parent': 3, 'parentname': 'Magnoliopsida', 'cd_accepted': 4, 'acceptedname': 'Fabales', 'status': 'ACCEPTED', 'gbifkey': 1370, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listTax?format=CSV>

------------------------------------------------------------------------

### 11.1.2 Only the Bivalve

The following code shows how to query the Bivalvia Class from the
database and shows the 10 firsts:

``` python
onlyBivalve={'childrenOf':'Bivalvia'}
response = requests.get(api_url+endpoint,json=onlyBivalve)
content=response.json()
len(content)
```

    ## 17

``` python
content[0:9]
```

    ## [{'cd_tax': 495, 'scientificname': 'Bivalvia', 'canonicalname': 'Bivalvia', 'authorship': None, 'tax_rank': 'CL', 'cd_parent': 9, 'parentname': 'Mollusca', 'cd_accepted': 495, 'acceptedname': 'Bivalvia', 'status': 'ACCEPTED', 'gbifkey': 137, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}, {'cd_tax': 496, 'scientificname': 'Venerida', 'canonicalname': 'Venerida', 'authorship': None, 'tax_rank': 'OR', 'cd_parent': 495, 'parentname': 'Bivalvia', 'cd_accepted': 496, 'acceptedname': 'Venerida', 'status': 'ACCEPTED', 'gbifkey': 9310756, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}, {'cd_tax': 497, 'scientificname': 'Cyrenidae', 'canonicalname': 'Cyrenidae', 'authorship': None, 'tax_rank': 'FAM', 'cd_parent': 496, 'parentname': 'Venerida', 'cd_accepted': 497, 'acceptedname': 'Cyrenidae', 'status': 'ACCEPTED', 'gbifkey': 6527076, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}, {'cd_tax': 498, 'scientificname': 'Corbicula Megerle von Mühlfeld, 1811', 'canonicalname': 'Corbicula', 'authorship': 'Megerle von Mühlfeld, 1811', 'tax_rank': 'GN', 'cd_parent': 497, 'parentname': 'Cyrenidae', 'cd_accepted': 498, 'acceptedname': 'Corbicula Megerle von Mühlfeld, 1811', 'status': 'DOUBTFUL', 'gbifkey': 11352197, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}, {'cd_tax': 499, 'scientificname': 'Corbicula fluminea (O.F.Müller, 1774)', 'canonicalname': 'Corbicula fluminea', 'authorship': '(O.F.Müller, 1774) ', 'tax_rank': 'SP', 'cd_parent': 498, 'parentname': 'Corbicula Megerle von Mühlfeld, 1811', 'cd_accepted': 499, 'acceptedname': 'Corbicula fluminea (O.F.Müller, 1774)', 'status': 'ACCEPTED', 'gbifkey': 8190231, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': True, 'hasthreatstatus': False}, {'cd_tax': 3132, 'scientificname': 'Arcida', 'canonicalname': 'Arcida', 'authorship': None, 'tax_rank': 'OR', 'cd_parent': 495, 'parentname': 'Bivalvia', 'cd_accepted': 3132, 'acceptedname': 'Arcida', 'status': 'ACCEPTED', 'gbifkey': 9574493, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}, {'cd_tax': 3133, 'scientificname': 'Arcidae', 'canonicalname': 'Arcidae', 'authorship': None, 'tax_rank': 'FAM', 'cd_parent': 3132, 'parentname': 'Arcida', 'cd_accepted': 3133, 'acceptedname': 'Arcidae', 'status': 'ACCEPTED', 'gbifkey': 3483, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}, {'cd_tax': 3134, 'scientificname': 'Anadara Gray, 1847', 'canonicalname': 'Anadara', 'authorship': 'Gray, 1847', 'tax_rank': 'GN', 'cd_parent': 3133, 'parentname': 'Arcidae', 'cd_accepted': 3134, 'acceptedname': 'Anadara Gray, 1847', 'status': 'ACCEPTED', 'gbifkey': 2286218, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': False}, {'cd_tax': 3135, 'scientificname': 'Anadara tuberculosa (G.B.Sowerby I, 1833)', 'canonicalname': 'Anadara tuberculosa', 'authorship': '(G.B.Sowerby I, 1833) ', 'tax_rank': 'SP', 'cd_parent': 3134, 'parentname': 'Anadara Gray, 1847', 'cd_accepted': 3135, 'acceptedname': 'Anadara tuberculosa (G.B.Sowerby I, 1833)', 'status': 'ACCEPTED', 'gbifkey': 5188932, 'synonyms': [None], 'hasendemstatus': False, 'hasexotstatus': False, 'hasthreatstatus': True}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listTax?childrenOf=Bivalvia&format=CSV>

------------------------------------------------------------------------

# 12 /listReferences

``` python
endpoint = "/listReferences"
```

## 12.1 GET

The GET method of the */listReferences* endpoint allows to get the
reference list from the API database.

### 12.1.1 Comprehensive list

Here to download the reference list and show the 10 first results:

``` python
response = requests.get(api_url+endpoint)
content=response.json()
len(content)
```

    ## 222

``` python
content[0:9]
```

    ## [{'cd_ref': 1, 'ref_citation': ' Instituto de Investigación de Recursos Biológicos Alexander von Humboldt (2020). Base de datos de información ecológica e invasividad de especies exóticas prioritarias de flora y fauna de Colombia. 43 registros.', 'link': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020', 'nb_endem': 0, 'nb_exot': 45, 'nb_threat': 0}, {'cd_ref': 2, 'ref_citation': 'Cárdenas D., Baptiste M.P., Castaño N. (2017). Plantas exóticas con alto potencial de invasión en Colombia. Instituto de Investigación de Recursos Biológicos Alexander von Humboldt. Bogotá, D. C., Colombia. 295 p.', 'link': None, 'nb_endem': 0, 'nb_exot': 36, 'nb_threat': 0}, {'cd_ref': 3, 'ref_citation': 'Mora, M. F., Rubio J., Ocampo R. & Barrera J.I. (2015). Catálogo de especies invasoras del territorio CAR. Publicado por Pontificia Universidad Javeriana & Corporación Autónoma Regional de Cundinamarca – CAR, 238 pp.', 'link': None, 'nb_endem': 0, 'nb_exot': 1, 'nb_threat': 0}, {'cd_ref': 4, 'ref_citation': 'Corporación Autónoma Regional (2018). Plan de Prevención, Control y Manejo (PPCM) de Caracol Gigante Africano (Achatina fulica) en la jurisdicción CAR. Dirección de Recursos Naturales. 61 pp.', 'link': 'https://www.car.gov.co/uploads/files/5b9033f095d34.pdf', 'nb_endem': 0, 'nb_exot': 1, 'nb_threat': 0}, {'cd_ref': 5, 'ref_citation': 'Invasive Species Specialist Group (2020). Achatina fulica.', 'link': 'http://www.iucngisd.org/gisd/speciesname/Achatina+fulica', 'nb_endem': 0, 'nb_exot': 1, 'nb_threat': 0}, {'cd_ref': 6, 'ref_citation': 'Garcés M., Patiño A., Gómez M., Giraldo A. & Bolívar G. (2016). Sustancias alternativas para el control del caracol africano (Achatina fulica) en el Valle del Cauca. Biota Colombiana. Vol. 17(1), 44 - 52 pp.', 'link': None, 'nb_endem': 0, 'nb_exot': 1, 'nb_threat': 0}, {'cd_ref': 7, 'ref_citation': 'Invasive Species Compendium (2019). Anthoxanthum odoratum (sweet vernal grass).', 'link': 'https://www.cabi.org/isc/datasheet/93023', 'nb_endem': 0, 'nb_exot': 1, 'nb_threat': 0}, {'cd_ref': 8, 'ref_citation': 'Invasive Species Compendium (2019). Arundo donax (giant reed).', 'link': 'https://www.cabi.org/isc/datasheet/1940', 'nb_endem': 0, 'nb_exot': 1, 'nb_threat': 0}, {'cd_ref': 9, 'ref_citation': 'Invasive Species Compendium (2019). Azolla filiculoides (water fern).', 'link': 'https://www.cabi.org/isc/datasheet/8119', 'nb_endem': 0, 'nb_exot': 1, 'nb_threat': 0}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listReferences?format=CSV>

------------------------------------------------------------------------

### 12.1.2 Only the references concerning exotic species

``` python
onlyExot={'onlyExot':True}
response = requests.get(api_url+endpoint, json=onlyExot)
content=response.json()
len(content)
```

    ## 90

``` python
content[0:9]
```

    ## [{'cd_ref': 1, 'ref_citation': ' Instituto de Investigación de Recursos Biológicos Alexander von Humboldt (2020). Base de datos de información ecológica e invasividad de especies exóticas prioritarias de flora y fauna de Colombia. 43 registros.', 'link': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020', 'nb_endem': 0, 'nb_exot': 45, 'nb_threat': 0}, {'cd_ref': 2, 'ref_citation': 'Cárdenas D., Baptiste M.P., Castaño N. (2017). Plantas exóticas con alto potencial de invasión en Colombia. Instituto de Investigación de Recursos Biológicos Alexander von Humboldt. Bogotá, D. C., Colombia. 295 p.', 'link': None, 'nb_endem': 0, 'nb_exot': 36, 'nb_threat': 0}, {'cd_ref': 3, 'ref_citation': 'Mora, M. F., Rubio J., Ocampo R. & Barrera J.I. (2015). Catálogo de especies invasoras del territorio CAR. Publicado por Pontificia Universidad Javeriana & Corporación Autónoma Regional de Cundinamarca – CAR, 238 pp.', 'link': None, 'nb_endem': 0, 'nb_exot': 1, 'nb_threat': 0}, {'cd_ref': 4, 'ref_citation': 'Corporación Autónoma Regional (2018). Plan de Prevención, Control y Manejo (PPCM) de Caracol Gigante Africano (Achatina fulica) en la jurisdicción CAR. Dirección de Recursos Naturales. 61 pp.', 'link': 'https://www.car.gov.co/uploads/files/5b9033f095d34.pdf', 'nb_endem': 0, 'nb_exot': 1, 'nb_threat': 0}, {'cd_ref': 5, 'ref_citation': 'Invasive Species Specialist Group (2020). Achatina fulica.', 'link': 'http://www.iucngisd.org/gisd/speciesname/Achatina+fulica', 'nb_endem': 0, 'nb_exot': 1, 'nb_threat': 0}, {'cd_ref': 6, 'ref_citation': 'Garcés M., Patiño A., Gómez M., Giraldo A. & Bolívar G. (2016). Sustancias alternativas para el control del caracol africano (Achatina fulica) en el Valle del Cauca. Biota Colombiana. Vol. 17(1), 44 - 52 pp.', 'link': None, 'nb_endem': 0, 'nb_exot': 1, 'nb_threat': 0}, {'cd_ref': 7, 'ref_citation': 'Invasive Species Compendium (2019). Anthoxanthum odoratum (sweet vernal grass).', 'link': 'https://www.cabi.org/isc/datasheet/93023', 'nb_endem': 0, 'nb_exot': 1, 'nb_threat': 0}, {'cd_ref': 8, 'ref_citation': 'Invasive Species Compendium (2019). Arundo donax (giant reed).', 'link': 'https://www.cabi.org/isc/datasheet/1940', 'nb_endem': 0, 'nb_exot': 1, 'nb_threat': 0}, {'cd_ref': 9, 'ref_citation': 'Invasive Species Compendium (2019). Azolla filiculoides (water fern).', 'link': 'https://www.cabi.org/isc/datasheet/8119', 'nb_endem': 0, 'nb_exot': 1, 'nb_threat': 0}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listReferences?onlyExot=True&format=CSV>

------------------------------------------------------------------------

### 12.1.3 Only the references concerning threatened species

``` python
onlyThreat={'onlyThreat':True}
response = requests.get(api_url+endpoint, json=onlyThreat)
content=response.json()
len(content)
```

    ## 1

``` python
content[0:9]
```

    ## [{'cd_ref': 222, 'ref_citation': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz', 'link': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads', 'nb_endem': 0, 'nb_exot': 0, 'nb_threat': 1299}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listReferences?onlyThreat=True&format=CSV>

------------------------------------------------------------------------

### 12.1.4 Only the references concerning endemic species

``` python
onlyEndem={'onlyEndem':True}
response = requests.get(api_url+endpoint, json=onlyEndem)
content=response.json()
len(content)
```

    ## 131

``` python
content[0:9]
```

    ## [{'cd_ref': 91, 'ref_citation': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue', 'link': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09', 'nb_endem': 308, 'nb_exot': 0, 'nb_threat': 0}, {'cd_ref': 92, 'ref_citation': 'Arbeláez-Cortés et al. 2011b', 'link': None, 'nb_endem': 14, 'nb_exot': 0, 'nb_threat': 0}, {'cd_ref': 93, 'ref_citation': 'Cuervo et al. 2008a', 'link': None, 'nb_endem': 6, 'nb_exot': 0, 'nb_threat': 0}, {'cd_ref': 94, 'ref_citation': 'Cuervo et al. 2008b', 'link': None, 'nb_endem': 7, 'nb_exot': 0, 'nb_threat': 0}, {'cd_ref': 95, 'ref_citation': 'Merkord 2010', 'link': None, 'nb_endem': 2, 'nb_exot': 0, 'nb_threat': 0}, {'cd_ref': 96, 'ref_citation': 'Rodríguez y Rojas-Suárez 2008', 'link': None, 'nb_endem': 1, 'nb_exot': 0, 'nb_threat': 0}, {'cd_ref': 97, 'ref_citation': 'Corpocaldas 2010', 'link': None, 'nb_endem': 6, 'nb_exot': 0, 'nb_threat': 0}, {'cd_ref': 98, 'ref_citation': 'Donegan et al. 2010', 'link': None, 'nb_endem': 25, 'nb_exot': 0, 'nb_threat': 0}, {'cd_ref': 99, 'ref_citation': 'Laverde-R. Et al. 2005b', 'link': None, 'nb_endem': 5, 'nb_exot': 0, 'nb_threat': 0}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listReferences?onlyEndem=True&format=CSV>

------------------------------------------------------------------------
