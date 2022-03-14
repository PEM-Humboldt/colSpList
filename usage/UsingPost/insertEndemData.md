Inserting endemic species with the colSpList API
================

------------------------------------------------------------------------

**Note**:

This document was created from a Rmarkdown document, with the output
format “github_document”. In order to use this type of file, please
install the packages *knitr* and *rmarkdown* in R.

1.  If you want to compile the document as a markdown document for
    github, while applying all the code contained in the file
    -   use `rmarkdown::render("file.Rmd")`
2.  If you want to extract the R code of the document as a R script
    -   use `knitr::purl("file.Rmd")`

------------------------------------------------------------------------

In order to show how to work with the colSpList API and the threatened
species, we will use the species list from Ceiba, concerning the endemic
bird species of Colombia (publicly available at
<http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09>)

# 1 Preformatting the dataset

The dataset downloaded from Ceiba includes various files, that we need
to preformat (here in R), in order to extract the information that we
may send to the API and its database:

``` r
directory = "../../data/dwca-biota_v14_n2_09"
(files = dir(directory))
```

    ## [1] "description.txt"      "distribution.txt"     "eml.xml"             
    ## [4] "meta.xml"             "taxon.txt"            "typesandspecimen.txt"
    ## [7] "vernacularname.txt"

In order to read all the text files in the directory:

``` r
fileNames <- files[grepl("\\.txt$",files)]
filesToRead <- paste(directory,fileNames,sep = "/")
data <- lapply(filesToRead,read.csv,sep="\t")
names(data) <- sub("\\.txt","",fileNames)
```

The first lines of each read file is :

