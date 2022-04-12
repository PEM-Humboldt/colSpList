Testing and getting species status with the colSpList API
================

The colSpList API allows to know whether species have a status for
Colombia in terms of endemism, threat and alien/invasive. In this
document, we will show how to use the *GET* endpoints of the API with
simple programs in R and/or Python.

<!--
La API colSpList permite saber si las especies son exóticas/invasivas, endémicas o amenazadas.
En este documento, mostraré como utilizar los endpoints GET de la API, desde códigos simples en R o Python.
-->

------------------------------------------------------------------------

**Note 1**:

This document was created from a Rmarkdown document, with the output
format “github_document”. In order to use this type of file, please
install the packages *knitr* and *rmarkdown* in R.

1.  If you want to compile the document as a markdown document for
    github, while applying all the code contained in the file
    -   use `rmarkdown::render("file.Rmd")`
2.  If you want to extract the R code of the document as a R script
    -   use `knitr::purl("file.Rmd")`

Note: extracting the python code may be done but it is a bit more
complex, please search the documentation of the packages *knitr* and
*rmarkdown*

**Note 2**:

In a near future these endpoints might return slightly different result
for 3 main reasons:

1.  For now, in order to work, the API try to insert all species which
    are sent as parameters. I made it that way because I wanted the API
    to gain efficiency with its use. However the API is hosted in
    Heroku, which limits to 10.000 the numbers of rows in the database.
    Therefore we might reach the maximum quite rapidly with this policy,
    therefore I will soon change this. **PLEASE DO NOT USE THE API WITH
    LARGE DATASETS JUST YET**
2.  For now, there is no explicit error handler in the API, so the error
    are not sent back to the user but need to be checked on the heroku
    logs. I think this should be changed soon.
3.  We did not yet implement the security policies, we might have to
    change slightly the functioning of the API in the future in order to
    implement token-based security of the API

------------------------------------------------------------------------

# 1 Generalities

The main endpoints to get informations about the species statuses are:

-   testEndem
-   testExot
-   testThreat

In all cases, the parameters of the endpoints may be sent through a http
query and/or a JSON objects associated with the query.

The parameters required for these endpoints to work are the ones that
allow the API to recognize the taxon that you are looking for:

-   **canonicalname**: the latin name of the species, without authorship
-   **scientificname**: the complete name, with authorship
-   **gbifkey** the key of the taxon in GBIF (speciesKey from the GBIF
    backbone)

Note that the API will automatically try to correct the small
orthographic mistakes and resolve cases of synonymy.

# 2 Simple usage from the internet browser

Copy the following link to your browser to check whether the taxon
*Espeletia paipana* is endemic in colombia:

<https://colsplist.herokuapp.com/testEndem?canonicalname=Espeletia%20paipana>

The result is directly visible in you browser.

In order to change the species, just edit the part after
`canonicalname=` with whichever species you are looking for.

Example of *Paroaria nigrogenis*:

<https://colsplist.herokuapp.com/testEndem?canonicalname=Paroaria%20nigrogenis>

The speciesKey of *Paroaria nigrogenis* in the gbif taxonomic backbone
is 5845551

So you may as well try the following URL, with the same result:

<https://colsplist.herokuapp.com/testEndem?gbifkey=5845551>

Now you may replace the “testEndem” by “testExot” (alien/invasive
status) or “testThreat” (threat status) in the URLs.

# 3 Simple usage in R

``` r
require(httr)
```

    ## Loading required package: httr

``` r
require(jsonlite)
```

    ## Loading required package: jsonlite

``` r
baseURL <- "https://colsplist.herokuapp.com/"
```

Testing whether *Hylocharis grayi* is endemic:

``` r
speciesToTest <- "Hylocharis grayi"
endpoint <- "testEndem"
res <- GET(paste0(baseURL,endpoint),query=list(canonicalname=speciesToTest),content_type("application/json"))
content(res)
```

    ## $message
    ## [1] "Internal Server Error"

Testing whether it is alien/invasive:

