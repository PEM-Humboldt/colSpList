Functionality tests and examples for the colSpListAPI: basic query
endpoints
================

-   [/testEndem](#testendem)
    -   [GET](#get)
        -   [Species with an endemic
            status](#species-with-an-endemic-status)
        -   [Species without an endemic
            status](#species-without-an-endemic-status)
        -   [Error: no sufficient information
            given](#error-no-sufficient-information-given)
-   [/testEndem/list](#testendemlist)
    -   [POST](#post)
-   [/testExot](#testexot)
    -   [GET](#get-1)
        -   [Species with an exotic
            status](#species-with-an-exotic-status)
        -   [Species without an exotic
            status](#species-without-an-exotic-status)
        -   [Error: no sufficient information
            given](#error-no-sufficient-information-given-1)
-   [/testExot/list](#testexotlist)
    -   [POST](#post-1)
-   [/testThreat](#testthreat)
    -   [GET](#get-2)
        -   [Species with an threatened
            status](#species-with-an-threatened-status)
        -   [Species without an threatened
            status](#species-without-an-threatened-status)
        -   [Error: no sufficient information
            given](#error-no-sufficient-information-given-2)
-   [/testThreat/list](#testthreatlist)
    -   [POST](#post-2)
-   [/listEndem](#listendem)
    -   [GET](#get-3)
        -   [Comprehensive list](#comprehensive-list)
        -   [Only the passerine birds](#only-the-passerine-birds)
        -   [Error: asking for an unknown
            group](#error-asking-for-an-unknown-group)
-   [/listExot](#listexot)
    -   [GET](#get-4)
        -   [Comprehensive list](#comprehensive-list-1)
        -   [Only the passerine birds](#only-the-passerine-birds-1)
        -   [Error: asking for an unknown
            group](#error-asking-for-an-unknown-group-1)
-   [/listThreat](#listthreat)
    -   [GET](#get-5)
        -   [Comprehensive list](#comprehensive-list-2)
        -   [Only the passerine birds](#only-the-passerine-birds-2)
        -   [Error: asking for an unknown
            group](#error-asking-for-an-unknown-group-2)
-   [/tax](#tax)
    -   [GET](#get-6)
        -   [From the cd_tax](#from-the-cd_tax)
        -   [From a scientific name](#from-a-scientific-name)
        -   [From a canonical name](#from-a-canonical-name)
        -   [Species which is not in
            database](#species-which-is-not-in-database)
        -   [Species which does not
            exist](#species-which-does-not-exist)
-   [/listTax](#listtax)
    -   [GET](#get-7)
        -   [Comprehensive list](#comprehensive-list-3)
        -   [Only the Bivalve](#only-the-bivalve)
-   [/listReferences](#listreferences)
    -   [GET](#get-8)
        -   [Comprehensive list](#comprehensive-list-4)
        -   [Only the references concerning exotic
            species](#only-the-references-concerning-exotic-species)
        -   [Only the references concerning threatened
            species](#only-the-references-concerning-threatened-species)
        -   [Only the references concerning endemic
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
from pprint import pprint as pp
api_url="http://colsplist.herokuapp.com"
```

# /testEndem

## GET

``` python
endpoint="/testEndem"
```

The /testEndem endpoint allows to search a taxon in the API database and
returns its endemism status if it has one.

### Species with an endemic status

#### From canonical name

``` python
toSend1={'canonicalname':'Accipiter collaris'}
response = requests.get(api_url+endpoint, json=toSend1)
pp(response.json())
```

    ## {'acceptedname': 'Accipiter collaris P.L.Sclater, 1860',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': 3,
    ##  'cd_tax': 1281,
    ##  'cd_tax_acc': 1281,
    ##  'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | '
    ##              'Vertiente oriental hacia Amazonía | Perú: Amazonas (desde '
    ##              'divisoria de aguas y principales drenajes al río Amazonas) | '
    ##              'occurrenceRemarks: Franja y región: Tierras bajas para especies '
    ##              'cuyos límites superiores de distribución están alrededor de '
    ##              '1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el '
    ##              'Golfo de Urabá hasta la Península de La Guajira, incluyendo las '
    ##              'estribaciones de la Sierra Nevada de Santa Marta y la Serranía '
    ##              'de Perijá en el norte de Cesar, y como subregión |Elevaciones '
    ##              'medias para especies que se distribuyen entre ca. 800-l000 y '
    ##              '2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones '
    ##              'medias para especies que se distribuyen entre ca. 800-l000 y '
    ##              '2000-2400 m s.n.m. Laderas más al norte de la cordillera '
    ##              'Occidental y de la cordillera Central y la ladera nororiental de '
    ##              'la Central hacia el sur hasta aproximadamente el límite sur de '
    ##              'Caldas |Elevaciones altas, para especies cuyos límites '
    ##              'inferiores caen por encima de ca. 2000 m s.n.m. cordillera '
    ##              'Central | ',
    ##  'endemism': 'Casi endémica',
    ##  'endemism_en': 'Almost endemic',
    ##  'foundGbif': True,
    ##  'gbifkey': 2480593,
    ##  'hasEndemStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##  'matchedname': 'Accipiter collaris',
    ##  'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, '
    ##                'S., Sua-Becerra, A. (2013). Listado actualizado de las aves '
    ##                'endémicas y casi-endémicas de Colombia. 308 registros. Versión '
    ##                '5.1. http://doi.org/10.15472/tozuue | Arbeláez-Cortés et al. '
    ##                '2011b | Cuervo et al. 2008a | Cuervo et al. 2008b | Merkord '
    ##                '2010 | Rodríguez y Rojas-Suárez 2008',
    ##  'syno': False}

#### From scientific name

``` python
toSend2={'scientificname':'Odontophorus strophium (Gould, 1844)'}
response = requests.get(api_url+endpoint, json=toSend2)
pp(response.json())
```

    ## {'acceptedname': 'Odontophorus strophium (Gould, 1844)',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': 4,
    ##  'cd_tax': 1678,
    ##  'cd_tax_acc': 1678,
    ##  'comments': 'occurrenceRemarks: Franja y región: Elevaciones medias para '
    ##              'especies que se distribuyen entre ca. 800-l000 y 2000-2400 m '
    ##              's.n.m. Vertiente occidental de la cordillera Oriental, desde el '
    ##              'sur de Cesar hasta Cundinamarca | ',
    ##  'endemism': 'Endémica',
    ##  'endemism_en': 'Endemic',
    ##  'foundGbif': True,
    ##  'gbifkey': 5228041,
    ##  'hasEndemStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##  'matchedname': 'Odontophorus strophium (Gould, 1844)',
    ##  'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, '
    ##                'S., Sua-Becerra, A. (2013). Listado actualizado de las aves '
    ##                'endémicas y casi-endémicas de Colombia. 308 registros. Versión '
    ##                '5.1. http://doi.org/10.15472/tozuue',
    ##  'syno': False}

#### From gbifkey

``` python
toSend3={'gbifkey':2480593}
response = requests.get(api_url+endpoint, json=toSend3)
pp(response.json())
```

    ## {'acceptedname': 'Accipiter collaris P.L.Sclater, 1860',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': 3,
    ##  'cd_tax': 1281,
    ##  'cd_tax_acc': 1281,
    ##  'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | '
    ##              'Vertiente oriental hacia Amazonía | Perú: Amazonas (desde '
    ##              'divisoria de aguas y principales drenajes al río Amazonas) | '
    ##              'occurrenceRemarks: Franja y región: Tierras bajas para especies '
    ##              'cuyos límites superiores de distribución están alrededor de '
    ##              '1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el '
    ##              'Golfo de Urabá hasta la Península de La Guajira, incluyendo las '
    ##              'estribaciones de la Sierra Nevada de Santa Marta y la Serranía '
    ##              'de Perijá en el norte de Cesar, y como subregión |Elevaciones '
    ##              'medias para especies que se distribuyen entre ca. 800-l000 y '
    ##              '2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones '
    ##              'medias para especies que se distribuyen entre ca. 800-l000 y '
    ##              '2000-2400 m s.n.m. Laderas más al norte de la cordillera '
    ##              'Occidental y de la cordillera Central y la ladera nororiental de '
    ##              'la Central hacia el sur hasta aproximadamente el límite sur de '
    ##              'Caldas |Elevaciones altas, para especies cuyos límites '
    ##              'inferiores caen por encima de ca. 2000 m s.n.m. cordillera '
    ##              'Central | ',
    ##  'endemism': 'Casi endémica',
    ##  'endemism_en': 'Almost endemic',
    ##  'foundGbif': True,
    ##  'gbifkey': 2480593,
    ##  'hasEndemStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##  'matchedname': 'Accipiter collaris P.L.Sclater, 1860',
    ##  'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, '
    ##                'S., Sua-Becerra, A. (2013). Listado actualizado de las aves '
    ##                'endémicas y casi-endémicas de Colombia. 308 registros. Versión '
    ##                '5.1. http://doi.org/10.15472/tozuue | Arbeláez-Cortés et al. '
    ##                '2011b | Cuervo et al. 2008a | Cuervo et al. 2008b | Merkord '
    ##                '2010 | Rodríguez y Rojas-Suárez 2008',
    ##  'syno': False}

#### synonym of a species with an endemic status

``` python
toSend4 = {'canonicalname':'Anas andium'}
response = requests.get(api_url+endpoint, json=toSend4)
pp(response.json())
```

    ## {'acceptedname': 'Anas flavirostris andium (P.L.Sclater & Salvin, 1873)',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': 3,
    ##  'cd_tax': 1303,
    ##  'cd_tax_acc': 1302,
    ##  'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | '
    ##              'Perú: Andes (incluido valles interandinos) | occurrenceRemarks: '
    ##              'Franja y región: Elevaciones altas, para especies cuyos límites '
    ##              'inferiores caen por encima de ca. 2000 m s.n.m. cordillera '
    ##              'Central |Elevaciones altas, para especies cuyos límites '
    ##              'inferiores caen por encima de ca. 2000 m s.n.m. altiplano '
    ##              'Cundiboyacense. | ',
    ##  'endemism': 'Casi endémica',
    ##  'endemism_en': 'Almost endemic',
    ##  'foundGbif': True,
    ##  'gbifkey': 2498068,
    ##  'hasEndemStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##  'matchedname': 'Anas andium',
    ##  'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, '
    ##                'S., Sua-Becerra, A. (2013). Listado actualizado de las aves '
    ##                'endémicas y casi-endémicas de Colombia. 308 registros. Versión '
    ##                '5.1. http://doi.org/10.15472/tozuue | Parra-Hernández et al. '
    ##                '2007',
    ##  'syno': True}

#### spelling error

(Accipiter coll**O**ris en lugat de Accipiter coll**A**ris)

``` python
toSend5 = {'canonicalname':'Accipiter colloris'}
response = requests.get(api_url+endpoint, json=toSend5)
pp(response.json())
```

    ## {'acceptedname': 'Accipiter collaris P.L.Sclater, 1860',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': 3,
    ##  'cd_tax': 1281,
    ##  'cd_tax_acc': 1281,
    ##  'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | '
    ##              'Vertiente oriental hacia Amazonía | Perú: Amazonas (desde '
    ##              'divisoria de aguas y principales drenajes al río Amazonas) | '
    ##              'occurrenceRemarks: Franja y región: Tierras bajas para especies '
    ##              'cuyos límites superiores de distribución están alrededor de '
    ##              '1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el '
    ##              'Golfo de Urabá hasta la Península de La Guajira, incluyendo las '
    ##              'estribaciones de la Sierra Nevada de Santa Marta y la Serranía '
    ##              'de Perijá en el norte de Cesar, y como subregión |Elevaciones '
    ##              'medias para especies que se distribuyen entre ca. 800-l000 y '
    ##              '2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones '
    ##              'medias para especies que se distribuyen entre ca. 800-l000 y '
    ##              '2000-2400 m s.n.m. Laderas más al norte de la cordillera '
    ##              'Occidental y de la cordillera Central y la ladera nororiental de '
    ##              'la Central hacia el sur hasta aproximadamente el límite sur de '
    ##              'Caldas |Elevaciones altas, para especies cuyos límites '
    ##              'inferiores caen por encima de ca. 2000 m s.n.m. cordillera '
    ##              'Central | ',
    ##  'endemism': 'Casi endémica',
    ##  'endemism_en': 'Almost endemic',
    ##  'foundGbif': True,
    ##  'gbifkey': 2480593,
    ##  'hasEndemStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##  'matchedname': 'Accipiter collaris',
    ##  'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, '
    ##                'S., Sua-Becerra, A. (2013). Listado actualizado de las aves '
    ##                'endémicas y casi-endémicas de Colombia. 308 registros. Versión '
    ##                '5.1. http://doi.org/10.15472/tozuue | Arbeláez-Cortés et al. '
    ##                '2011b | Cuervo et al. 2008a | Cuervo et al. 2008b | Merkord '
    ##                '2010 | Rodríguez y Rojas-Suárez 2008',
    ##  'syno': False}

### Species without an endemic status

#### Species which is in the database but has no endemic status

``` python
toSend6={'canonicalname':'Elaeis guineensis'}
response = requests.get(api_url+endpoint, json=toSend6)
pp(response.json())
```

    ## {'acceptedname': 'Elaeis guineensis Jacq.',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': None,
    ##  'cd_tax': 62,
    ##  'cd_tax_acc': 62,
    ##  'comments': None,
    ##  'descr_endem_es': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 2731882,
    ##  'hasEndemStatus': False,
    ##  'insertedTax': [],
    ##  'links': None,
    ##  'matchedname': 'Elaeis guineensis',
    ##  'references': None,
    ##  'syno': False}

#### Species which is not in the database

``` python
toSend7={'canonicalname':'Espeletia grandiflora'}
response = requests.get(api_url+endpoint, json=toSend7)
pp(response.json())
```

    ## {'acceptedname': 'Espeletia grandiflora Humb. & Bonpl.',
    ##  'alreadyInDb': False,
    ##  'cd_status': None,
    ##  'cd_tax': 0,
    ##  'cd_tax_acc': 0,
    ##  'comments': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 3105059,
    ##  'hasEndemStatus': False,
    ##  'insertedTax': [],
    ##  'links': [],
    ##  'matchedname': 'Espeletia grandiflora',
    ##  'references': [],
    ##  'syno': False}

#### Species which does not exists

``` python
toSend8={'canonicalname':'Asriwendosa machibibus'}
response = requests.get(api_url+endpoint, json=toSend8)
pp(response.json())
```

    ## {'acceptedname': None,
    ##  'alreadyInDb': False,
    ##  'cd_status': None,
    ##  'cd_tax': 0,
    ##  'cd_tax_acc': 0,
    ##  'comments': None,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasEndemStatus': False,
    ##  'insertedTax': [],
    ##  'links': [],
    ##  'matchedname': None,
    ##  'references': [],
    ##  'syno': False}

### Error: no sufficient information given

``` python
toSend9={}
response = requests.get(api_url+endpoint, json=toSend9)
pp(response.json())
```

    ## {'error': 'You did not provide GBIF taxon key nor name with nor without '
    ##           "authorship, missing argument: 'scientificname', 'canonicalname' or "
    ##           "'gbifkey'"}

# /testEndem/list

## POST

``` python
endpoint="/testEndem/list"
```

``` python
ListToSend={'list':[toSend1,toSend2,toSend3,toSend4,toSend5,toSend6,toSend7,toSend8,toSend9]}
response = requests.post(api_url+endpoint, json=ListToSend)
pp(response.json())
```

    ## [{'acceptedname': 'Accipiter collaris P.L.Sclater, 1860',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': 3,
    ##   'cd_tax': 1281,
    ##   'cd_tax_acc': 1281,
    ##   'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | '
    ##               'Vertiente oriental hacia Amazonía | Perú: Amazonas (desde '
    ##               'divisoria de aguas y principales drenajes al río Amazonas) | '
    ##               'occurrenceRemarks: Franja y región: Tierras bajas para especies '
    ##               'cuyos límites superiores de distribución están alrededor de '
    ##               '1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el '
    ##               'Golfo de Urabá hasta la Península de La Guajira, incluyendo las '
    ##               'estribaciones de la Sierra Nevada de Santa Marta y la Serranía '
    ##               'de Perijá en el norte de Cesar, y como subregión |Elevaciones '
    ##               'medias para especies que se distribuyen entre ca. 800-l000 y '
    ##               '2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones '
    ##               'medias para especies que se distribuyen entre ca. 800-l000 y '
    ##               '2000-2400 m s.n.m. Laderas más al norte de la cordillera '
    ##               'Occidental y de la cordillera Central y la ladera nororiental '
    ##               'de la Central hacia el sur hasta aproximadamente el límite sur '
    ##               'de Caldas |Elevaciones altas, para especies cuyos límites '
    ##               'inferiores caen por encima de ca. 2000 m s.n.m. cordillera '
    ##               'Central | ',
    ##   'endemism': 'Casi endémica',
    ##   'endemism_en': 'Almost endemic',
    ##   'foundGbif': True,
    ##   'gbifkey': 2480593,
    ##   'hasEndemStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##   'matchedname': 'Accipiter collaris',
    ##   'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., '
    ##                 'Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado '
    ##                 'actualizado de las aves endémicas y casi-endémicas de '
    ##                 'Colombia. 308 registros. Versión 5.1. '
    ##                 'http://doi.org/10.15472/tozuue | Arbeláez-Cortés et al. 2011b '
    ##                 '| Cuervo et al. 2008a | Cuervo et al. 2008b | Merkord 2010 | '
    ##                 'Rodríguez y Rojas-Suárez 2008',
    ##   'syno': False},
    ##  {'acceptedname': 'Odontophorus strophium (Gould, 1844)',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': 4,
    ##   'cd_tax': 1678,
    ##   'cd_tax_acc': 1678,
    ##   'comments': 'occurrenceRemarks: Franja y región: Elevaciones medias para '
    ##               'especies que se distribuyen entre ca. 800-l000 y 2000-2400 m '
    ##               's.n.m. Vertiente occidental de la cordillera Oriental, desde el '
    ##               'sur de Cesar hasta Cundinamarca | ',
    ##   'endemism': 'Endémica',
    ##   'endemism_en': 'Endemic',
    ##   'foundGbif': True,
    ##   'gbifkey': 5228041,
    ##   'hasEndemStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##   'matchedname': 'Odontophorus strophium (Gould, 1844)',
    ##   'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., '
    ##                 'Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado '
    ##                 'actualizado de las aves endémicas y casi-endémicas de '
    ##                 'Colombia. 308 registros. Versión 5.1. '
    ##                 'http://doi.org/10.15472/tozuue',
    ##   'syno': False},
    ##  {'acceptedname': 'Accipiter collaris P.L.Sclater, 1860',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': 3,
    ##   'cd_tax': 1281,
    ##   'cd_tax_acc': 1281,
    ##   'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | '
    ##               'Vertiente oriental hacia Amazonía | Perú: Amazonas (desde '
    ##               'divisoria de aguas y principales drenajes al río Amazonas) | '
    ##               'occurrenceRemarks: Franja y región: Tierras bajas para especies '
    ##               'cuyos límites superiores de distribución están alrededor de '
    ##               '1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el '
    ##               'Golfo de Urabá hasta la Península de La Guajira, incluyendo las '
    ##               'estribaciones de la Sierra Nevada de Santa Marta y la Serranía '
    ##               'de Perijá en el norte de Cesar, y como subregión |Elevaciones '
    ##               'medias para especies que se distribuyen entre ca. 800-l000 y '
    ##               '2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones '
    ##               'medias para especies que se distribuyen entre ca. 800-l000 y '
    ##               '2000-2400 m s.n.m. Laderas más al norte de la cordillera '
    ##               'Occidental y de la cordillera Central y la ladera nororiental '
    ##               'de la Central hacia el sur hasta aproximadamente el límite sur '
    ##               'de Caldas |Elevaciones altas, para especies cuyos límites '
    ##               'inferiores caen por encima de ca. 2000 m s.n.m. cordillera '
    ##               'Central | ',
    ##   'endemism': 'Casi endémica',
    ##   'endemism_en': 'Almost endemic',
    ##   'foundGbif': True,
    ##   'gbifkey': 2480593,
    ##   'hasEndemStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##   'matchedname': 'Accipiter collaris P.L.Sclater, 1860',
    ##   'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., '
    ##                 'Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado '
    ##                 'actualizado de las aves endémicas y casi-endémicas de '
    ##                 'Colombia. 308 registros. Versión 5.1. '
    ##                 'http://doi.org/10.15472/tozuue | Arbeláez-Cortés et al. 2011b '
    ##                 '| Cuervo et al. 2008a | Cuervo et al. 2008b | Merkord 2010 | '
    ##                 'Rodríguez y Rojas-Suárez 2008',
    ##   'syno': False},
    ##  {'acceptedname': 'Anas flavirostris andium (P.L.Sclater & Salvin, 1873)',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': 3,
    ##   'cd_tax': 1303,
    ##   'cd_tax_acc': 1302,
    ##   'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | '
    ##               'Perú: Andes (incluido valles interandinos) | occurrenceRemarks: '
    ##               'Franja y región: Elevaciones altas, para especies cuyos límites '
    ##               'inferiores caen por encima de ca. 2000 m s.n.m. cordillera '
    ##               'Central |Elevaciones altas, para especies cuyos límites '
    ##               'inferiores caen por encima de ca. 2000 m s.n.m. altiplano '
    ##               'Cundiboyacense. | ',
    ##   'endemism': 'Casi endémica',
    ##   'endemism_en': 'Almost endemic',
    ##   'foundGbif': True,
    ##   'gbifkey': 2498068,
    ##   'hasEndemStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##   'matchedname': 'Anas andium',
    ##   'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., '
    ##                 'Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado '
    ##                 'actualizado de las aves endémicas y casi-endémicas de '
    ##                 'Colombia. 308 registros. Versión 5.1. '
    ##                 'http://doi.org/10.15472/tozuue | Parra-Hernández et al. 2007',
    ##   'syno': True},
    ##  {'acceptedname': 'Accipiter collaris P.L.Sclater, 1860',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': 3,
    ##   'cd_tax': 1281,
    ##   'cd_tax_acc': 1281,
    ##   'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | '
    ##               'Vertiente oriental hacia Amazonía | Perú: Amazonas (desde '
    ##               'divisoria de aguas y principales drenajes al río Amazonas) | '
    ##               'occurrenceRemarks: Franja y región: Tierras bajas para especies '
    ##               'cuyos límites superiores de distribución están alrededor de '
    ##               '1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el '
    ##               'Golfo de Urabá hasta la Península de La Guajira, incluyendo las '
    ##               'estribaciones de la Sierra Nevada de Santa Marta y la Serranía '
    ##               'de Perijá en el norte de Cesar, y como subregión |Elevaciones '
    ##               'medias para especies que se distribuyen entre ca. 800-l000 y '
    ##               '2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones '
    ##               'medias para especies que se distribuyen entre ca. 800-l000 y '
    ##               '2000-2400 m s.n.m. Laderas más al norte de la cordillera '
    ##               'Occidental y de la cordillera Central y la ladera nororiental '
    ##               'de la Central hacia el sur hasta aproximadamente el límite sur '
    ##               'de Caldas |Elevaciones altas, para especies cuyos límites '
    ##               'inferiores caen por encima de ca. 2000 m s.n.m. cordillera '
    ##               'Central | ',
    ##   'endemism': 'Casi endémica',
    ##   'endemism_en': 'Almost endemic',
    ##   'foundGbif': True,
    ##   'gbifkey': 2480593,
    ##   'hasEndemStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##   'matchedname': 'Accipiter collaris',
    ##   'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., '
    ##                 'Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado '
    ##                 'actualizado de las aves endémicas y casi-endémicas de '
    ##                 'Colombia. 308 registros. Versión 5.1. '
    ##                 'http://doi.org/10.15472/tozuue | Arbeláez-Cortés et al. 2011b '
    ##                 '| Cuervo et al. 2008a | Cuervo et al. 2008b | Merkord 2010 | '
    ##                 'Rodríguez y Rojas-Suárez 2008',
    ##   'syno': False},
    ##  {'acceptedname': 'Elaeis guineensis Jacq.',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': None,
    ##   'cd_tax': 62,
    ##   'cd_tax_acc': 62,
    ##   'comments': None,
    ##   'descr_endem_es': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 2731882,
    ##   'hasEndemStatus': False,
    ##   'insertedTax': [],
    ##   'links': None,
    ##   'matchedname': 'Elaeis guineensis',
    ##   'references': None,
    ##   'syno': False},
    ##  {'acceptedname': 'Espeletia grandiflora Humb. & Bonpl.',
    ##   'alreadyInDb': False,
    ##   'cd_status': None,
    ##   'cd_tax': 0,
    ##   'cd_tax_acc': 0,
    ##   'comments': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 3105059,
    ##   'hasEndemStatus': False,
    ##   'insertedTax': [],
    ##   'links': [],
    ##   'matchedname': 'Espeletia grandiflora',
    ##   'references': [],
    ##   'syno': False},
    ##  {'acceptedname': None,
    ##   'alreadyInDb': False,
    ##   'cd_status': None,
    ##   'cd_tax': 0,
    ##   'cd_tax_acc': 0,
    ##   'comments': None,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasEndemStatus': False,
    ##   'insertedTax': [],
    ##   'links': [],
    ##   'matchedname': None,
    ##   'references': [],
    ##   'syno': False},
    ##  {'error': 'You did not provide GBIF taxon key nor name with nor without '
    ##            "authorship, missing argument: 'scientificname', 'canonicalname' or "
    ##            "'gbifkey'"}]

# /testExot

## GET

``` python
endpoint="/testExot"
```

The /testExot endpoint allows to search a taxon in the API database and
returns its exotic status if it has one.

### Species with an exotic status

#### From canonical name

``` python
toSend1={'canonicalname':'Gymnocorymbus ternetzi'}
response = requests.get(api_url+endpoint, json=toSend1)
pp(response.json())
```

    ## {'acceptedname': 'Gymnocorymbus ternetzi (Boulenger, 1895)',
    ##  'alreadyInDb': True,
    ##  'cd_tax': 690,
    ##  'cd_tax_acc': 690,
    ##  'comments': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 2353920,
    ##  'hasExotStatus': True,
    ##  'insertedTax': [],
    ##  'is_alien': True,
    ##  'is_invasive': False,
    ##  'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91',
    ##  'matchedname': 'Gymnocorymbus ternetzi',
    ##  'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, '
    ##                'Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, '
    ##                'E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, '
    ##                'Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, '
    ##                'Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, '
    ##                'DoNascimiento C, Alexandra Duque R, Victoria Flechas S, '
    ##                'Dimitri Forero I, José Gómez Hoyos A, González Durán G, '
    ##                'Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, '
    ##                'Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, '
    ##                'Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado '
    ##                'M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona '
    ##                'N, Paola Velásquez L, Wong L J, Pagad S (2020). Global '
    ##                'Register of Introduced and Invasive Species - Colombia. '
    ##                'Version 1.5. Invasive Species Specialist Group ISSG.',
    ##  'syno': False}

#### From scientific name

``` python
toSend2={'scientificname':'Rosa chinensis Jacq.'}
response = requests.get(api_url+endpoint, json=toSend2)
pp(response.json())
```

    ## {'acceptedname': 'Rosa chinensis Jacq.',
    ##  'alreadyInDb': True,
    ##  'cd_tax': 1133,
    ##  'cd_tax_acc': 1133,
    ##  'comments': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 3005039,
    ##  'hasExotStatus': True,
    ##  'insertedTax': [],
    ##  'is_alien': True,
    ##  'is_invasive': False,
    ##  'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91',
    ##  'matchedname': 'Rosa chinensis Jacq.',
    ##  'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, '
    ##                'Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, '
    ##                'E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, '
    ##                'Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, '
    ##                'Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, '
    ##                'DoNascimiento C, Alexandra Duque R, Victoria Flechas S, '
    ##                'Dimitri Forero I, José Gómez Hoyos A, González Durán G, '
    ##                'Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, '
    ##                'Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, '
    ##                'Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado '
    ##                'M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona '
    ##                'N, Paola Velásquez L, Wong L J, Pagad S (2020). Global '
    ##                'Register of Introduced and Invasive Species - Colombia. '
    ##                'Version 1.5. Invasive Species Specialist Group ISSG.',
    ##  'syno': False}

#### From gbifkey

``` python
toSend3={'gbifkey':5190769}
response = requests.get(api_url+endpoint, json=toSend3)
pp(response.json())
```

    ## {'acceptedname': 'Oxychilus alliarius (J.S.Miller, 1822)',
    ##  'alreadyInDb': True,
    ##  'cd_tax': 959,
    ##  'cd_tax_acc': 959,
    ##  'comments': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 5190769,
    ##  'hasExotStatus': True,
    ##  'insertedTax': [],
    ##  'is_alien': True,
    ##  'is_invasive': False,
    ##  'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91',
    ##  'matchedname': 'Oxychilus alliarius (J.S.Miller, 1822)',
    ##  'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, '
    ##                'Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, '
    ##                'E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, '
    ##                'Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, '
    ##                'Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, '
    ##                'DoNascimiento C, Alexandra Duque R, Victoria Flechas S, '
    ##                'Dimitri Forero I, José Gómez Hoyos A, González Durán G, '
    ##                'Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, '
    ##                'Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, '
    ##                'Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado '
    ##                'M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona '
    ##                'N, Paola Velásquez L, Wong L J, Pagad S (2020). Global '
    ##                'Register of Introduced and Invasive Species - Colombia. '
    ##                'Version 1.5. Invasive Species Specialist Group ISSG.',
    ##  'syno': False}

#### synonym of a species with an exotic status

``` python
toSend4 = {'canonicalname':'Cnidoscolus chayamansa'}
response = requests.get(api_url+endpoint, json=toSend4)
pp(response.json())
```

    ## {'acceptedname': 'Cnidoscolus aconitifolius subsp. aconitifolius',
    ##  'alreadyInDb': True,
    ##  'cd_tax': 479,
    ##  'cd_tax_acc': 478,
    ##  'comments': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 3073521,
    ##  'hasExotStatus': True,
    ##  'insertedTax': [],
    ##  'is_alien': True,
    ##  'is_invasive': False,
    ##  'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91',
    ##  'matchedname': 'Cnidoscolus chayamansa',
    ##  'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, '
    ##                'Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, '
    ##                'E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, '
    ##                'Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, '
    ##                'Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, '
    ##                'DoNascimiento C, Alexandra Duque R, Victoria Flechas S, '
    ##                'Dimitri Forero I, José Gómez Hoyos A, González Durán G, '
    ##                'Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, '
    ##                'Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, '
    ##                'Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado '
    ##                'M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona '
    ##                'N, Paola Velásquez L, Wong L J, Pagad S (2020). Global '
    ##                'Register of Introduced and Invasive Species - Colombia. '
    ##                'Version 1.5. Invasive Species Specialist Group ISSG.',
    ##  'syno': True}

#### spelling error

(Accipiter Rosa chin**A**nsis en lugar de Rosa chin**E**nsis)

``` python
toSend5 = {'canonicalname':'Rosa chinansis'}
response = requests.get(api_url+endpoint, json=toSend5)
pp(response.json())
```

    ## {'acceptedname': 'Rosa chinensis Jacq.',
    ##  'alreadyInDb': True,
    ##  'cd_tax': 1133,
    ##  'cd_tax_acc': 1133,
    ##  'comments': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 3005039,
    ##  'hasExotStatus': True,
    ##  'insertedTax': [],
    ##  'is_alien': True,
    ##  'is_invasive': False,
    ##  'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91',
    ##  'matchedname': 'Rosa chinensis',
    ##  'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, '
    ##                'Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, '
    ##                'E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, '
    ##                'Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, '
    ##                'Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, '
    ##                'DoNascimiento C, Alexandra Duque R, Victoria Flechas S, '
    ##                'Dimitri Forero I, José Gómez Hoyos A, González Durán G, '
    ##                'Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, '
    ##                'Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, '
    ##                'Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado '
    ##                'M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona '
    ##                'N, Paola Velásquez L, Wong L J, Pagad S (2020). Global '
    ##                'Register of Introduced and Invasive Species - Colombia. '
    ##                'Version 1.5. Invasive Species Specialist Group ISSG.',
    ##  'syno': False}

### Species without an exotic status

#### Species which is in the database but has no exotic status

``` python
toSend6={'canonicalname':'Licania glauca'}
response = requests.get(api_url+endpoint, json=toSend6)
pp(response.json())
```

    ## {'acceptedname': 'Licania glauca Cuatrec.',
    ##  'alreadyInDb': True,
    ##  'cd_nivel': None,
    ##  'cd_tax': 2810,
    ##  'cd_tax_acc': 2810,
    ##  'comments': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 2985428,
    ##  'hasExotStatus': False,
    ##  'insertedTax': [],
    ##  'is_alien': None,
    ##  'is_invasive': None,
    ##  'links': None,
    ##  'matchedname': 'Licania glauca',
    ##  'references': None,
    ##  'syno': False}

#### Species which is not in the database

``` python
toSend7={'canonicalname':'Espeletia grandiflora'}
response = requests.get(api_url+endpoint, json=toSend7)
pp(response.json())
```

    ## {'acceptedname': 'Espeletia grandiflora Humb. & Bonpl.',
    ##  'alreadyInDb': False,
    ##  'cd_tax': 0,
    ##  'cd_tax_acc': 0,
    ##  'comments': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 3105059,
    ##  'hasExotStatus': False,
    ##  'insertedTax': [],
    ##  'is_alien': None,
    ##  'is_invasive': None,
    ##  'links': [],
    ##  'matchedname': 'Espeletia grandiflora',
    ##  'references': [],
    ##  'syno': False}

#### Species which does not exists

``` python
toSend8={'canonicalname':'Asriwendosa machibibus'}
response = requests.get(api_url+endpoint, json=toSend8)
pp(response.json())
```

    ## {'acceptedname': None,
    ##  'alreadyInDb': False,
    ##  'cd_tax': 0,
    ##  'cd_tax_acc': 0,
    ##  'comments': None,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasExotStatus': False,
    ##  'insertedTax': [],
    ##  'is_alien': None,
    ##  'is_invasive': None,
    ##  'links': [],
    ##  'matchedname': None,
    ##  'references': [],
    ##  'syno': False}

### Error: no sufficient information given

``` python
toSend9={}
response = requests.get(api_url+endpoint, json=toSend9)
pp(response.json())
```

    ## {'error': 'You did not provide GBIF taxon key nor name with nor without '
    ##           "authorship, missing argument: 'scientificname', 'canonicalname' or "
    ##           "'gbifkey'"}

# /testExot/list

## POST

``` python
endpoint="/testExot/list"
```

``` python
ListToSend={'list':[toSend1,toSend2,toSend3,toSend4,toSend5,toSend6,toSend7,toSend8,toSend9]}
response = requests.post(api_url+endpoint, json=ListToSend)
pp(response.json())
```

    ## [{'acceptedname': 'Gymnocorymbus ternetzi (Boulenger, 1895)',
    ##   'alreadyInDb': True,
    ##   'cd_tax': 690,
    ##   'cd_tax_acc': 690,
    ##   'comments': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 2353920,
    ##   'hasExotStatus': True,
    ##   'insertedTax': [],
    ##   'is_alien': True,
    ##   'is_invasive': False,
    ##   'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91',
    ##   'matchedname': 'Gymnocorymbus ternetzi',
    ##   'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, '
    ##                 'Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, '
    ##                 'E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, '
    ##                 'Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes '
    ##                 'Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, '
    ##                 'DoNascimiento C, Alexandra Duque R, Victoria Flechas S, '
    ##                 'Dimitri Forero I, José Gómez Hoyos A, González Durán G, '
    ##                 'Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, '
    ##                 'Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, '
    ##                 'Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado '
    ##                 'M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, '
    ##                 'Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S '
    ##                 '(2020). Global Register of Introduced and Invasive Species - '
    ##                 'Colombia. Version 1.5. Invasive Species Specialist Group '
    ##                 'ISSG.',
    ##   'syno': False},
    ##  {'acceptedname': 'Rosa chinensis Jacq.',
    ##   'alreadyInDb': True,
    ##   'cd_tax': 1133,
    ##   'cd_tax_acc': 1133,
    ##   'comments': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 3005039,
    ##   'hasExotStatus': True,
    ##   'insertedTax': [],
    ##   'is_alien': True,
    ##   'is_invasive': False,
    ##   'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91',
    ##   'matchedname': 'Rosa chinensis Jacq.',
    ##   'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, '
    ##                 'Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, '
    ##                 'E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, '
    ##                 'Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes '
    ##                 'Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, '
    ##                 'DoNascimiento C, Alexandra Duque R, Victoria Flechas S, '
    ##                 'Dimitri Forero I, José Gómez Hoyos A, González Durán G, '
    ##                 'Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, '
    ##                 'Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, '
    ##                 'Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado '
    ##                 'M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, '
    ##                 'Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S '
    ##                 '(2020). Global Register of Introduced and Invasive Species - '
    ##                 'Colombia. Version 1.5. Invasive Species Specialist Group '
    ##                 'ISSG.',
    ##   'syno': False},
    ##  {'acceptedname': 'Oxychilus alliarius (J.S.Miller, 1822)',
    ##   'alreadyInDb': True,
    ##   'cd_tax': 959,
    ##   'cd_tax_acc': 959,
    ##   'comments': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 5190769,
    ##   'hasExotStatus': True,
    ##   'insertedTax': [],
    ##   'is_alien': True,
    ##   'is_invasive': False,
    ##   'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91',
    ##   'matchedname': 'Oxychilus alliarius (J.S.Miller, 1822)',
    ##   'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, '
    ##                 'Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, '
    ##                 'E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, '
    ##                 'Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes '
    ##                 'Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, '
    ##                 'DoNascimiento C, Alexandra Duque R, Victoria Flechas S, '
    ##                 'Dimitri Forero I, José Gómez Hoyos A, González Durán G, '
    ##                 'Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, '
    ##                 'Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, '
    ##                 'Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado '
    ##                 'M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, '
    ##                 'Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S '
    ##                 '(2020). Global Register of Introduced and Invasive Species - '
    ##                 'Colombia. Version 1.5. Invasive Species Specialist Group '
    ##                 'ISSG.',
    ##   'syno': False},
    ##  {'acceptedname': 'Cnidoscolus aconitifolius subsp. aconitifolius',
    ##   'alreadyInDb': True,
    ##   'cd_tax': 479,
    ##   'cd_tax_acc': 478,
    ##   'comments': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 3073521,
    ##   'hasExotStatus': True,
    ##   'insertedTax': [],
    ##   'is_alien': True,
    ##   'is_invasive': False,
    ##   'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91',
    ##   'matchedname': 'Cnidoscolus chayamansa',
    ##   'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, '
    ##                 'Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, '
    ##                 'E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, '
    ##                 'Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes '
    ##                 'Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, '
    ##                 'DoNascimiento C, Alexandra Duque R, Victoria Flechas S, '
    ##                 'Dimitri Forero I, José Gómez Hoyos A, González Durán G, '
    ##                 'Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, '
    ##                 'Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, '
    ##                 'Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado '
    ##                 'M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, '
    ##                 'Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S '
    ##                 '(2020). Global Register of Introduced and Invasive Species - '
    ##                 'Colombia. Version 1.5. Invasive Species Specialist Group '
    ##                 'ISSG.',
    ##   'syno': True},
    ##  {'acceptedname': 'Rosa chinensis Jacq.',
    ##   'alreadyInDb': True,
    ##   'cd_tax': 1133,
    ##   'cd_tax_acc': 1133,
    ##   'comments': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 3005039,
    ##   'hasExotStatus': True,
    ##   'insertedTax': [],
    ##   'is_alien': True,
    ##   'is_invasive': False,
    ##   'links': 'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91',
    ##   'matchedname': 'Rosa chinensis',
    ##   'references': 'Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, '
    ##                 'Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, '
    ##                 'E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, '
    ##                 'Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes '
    ##                 'Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, '
    ##                 'DoNascimiento C, Alexandra Duque R, Victoria Flechas S, '
    ##                 'Dimitri Forero I, José Gómez Hoyos A, González Durán G, '
    ##                 'Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, '
    ##                 'Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, '
    ##                 'Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado '
    ##                 'M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, '
    ##                 'Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S '
    ##                 '(2020). Global Register of Introduced and Invasive Species - '
    ##                 'Colombia. Version 1.5. Invasive Species Specialist Group '
    ##                 'ISSG.',
    ##   'syno': False},
    ##  {'acceptedname': 'Licania glauca Cuatrec.',
    ##   'alreadyInDb': True,
    ##   'cd_nivel': None,
    ##   'cd_tax': 2810,
    ##   'cd_tax_acc': 2810,
    ##   'comments': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 2985428,
    ##   'hasExotStatus': False,
    ##   'insertedTax': [],
    ##   'is_alien': None,
    ##   'is_invasive': None,
    ##   'links': None,
    ##   'matchedname': 'Licania glauca',
    ##   'references': None,
    ##   'syno': False},
    ##  {'acceptedname': 'Espeletia grandiflora Humb. & Bonpl.',
    ##   'alreadyInDb': False,
    ##   'cd_tax': 0,
    ##   'cd_tax_acc': 0,
    ##   'comments': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 3105059,
    ##   'hasExotStatus': False,
    ##   'insertedTax': [],
    ##   'is_alien': None,
    ##   'is_invasive': None,
    ##   'links': [],
    ##   'matchedname': 'Espeletia grandiflora',
    ##   'references': [],
    ##   'syno': False},
    ##  {'acceptedname': None,
    ##   'alreadyInDb': False,
    ##   'cd_tax': 0,
    ##   'cd_tax_acc': 0,
    ##   'comments': None,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasExotStatus': False,
    ##   'insertedTax': [],
    ##   'is_alien': None,
    ##   'is_invasive': None,
    ##   'links': [],
    ##   'matchedname': None,
    ##   'references': [],
    ##   'syno': False},
    ##  {'error': 'You did not provide GBIF taxon key nor name with nor without '
    ##            "authorship, missing argument: 'scientificname', 'canonicalname' or "
    ##            "'gbifkey'"}]

# /testThreat

## GET

``` python
endpoint="/testThreat"
```

The /testThreat endpoint allows to search a taxon in the API database
and returns its threat status if it has one.

### Species with an threatened status

#### From canonical name

``` python
toSend1={'canonicalname':'Podocarpus guatemalensis'}
response = requests.get(api_url+endpoint, json=toSend1)
pp(response.json())
```

    ## {'acceptedname': 'Podocarpus guatemalensis Standl.',
    ##  'alreadyInDb': True,
    ##  'cd_status': 'VU',
    ##  'cd_tax': 2099,
    ##  'cd_tax_acc': 2099,
    ##  'comments': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 5285893,
    ##  'hasThreatStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads',
    ##  'matchedname': 'Podocarpus guatemalensis',
    ##  'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista '
    ##                'de especies silvestres amenazadas de la diversidad biológica '
    ##                'continental y marino-costera de Colombia - Resolución 1912 de '
    ##                '2017 expedida por el Ministerio de Ambiente y Desarrollo '
    ##                'Sostenible. v2.5. Ministerio de Ambiente y Desarrollo '
    ##                'Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz',
    ##  'syno': False}

#### From scientific name

``` python
toSend2={'scientificname':'Puya ochroleuca Betancur & Callejas'}
response = requests.get(api_url+endpoint, json=toSend2)
pp(response.json())
```

    ## {'acceptedname': 'Puya ochroleuca Betancur & Callejas',
    ##  'alreadyInDb': True,
    ##  'cd_status': 'EN',
    ##  'cd_tax': 2503,
    ##  'cd_tax_acc': 2503,
    ##  'comments': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 2696064,
    ##  'hasThreatStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads',
    ##  'matchedname': 'Puya ochroleuca Betancur & Callejas',
    ##  'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista '
    ##                'de especies silvestres amenazadas de la diversidad biológica '
    ##                'continental y marino-costera de Colombia - Resolución 1912 de '
    ##                '2017 expedida por el Ministerio de Ambiente y Desarrollo '
    ##                'Sostenible. v2.5. Ministerio de Ambiente y Desarrollo '
    ##                'Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz',
    ##  'syno': False}

#### From gbifkey

``` python
toSend3={'gbifkey':5789077}
response = requests.get(api_url+endpoint, json=toSend3)
pp(response.json())
```

    ## {'acceptedname': 'Scytalopus rodriguezi Krabbe, P.G.W.Salaman, A.Cortes, '
    ##                  'A.Quevedo, L.A.Ortega & C.D.Cadena, 2005',
    ##  'alreadyInDb': True,
    ##  'cd_status': 'VU',
    ##  'cd_tax': 1777,
    ##  'cd_tax_acc': 1777,
    ##  'comments': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 5789077,
    ##  'hasThreatStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads',
    ##  'matchedname': 'Scytalopus rodriguezi Krabbe, P.G.W.Salaman, A.Cortes, '
    ##                 'A.Quevedo, L.A.Ortega & C.D.Cadena, 2005',
    ##  'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista '
    ##                'de especies silvestres amenazadas de la diversidad biológica '
    ##                'continental y marino-costera de Colombia - Resolución 1912 de '
    ##                '2017 expedida por el Ministerio de Ambiente y Desarrollo '
    ##                'Sostenible. v2.5. Ministerio de Ambiente y Desarrollo '
    ##                'Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz',
    ##  'syno': False}

#### synonym of a species with an threatened status

``` python
toSend4 = {'canonicalname':'Ptychoglossus danieli'}
response = requests.get(api_url+endpoint, json=toSend4)
pp(response.json())
```

    ## {'acceptedname': 'Alopoglossus danieli (Harris, 1994)',
    ##  'alreadyInDb': True,
    ##  'cd_status': 'CR',
    ##  'cd_tax': 3515,
    ##  'cd_tax_acc': 3514,
    ##  'comments': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 2450617,
    ##  'hasThreatStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads',
    ##  'matchedname': 'Ptychoglossus danieli',
    ##  'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista '
    ##                'de especies silvestres amenazadas de la diversidad biológica '
    ##                'continental y marino-costera de Colombia - Resolución 1912 de '
    ##                '2017 expedida por el Ministerio de Ambiente y Desarrollo '
    ##                'Sostenible. v2.5. Ministerio de Ambiente y Desarrollo '
    ##                'Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz',
    ##  'syno': True}

#### spelling error

(Espeletia pa**y**pana en lugat de Espeletia pa**i**pana)

``` python
toSend5 = {'canonicalname':'Espeletia paypana'}
response = requests.get(api_url+endpoint, json=toSend5)
pp(response.json())
```

    ## {'acceptedname': 'Espeletia paipana S.Díaz & Pedraza',
    ##  'alreadyInDb': True,
    ##  'cd_status': 'CR',
    ##  'cd_tax': 2831,
    ##  'cd_tax_acc': 2831,
    ##  'comments': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 3105080,
    ##  'hasThreatStatus': True,
    ##  'insertedTax': [],
    ##  'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads',
    ##  'matchedname': 'Espeletia paipana',
    ##  'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista '
    ##                'de especies silvestres amenazadas de la diversidad biológica '
    ##                'continental y marino-costera de Colombia - Resolución 1912 de '
    ##                '2017 expedida por el Ministerio de Ambiente y Desarrollo '
    ##                'Sostenible. v2.5. Ministerio de Ambiente y Desarrollo '
    ##                'Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz',
    ##  'syno': False}

### Species without an threatened status

#### Species which is in the database but has no threatened status

``` python
toSend6={'canonicalname':'Tangara johannae'}
response = requests.get(api_url+endpoint, json=toSend6)
pp(response.json())
```

    ## {'acceptedname': 'Tangara johannae (Dalmas, 1900)',
    ##  'alreadyInDb': True,
    ##  'cd_status': None,
    ##  'cd_tax': 1797,
    ##  'cd_tax_acc': 1797,
    ##  'comments': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 2488153,
    ##  'hasThreatStatus': False,
    ##  'insertedTax': [],
    ##  'links': None,
    ##  'matchedname': 'Tangara johannae',
    ##  'references': None,
    ##  'syno': False}

#### Species which is not in the database

``` python
toSend7={'canonicalname':'Espeletia grandiflora'}
response = requests.get(api_url+endpoint, json=toSend7)
pp(response.json())
```

    ## {'acceptedname': 'Espeletia grandiflora Humb. & Bonpl.',
    ##  'alreadyInDb': False,
    ##  'cd_status': None,
    ##  'cd_tax': 0,
    ##  'cd_tax_acc': 0,
    ##  'comments': None,
    ##  'foundGbif': True,
    ##  'gbifkey': 3105059,
    ##  'hasThreatStatus': False,
    ##  'insertedTax': [],
    ##  'links': [],
    ##  'matchedname': 'Espeletia grandiflora',
    ##  'references': [],
    ##  'syno': False}

#### Species which does not exists

``` python
toSend8={'canonicalname':'Asriwendosa machibibus'}
response = requests.get(api_url+endpoint, json=toSend8)
pp(response.json())
```

    ## {'acceptedname': None,
    ##  'alreadyInDb': False,
    ##  'cd_status': None,
    ##  'cd_tax': 0,
    ##  'cd_tax_acc': 0,
    ##  'comments': None,
    ##  'foundGbif': False,
    ##  'gbifkey': None,
    ##  'hasThreatStatus': False,
    ##  'insertedTax': [],
    ##  'links': [],
    ##  'matchedname': None,
    ##  'references': [],
    ##  'syno': False}

### Error: no sufficient information given

``` python
toSend9={}
response = requests.get(api_url+endpoint, json=toSend9)
pp(response.json())
```

    ## {'error': 'You did not provide GBIF taxon key nor name with nor without '
    ##           "authorship, missing argument: 'scientificname', 'canonicalname' or "
    ##           "'gbifkey'"}

# /testThreat/list

## POST

``` python
endpoint="/testThreat/list"
```

``` python
ListToSend={'list':[toSend1,toSend2,toSend3,toSend4,toSend5,toSend6,toSend7,toSend8,toSend9]}
response = requests.post(api_url+endpoint, json=ListToSend)
pp(response.json())
```

    ## [{'acceptedname': 'Podocarpus guatemalensis Standl.',
    ##   'alreadyInDb': True,
    ##   'cd_status': 'VU',
    ##   'cd_tax': 2099,
    ##   'cd_tax_acc': 2099,
    ##   'comments': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 5285893,
    ##   'hasThreatStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads',
    ##   'matchedname': 'Podocarpus guatemalensis',
    ##   'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): '
    ##                 'Lista de especies silvestres amenazadas de la diversidad '
    ##                 'biológica continental y marino-costera de Colombia - '
    ##                 'Resolución 1912 de 2017 expedida por el Ministerio de '
    ##                 'Ambiente y Desarrollo Sostenible. v2.5. Ministerio de '
    ##                 'Ambiente y Desarrollo Sostenible. Dataset/Checklist. '
    ##                 'https://doi.org/10.15472/5an5tz',
    ##   'syno': False},
    ##  {'acceptedname': 'Puya ochroleuca Betancur & Callejas',
    ##   'alreadyInDb': True,
    ##   'cd_status': 'EN',
    ##   'cd_tax': 2503,
    ##   'cd_tax_acc': 2503,
    ##   'comments': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 2696064,
    ##   'hasThreatStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads',
    ##   'matchedname': 'Puya ochroleuca Betancur & Callejas',
    ##   'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): '
    ##                 'Lista de especies silvestres amenazadas de la diversidad '
    ##                 'biológica continental y marino-costera de Colombia - '
    ##                 'Resolución 1912 de 2017 expedida por el Ministerio de '
    ##                 'Ambiente y Desarrollo Sostenible. v2.5. Ministerio de '
    ##                 'Ambiente y Desarrollo Sostenible. Dataset/Checklist. '
    ##                 'https://doi.org/10.15472/5an5tz',
    ##   'syno': False},
    ##  {'acceptedname': 'Scytalopus rodriguezi Krabbe, P.G.W.Salaman, A.Cortes, '
    ##                   'A.Quevedo, L.A.Ortega & C.D.Cadena, 2005',
    ##   'alreadyInDb': True,
    ##   'cd_status': 'VU',
    ##   'cd_tax': 1777,
    ##   'cd_tax_acc': 1777,
    ##   'comments': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 5789077,
    ##   'hasThreatStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads',
    ##   'matchedname': 'Scytalopus rodriguezi Krabbe, P.G.W.Salaman, A.Cortes, '
    ##                  'A.Quevedo, L.A.Ortega & C.D.Cadena, 2005',
    ##   'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): '
    ##                 'Lista de especies silvestres amenazadas de la diversidad '
    ##                 'biológica continental y marino-costera de Colombia - '
    ##                 'Resolución 1912 de 2017 expedida por el Ministerio de '
    ##                 'Ambiente y Desarrollo Sostenible. v2.5. Ministerio de '
    ##                 'Ambiente y Desarrollo Sostenible. Dataset/Checklist. '
    ##                 'https://doi.org/10.15472/5an5tz',
    ##   'syno': False},
    ##  {'acceptedname': 'Alopoglossus danieli (Harris, 1994)',
    ##   'alreadyInDb': True,
    ##   'cd_status': 'CR',
    ##   'cd_tax': 3515,
    ##   'cd_tax_acc': 3514,
    ##   'comments': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 2450617,
    ##   'hasThreatStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads',
    ##   'matchedname': 'Ptychoglossus danieli',
    ##   'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): '
    ##                 'Lista de especies silvestres amenazadas de la diversidad '
    ##                 'biológica continental y marino-costera de Colombia - '
    ##                 'Resolución 1912 de 2017 expedida por el Ministerio de '
    ##                 'Ambiente y Desarrollo Sostenible. v2.5. Ministerio de '
    ##                 'Ambiente y Desarrollo Sostenible. Dataset/Checklist. '
    ##                 'https://doi.org/10.15472/5an5tz',
    ##   'syno': True},
    ##  {'acceptedname': 'Espeletia paipana S.Díaz & Pedraza',
    ##   'alreadyInDb': True,
    ##   'cd_status': 'CR',
    ##   'cd_tax': 2831,
    ##   'cd_tax_acc': 2831,
    ##   'comments': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 3105080,
    ##   'hasThreatStatus': True,
    ##   'insertedTax': [],
    ##   'links': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads',
    ##   'matchedname': 'Espeletia paipana',
    ##   'references': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): '
    ##                 'Lista de especies silvestres amenazadas de la diversidad '
    ##                 'biológica continental y marino-costera de Colombia - '
    ##                 'Resolución 1912 de 2017 expedida por el Ministerio de '
    ##                 'Ambiente y Desarrollo Sostenible. v2.5. Ministerio de '
    ##                 'Ambiente y Desarrollo Sostenible. Dataset/Checklist. '
    ##                 'https://doi.org/10.15472/5an5tz',
    ##   'syno': False},
    ##  {'acceptedname': 'Tangara johannae (Dalmas, 1900)',
    ##   'alreadyInDb': True,
    ##   'cd_status': None,
    ##   'cd_tax': 1797,
    ##   'cd_tax_acc': 1797,
    ##   'comments': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 2488153,
    ##   'hasThreatStatus': False,
    ##   'insertedTax': [],
    ##   'links': None,
    ##   'matchedname': 'Tangara johannae',
    ##   'references': None,
    ##   'syno': False},
    ##  {'acceptedname': 'Espeletia grandiflora Humb. & Bonpl.',
    ##   'alreadyInDb': False,
    ##   'cd_status': None,
    ##   'cd_tax': 0,
    ##   'cd_tax_acc': 0,
    ##   'comments': None,
    ##   'foundGbif': True,
    ##   'gbifkey': 3105059,
    ##   'hasThreatStatus': False,
    ##   'insertedTax': [],
    ##   'links': [],
    ##   'matchedname': 'Espeletia grandiflora',
    ##   'references': [],
    ##   'syno': False},
    ##  {'acceptedname': None,
    ##   'alreadyInDb': False,
    ##   'cd_status': None,
    ##   'cd_tax': 0,
    ##   'cd_tax_acc': 0,
    ##   'comments': None,
    ##   'foundGbif': False,
    ##   'gbifkey': None,
    ##   'hasThreatStatus': False,
    ##   'insertedTax': [],
    ##   'links': [],
    ##   'matchedname': None,
    ##   'references': [],
    ##   'syno': False},
    ##  {'error': 'You did not provide GBIF taxon key nor name with nor without '
    ##            "authorship, missing argument: 'scientificname', 'canonicalname' or "
    ##            "'gbifkey'"}]

# /listEndem

## GET

``` python
endpoint="/listEndem"
```

### Comprehensive list

We will download the list and show the 5 first taxa:

``` python
response = requests.get(api_url+endpoint)
content=response.json()
len(content)
```

    ## 308

``` python
pp(content[0:4])
```

    ## [{'cd_status': 'Especie de interés',
    ##   'cd_tax': 976,
    ##   'comments': 'occurrenceRemarks: Franja y región: Tierras bajas para especies '
    ##               'cuyos límites superiores de distribución están alrededor de '
    ##               '1000-1200 m s.n.m. Llanos Orientales desde el norte de la '
    ##               'Serranía de la Macarena aproximadamente siguiendo el curso del '
    ##               'río Ariari y luego el río Guaviare hasta el río Orinoco | ',
    ##   'gbifkey': 5845551,
    ##   'links': ['91: '
    ##             'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##             None],
    ##   'parentname': 'Paroaria Bonaparte, 1832',
    ##   'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., '
    ##                  'Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado '
    ##                  'actualizado de las aves endémicas y casi-endémicas de '
    ##                  'Colombia. 308 registros. Versión 5.1. '
    ##                  'http://doi.org/10.15472/tozuue',
    ##                  '194: Davalos y Porzecanski 2009'],
    ##   'scientificname': 'Paroaria nigrogenis (Lafresnaye, 1846)',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_status': 'Casi endémica',
    ##   'cd_tax': 1281,
    ##   'comments': 'locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | '
    ##               'Vertiente oriental hacia Amazonía | Perú: Amazonas (desde '
    ##               'divisoria de aguas y principales drenajes al río Amazonas) | '
    ##               'occurrenceRemarks: Franja y región: Tierras bajas para especies '
    ##               'cuyos límites superiores de distribución están alrededor de '
    ##               '1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el '
    ##               'Golfo de Urabá hasta la Península de La Guajira, incluyendo las '
    ##               'estribaciones de la Sierra Nevada de Santa Marta y la Serranía '
    ##               'de Perijá en el norte de Cesar, y como subregión |Elevaciones '
    ##               'medias para especies que se distribuyen entre ca. 800-l000 y '
    ##               '2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones '
    ##               'medias para especies que se distribuyen entre ca. 800-l000 y '
    ##               '2000-2400 m s.n.m. Laderas más al norte de la cordillera '
    ##               'Occidental y de la cordillera Central y la ladera nororiental '
    ##               'de la Central hacia el sur hasta aproximadamente el límite sur '
    ##               'de Caldas |Elevaciones altas, para especies cuyos límites '
    ##               'inferiores caen por encima de ca. 2000 m s.n.m. cordillera '
    ##               'Central | ',
    ##   'gbifkey': 2480593,
    ##   'links': ['91: '
    ##             'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##             None,
    ##             None,
    ##             None,
    ##             None,
    ##             None],
    ##   'parentname': 'Accipiter Brisson, 1760',
    ##   'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., '
    ##                  'Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado '
    ##                  'actualizado de las aves endémicas y casi-endémicas de '
    ##                  'Colombia. 308 registros. Versión 5.1. '
    ##                  'http://doi.org/10.15472/tozuue',
    ##                  '92: Arbeláez-Cortés et al. 2011b',
    ##                  '93: Cuervo et al. 2008a',
    ##                  '94: Cuervo et al. 2008b',
    ##                  '95: Merkord 2010',
    ##                  '96: Rodríguez y Rojas-Suárez 2008'],
    ##   'scientificname': 'Accipiter collaris P.L.Sclater, 1860',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_status': 'Casi endémica',
    ##   'cd_tax': 1285,
    ##   'comments': 'locality: Ecuador: Vertiente pacífica del Ecuador | '
    ##               'occurrenceRemarks: Franja y región: Tierras bajas para especies '
    ##               'cuyos límites superiores de distribución están alrededor de '
    ##               '1000-1200 m s.n.m. Andén del Pacífico, desde la zona media del '
    ##               'Darién en límites con Panamá, al lado izquierdo del bajo río '
    ##               'Atrato, hasta el Ecuador |Elevaciones medias para especies que '
    ##               'se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. '
    ##               'Vertiente occidental de la cordillera Occidental que incluye | ',
    ##   'gbifkey': 2476385,
    ##   'links': ['91: '
    ##             'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09'],
    ##   'parentname': 'Aglaiocercus J.T.Zimmer, 1930',
    ##   'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., '
    ##                  'Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado '
    ##                  'actualizado de las aves endémicas y casi-endémicas de '
    ##                  'Colombia. 308 registros. Versión 5.1. '
    ##                  'http://doi.org/10.15472/tozuue'],
    ##   'scientificname': 'Aglaiocercus coelestis (Gould, 1861)',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_status': 'Especie de interés',
    ##   'cd_tax': 1287,
    ##   'comments': 'locality: Ecuador: Vertiente pacífica del Ecuador | '
    ##               'occurrenceRemarks: Franja y región: Tierras bajas para especies '
    ##               'cuyos límites superiores de distribución están alrededor de '
    ##               '1000-1200 m s.n.m. Región más húmeda inmediatamente al sur de '
    ##               'la región 1, desde el bajo río Atrato hasta la parte media del '
    ##               'valle del río Magdalena, incluyendo el alto río Sinú y alto río '
    ##               'Nechí |Tierras bajas para especies cuyos límites superiores de '
    ##               'distribución están alrededor de 1000-1200 m s.n.m. Andén del '
    ##               'Pacífico, desde la zona media del Darién en límites con Panamá, '
    ##               'al lado izquierdo del bajo río Atrato, hasta el Ecuador '
    ##               '|Tierras bajas para especies cuyos límites superiores de '
    ##               'distribución están alrededor de 1000-1200 m s.n.m. Alto valle '
    ##               'del río Magdalena, principalmente en Tolima y Huila '
    ##               '|Elevaciones medias para especies que se distribuyen entre ca. '
    ##               '800-l000 y 2000-2400 m s.n.m. Laderas más al norte de la '
    ##               'cordillera Occidental y de la cordillera Central y la ladera '
    ##               'nororiental de la Central hacia el sur hasta aproximadamente el '
    ##               'límite sur de Caldas |Elevaciones medias para especies que se '
    ##               'distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas del '
    ##               'alto valle del río Magdalena principalmente en Tolima y Huila '
    ##               '|Elevaciones medias para especies que se distribuyen entre ca. '
    ##               '800-l000 y 2000-2400 m s.n.m. Vertiente occidental de la '
    ##               'cordillera Oriental, desde el sur de Cesar hasta Cundinamarca '
    ##               '| ',
    ##   'gbifkey': 5788536,
    ##   'links': ['91: '
    ##             'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##             None,
    ##             None,
    ##             None,
    ##             None],
    ##   'parentname': 'Polyerata Heine, 1863',
    ##   'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., '
    ##                  'Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado '
    ##                  'actualizado de las aves endémicas y casi-endémicas de '
    ##                  'Colombia. 308 registros. Versión 5.1. '
    ##                  'http://doi.org/10.15472/tozuue',
    ##                  '97: Corpocaldas 2010',
    ##                  '98: Donegan et al. 2010',
    ##                  '99: Laverde-R. Et al. 2005b',
    ##                  '100: Parra-Hernández et al. 2007'],
    ##   'scientificname': 'Polyerata amabilis (Gould, 1853)',
    ##   'synonyms': ['Amazilia amabilis (Gould, 1853)'],
    ##   'tax_rank': 'SP'}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listEndem?format=CSV>

------------------------------------------------------------------------

### Only the passerine birds

The five first passerine birds of the endemic list:

``` python
onlyPasserine={'childrenOf':'Passeriformes'}
response = requests.get(api_url+endpoint,json=onlyPasserine)
content=response.json()
len(content)
```

    ## 167

``` python
pp(content[0:4])
```

    ## [{'cd_status': 'Especie de interés',
    ##   'cd_tax': 976,
    ##   'comments': 'occurrenceRemarks: Franja y región: Tierras bajas para especies '
    ##               'cuyos límites superiores de distribución están alrededor de '
    ##               '1000-1200 m s.n.m. Llanos Orientales desde el norte de la '
    ##               'Serranía de la Macarena aproximadamente siguiendo el curso del '
    ##               'río Ariari y luego el río Guaviare hasta el río Orinoco | ',
    ##   'gbifkey': 5845551,
    ##   'links': ['91: '
    ##             'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##             None],
    ##   'parentname': 'Paroaria Bonaparte, 1832',
    ##   'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., '
    ##                  'Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado '
    ##                  'actualizado de las aves endémicas y casi-endémicas de '
    ##                  'Colombia. 308 registros. Versión 5.1. '
    ##                  'http://doi.org/10.15472/tozuue',
    ##                  '194: Davalos y Porzecanski 2009'],
    ##   'scientificname': 'Paroaria nigrogenis (Lafresnaye, 1846)',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_status': 'Casi endémica',
    ##   'cd_tax': 1300,
    ##   'comments': 'locality: Ecuador: Los Andes | Venezuela: Andes venezolanos | '
    ##               'occurrenceRemarks: Franja y región: Elevaciones altas, para '
    ##               'especies cuyos límites inferiores caen por encima de ca. 2000 m '
    ##               's.n.m. cordillera Central |Elevaciones altas, para especies '
    ##               'cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. '
    ##               'cordillera Oriental con | ',
    ##   'gbifkey': 2482692,
    ##   'links': ['91: '
    ##             'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##             None,
    ##             None,
    ##             None,
    ##             None,
    ##             None],
    ##   'parentname': 'Anairetes Reichenbach, 1850',
    ##   'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., '
    ##                  'Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado '
    ##                  'actualizado de las aves endémicas y casi-endémicas de '
    ##                  'Colombia. 308 registros. Versión 5.1. '
    ##                  'http://doi.org/10.15472/tozuue',
    ##                  '92: Arbeláez-Cortés et al. 2011b',
    ##                  '97: Corpocaldas 2010',
    ##                  '100: Parra-Hernández et al. 2007',
    ##                  '103: Ayerbe-Quiñones et al. 2008',
    ##                  '107: López-Guzmán y Gómez-Botero 2005'],
    ##   'scientificname': 'Anairetes agilis (P.L.Sclater, 1856)',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_status': 'Endémica',
    ##   'cd_tax': 1311,
    ##   'comments': 'occurrenceRemarks: Franja y región: Elevaciones medias para '
    ##               'especies que se distribuyen entre ca. 800-l000 y 2000-2400 m '
    ##               's.n.m. Sierra Nevada de Santa Marta |Elevaciones altas, para '
    ##               'especies cuyos límites inferiores caen por encima de ca. 2000 m '
    ##               's.n.m. Sierra Nevada de Santa Marta | ',
    ##   'gbifkey': 5230546,
    ##   'links': ['91: '
    ##             'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09'],
    ##   'parentname': 'Anisognathus Reichenbach, 1850',
    ##   'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., '
    ##                  'Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado '
    ##                  'actualizado de las aves endémicas y casi-endémicas de '
    ##                  'Colombia. 308 registros. Versión 5.1. '
    ##                  'http://doi.org/10.15472/tozuue'],
    ##   'scientificname': 'Anisognathus melanogenys (Salvin & Godman, 1880)',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_status': 'Casi endémica',
    ##   'cd_tax': 1312,
    ##   'comments': 'locality: Ecuador: Vertiente pacífica del Ecuador | '
    ##               'occurrenceRemarks: Franja y región: Tierras bajas para especies '
    ##               'cuyos límites superiores de distribución están alrededor de '
    ##               '1000-1200 m s.n.m. Andén del Pacífico, desde la zona media del '
    ##               'Darién en límites con Panamá, al lado izquierdo del bajo río '
    ##               'Atrato, hasta el Ecuador |Elevaciones medias para especies que '
    ##               'se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. '
    ##               'Vertiente occidental de la cordillera Occidental que incluye | ',
    ##   'gbifkey': 5230540,
    ##   'links': ['91: '
    ##             'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09'],
    ##   'parentname': 'Anisognathus Reichenbach, 1850',
    ##   'references': ['91: Chaparro-Herrera, S., Echeverry-Galvis, M.A., '
    ##                  'Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado '
    ##                  'actualizado de las aves endémicas y casi-endémicas de '
    ##                  'Colombia. 308 registros. Versión 5.1. '
    ##                  'http://doi.org/10.15472/tozuue'],
    ##   'scientificname': 'Anisognathus notabilis (P.L.Sclater, 1855)',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listEndem?childrenOf=Passeriformes&format=CSV>

------------------------------------------------------------------------

### Error: asking for an unknown group

We will ask for all the children of the genus Abies (Fir genus)

``` python
onlyAbies={'childrenOf':'Abies'}
response = requests.get(api_url+endpoint,json=onlyAbies)
pp(response.json())
```

    ## {'error': "'childrenOf' taxon not recognized: taxon Abies was not found in the "
    ##           'database'}

# /listExot

## GET

``` python
endpoint="/listExot"
```

### Comprehensive list

We will download the list and show the 5 first taxa:

``` python
response = requests.get(api_url+endpoint)
content=response.json()
len(content)
```

    ## 511

``` python
pp(content[0:4])
```

    ## [{'cd_tax': 7,
    ##   'comments': 'Altitud máxima: 3200 | Altitud máxima Unit: m.s.n.m. | Altitud '
    ##               'mínima: 1600 | Altitud mínima Unit: m.s.n.m. | Asociación '
    ##               'invasiva: No se encontraron datos | Aspectos generales de '
    ##               'invasividad: Producción abundante de semillas, rápida '
    ##               'germinación, alta viabilidad, resistencia a inundaciones y '
    ##               'fuego, alta producción vegetativa, sustancias alelopáticas | '
    ##               'Causas de introducción: Usos ornamentales | Distribución como '
    ##               'exótica: Cosmopólita | Distribución nativa: ARG , AUS , NZL , '
    ##               'URY , ZAF | Estatus: Exótica | Translocada | Factores '
    ##               'limitantes para el establecimiento: Heladas, no tiene éxito por '
    ##               'debajo de los 1000 msnm, zonas húmedas y secas tropicales | '
    ##               'Hábito: Terrestre | Impactos de introducción: Migración de '
    ##               'zonas de cultivos a espacios naturales, aumento regímenes de '
    ##               'incendio, restricción en la regeneración natural de especies '
    ##               'nativas, impedimento en el movimiento de fauna | Introducida '
    ##               'después de (año): 1963 | Medidas de manejo y control: En África '
    ##               'se ha evidenciado el control biológico sobre semillas con la '
    ##               'especie Melanterius maculatus (Curculionidae) y en Nueva '
    ##               'Zelanda con Bruchophagus acaciae (Hymenoptera) | Observaciones '
    ##               'de ocurrencia: Frecuentemente en zonas de incendios y áreas '
    ##               'perturbadas | pH: 7 | Precipitación máxima: 1200 | '
    ##               'Precipitación máxima Unit: mm | Precipitación mínima: 750 | '
    ##               'Precipitación mínima Unit: mm | Puntaje Riesgo de Invasión: 5 | '
    ##               'Puntaje Riesgo de Invasión Remarks: Fuente: I3N | Riesgo de '
    ##               'invasión: Alto riesgo | Temperatura máxima: 18 | Temperatura '
    ##               'máxima Unit: °C | Temperatura mínima: 14 | Temperatura mínima '
    ##               'Unit: °C | Tipo de dispersión: Anemocoría, zoocoría | Tipo de '
    ##               'introducción: Intencional | Tipo de reproducción: Semillas | '
    ##               'Tipo de suelo: Arenosos-arcillosos | Vías de introducción: '
    ##               'Sembrada',
    ##   'gbifkey': 2979778,
    ##   'is_alien': True,
    ##   'is_invasive': True,
    ##   'links': ['1: '
    ##             'http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020',
    ##             None,
    ##             None,
    ##             '90: '
    ##             'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'],
    ##   'parentname': 'Acacia Mill.',
    ##   'references': ['1:  Instituto de Investigación de Recursos Biológicos '
    ##                  'Alexander von Humboldt (2020). Base de datos de información '
    ##                  'ecológica e invasividad de especies exóticas prioritarias de '
    ##                  'flora y fauna de Colombia. 43 registros.',
    ##                  '2: Cárdenas D., Baptiste M.P., Castaño N. (2017). Plantas '
    ##                  'exóticas con alto potencial de invasión en Colombia. '
    ##                  'Instituto de Investigación de Recursos Biológicos Alexander '
    ##                  'von Humboldt. Bogotá, D. C., Colombia. 295 p.',
    ##                  '3: Mora, M. F., Rubio J., Ocampo R. & Barrera J.I. (2015). '
    ##                  'Catálogo de especies invasoras del territorio CAR. Publicado '
    ##                  'por Pontificia Universidad Javeriana & Corporación Autónoma '
    ##                  'Regional de Cundinamarca – CAR, 238 pp.',
    ##                  '90: Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry '
    ##                  'O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco '
    ##                  'A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez '
    ##                  'C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, '
    ##                  'Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, '
    ##                  'Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, '
    ##                  'Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, '
    ##                  'González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, '
    ##                  'Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino '
    ##                  'M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, '
    ##                  'del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, '
    ##                  'Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, '
    ##                  'Pagad S (2020). Global Register of Introduced and Invasive '
    ##                  'Species - Colombia. Version 1.5. Invasive Species Specialist '
    ##                  'Group ISSG.'],
    ##   'scientificname': 'Acacia decurrens (J.C.Wendl.) Willd.',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_tax': 14,
    ##   'comments': 'Altitud máxima: 1233 | Altitud máxima Unit: m.s.n.m. | Altitud '
    ##               'mínima: 0 | Altitud mínima Unit: m.s.n.m. | Asociación '
    ##               'invasiva: Hospedero intermediario de Angyostrongylus '
    ##               'Cantonensis (causante de la meningoencefalitis eosinofílica) y '
    ##               'Angyostrongylus costaricensis (causante de angiostrongilosis '
    ##               'abdominal) | Aspectos generales de invasividad: Dieta '
    ##               'generalista que le permite alimentarse de hongos, plantas, '
    ##               'materia orgánica en descomposición, papel y paredes estucadas. '
    ##               'Ausencia de depredadores naturales en ambientes antrópicos. '
    ##               'Comienzan a reproducirse desde los 5 o 6 meses, llegando a '
    ##               'poner hasta 1000 huevos en condiciones óptimas. En condiciones '
    ##               'climáticas adversas es capaz de estivar. | Causas de '
    ##               'introducción: Propósitos estéticos, alimenticios y medicinales '
    ##               '| Distribución como exótica: AIA , ASM , BGD , BRA , BRB , CHN '
    ##               ', COK , COL , ECU , ETH , GHA , GLP , GNQ , GUF , GUM , GUY , '
    ##               'HKG , IDN , IND , JPN , KEN , KIR , LCA , LKA , MAF , MAR , MDG '
    ##               ', MHL , MNP , MOZ , MTQ , MUS , MYS , MYT , NCL , NPL , NZL , '
    ##               'PER , PHL , PLW , PNG , PRY , PYF , SGP , SLB , SOM , STP , SUR '
    ##               ', SYC , THA , TTO , TUV , TWN , UMI , VEN , VUT , WLF , WSM , '
    ##               'ZAF | Distribución nativa: ETH , KEN , TZA | Estatus: Exótica | '
    ##               'Factores limitantes para el establecimiento: Temperaturas de '
    ##               '0°C producen la congelación del agua de los tejidos y las '
    ##               'superiores a 30°C puede soportarlas siempre y cuando haya '
    ##               'suficiente humedad. | Hábito: Terrestre | Impactos de '
    ##               'introducción: Impactos a la agricultura ya que puede '
    ##               'alimentarse de más de 200 especies vegetales | Introducida '
    ##               'después de (año): 2008 | Medidas de manejo y control: '
    ##               'Restricción del uso de la especie para cualquier fin. Control '
    ##               'físico y control químico con disposición final controlada | '
    ##               'Observaciones de ocurrencia: Áreas de baja a mediana elevación '
    ##               'en clima tropical con calentamiento constante, aunque ya se han '
    ##               'adaptado a climas templados. Abunda en zonas agrícolas, zonas '
    ##               'costeras, humedales, áreas perturbadas, bosques, zonas urbanas '
    ##               'y zonas de ribera | pH: No aplica | Precipitación máxima: 7650 '
    ##               '| Precipitación máxima Unit: mm | Precipitación mínima: 900 | '
    ##               'Precipitación mínima Unit: mm | Puntaje Riesgo de Invasión: No '
    ##               'evaluada | Puntaje Riesgo de Invasión Remarks: No evaluada | '
    ##               'Riesgo de invasión: No evaluada | Temperatura máxima: 29 | '
    ##               'Temperatura máxima Unit: °C | Temperatura mínima: 9 | '
    ##               'Temperatura mínima Unit: °C | Tipo de dispersión: Antropocoría '
    ##               'y medios propios | Tipo de introducción: Intencional y no '
    ##               'intencional | Tipo de reproducción: sexual | Tipo de suelo: No '
    ##               'aplica | Vías de introducción: Intencional por propósitos '
    ##               'estéticos, alimenticios y medicinales y no intencional a través '
    ##               'del transporte de carga.',
    ##   'gbifkey': 2295966,
    ##   'is_alien': True,
    ##   'is_invasive': True,
    ##   'links': ['1: '
    ##             'http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020',
    ##             '4: https://www.car.gov.co/uploads/files/5b9033f095d34.pdf',
    ##             '5: http://www.iucngisd.org/gisd/speciesname/Achatina+fulica',
    ##             None,
    ##             '90: '
    ##             'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'],
    ##   'parentname': 'Achatina Lamarck, 1799',
    ##   'references': ['1:  Instituto de Investigación de Recursos Biológicos '
    ##                  'Alexander von Humboldt (2020). Base de datos de información '
    ##                  'ecológica e invasividad de especies exóticas prioritarias de '
    ##                  'flora y fauna de Colombia. 43 registros.',
    ##                  '4: Corporación Autónoma Regional (2018). Plan de Prevención, '
    ##                  'Control y Manejo (PPCM) de Caracol Gigante Africano '
    ##                  '(Achatina fulica) en la jurisdicción CAR. Dirección de '
    ##                  'Recursos Naturales. 61 pp.',
    ##                  '5: Invasive Species Specialist Group (2020). Achatina '
    ##                  'fulica.',
    ##                  '6: Garcés M., Patiño A., Gómez M., Giraldo A. & Bolívar G. '
    ##                  '(2016). Sustancias alternativas para el control del caracol '
    ##                  'africano (Achatina fulica) en el Valle del Cauca. Biota '
    ##                  'Colombiana. Vol. 17(1), 44 - 52 pp.',
    ##                  '90: Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry '
    ##                  'O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco '
    ##                  'A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez '
    ##                  'C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, '
    ##                  'Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, '
    ##                  'Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, '
    ##                  'Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, '
    ##                  'González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, '
    ##                  'Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino '
    ##                  'M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, '
    ##                  'del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, '
    ##                  'Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, '
    ##                  'Pagad S (2020). Global Register of Introduced and Invasive '
    ##                  'Species - Colombia. Version 1.5. Invasive Species Specialist '
    ##                  'Group ISSG.'],
    ##   'scientificname': 'Achatina fulica (Férussac, 1821)',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_tax': 19,
    ##   'comments': 'Altitud máxima: 4500 | Altitud máxima Unit: m.s.n.m. | Altitud '
    ##               'mínima: 1500 | Altitud mínima Unit: m.s.n.m. | Asociación '
    ##               'invasiva: Holcus lanatus | Aspectos generales de invasividad: '
    ##               'Florecimiento en todo el año, producción de gran cantidad de '
    ##               'semillas, alta viabilidad de semillas | Causas de introducción: '
    ##               'Constitución de céspedes, especie forrajera para el incremento '
    ##               'de producción de leche de ganado vacuno, arreglos florales | '
    ##               'Distribución como exótica: América , AUS , ZAF | Distribución '
    ##               'nativa: BEL , CHN , ESP , FRA , GRB , GRC , IRN , PRT , RUS | '
    ##               'Estatus: Exótica | Factores limitantes para el establecimiento: '
    ##               'No se encontraron datos | Hábito: Terrestre | Impactos de '
    ##               'introducción: Desplazamiento de especies nativas | Introducida '
    ##               'después de (año): No se encontraron datos | Medidas de manejo y '
    ##               'control: Actividades de siega antes de que las semillas hayan '
    ##               'madurado | Observaciones de ocurrencia: Áreas abiertas con '
    ##               'sombrío parcial entre media y alta montaña, sustratos arenosos, '
    ##               'rocosos, arcillosos | pH: 3,7 - 7,5 | Precipitación máxima: No '
    ##               'se encontraron datos | Precipitación máxima Unit: mm | '
    ##               'Precipitación mínima: No se encontraron datos | Precipitación '
    ##               'mínima Unit: mm | Puntaje Riesgo de Invasión: 6.14 | Puntaje '
    ##               'Riesgo de Invasión Remarks: Fuente: I3N | Riesgo de invasión: '
    ##               'Alto riesgo | Temperatura máxima: 18 | Temperatura máxima Unit: '
    ##               '°C | Temperatura mínima: 0 | Temperatura mínima Unit: °C | Tipo '
    ##               'de dispersión: Antropocoría | Tipo de introducción: Intencional '
    ##               '| Tipo de reproducción: Vegetativa | Tipo de suelo: '
    ##               'Arenoso-arcilloso | Vías de introducción: Sembrada',
    ##   'gbifkey': 2705975,
    ##   'is_alien': True,
    ##   'is_invasive': True,
    ##   'links': ['1: '
    ##             'http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020',
    ##             None,
    ##             '7: https://www.cabi.org/isc/datasheet/93023'],
    ##   'parentname': 'Anthoxanthum L.',
    ##   'references': ['1:  Instituto de Investigación de Recursos Biológicos '
    ##                  'Alexander von Humboldt (2020). Base de datos de información '
    ##                  'ecológica e invasividad de especies exóticas prioritarias de '
    ##                  'flora y fauna de Colombia. 43 registros.',
    ##                  '2: Cárdenas D., Baptiste M.P., Castaño N. (2017). Plantas '
    ##                  'exóticas con alto potencial de invasión en Colombia. '
    ##                  'Instituto de Investigación de Recursos Biológicos Alexander '
    ##                  'von Humboldt. Bogotá, D. C., Colombia. 295 p.',
    ##                  '7: Invasive Species Compendium (2019). Anthoxanthum odoratum '
    ##                  '(sweet vernal grass).'],
    ##   'scientificname': 'Anthoxanthum odoratum L.',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_tax': 21,
    ##   'comments': 'Altitud máxima: 3000 | Altitud máxima Unit: m.s.n.m. | Altitud '
    ##               'mínima: 500 | Altitud mínima Unit: m.s.n.m. | Asociación '
    ##               'invasiva: No se encontraron datos | Aspectos generales de '
    ##               'invasividad: Tolerancia a altos niveles de salinidad | Causas '
    ##               'de introducción: Usos de cestería, elaboración de utensilios de '
    ##               'cocina, instrumentos musicales, muebles, juguetes, papel '
    ##               'artesanal, protección de cuencas, estabilización y/o '
    ##               'recuperación de suelos y taludes, establecimiento de cercas '
    ##               'vivas y rompevientos | Distribución como exótica: América del '
    ##               'Sur , AUS , USA , ZEF | Distribución nativa: AFG , CHN , IDN , '
    ##               'IND , IRN , IRQ , JPN , KHM , NPL | Estatus: Exótica | Factores '
    ##               'limitantes para el establecimiento: Requiere de fotoperíodos '
    ##               'prolongados que no encuentra en países como Colombia | Hábito: '
    ##               'Terrestre | Impactos de introducción: Fuerte competidora de '
    ##               'especies nativas, absorbe gran cantidad de agua del suelo, '
    ##               'alteraciones de hidrología, en el control de inundaciones, en '
    ##               'el ciclo de nutrientes y el régimen de incendios | Introducida '
    ##               'después de (año): No se encontraron datos | Medidas de manejo y '
    ##               'control: Control mecánico especialmente de plantas jóvenes, '
    ##               'prestando atención a la eliminación del rizoma. Control químico '
    ##               'con glifosato. Se ha reportado control biológico usando orugas '
    ##               'de Phothedes dulcis en Francia, larvas de Zyginidia manaliensis '
    ##               'en Pakistán y las de Diatraea sacchararalis en Barbados | '
    ##               'Observaciones de ocurrencia: Ambientes abiertos y de suelos con '
    ##               'humedad permanente, orillas de diferentes corrientes hídricas | '
    ##               'pH: 5,0 - 8,7 | Precipitación máxima: 4000 | Precipitación '
    ##               'máxima Unit: mm | Precipitación mínima: 300 | Precipitación '
    ##               'mínima Unit: mm | Puntaje Riesgo de Invasión: 5.35 | Puntaje '
    ##               'Riesgo de Invasión Remarks: Fuente: I3N | Riesgo de invasión: '
    ##               'Alto riesgo | Temperatura máxima: 29 | Temperatura máxima Unit: '
    ##               '°C | Temperatura mínima: 9 | Temperatura mínima Unit: °C | Tipo '
    ##               'de dispersión: Vegetación flotante | Tipo de introducción: No '
    ##               'intencional | Tipo de reproducción: Vegetativa por rizomas | '
    ##               'Tipo de suelo: Arenas de partícula gruesa, grava, arcillas '
    ##               'pesadas y sedimentos de ríos | Vías de introducción: Dispersión '
    ##               'voluntaria',
    ##   'gbifkey': 2703041,
    ##   'is_alien': True,
    ##   'is_invasive': True,
    ##   'links': ['1: '
    ##             'http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020',
    ##             None,
    ##             '8: https://www.cabi.org/isc/datasheet/1940'],
    ##   'parentname': 'Arundo L.',
    ##   'references': ['1:  Instituto de Investigación de Recursos Biológicos '
    ##                  'Alexander von Humboldt (2020). Base de datos de información '
    ##                  'ecológica e invasividad de especies exóticas prioritarias de '
    ##                  'flora y fauna de Colombia. 43 registros.',
    ##                  '2: Cárdenas D., Baptiste M.P., Castaño N. (2017). Plantas '
    ##                  'exóticas con alto potencial de invasión en Colombia. '
    ##                  'Instituto de Investigación de Recursos Biológicos Alexander '
    ##                  'von Humboldt. Bogotá, D. C., Colombia. 295 p.',
    ##                  '8: Invasive Species Compendium (2019). Arundo donax (giant '
    ##                  'reed).'],
    ##   'scientificname': 'Arundo donax L.',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listExot?format=CSV>

------------------------------------------------------------------------

### Only the passerine birds

The five first passerine birds of the endemic list:

``` python
onlyPasserine={'childrenOf':'Passeriformes'}
response = requests.get(api_url+endpoint,json=onlyPasserine)
content=response.json()
len(content)
```

    ## 10

``` python
pp(content[0:4])
```

    ## [{'cd_tax': 99,
    ##   'comments': 'Altitud máxima: 2500 | Altitud máxima Unit: m.s.n.m. | Altitud '
    ##               'mínima: 550 | Altitud mínima Unit: m.s.n.m. | Asociación '
    ##               'invasiva: Se alimenta principalmente de arroz (Oryza sativa) y '
    ##               'sorgo (sorghum bicolor). Abunda en corredores de pasto donde '
    ##               'predomina Urochloa maxima e Hyparrhenia rufa para desplazarse y '
    ##               'como sitio de descanso. | Aspectos generales de invasividad: '
    ##               'Forman grandes bandadas, comúnmente entre 10 y 30 individuos. '
    ##               'Grupos pequeñas tienden a unirse a otros para alimentación y '
    ##               'desplazamiento | Causas de introducción: Importadas como aves '
    ##               'ornamentales | Distribución como exótica: AUS , BLZ , CHN , COL '
    ##               ', CRI , CUB , DOM , HND , JPN , MEX , PRI , SLV , USA , VEN | '
    ##               'Distribución nativa: IDN , IND , KHM , LKA , MYS , PHL , SGP , '
    ##               'TWN , VNM | Estatus: Exótica | Factores limitantes para el '
    ##               'establecimiento: No se encontraron datos | Hábito: Terrestre | '
    ##               'Impactos de introducción: Se desconoce su impacto en la '
    ##               'biodiversidad nativa en Colombia, pero se reporta como plaga de '
    ##               'cultivos en países vecinos. | Introducida después de (año): '
    ##               '2005 | Medidas de manejo y control: No se cuenta en el momento '
    ##               'con planes de manejo y control debido a la falta de información '
    ##               'de esta especie en el Neotrópico | Observaciones de ocurrencia: '
    ##               'Registrada en pastos naturales y artificiales en zonas urbanas '
    ##               'y suburbanas, y recientemente en cañaduzales. En otros países '
    ##               'se registra como colonizador de ecosistemas de humedales | pH: '
    ##               'No aplica | Precipitación máxima: No se encontraron datos | '
    ##               'Precipitación máxima Unit: mm | Precipitación mínima: No se '
    ##               'encontraron datos | Precipitación mínima Unit: mm | Puntaje '
    ##               'Riesgo de Invasión: 3.6 | Puntaje Riesgo de Invasión Remarks: '
    ##               'Fuente: AR - Vertebrados Terrestres | Riesgo de invasión: Alto '
    ##               'riesgo | Temperatura máxima: 28 | Temperatura máxima Unit: °C | '
    ##               'Temperatura mínima: 17 | Temperatura mínima Unit: °C | Tipo de '
    ##               'dispersión: Antropocoría y dispersión natural | Tipo de '
    ##               'introducción: Intencional | Tipo de reproducción: Sexual | Tipo '
    ##               'de suelo: No aplica | Vías de introducción: Escape accidental',
    ##   'gbifkey': 2493626,
    ##   'is_alien': True,
    ##   'is_invasive': True,
    ##   'links': ['1: '
    ##             'http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020',
    ##             None,
    ##             None,
    ##             None,
    ##             '57: '
    ##             'https://www.gob.mx/cms/uploads/attachment/file/222403/Lonchura_malacca.pdf',
    ##             None,
    ##             '90: '
    ##             'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'],
    ##   'parentname': 'Lonchura Sykes, 1832',
    ##   'references': ['1:  Instituto de Investigación de Recursos Biológicos '
    ##                  'Alexander von Humboldt (2020). Base de datos de información '
    ##                  'ecológica e invasividad de especies exóticas prioritarias de '
    ##                  'flora y fauna de Colombia. 43 registros.',
    ##                  '18: Baptiste M.P., Castaño N., Cárdenas D., Gutiérrez F.P., '
    ##                  'Gil D. & Lasso C.A. (eds). (2010). Análisis de riesgo y '
    ##                  'propuesta de categorización de especies introducidas para '
    ##                  'Colombia. Instituto de Investigación de Recursos Biológicos '
    ##                  'Alexander von Humboldt. Bogotá, D. C., Colombia. 200 pp.',
    ##                  '19: Instituto de Investigación de Recursos Biológicos '
    ##                  'Alexander von Humboldt. (2011). Fauna exótica e invasora de '
    ##                  'Colombia. Bogotá, D. C., Colombia. 71 pp.',
    ##                  '56: Parra R., Tolosa Y. & Figueroa W. (2015). Nuevos '
    ##                  'registros y estado actual de las especies introducidas en el '
    ##                  'municipio de Ibagué. Revista Tumbaga, Vol. 10(1), 58 - 75 '
    ##                  'pp.',
    ##                  '57: CONABIO (2014). Método de Evaluación Rápida de '
    ##                  'Invasividad (MERI) para especies exóticas en México - '
    ##                  'Lonchura malacca, 1766, 9 pp. Gobierno de México.',
    ##                  '58: Carantón D., Certuche K., Díaz C., Parra R., Sanabria J. '
    ##                  '& Moreno M. (2008). Aspectos biológicos de una nueva '
    ##                  'población del Capuchino de cabeza negra (Lonchura malacca, '
    ##                  'Estrildidae) en el alto valle del Magdalena, Boletín SAO, '
    ##                  'Vol. 18(2), 54 - 63 pp.',
    ##                  '90: Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry '
    ##                  'O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco '
    ##                  'A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez '
    ##                  'C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, '
    ##                  'Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, '
    ##                  'Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, '
    ##                  'Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, '
    ##                  'González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, '
    ##                  'Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino '
    ##                  'M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, '
    ##                  'del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, '
    ##                  'Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, '
    ##                  'Pagad S (2020). Global Register of Introduced and Invasive '
    ##                  'Species - Colombia. Version 1.5. Invasive Species Specialist '
    ##                  'Group ISSG.'],
    ##   'scientificname': 'Lonchura malacca (Linnaeus, 1766)',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_tax': 455,
    ##   'comments': None,
    ##   'gbifkey': 5789080,
    ##   'is_alien': True,
    ##   'is_invasive': False,
    ##   'links': ['90: '
    ##             'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'],
    ##   'parentname': 'Erythrura Swainson, 1837',
    ##   'references': ['90: Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry '
    ##                  'O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco '
    ##                  'A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez '
    ##                  'C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, '
    ##                  'Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, '
    ##                  'Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, '
    ##                  'Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, '
    ##                  'González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, '
    ##                  'Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino '
    ##                  'M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, '
    ##                  'del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, '
    ##                  'Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, '
    ##                  'Pagad S (2020). Global Register of Introduced and Invasive '
    ##                  'Species - Colombia. Version 1.5. Invasive Species Specialist '
    ##                  'Group ISSG.'],
    ##   'scientificname': 'Erythrura gouldiae (Gould, 1844)',
    ##   'synonyms': ['Chloebia gouldiae (Gould, 1844)'],
    ##   'tax_rank': 'SP'},
    ##  {'cd_tax': 812,
    ##   'comments': None,
    ##   'gbifkey': 2493623,
    ##   'is_alien': True,
    ##   'is_invasive': False,
    ##   'links': ['90: '
    ##             'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'],
    ##   'parentname': 'Lonchura Sykes, 1832',
    ##   'references': ['90: Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry '
    ##                  'O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco '
    ##                  'A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez '
    ##                  'C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, '
    ##                  'Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, '
    ##                  'Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, '
    ##                  'Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, '
    ##                  'González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, '
    ##                  'Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino '
    ##                  'M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, '
    ##                  'del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, '
    ##                  'Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, '
    ##                  'Pagad S (2020). Global Register of Introduced and Invasive '
    ##                  'Species - Colombia. Version 1.5. Invasive Species Specialist '
    ##                  'Group ISSG.'],
    ##   'scientificname': 'Lonchura atricapilla (Vieillot, 1807)',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_tax': 813,
    ##   'comments': None,
    ##   'gbifkey': 4845776,
    ##   'is_alien': True,
    ##   'is_invasive': False,
    ##   'links': ['90: '
    ##             'https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'],
    ##   'parentname': 'Lonchura Sykes, 1832',
    ##   'references': ['90: Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry '
    ##                  'O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco '
    ##                  'A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez '
    ##                  'C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, '
    ##                  'Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, '
    ##                  'Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, '
    ##                  'Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, '
    ##                  'González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, '
    ##                  'Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino '
    ##                  'M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, '
    ##                  'del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, '
    ##                  'Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, '
    ##                  'Pagad S (2020). Global Register of Introduced and Invasive '
    ##                  'Species - Colombia. Version 1.5. Invasive Species Specialist '
    ##                  'Group ISSG.'],
    ##   'scientificname': 'Lonchura oryzivora (Linnaeus, 1758)',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listExot?childrenOf=Passeriformes&format=CSV>

------------------------------------------------------------------------

### Error: asking for an unknown group

We will ask for all the children of the genus Abies (Fir genus)

``` python
onlyAbies={'childrenOf':'Abies'}
response = requests.get(api_url+endpoint,json=onlyAbies)
pp(response.json())
```

    ## {'error': "'childrenOf' taxon not recognized: taxon Abies was not found in the "
    ##           'database'}

# /listThreat

## GET

``` python
endpoint="/listThreat"
```

### Comprehensive list

We will download the list and show the 5 first taxa:

``` python
response = requests.get(api_url+endpoint)
content=response.json()
len(content)
```

    ## 1299

``` python
pp(content[0:4])
```

    ## [{'cd_status': 'VU',
    ##   'cd_tax': 274,
    ##   'comments': None,
    ##   'gbifkey': 5212877,
    ##   'links': ['222: '
    ##             'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'],
    ##   'parentname': 'Arapaima Müller, 1843',
    ##   'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . '
    ##                  '(2020): Lista de especies silvestres amenazadas de la '
    ##                  'diversidad biológica continental y marino-costera de '
    ##                  'Colombia - Resolución 1912 de 2017 expedida por el '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. v2.5. '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. '
    ##                  'Dataset/Checklist. https://doi.org/10.15472/5an5tz'],
    ##   'scientificname': 'Arapaima gigas (Schinz, 1822)',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_status': 'VU',
    ##   'cd_tax': 641,
    ##   'comments': None,
    ##   'gbifkey': 5202895,
    ##   'links': ['222: '
    ##             'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'],
    ##   'parentname': 'Eremophilus Humboldt, 1805',
    ##   'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . '
    ##                  '(2020): Lista de especies silvestres amenazadas de la '
    ##                  'diversidad biológica continental y marino-costera de '
    ##                  'Colombia - Resolución 1912 de 2017 expedida por el '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. v2.5. '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. '
    ##                  'Dataset/Checklist. https://doi.org/10.15472/5an5tz'],
    ##   'scientificname': 'Eremophilus mutisii Humboldt, 1805',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_status': 'CR',
    ##   'cd_tax': 1059,
    ##   'comments': None,
    ##   'gbifkey': 2442795,
    ##   'links': ['222: '
    ##             'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'],
    ##   'parentname': 'Podocnemis Wagler, 1830',
    ##   'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . '
    ##                  '(2020): Lista de especies silvestres amenazadas de la '
    ##                  'diversidad biológica continental y marino-costera de '
    ##                  'Colombia - Resolución 1912 de 2017 expedida por el '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. v2.5. '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. '
    ##                  'Dataset/Checklist. https://doi.org/10.15472/5an5tz'],
    ##   'scientificname': 'Podocnemis expansa (Schweigger, 1812)',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_status': 'EN',
    ##   'cd_tax': 1060,
    ##   'comments': None,
    ##   'gbifkey': 2442782,
    ##   'links': ['222: '
    ##             'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'],
    ##   'parentname': 'Podocnemis Wagler, 1830',
    ##   'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . '
    ##                  '(2020): Lista de especies silvestres amenazadas de la '
    ##                  'diversidad biológica continental y marino-costera de '
    ##                  'Colombia - Resolución 1912 de 2017 expedida por el '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. v2.5. '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. '
    ##                  'Dataset/Checklist. https://doi.org/10.15472/5an5tz'],
    ##   'scientificname': 'Podocnemis unifilis Troschel, 1848',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listThreat?format=CSV>

------------------------------------------------------------------------

### Only the passerine birds

The five first passerine birds of the endemic list:

``` python
onlyPasserine={'childrenOf':'Passeriformes'}
response = requests.get(api_url+endpoint,json=onlyPasserine)
content=response.json()
len(content)
```

    ## 71

``` python
pp(content[0:4])
```

    ## [{'cd_status': 'VU',
    ##   'cd_tax': 1327,
    ##   'comments': None,
    ##   'gbifkey': 2491624,
    ##   'links': ['222: '
    ##             'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'],
    ##   'parentname': 'Arremon Vieillot, 1816',
    ##   'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . '
    ##                  '(2020): Lista de especies silvestres amenazadas de la '
    ##                  'diversidad biológica continental y marino-costera de '
    ##                  'Colombia - Resolución 1912 de 2017 expedida por el '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. v2.5. '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. '
    ##                  'Dataset/Checklist. https://doi.org/10.15472/5an5tz'],
    ##   'scientificname': 'Arremon schlegeli Bonaparte, 1850',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_status': 'EN',
    ##   'cd_tax': 1332,
    ##   'comments': None,
    ##   'gbifkey': 6088359,
    ##   'links': ['222: '
    ##             'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'],
    ##   'parentname': 'Asthenes Reichenbach, 1853',
    ##   'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . '
    ##                  '(2020): Lista de especies silvestres amenazadas de la '
    ##                  'diversidad biológica continental y marino-costera de '
    ##                  'Colombia - Resolución 1912 de 2017 expedida por el '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. v2.5. '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. '
    ##                  'Dataset/Checklist. https://doi.org/10.15472/5an5tz'],
    ##   'scientificname': 'Asthenes perijana (Phelps, 1977)',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_status': 'CR',
    ##   'cd_tax': 1335,
    ##   'comments': None,
    ##   'gbifkey': 5788834,
    ##   'links': ['222: '
    ##             'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'],
    ##   'parentname': 'Atlapetes Wagler, 1831',
    ##   'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . '
    ##                  '(2020): Lista de especies silvestres amenazadas de la '
    ##                  'diversidad biológica continental y marino-costera de '
    ##                  'Colombia - Resolución 1912 de 2017 expedida por el '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. v2.5. '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. '
    ##                  'Dataset/Checklist. https://doi.org/10.15472/5an5tz'],
    ##   'scientificname': 'Atlapetes blancae Donegan, 2007',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'cd_status': 'VU',
    ##   'cd_tax': 1336,
    ##   'comments': None,
    ##   'gbifkey': 2491438,
    ##   'links': ['222: '
    ##             'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads'],
    ##   'parentname': 'Atlapetes Wagler, 1831',
    ##   'references': ['222: Ministerio de Ambiente y Desarrollo Sostenible . '
    ##                  '(2020): Lista de especies silvestres amenazadas de la '
    ##                  'diversidad biológica continental y marino-costera de '
    ##                  'Colombia - Resolución 1912 de 2017 expedida por el '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. v2.5. '
    ##                  'Ministerio de Ambiente y Desarrollo Sostenible. '
    ##                  'Dataset/Checklist. https://doi.org/10.15472/5an5tz'],
    ##   'scientificname': 'Atlapetes flaviceps Chapman, 1912',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listThreat?childrenOf=Passeriformes&format=CSV>

------------------------------------------------------------------------

### Error: asking for an unknown group

We will ask for all the children of the genus Abies (Fir genus)

``` python
onlyAbies={'childrenOf':'Abies'}
response = requests.get(api_url+endpoint,json=onlyAbies)
pp(response.json())
```

    ## {'error': "'childrenOf' taxon not recognized: taxon Abies was not found in the "
    ##           'database'}

# /tax

## GET

``` python
endpoint = "/tax"
```

The /tax endpoints allows to query the API database for a taxon.

### From the cd_tax

cd_tax is the identificator of the taxon in the database and is returned
from many API endpoints. Therefore it might be useful to download the
information from this cd_tax

``` python
toSend={'cd_tax':150}
response = requests.get(api_url+endpoint, json=toSend)
pp(response.json())
```

    ## {'acceptedname': 'Brachiaria eminii (Mez) Robyns',
    ##  'authorship': '(Mez) Robyns',
    ##  'canonicalname': 'Brachiaria eminii',
    ##  'cd_accepted': 150,
    ##  'cd_parent': 147,
    ##  'cd_tax': 150,
    ##  'gbifkey': 4933082,
    ##  'hasendemstatus': False,
    ##  'hasexotstatus': True,
    ##  'hasthreatstatus': False,
    ##  'parentname': 'Brachiaria (Trin.) Griseb.',
    ##  'scientificname': 'Brachiaria eminii (Mez) Robyns',
    ##  'status': 'ACCEPTED',
    ##  'synonyms': ['Brachiaria decumbens Stapf',
    ##               'Urochloa decumbens (Stapf) R.D.Webster'],
    ##  'tax_rank': 'SP'}

### From a scientific name

``` python
toSend={'scientificname':"Urochloa brizantha (A.Rich.) R.D.Webster"}
response = requests.get(api_url+endpoint, json=toSend)
pp(response.json())
```

    ## {'acceptedname': 'Brachiaria brizantha (A.Rich.) Stapf',
    ##  'authorship': '(A.Rich.) R.D.Webster',
    ##  'canonicalname': 'Urochloa brizantha',
    ##  'cd_accepted': 148,
    ##  'cd_parent': None,
    ##  'cd_tax': 149,
    ##  'gbifkey': 2705862,
    ##  'hasendemstatus': False,
    ##  'hasexotstatus': False,
    ##  'hasthreatstatus': False,
    ##  'parentname': None,
    ##  'scientificname': 'Urochloa brizantha (A.Rich.) R.D.Webster',
    ##  'status': 'SYNONYM',
    ##  'synonyms': [None],
    ##  'tax_rank': 'SP'}

### From a canonical name

``` python
toSend={'canonicalname':'Rottboellia cochinchinensis'}
response = requests.get(api_url+endpoint, json=toSend)
pp(response.json())
```

    ## {'acceptedname': 'Rottboellia cochinchinensis (Lour.) Clayton',
    ##  'authorship': '(Lour.) Clayton',
    ##  'canonicalname': 'Rottboellia cochinchinensis',
    ##  'cd_accepted': 135,
    ##  'cd_parent': 134,
    ##  'cd_tax': 135,
    ##  'gbifkey': 2704075,
    ##  'hasendemstatus': False,
    ##  'hasexotstatus': True,
    ##  'hasthreatstatus': False,
    ##  'parentname': 'Rottboellia L.f.',
    ##  'scientificname': 'Rottboellia cochinchinensis (Lour.) Clayton',
    ##  'status': 'ACCEPTED',
    ##  'synonyms': [None],
    ##  'tax_rank': 'SP'}

### Species which is not in database

The API send back an empty JSON variable

``` python
toSend={'canonicalname':'Amanita caesarea'}
response = requests.get(api_url+endpoint, json=toSend)
pp(response.json())
```

    ## None

### Species which does not exist

The API send back an empty JSON variable

``` python
toSend={'canonicalname':'Inventadus inexistus'}
response = requests.get(api_url+endpoint, json=toSend)
pp(response.json())
```

    ## None

# /listTax

## GET

The “/listTax” endpoints allows to query the taxonomic table of the
database API.

``` python
endpoint="/listTax"
```

### Comprehensive list

Here is the code to download the complete list of taxa in the database
and show the 5 first taxa.

``` python
response = requests.get(api_url+endpoint)
content=response.json()
len(content)
```

    ## 3756

``` python
pp(content[0:4])
```

    ## [{'acceptedname': 'Plantae',
    ##   'authorship': None,
    ##   'canonicalname': 'Plantae',
    ##   'cd_accepted': 1,
    ##   'cd_parent': None,
    ##   'cd_tax': 1,
    ##   'gbifkey': 6,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': None,
    ##   'scientificname': 'Plantae',
    ##   'status': 'ACCEPTED',
    ##   'synonyms': [None],
    ##   'tax_rank': 'KG'},
    ##  {'acceptedname': 'Tracheophyta',
    ##   'authorship': None,
    ##   'canonicalname': 'Tracheophyta',
    ##   'cd_accepted': 2,
    ##   'cd_parent': 1,
    ##   'cd_tax': 2,
    ##   'gbifkey': 7707728,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Plantae',
    ##   'scientificname': 'Tracheophyta',
    ##   'status': 'ACCEPTED',
    ##   'synonyms': [None],
    ##   'tax_rank': 'PHY'},
    ##  {'acceptedname': 'Magnoliopsida',
    ##   'authorship': None,
    ##   'canonicalname': 'Magnoliopsida',
    ##   'cd_accepted': 3,
    ##   'cd_parent': 2,
    ##   'cd_tax': 3,
    ##   'gbifkey': 220,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Tracheophyta',
    ##   'scientificname': 'Magnoliopsida',
    ##   'status': 'ACCEPTED',
    ##   'synonyms': [None],
    ##   'tax_rank': 'CL'},
    ##  {'acceptedname': 'Fabales',
    ##   'authorship': None,
    ##   'canonicalname': 'Fabales',
    ##   'cd_accepted': 4,
    ##   'cd_parent': 3,
    ##   'cd_tax': 4,
    ##   'gbifkey': 1370,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Magnoliopsida',
    ##   'scientificname': 'Fabales',
    ##   'status': 'ACCEPTED',
    ##   'synonyms': [None],
    ##   'tax_rank': 'OR'}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listTax?format=CSV>

------------------------------------------------------------------------

### Only the Bivalve

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
pp(content[0:9])
```

    ## [{'acceptedname': 'Bivalvia',
    ##   'authorship': None,
    ##   'canonicalname': 'Bivalvia',
    ##   'cd_accepted': 495,
    ##   'cd_parent': 9,
    ##   'cd_tax': 495,
    ##   'gbifkey': 137,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Mollusca',
    ##   'scientificname': 'Bivalvia',
    ##   'status': 'ACCEPTED',
    ##   'synonyms': [None],
    ##   'tax_rank': 'CL'},
    ##  {'acceptedname': 'Venerida',
    ##   'authorship': None,
    ##   'canonicalname': 'Venerida',
    ##   'cd_accepted': 496,
    ##   'cd_parent': 495,
    ##   'cd_tax': 496,
    ##   'gbifkey': 9310756,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Bivalvia',
    ##   'scientificname': 'Venerida',
    ##   'status': 'ACCEPTED',
    ##   'synonyms': [None],
    ##   'tax_rank': 'OR'},
    ##  {'acceptedname': 'Cyrenidae',
    ##   'authorship': None,
    ##   'canonicalname': 'Cyrenidae',
    ##   'cd_accepted': 497,
    ##   'cd_parent': 496,
    ##   'cd_tax': 497,
    ##   'gbifkey': 6527076,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Venerida',
    ##   'scientificname': 'Cyrenidae',
    ##   'status': 'ACCEPTED',
    ##   'synonyms': [None],
    ##   'tax_rank': 'FAM'},
    ##  {'acceptedname': 'Corbicula Megerle von Mühlfeld, 1811',
    ##   'authorship': 'Megerle von Mühlfeld, 1811',
    ##   'canonicalname': 'Corbicula',
    ##   'cd_accepted': 498,
    ##   'cd_parent': 497,
    ##   'cd_tax': 498,
    ##   'gbifkey': 11352197,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Cyrenidae',
    ##   'scientificname': 'Corbicula Megerle von Mühlfeld, 1811',
    ##   'status': 'DOUBTFUL',
    ##   'synonyms': [None],
    ##   'tax_rank': 'GN'},
    ##  {'acceptedname': 'Corbicula fluminea (O.F.Müller, 1774)',
    ##   'authorship': '(O.F.Müller, 1774) ',
    ##   'canonicalname': 'Corbicula fluminea',
    ##   'cd_accepted': 499,
    ##   'cd_parent': 498,
    ##   'cd_tax': 499,
    ##   'gbifkey': 8190231,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': True,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Corbicula Megerle von Mühlfeld, 1811',
    ##   'scientificname': 'Corbicula fluminea (O.F.Müller, 1774)',
    ##   'status': 'ACCEPTED',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'},
    ##  {'acceptedname': 'Arcida',
    ##   'authorship': None,
    ##   'canonicalname': 'Arcida',
    ##   'cd_accepted': 3132,
    ##   'cd_parent': 495,
    ##   'cd_tax': 3132,
    ##   'gbifkey': 9574493,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Bivalvia',
    ##   'scientificname': 'Arcida',
    ##   'status': 'ACCEPTED',
    ##   'synonyms': [None],
    ##   'tax_rank': 'OR'},
    ##  {'acceptedname': 'Arcidae',
    ##   'authorship': None,
    ##   'canonicalname': 'Arcidae',
    ##   'cd_accepted': 3133,
    ##   'cd_parent': 3132,
    ##   'cd_tax': 3133,
    ##   'gbifkey': 3483,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Arcida',
    ##   'scientificname': 'Arcidae',
    ##   'status': 'ACCEPTED',
    ##   'synonyms': [None],
    ##   'tax_rank': 'FAM'},
    ##  {'acceptedname': 'Anadara Gray, 1847',
    ##   'authorship': 'Gray, 1847',
    ##   'canonicalname': 'Anadara',
    ##   'cd_accepted': 3134,
    ##   'cd_parent': 3133,
    ##   'cd_tax': 3134,
    ##   'gbifkey': 2286218,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': False,
    ##   'parentname': 'Arcidae',
    ##   'scientificname': 'Anadara Gray, 1847',
    ##   'status': 'ACCEPTED',
    ##   'synonyms': [None],
    ##   'tax_rank': 'GN'},
    ##  {'acceptedname': 'Anadara tuberculosa (G.B.Sowerby I, 1833)',
    ##   'authorship': '(G.B.Sowerby I, 1833) ',
    ##   'canonicalname': 'Anadara tuberculosa',
    ##   'cd_accepted': 3135,
    ##   'cd_parent': 3134,
    ##   'cd_tax': 3135,
    ##   'gbifkey': 5188932,
    ##   'hasendemstatus': False,
    ##   'hasexotstatus': False,
    ##   'hasthreatstatus': True,
    ##   'parentname': 'Anadara Gray, 1847',
    ##   'scientificname': 'Anadara tuberculosa (G.B.Sowerby I, 1833)',
    ##   'status': 'ACCEPTED',
    ##   'synonyms': [None],
    ##   'tax_rank': 'SP'}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listTax?childrenOf=Bivalvia&format=CSV>

------------------------------------------------------------------------

# /listReferences

``` python
endpoint = "/listReferences"
```

## GET

The GET method of the */listReferences* endpoint allows to get the
reference list from the API database.

### Comprehensive list

Here to download the reference list and show the 10 first results:

``` python
response = requests.get(api_url+endpoint)
content=response.json()
len(content)
```

    ## 222

``` python
pp(content[0:9])
```

    ## [{'cd_ref': 1,
    ##   'link': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020',
    ##   'nb_endem': 0,
    ##   'nb_exot': 45,
    ##   'nb_threat': 0,
    ##   'ref_citation': ' Instituto de Investigación de Recursos Biológicos '
    ##                   'Alexander von Humboldt (2020). Base de datos de información '
    ##                   'ecológica e invasividad de especies exóticas prioritarias '
    ##                   'de flora y fauna de Colombia. 43 registros.'},
    ##  {'cd_ref': 2,
    ##   'link': None,
    ##   'nb_endem': 0,
    ##   'nb_exot': 36,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Cárdenas D., Baptiste M.P., Castaño N. (2017). Plantas '
    ##                   'exóticas con alto potencial de invasión en Colombia. '
    ##                   'Instituto de Investigación de Recursos Biológicos Alexander '
    ##                   'von Humboldt. Bogotá, D. C., Colombia. 295 p.'},
    ##  {'cd_ref': 3,
    ##   'link': None,
    ##   'nb_endem': 0,
    ##   'nb_exot': 1,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Mora, M. F., Rubio J., Ocampo R. & Barrera J.I. (2015). '
    ##                   'Catálogo de especies invasoras del territorio CAR. '
    ##                   'Publicado por Pontificia Universidad Javeriana & '
    ##                   'Corporación Autónoma Regional de Cundinamarca – CAR, 238 '
    ##                   'pp.'},
    ##  {'cd_ref': 4,
    ##   'link': 'https://www.car.gov.co/uploads/files/5b9033f095d34.pdf',
    ##   'nb_endem': 0,
    ##   'nb_exot': 1,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Corporación Autónoma Regional (2018). Plan de Prevención, '
    ##                   'Control y Manejo (PPCM) de Caracol Gigante Africano '
    ##                   '(Achatina fulica) en la jurisdicción CAR. Dirección de '
    ##                   'Recursos Naturales. 61 pp.'},
    ##  {'cd_ref': 5,
    ##   'link': 'http://www.iucngisd.org/gisd/speciesname/Achatina+fulica',
    ##   'nb_endem': 0,
    ##   'nb_exot': 1,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Invasive Species Specialist Group (2020). Achatina fulica.'},
    ##  {'cd_ref': 6,
    ##   'link': None,
    ##   'nb_endem': 0,
    ##   'nb_exot': 1,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Garcés M., Patiño A., Gómez M., Giraldo A. & Bolívar G. '
    ##                   '(2016). Sustancias alternativas para el control del caracol '
    ##                   'africano (Achatina fulica) en el Valle del Cauca. Biota '
    ##                   'Colombiana. Vol. 17(1), 44 - 52 pp.'},
    ##  {'cd_ref': 7,
    ##   'link': 'https://www.cabi.org/isc/datasheet/93023',
    ##   'nb_endem': 0,
    ##   'nb_exot': 1,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Invasive Species Compendium (2019). Anthoxanthum odoratum '
    ##                   '(sweet vernal grass).'},
    ##  {'cd_ref': 8,
    ##   'link': 'https://www.cabi.org/isc/datasheet/1940',
    ##   'nb_endem': 0,
    ##   'nb_exot': 1,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Invasive Species Compendium (2019). Arundo donax (giant '
    ##                   'reed).'},
    ##  {'cd_ref': 9,
    ##   'link': 'https://www.cabi.org/isc/datasheet/8119',
    ##   'nb_endem': 0,
    ##   'nb_exot': 1,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Invasive Species Compendium (2019). Azolla filiculoides '
    ##                   '(water fern).'}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listReferences?format=CSV>

------------------------------------------------------------------------

### Only the references concerning exotic species

``` python
onlyExot={'onlyExot':True}
response = requests.get(api_url+endpoint, json=onlyExot)
content=response.json()
len(content)
```

    ## 90

``` python
pp(content[0:9])
```

    ## [{'cd_ref': 1,
    ##   'link': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020',
    ##   'nb_endem': 0,
    ##   'nb_exot': 45,
    ##   'nb_threat': 0,
    ##   'ref_citation': ' Instituto de Investigación de Recursos Biológicos '
    ##                   'Alexander von Humboldt (2020). Base de datos de información '
    ##                   'ecológica e invasividad de especies exóticas prioritarias '
    ##                   'de flora y fauna de Colombia. 43 registros.'},
    ##  {'cd_ref': 2,
    ##   'link': None,
    ##   'nb_endem': 0,
    ##   'nb_exot': 36,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Cárdenas D., Baptiste M.P., Castaño N. (2017). Plantas '
    ##                   'exóticas con alto potencial de invasión en Colombia. '
    ##                   'Instituto de Investigación de Recursos Biológicos Alexander '
    ##                   'von Humboldt. Bogotá, D. C., Colombia. 295 p.'},
    ##  {'cd_ref': 3,
    ##   'link': None,
    ##   'nb_endem': 0,
    ##   'nb_exot': 1,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Mora, M. F., Rubio J., Ocampo R. & Barrera J.I. (2015). '
    ##                   'Catálogo de especies invasoras del territorio CAR. '
    ##                   'Publicado por Pontificia Universidad Javeriana & '
    ##                   'Corporación Autónoma Regional de Cundinamarca – CAR, 238 '
    ##                   'pp.'},
    ##  {'cd_ref': 4,
    ##   'link': 'https://www.car.gov.co/uploads/files/5b9033f095d34.pdf',
    ##   'nb_endem': 0,
    ##   'nb_exot': 1,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Corporación Autónoma Regional (2018). Plan de Prevención, '
    ##                   'Control y Manejo (PPCM) de Caracol Gigante Africano '
    ##                   '(Achatina fulica) en la jurisdicción CAR. Dirección de '
    ##                   'Recursos Naturales. 61 pp.'},
    ##  {'cd_ref': 5,
    ##   'link': 'http://www.iucngisd.org/gisd/speciesname/Achatina+fulica',
    ##   'nb_endem': 0,
    ##   'nb_exot': 1,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Invasive Species Specialist Group (2020). Achatina fulica.'},
    ##  {'cd_ref': 6,
    ##   'link': None,
    ##   'nb_endem': 0,
    ##   'nb_exot': 1,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Garcés M., Patiño A., Gómez M., Giraldo A. & Bolívar G. '
    ##                   '(2016). Sustancias alternativas para el control del caracol '
    ##                   'africano (Achatina fulica) en el Valle del Cauca. Biota '
    ##                   'Colombiana. Vol. 17(1), 44 - 52 pp.'},
    ##  {'cd_ref': 7,
    ##   'link': 'https://www.cabi.org/isc/datasheet/93023',
    ##   'nb_endem': 0,
    ##   'nb_exot': 1,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Invasive Species Compendium (2019). Anthoxanthum odoratum '
    ##                   '(sweet vernal grass).'},
    ##  {'cd_ref': 8,
    ##   'link': 'https://www.cabi.org/isc/datasheet/1940',
    ##   'nb_endem': 0,
    ##   'nb_exot': 1,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Invasive Species Compendium (2019). Arundo donax (giant '
    ##                   'reed).'},
    ##  {'cd_ref': 9,
    ##   'link': 'https://www.cabi.org/isc/datasheet/8119',
    ##   'nb_endem': 0,
    ##   'nb_exot': 1,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Invasive Species Compendium (2019). Azolla filiculoides '
    ##                   '(water fern).'}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listReferences?onlyExot=True&format=CSV>

------------------------------------------------------------------------

### Only the references concerning threatened species

``` python
onlyThreat={'onlyThreat':True}
response = requests.get(api_url+endpoint, json=onlyThreat)
content=response.json()
len(content)
```

    ## 1

``` python
pp(content[0:9])
```

    ## [{'cd_ref': 222,
    ##   'link': 'https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads',
    ##   'nb_endem': 0,
    ##   'nb_exot': 0,
    ##   'nb_threat': 1299,
    ##   'ref_citation': 'Ministerio de Ambiente y Desarrollo Sostenible . (2020): '
    ##                   'Lista de especies silvestres amenazadas de la diversidad '
    ##                   'biológica continental y marino-costera de Colombia - '
    ##                   'Resolución 1912 de 2017 expedida por el Ministerio de '
    ##                   'Ambiente y Desarrollo Sostenible. v2.5. Ministerio de '
    ##                   'Ambiente y Desarrollo Sostenible. Dataset/Checklist. '
    ##                   'https://doi.org/10.15472/5an5tz'}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listReferences?onlyThreat=True&format=CSV>

------------------------------------------------------------------------

### Only the references concerning endemic species

``` python
onlyEndem={'onlyEndem':True}
response = requests.get(api_url+endpoint, json=onlyEndem)
content=response.json()
len(content)
```

    ## 131

``` python
pp(content[0:9])
```

    ## [{'cd_ref': 91,
    ##   'link': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09',
    ##   'nb_endem': 308,
    ##   'nb_exot': 0,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., '
    ##                   'Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado '
    ##                   'actualizado de las aves endémicas y casi-endémicas de '
    ##                   'Colombia. 308 registros. Versión 5.1. '
    ##                   'http://doi.org/10.15472/tozuue'},
    ##  {'cd_ref': 92,
    ##   'link': None,
    ##   'nb_endem': 14,
    ##   'nb_exot': 0,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Arbeláez-Cortés et al. 2011b'},
    ##  {'cd_ref': 93,
    ##   'link': None,
    ##   'nb_endem': 6,
    ##   'nb_exot': 0,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Cuervo et al. 2008a'},
    ##  {'cd_ref': 94,
    ##   'link': None,
    ##   'nb_endem': 7,
    ##   'nb_exot': 0,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Cuervo et al. 2008b'},
    ##  {'cd_ref': 95,
    ##   'link': None,
    ##   'nb_endem': 2,
    ##   'nb_exot': 0,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Merkord 2010'},
    ##  {'cd_ref': 96,
    ##   'link': None,
    ##   'nb_endem': 1,
    ##   'nb_exot': 0,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Rodríguez y Rojas-Suárez 2008'},
    ##  {'cd_ref': 97,
    ##   'link': None,
    ##   'nb_endem': 6,
    ##   'nb_exot': 0,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Corpocaldas 2010'},
    ##  {'cd_ref': 98,
    ##   'link': None,
    ##   'nb_endem': 25,
    ##   'nb_exot': 0,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Donegan et al. 2010'},
    ##  {'cd_ref': 99,
    ##   'link': None,
    ##   'nb_endem': 5,
    ##   'nb_exot': 0,
    ##   'nb_threat': 0,
    ##   'ref_citation': 'Laverde-R. Et al. 2005b'}]

------------------------------------------------------------------------

**Note**:

You might want to download the list as a CSV file, the most practical
way to do that is not from the python interface, just click here:

<https://colsplist.herokuapp.com/listReferences?onlyEndem=True&format=CSV>

------------------------------------------------------------------------