``` r
lapply(data,head,5)
```

    ## $description
    ##                                   id        description         type
    ## 1 urn:lsid:ubio.org:namebank:3851488      Casi endémica Distribución
    ## 2 urn:lsid:ubio.org:namebank:3853053      Casi endémica Distribución
    ## 3 urn:lsid:ubio.org:namebank:3852923 Especie de interés Distribución
    ## 4 urn:lsid:ubio.org:namebank:3852937           Endémica Distribución
    ## 5 urn:lsid:ubio.org:namebank:3854768           Endémica Distribución
    ## 
    ## $distribution
    ##                                   id
    ## 1 urn:lsid:ubio.org:namebank:3851488
    ## 2 urn:lsid:ubio.org:namebank:3853053
    ## 3 urn:lsid:ubio.org:namebank:3852923
    ## 4 urn:lsid:ubio.org:namebank:3852937
    ## 5 urn:lsid:ubio.org:namebank:3854768
    ##                                                                                                                                                                   locality
    ## 1 Venezuela: Andes venezolanos | Ecuador: Los Andes | Vertiente oriental hacia Amazonía | Perú: Amazonas (desde divisoria de aguas y principales drenajes al río Amazonas)
    ## 2                                                                                                                                  Ecuador: Vertiente pacífica del Ecuador
    ## 3                                                                                                                                  Ecuador: Vertiente pacífica del Ecuador
    ## 4                                                                                                                                                                         
    ## 5                                                                                                                                                                         
    ##                  countryCode
    ## 1        VE:00; PE:00; EC:00
    ## 2                      EC:00
    ## 3 EC:00; PA:00; NI:00; CR:00
    ## 4                           
    ## 5                           
    ##                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             occurrenceRemarks
    ## 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el Golfo de Urabá hasta la Península de La Guajira, incluyendo las estribaciones de la Sierra Nevada de Santa Marta y la Serranía de Perijá en el norte de Cesar, y como subregión |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas más al norte de la cordillera Occidental y de la cordillera Central y la ladera nororiental de la Central hacia el sur hasta aproximadamente el límite sur de Caldas |Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. cordillera Central
    ## 2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Andén del Pacífico, desde la zona media del Darién en límites con Panamá, al lado izquierdo del bajo río Atrato, hasta el Ecuador |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Vertiente occidental de la cordillera Occidental que incluye
    ## 3 Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Región más húmeda inmediatamente al sur de la región 1, desde el bajo río Atrato hasta la parte media del valle del río Magdalena, incluyendo el alto río Sinú y alto río Nechí |Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Andén del Pacífico, desde la zona media del Darién en límites con Panamá, al lado izquierdo del bajo río Atrato, hasta el Ecuador |Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Alto valle del río Magdalena, principalmente en Tolima y Huila |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas más al norte de la cordillera Occidental y de la cordillera Central y la ladera nororiental de la Central hacia el sur hasta aproximadamente el límite sur de Caldas |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas del alto valle del río Magdalena principalmente en Tolima y Huila |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Vertiente occidental de la cordillera Oriental, desde el sur de Cesar hasta Cundinamarca
    ## 4                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       Franja y región: Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Vertiente occidental de la cordillera Oriental, desde el sur de Cesar hasta Cundinamarca
    ## 5                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              Franja y región: Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Vertiente occidental de la cordillera Oriental, desde el sur de Cesar hasta Cundinamarca |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas del Valle del Cauca
    ## 
    ## $taxon
    ##                                   id                            taxonID
    ## 1 urn:lsid:ubio.org:namebank:3851488 urn:lsid:ubio.org:namebank:3851488
    ## 2 urn:lsid:ubio.org:namebank:3853053 urn:lsid:ubio.org:namebank:3853053
    ## 3 urn:lsid:ubio.org:namebank:3852923 urn:lsid:ubio.org:namebank:3852923
    ## 4 urn:lsid:ubio.org:namebank:3852937 urn:lsid:ubio.org:namebank:3852937
    ## 5 urn:lsid:ubio.org:namebank:3854768 urn:lsid:ubio.org:namebank:3854768
    ##             scientificName acceptedNameUsage
    ## 1       Accipiter collaris                  
    ## 2   Aglaiocercus coelestis                  
    ## 3        Amazilia amabilis                  
    ## 4 Amazilia castaneiventris                  
    ## 5      Amazilia cyanifrons                  
    ##                                                                       nameAccordingTo
    ## 1 Taxonomía y estado taxonómico tomado de:Species 2000 & ITIS Catalogue of Life: 2014
    ## 2 Taxonomía y estado taxonómico tomado de:Species 2000 & ITIS Catalogue of Life: 2014
    ## 3 Taxonomía y estado taxonómico tomado de:Species 2000 & ITIS Catalogue of Life: 2014
    ## 4 Taxonomía y estado taxonómico tomado de:Species 2000 & ITIS Catalogue of Life: 2014
    ## 5 Taxonomía y estado taxonómico tomado de:Species 2000 & ITIS Catalogue of Life: 2014
    ##    kingdom   phylum class           order       family        genus
    ## 1 Animalia Chordata  Aves Accipitriformes Accipitridae    Accipiter
    ## 2 Animalia Chordata  Aves     Apodiformes  Trochilidae Aglaiocercus
    ## 3 Animalia Chordata  Aves     Apodiformes  Trochilidae     Amazilia
    ## 4 Animalia Chordata  Aves     Apodiformes  Trochilidae     Amazilia
    ## 5 Animalia Chordata  Aves     Apodiformes  Trochilidae     Amazilia
    ##   specificEpithet taxonomicStatus
    ## 1        collaris        Aceptado
    ## 2       coelestis        Aceptado
    ## 3        amabilis        Aceptado
    ## 4 castaneiventris        Aceptado
    ## 5      cyanifrons        Aceptado
    ## 
    ## $typesandspecimen
    ##                                   id
    ## 1 urn:lsid:ubio.org:namebank:3851488
    ## 2 urn:lsid:ubio.org:namebank:3853053
    ## 3 urn:lsid:ubio.org:namebank:3852923
    ## 4 urn:lsid:ubio.org:namebank:3852937
    ## 5 urn:lsid:ubio.org:namebank:3854768
    ##                                          occurrenceID
    ## 1 IAvH:BIOTA:COLOMBIA:AVES:LE:I2D-BIO_2015_IPT043:001
    ## 2 IAvH:BIOTA:COLOMBIA:AVES:LE:I2D-BIO_2015_IPT043:002
    ## 3 IAvH:BIOTA:COLOMBIA:AVES:LE:I2D-BIO_2015_IPT043:003
    ## 4 IAvH:BIOTA:COLOMBIA:AVES:LE:I2D-BIO_2015_IPT043:004
    ## 5 IAvH:BIOTA:COLOMBIA:AVES:LE:I2D-BIO_2015_IPT043:005
    ## 
    ## $vernacularname
    ##                                   id         vernacularName language
    ## 1 urn:lsid:ubio.org:namebank:3851488         Azor Collarejo       ES
    ## 2 urn:lsid:ubio.org:namebank:3853053          Silfo violeta       ES
    ## 3 urn:lsid:ubio.org:namebank:3852923     Amazilia Pechiazul       ES
    ## 4 urn:lsid:ubio.org:namebank:3852937 Amazilia Ventricastaño       ES
    ## 5 urn:lsid:ubio.org:namebank:3854768        Amazilia Ciáneo       ES