``` r
endpoint <- "testExot"
res <- GET(paste0(baseURL,endpoint),query=list(canonicalname=speciesToTest),content_type("application/json"))
content(res)
```

    ## $message
    ## [1] "Internal Server Error"

Testing whether *Espeletia paipana* is threatened in Colombia

``` r
speciesToTest <- "Espeletia paipana"
endpoint <- "testThreat"
res <- GET(paste0(baseURL,endpoint),query=list(canonicalname=speciesToTest),content_type("application/json"))
content(res)
```

    ## $cd_tax
    ## [1] 2831
    ## 
    ## $cd_tax_acc
    ## [1] 2831
    ## 
    ## $alreadyInDb
    ## [1] TRUE
    ## 
    ## $foundGbif
    ## [1] TRUE
    ## 
    ## $matchedname
    ## [1] "Espeletia paipana"
    ## 
    ## $acceptedname
    ## [1] "Espeletia paipana S.Díaz & Pedraza"
    ## 
    ## $gbifkey
    ## [1] 3105080
    ## 
    ## $syno
    ## [1] FALSE
    ## 
    ## $insertedTax
    ## list()
    ## 
    ## $hasThreatStatus
    ## [1] TRUE
    ## 
    ## $cd_status
    ## [1] "CR"
    ## 
    ## $comments
    ## NULL
    ## 
    ## $references
    ## [1] "Ministerio de Ambiente y Desarrollo Sostenible . (2020): Lista de especies silvestres amenazadas de la diversidad biológica continental y marino-costera de Colombia - Resolución 1912 de 2017 expedida por el Ministerio de Ambiente y Desarrollo Sostenible. v2.5. Ministerio de Ambiente y Desarrollo Sostenible. Dataset/Checklist. https://doi.org/10.15472/5an5tz"
    ## 
    ## $links
    ## [1] "https://ipt.biodiversidad.co/sib/resource?r=resolucion1912-2017mads#anchor-downloads"

# 4 Basic usage in Python

Testing whether *Polyerata amabilis* is endemic in Colombia:

``` python
import requests
import json
baseURL = "https://colsplist.herokuapp.com/"
endpoint = "testEndem"
speciesToCheck = "Polyerata amabilis"
response = requests.get(baseURL+endpoint, params={'canonicalname':speciesToCheck})
response.json()
```

    ## {'cd_tax': 1287, 'cd_tax_acc': 1287, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Polyerata amabilis', 'acceptedname': 'Polyerata amabilis (Gould, 1853)', 'gbifkey': 5788536, 'syno': False, 'insertedTax': [], 'hasEndemStatus': True, 'cd_nivel': 1, 'endemism': 'Especie de interés', 'comments': 'locality: Ecuador: Vertiente pacífica del Ecuador | occurrenceRemarks: Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Región más húmeda inmediatamente al sur de la región 1, desde el bajo río Atrato hasta la parte media del valle del río Magdalena, incluyendo el alto río Sinú y alto río Nechí |Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Andén del Pacífico, desde la zona media del Darién en límites con Panamá, al lado izquierdo del bajo río Atrato, hasta el Ecuador |Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Alto valle del río Magdalena, principalmente en Tolima y Huila |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas más al norte de la cordillera Occidental y de la cordillera Central y la ladera nororiental de la Central hacia el sur hasta aproximadamente el límite sur de Caldas |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas del alto valle del río Magdalena principalmente en Tolima y Huila |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Vertiente occidental de la cordillera Oriental, desde el sur de Cesar hasta Cundinamarca | ', 'references': 'Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue | Corpocaldas 2010 | Donegan et al. 2010 | Laverde-R. Et al. 2005b | Parra-Hernández et al. 2007', 'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09'}

Testing whether *Polyerata amabilis* is threatened in Colombia:

``` python
import requests
import json
baseURL = "https://colsplist.herokuapp.com/"
endpoint = "testThreat"
speciesToCheck = "Polyerata amabilis"
response = requests.get(baseURL+endpoint, params={'canonicalname':speciesToCheck})
response.json()
```

    ## {'cd_tax': 1287, 'cd_tax_acc': 1287, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Polyerata amabilis', 'acceptedname': 'Polyerata amabilis (Gould, 1853)', 'gbifkey': 5788536, 'syno': False, 'insertedTax': [], 'hasThreatStatus': False, 'cd_status': None, 'comments': None, 'references': None, 'links': None}

Testing whether *Acacia decurrens* is alien/invasive in Colombia:

``` python
import requests
import json
baseURL = "https://colsplist.herokuapp.com/"
endpoint = "testExot"
speciesToCheck = "Acacia decurrens"
response = requests.get(baseURL+endpoint, params={'canonicalname':speciesToCheck})
response.json()
```

    ## {'cd_tax': 7, 'cd_tax_acc': 7, 'alreadyInDb': True, 'foundGbif': True, 'matchedname': 'Acacia decurrens', 'acceptedname': 'Acacia decurrens (J.C.Wendl.) Willd.', 'gbifkey': 2979778, 'syno': False, 'insertedTax': [], 'hasExotStatus': True, 'is_alien': True, 'is_invasive': True, 'comments': 'Altitud máxima: 3200 | Altitud máxima Unit: m.s.n.m. | Altitud mínima: 1600 | Altitud mínima Unit: m.s.n.m. | Asociación invasiva: No se encontraron datos | Aspectos generales de invasividad: Producción abundante de semillas, rápida germinación, alta viabilidad, resistencia a inundaciones y fuego, alta producción vegetativa, sustancias alelopáticas | Causas de introducción: Usos ornamentales | Distribución como exótica: Cosmopólita | Distribución nativa: ARG , AUS , NZL , URY , ZAF | Estatus: Exótica | Translocada | Factores limitantes para el establecimiento: Heladas, no tiene éxito por debajo de los 1000 msnm, zonas húmedas y secas tropicales | Hábito: Terrestre | Impactos de introducción: Migración de zonas de cultivos a espacios naturales, aumento regímenes de incendio, restricción en la regeneración natural de especies nativas, impedimento en el movimiento de fauna | Introducida después de (año): 1963 | Medidas de manejo y control: En África se ha evidenciado el control biológico sobre semillas con la especie Melanterius maculatus (Curculionidae) y en Nueva Zelanda con Bruchophagus acaciae (Hymenoptera) | Observaciones de ocurrencia: Frecuentemente en zonas de incendios y áreas perturbadas | pH: 7 | Precipitación máxima: 1200 | Precipitación máxima Unit: mm | Precipitación mínima: 750 | Precipitación mínima Unit: mm | Puntaje Riesgo de Invasión: 5 | Puntaje Riesgo de Invasión Remarks: Fuente: I3N | Riesgo de invasión: Alto riesgo | Temperatura máxima: 18 | Temperatura máxima Unit: °C | Temperatura mínima: 14 | Temperatura mínima Unit: °C | Tipo de dispersión: Anemocoría, zoocoría | Tipo de introducción: Intencional | Tipo de reproducción: Semillas | Tipo de suelo: Arenosos-arcillosos | Vías de introducción: Sembrada', 'references': ' Instituto de Investigación de Recursos Biológicos Alexander von Humboldt (2020). Base de datos de información ecológica e invasividad de especies exóticas prioritarias de flora y fauna de Colombia. 43 registros. | Cárdenas D., Baptiste M.P., Castaño N. (2017). Plantas exóticas con alto potencial de invasión en Colombia. Instituto de Investigación de Recursos Biológicos Alexander von Humboldt. Bogotá, D. C., Colombia. 295 p. | Mora, M. F., Rubio J., Ocampo R. & Barrera J.I. (2015). Catálogo de especies invasoras del territorio CAR. Publicado por Pontificia Universidad Javeriana & Corporación Autónoma Regional de Cundinamarca – CAR, 238 pp. | Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG.', 'links': 'http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020 | https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91'}