## 1.1 Taxonomic information

The “taxon” file contains all the taxonomic information.

``` r
colnames(data[["taxon"]])
```

    ##  [1] "id"                "taxonID"           "scientificName"   
    ##  [4] "acceptedNameUsage" "nameAccordingTo"   "kingdom"          
    ##  [7] "phylum"            "class"             "order"            
    ## [10] "family"            "genus"             "specificEpithet"  
    ## [13] "taxonomicStatus"

The “scientificName” is actually the “canonicalName” here, and does not
include the authorship for the species.

``` r
data$taxon$scientificName[1:10]
```

    ##  [1] "Accipiter collaris"       "Aglaiocercus coelestis"  
    ##  [3] "Amazilia amabilis"        "Amazilia castaneiventris"
    ##  [5] "Amazilia cyanifrons"      "Amazilia rosenbergi"     
    ##  [7] "Amazilia saucerrottei"    "Anairetes agilis"        
    ##  [9] "Anas andium"              "Andigena nigrirostris"

The taxonomic status of the species is written in spanish:

``` r
table(data[["taxon"]]['taxonomicStatus'])
```

    ## 
    ##          Aceptado Sinónimo 
    ##       20      282        6

In case taxon names are synonyms, the column “acceptedNameUsage” gives
the accepted name of the taxon, in a weird form of a “canonicalName”
(without markers) associated with authorship:

``` r
table(data[["taxon"]]$acceptedNameUsage,data[["taxon"]]$taxonomicStatus)
```

    ##                                                          
    ##                                                               Aceptado Sinónimo
    ##                                                            20      282        0
    ##   Anas flavirostris andium (P. L. Sclater & Salvin, 1873)   0        0        1
    ##   Coeligena bonapartei orina Wetmore, 1953                  0        0        1
    ##   Grallaria fenwickorum Barrera & Bartels, 2010             0        0        1
    ##   Nystactes noanamae (Hellmayr, 1909)                       0        0        1
    ##   Ortalis guttata columbiana Hellmayr, 1906                 0        0        1
    ##   Piculus leucolaemus litae (Rothschild, 1901)              0        0        1

Our most simple way here to get the rank of the taxon is to check which
column contains information:

``` r
taxRankColumns <- c("kingdom","phylum","class","order","family","genus","specificEpithet")
ranksAssociated <- c("KG","PHY","CL","OR","FAM","GN","SP")
ranks <- apply(data[["taxon"]][,taxRankColumns],1,function(x,r)r[max(which(!is.na(x) & x != ""))], r = ranksAssociated)
table(ranks)
```

    ## ranks
    ##  SP 
    ## 308

It appears that all the taxon have a specific epithet. We need now to
check that all scientificName are indeed a genus and a specific epithet.

``` r
regexGnSp <- "^[A-Z][a-z]+ [a-z]+$"
all(grepl(regexGnSp,data[["taxon"]]$scientificName))
```

    ## [1] TRUE

So, indeed all names in scientificName correspond to species.

### 1.1.1 Taxonomic preformatting

``` r
syno <- data$taxon$acceptedNameUsage != "" | data$taxon$taxonomicStatus == "Sinónimo"
pf_taxon <- data.frame(id = data$taxon$id,canonicalname = data$taxon$scientificName,rank="SP",synoscientificname = ifelse(data$taxon$acceptedNameUsage == "", NA, data$taxon$acceptedNameUsage), parentcanonicalname = data$taxon$genus, syno = syno)
head(pf_taxon)
```

    ##                                   id            canonicalname rank
    ## 1 urn:lsid:ubio.org:namebank:3851488       Accipiter collaris   SP
    ## 2 urn:lsid:ubio.org:namebank:3853053   Aglaiocercus coelestis   SP
    ## 3 urn:lsid:ubio.org:namebank:3852923        Amazilia amabilis   SP
    ## 4 urn:lsid:ubio.org:namebank:3852937 Amazilia castaneiventris   SP
    ## 5 urn:lsid:ubio.org:namebank:3854768      Amazilia cyanifrons   SP
    ## 6 urn:lsid:ubio.org:namebank:3852925      Amazilia rosenbergi   SP
    ##   synoscientificname parentcanonicalname  syno
    ## 1               <NA>           Accipiter FALSE
    ## 2               <NA>        Aglaiocercus FALSE
    ## 3               <NA>            Amazilia FALSE
    ## 4               <NA>            Amazilia FALSE
    ## 5               <NA>            Amazilia FALSE
    ## 6               <NA>            Amazilia FALSE

## 1.2 Endemic status, references and comments

In the “description” file, we can find both the endemism status of the
species and the references to cite, in different rows.

``` r
by(data$description,data$description$type,head)
```

    ## data$description$type: 
    ##                                     id description type
    ## 310 urn:lsid:ubio.org:namebank:3853053                 
    ## 314 urn:lsid:ubio.org:namebank:3852925                 
    ## 318 urn:lsid:ubio.org:namebank:3854012                 
    ## 319 urn:lsid:ubio.org:namebank:3852817                 
    ## 321 urn:lsid:ubio.org:namebank:3850601                 
    ## 322 urn:lsid:ubio.org:namebank:3852959                 
    ## ------------------------------------------------------------ 
    ## data$description$type: Distribución
    ##                                   id        description         type
    ## 1 urn:lsid:ubio.org:namebank:3851488      Casi endémica Distribución
    ## 2 urn:lsid:ubio.org:namebank:3853053      Casi endémica Distribución
    ## 3 urn:lsid:ubio.org:namebank:3852923 Especie de interés Distribución
    ## 4 urn:lsid:ubio.org:namebank:3852937           Endémica Distribución
    ## 5 urn:lsid:ubio.org:namebank:3854768           Endémica Distribución
    ## 6 urn:lsid:ubio.org:namebank:3852925      Casi endémica Distribución
    ## ------------------------------------------------------------ 
    ## data$description$type: Literatura
    ##                                     id
    ## 309 urn:lsid:ubio.org:namebank:3851488
    ## 311 urn:lsid:ubio.org:namebank:3852923
    ## 312 urn:lsid:ubio.org:namebank:3852937
    ## 313 urn:lsid:ubio.org:namebank:3854768
    ## 315 urn:lsid:ubio.org:namebank:3854778
    ## 316   urn:lsid:ubio.org:namebank:13220
    ##                                                                                                                                    description
    ## 309                   Arbeláez-Cortés et al. 2011b, Cuervo et al. 2008a, Cuervo et al. 2008b, Merkord 2010, Rodríguez y Rojas-Suárez 2008, 137
    ## 311                                           Corpocaldas 2010, Donegan et al. 2010, Laverde-R. Et al. 2005b, Parra-Hernández et al. 2007, 136
    ## 312                                                                          Chaves-Portilla y Cortés-Herrera 2006, Cortés-Herrera et al. 2004
    ## 313                                             Ayerbe-Quiñones et al. 2008, Losada-Prado et al. 2005a, Peraza et al. 2004, Sáenz-Jimenez 2010
    ## 315                                                        Arbeláez-Cortés et al. 2011b, Donegan et al. 2010, Parra-Hernández et al. 2007, 137
    ## 316 Arbeláez-Cortés et al. 2011b, Ayerbe-Quiñones et al. 2008, Corpocaldas 2010, López-Guzmán y Gómez-Botero 2005, Parra-Hernández et al. 2007
    ##           type
    ## 309 Literatura
    ## 311 Literatura
    ## 312 Literatura
    ## 313 Literatura
    ## 315 Literatura
    ## 316 Literatura

``` r
tabStatus <- data.frame(id = data$description$id[data$description$type == "Distribución"], endemstatus = data$description$description[data$description$type == "Distribución"])
tabRef <- data.frame(id = data$description$id[data$description$type == "Literatura"], rawRef = data$description$description[data$description$type == "Literatura"])
listRef <- strsplit(tabRef$rawRef,", ?")
names(listRef) <- tabRef$id
# There are numbers, that we will supress from the list
listRef <- lapply(listRef,function(x)return(x[!grepl("^[0-9]*$",x)]))
listRef <- listRef[sapply(listRef,length)>0]
listRef[1:5]
```

    ## $`urn:lsid:ubio.org:namebank:3851488`
    ## [1] "Arbeláez-Cortés et al. 2011b"  "Cuervo et al. 2008a"          
    ## [3] "Cuervo et al. 2008b"           "Merkord 2010"                 
    ## [5] "Rodríguez y Rojas-Suárez 2008"
    ## 
    ## $`urn:lsid:ubio.org:namebank:3852923`
    ## [1] "Corpocaldas 2010"            "Donegan et al. 2010"        
    ## [3] "Laverde-R. Et al. 2005b"     "Parra-Hernández et al. 2007"
    ## 
    ## $`urn:lsid:ubio.org:namebank:3852937`
    ## [1] "Chaves-Portilla y Cortés-Herrera 2006"
    ## [2] "Cortés-Herrera et al. 2004"           
    ## 
    ## $`urn:lsid:ubio.org:namebank:3854768`
    ## [1] "Ayerbe-Quiñones et al. 2008" "Losada-Prado et al. 2005a"  
    ## [3] "Peraza et al. 2004"          "Sáenz-Jimenez 2010"         
    ## 
    ## $`urn:lsid:ubio.org:namebank:3854778`
    ## [1] "Arbeláez-Cortés et al. 2011b" "Donegan et al. 2010"         
    ## [3] "Parra-Hernández et al. 2007"

We might use a more complex data schema in the future, but right now we
do not have the specific structures for integrating the information
which is contained in the “distribution” table. For now, what we will do
is to concatenate the information in a “comments” field, which already
exists in the database.

``` r
head(data$distribution)
```

    ##                                   id
    ## 1 urn:lsid:ubio.org:namebank:3851488
    ## 2 urn:lsid:ubio.org:namebank:3853053
    ## 3 urn:lsid:ubio.org:namebank:3852923
    ## 4 urn:lsid:ubio.org:namebank:3852937
    ## 5 urn:lsid:ubio.org:namebank:3854768
    ## 6 urn:lsid:ubio.org:namebank:3852925
    ##                                                                                                                                                                   locality
    ## 1 Venezuela: Andes venezolanos | Ecuador: Los Andes | Vertiente oriental hacia Amazonía | Perú: Amazonas (desde divisoria de aguas y principales drenajes al río Amazonas)
    ## 2                                                                                                                                  Ecuador: Vertiente pacífica del Ecuador
    ## 3                                                                                                                                  Ecuador: Vertiente pacífica del Ecuador
    ## 4                                                                                                                                                                         
    ## 5                                                                                                                                                                         
    ## 6                                                                                                                                  Ecuador: Vertiente pacífica del Ecuador
    ##                  countryCode
    ## 1        VE:00; PE:00; EC:00
    ## 2                      EC:00
    ## 3 EC:00; PA:00; NI:00; CR:00
    ## 4                           
    ## 5                           
    ## 6                      EC:00
    ##                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             occurrenceRemarks
    ## 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el Golfo de Urabá hasta la Península de La Guajira, incluyendo las estribaciones de la Sierra Nevada de Santa Marta y la Serranía de Perijá en el norte de Cesar, y como subregión |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas más al norte de la cordillera Occidental y de la cordillera Central y la ladera nororiental de la Central hacia el sur hasta aproximadamente el límite sur de Caldas |Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. cordillera Central
    ## 2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Andén del Pacífico, desde la zona media del Darién en límites con Panamá, al lado izquierdo del bajo río Atrato, hasta el Ecuador |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Vertiente occidental de la cordillera Occidental que incluye
    ## 3 Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Región más húmeda inmediatamente al sur de la región 1, desde el bajo río Atrato hasta la parte media del valle del río Magdalena, incluyendo el alto río Sinú y alto río Nechí |Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Andén del Pacífico, desde la zona media del Darién en límites con Panamá, al lado izquierdo del bajo río Atrato, hasta el Ecuador |Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Alto valle del río Magdalena, principalmente en Tolima y Huila |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas más al norte de la cordillera Occidental y de la cordillera Central y la ladera nororiental de la Central hacia el sur hasta aproximadamente el límite sur de Caldas |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas del alto valle del río Magdalena principalmente en Tolima y Huila |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Vertiente occidental de la cordillera Oriental, desde el sur de Cesar hasta Cundinamarca
    ## 4                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       Franja y región: Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Vertiente occidental de la cordillera Oriental, desde el sur de Cesar hasta Cundinamarca
    ## 5                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              Franja y región: Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Vertiente occidental de la cordillera Oriental, desde el sur de Cesar hasta Cundinamarca |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas del Valle del Cauca
    ## 6                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m. Andén del Pacífico, desde la zona media del Darién en límites con Panamá, al lado izquierdo del bajo río Atrato, hasta el Ecuador

``` r
commentLocality <- paste("locality:", data$distribution$locality)
tabComments <- data.frame(id = data$distribution$id,
                          comments = paste0(
                            ifelse(data$distribution$locality != "",paste("locality:",data$distribution$locality,"| "),""),
                            ifelse(data$distribution$occurrenceRemarks != "", paste("occurrenceRemarks:",data$distribution$occurrenceRemarks,"| "),"")
                          ))
```

## 1.3 Final preformatting

The goal here is to associate the taxonomic information, the endemic
status, the references, and the comments in lists that may be directly
transformed to json in order to send them to the API post method.

``` r
# First we prepare the global reference and link for the dataset, to add in each taxon
baseRef <- list(
  ref_citation = list("Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue"),
  link = list("http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09")
  )
masterList <- list()
for(i in 1:nrow(pf_taxon))
{
  id <- pf_taxon[i,"id"]
  masterList[[i]] <- as.list(pf_taxon[i,colnames(pf_taxon) != "id" & !is.na(pf_taxon[i,])])
  masterList[[i]] <- append(masterList[[i]],list(endemstatus = tabStatus[tabStatus$id==id,"endemstatus"]))
  masterList[[i]] <- append(masterList[[i]],baseRef)
  # Then we add the potential references already preformatted for this taxon
  if(id %in% names(listRef))
  {
    masterList[[i]]$ref_citation <- append(masterList[[i]]$ref_citation,listRef[[id]])
    masterList[[i]]$link <- append(masterList[[i]]$link,as.list(rep(" ",length(listRef[[id]]))))
  }
  masterList[[i]]$comments<-tabComments$comments[tabComments$id == id]
}
```

# 2 Basic usage : example of one only species

If we take the first example of the list that we formatted on the
previous part of the document, we obtain:

``` r
masterList[[1]]
```

    ## $canonicalname
    ## [1] "Accipiter collaris"
    ## 
    ## $rank
    ## [1] "SP"
    ## 
    ## $parentcanonicalname
    ## [1] "Accipiter"
    ## 
    ## $syno
    ## [1] FALSE
    ## 
    ## $endemstatus
    ## [1] "Casi endémica"
    ## 
    ## $ref_citation
    ## $ref_citation[[1]]
    ## [1] "Chaparro-Herrera, S., Echeverry-Galvis, M.A., Córdoba-Córdoba, S., Sua-Becerra, A. (2013). Listado actualizado de las aves endémicas y casi-endémicas de Colombia. 308 registros. Versión 5.1. http://doi.org/10.15472/tozuue"
    ## 
    ## $ref_citation[[2]]
    ## [1] "Arbeláez-Cortés et al. 2011b"
    ## 
    ## $ref_citation[[3]]
    ## [1] "Cuervo et al. 2008a"
    ## 
    ## $ref_citation[[4]]
    ## [1] "Cuervo et al. 2008b"
    ## 
    ## $ref_citation[[5]]
    ## [1] "Merkord 2010"
    ## 
    ## $ref_citation[[6]]
    ## [1] "Rodríguez y Rojas-Suárez 2008"
    ## 
    ## 
    ## $link
    ## $link[[1]]
    ## [1] "http://i2d.humboldt.org.co/ceiba/resource.do?r=biota_v14_n2_09"
    ## 
    ## $link[[2]]
    ## [1] " "
    ## 
    ## $link[[3]]
    ## [1] " "
    ## 
    ## $link[[4]]
    ## [1] " "
    ## 
    ## $link[[5]]
    ## [1] " "
    ## 
    ## $link[[6]]
    ## [1] " "
    ## 
    ## 
    ## $comments
    ## [1] "locality: Venezuela: Andes venezolanos | Ecuador: Los Andes | Vertiente oriental hacia Amazonía | Perú: Amazonas (desde divisoria de aguas y principales drenajes al río Amazonas) | occurrenceRemarks: Franja y región: Tierras bajas para especies cuyos límites superiores de distribución están alrededor de 1000-1200 m s.n.m.Zona Caribe norte, aproximadamente desde el Golfo de Urabá hasta la Península de La Guajira, incluyendo las estribaciones de la Sierra Nevada de Santa Marta y la Serranía de Perijá en el norte de Cesar, y como subregión |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Sierra Nevada de Santa Marta |Elevaciones medias para especies que se distribuyen entre ca. 800-l000 y 2000-2400 m s.n.m. Laderas más al norte de la cordillera Occidental y de la cordillera Central y la ladera nororiental de la Central hacia el sur hasta aproximadamente el límite sur de Caldas |Elevaciones altas, para especies cuyos límites inferiores caen por encima de ca. 2000 m s.n.m. cordillera Central | "

As you can see, the list is already formatted with the specifications of
the API:

in order to send the status to the database, we use a json “dictionary”
with the following elements:

-   the identification of the species, with either:
    -   *gbifkey* : integer corresponding to the taxonKey used in GBIF
    -   *scientificname* : string corresponding to the scientificName in
        the GBIF backbone
    -   *canonicalname* : string corresponding to the canonicalName in
        the GBIF backbone (formally, it is better to use the
        canonicalNameWithMarker) used by the name parser of the GBIF
        backbone)
    -   *rank*: taxonomic rank of the taxon
    -   *syno*: boolean describing whether the name is a synonym to an
        accepted taxon
    -   *parentgbifkey*, *parentcanonicalname* and
        *parentscientificname*: equivalent of the identification of the
        taxon, for the parent taxon
    -   *synogbifkey*, *synocanonicalname* and *synoscientificname*:
        equivalent of the identification of the taxon, for the accepted
        taxon in case the name sent is a synonym
-   *endemstatus* : the endemism level
-   *ref_citation* : a list of the references on which are based the
    inclusion of the taxon and its endemism status in the API
-   *link* : a list of the url links (corresponding in length and order
    to the *ref_citation*)
-   *comments* : comment on the endemism status of the taxon

## 2.1 In R

``` r
require(httr)
```

    ## Loading required package: httr

``` r
require(jsonify)
```

    ## Loading required package: jsonify

``` r
sendJson <- to_json(masterList[[1]],unbox=T)
baseURL <- 'http://localhost:5000'
baseResource <- "insertEndem"
POST('http://localhost:5000/insertEndem',body=sendJson, content_type("application/json"),verbose())
```

    ## Response [http://localhost:5000/insertEndem]
    ##   Date: 2022-03-14 01:33
    ##   Status: 200
    ##   Content-Type: application/json
    ##   Size: 53 B
    ## {"cd_tax": 1281, "cdRefs": [91, 92, 93, 94, 95, 96]}

Now we do it for all the list:

``` r
res = list()
for(i in 1:length(masterList))
{
  res[[i]] <- POST(paste(baseURL,baseResource,sep="/"),body=to_json(masterList[[i]],unbox=T), content_type("application/json"))
}
```

# 3 Problems

``` r
pbs <- !sapply(res,function(x)"cd_tax"%in%names(content(x)))
```

    ## Registered S3 method overwritten by 'jsonlite':
    ##   method     from   
    ##   print.json jsonify

``` r
any(pbs)
```

    ## [1] FALSE

No problem found!
