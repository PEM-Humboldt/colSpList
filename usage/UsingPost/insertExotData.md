Inserting exotic and invasive species with the colSpList API
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

The API is running on a heroku server which may be used with the
following parameters:

``` r
baseURL <- 'http://colsplist.herokuapp.com'
```

However, in order to present the API, I will use the API running locally
in my computer (and a local database) using `heroku local`.

``` r
baseURL <- 'http://localhost:5000'
baseResource <- "insertExot"
```

# 1 Flora exotica

One of the datasets concerns exotic species in Colombia and is focused
in flora, it is the reference: Instituto de Investigación de Recursos
Biológicos Alexander von Humboldt (2020). Base de datos de información
ecológica e invasividad de especies exóticas prioritarias de flora y
fauna de Colombia. 43 registros. (publicly available at
<http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020>)

## 1.1 Preformatting the dataset

The dataset downloaded from GBIF includes various files, that we need to
preformat (here in R), in order to extract the information that we may
send to the API and its database:

``` r
directory = "../../data/dwca-lista_colombia_exoticas_2020/"
(files = dir(directory))
```

    ## [1] "eml.xml"               "identifier.txt"        "measurementorfact.txt"
    ## [4] "meta.xml"              "taxon.txt"

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

    ## $identifier
    ##                                     id
    ## 1 https://www.gbif.org/species/2979778
    ## 2 https://www.gbif.org/species/2295966
    ## 3 https://www.gbif.org/species/2705975
    ## 4 https://www.gbif.org/species/2703041
    ## 5 https://www.gbif.org/species/2650107
    ##                                                       identifier
    ## 1 IAvH:CBB:COLOMBIA:ANIMALIAPLANTAE-EXOTICAS:I2D-BIO_2020_007:01
    ## 2 IAvH:CBB:COLOMBIA:ANIMALIAPLANTAE-EXOTICAS:I2D-BIO_2020_007:02
    ## 3 IAvH:CBB:COLOMBIA:ANIMALIAPLANTAE-EXOTICAS:I2D-BIO_2020_007:03
    ## 4 IAvH:CBB:COLOMBIA:ANIMALIAPLANTAE-EXOTICAS:I2D-BIO_2020_007:04
    ## 5 IAvH:CBB:COLOMBIA:ANIMALIAPLANTAE-EXOTICAS:I2D-BIO_2020_007:05
    ## 
    ## $measurementorfact
    ##                                     id     measurementType
    ## 1 https://www.gbif.org/species/2979778 Distribución nativa
    ## 2 https://www.gbif.org/species/2295966 Distribución nativa
    ## 3 https://www.gbif.org/species/2705975 Distribución nativa
    ## 4 https://www.gbif.org/species/2703041 Distribución nativa
    ## 5 https://www.gbif.org/species/2650107 Distribución nativa
    ##                                      measurementValue measurementUnit
    ## 1                         ARG | AUS | NZL | URY | ZAF                
    ## 2                                     ETH | KEN | TZA                
    ## 3 BEL | CHN | ESP | FRA | GRB | GRC | IRN | PRT | RUS                
    ## 4 AFG | CHN | IDN | IND | IRN | IRQ | JPN | KHM | NPL                
    ## 5                                        Criptogénica                
    ##   measurementRemarks
    ## 1                   
    ## 2                   
    ## 3                   
    ## 4                   
    ## 5                   
    ## 
    ## $taxon
    ##                                     id                              taxonID
    ## 1 https://www.gbif.org/species/2979778 https://www.gbif.org/species/2979778
    ## 2 https://www.gbif.org/species/2295966 https://www.gbif.org/species/2295966
    ## 3 https://www.gbif.org/species/2705975 https://www.gbif.org/species/2705975
    ## 4 https://www.gbif.org/species/2703041 https://www.gbif.org/species/2703041
    ## 5 https://www.gbif.org/species/2650107 https://www.gbif.org/species/2650107
    ##          scientificName  kingdom        phylum         class           order
    ## 1      Acacia decurrens  Plantae Magnoliophyta Magnoliopsida         Fabales
    ## 2       Achatina fulica Animalia      Mollusca    Gastropoda Stylommatophora
    ## 3 Anthoxanthum odoratum  Plantae Magnoliophyta    Liliopsida       Cyperales
    ## 4          Arundo donax  Plantae Magnoliophyta    Liliopsida       Cyperales
    ## 5   Azolla filiculoides  Plantae  Pteridophyta   Filicopsida     Salviniales
    ##         family        genus specificEpithet taxonRank scientificNameAuthorship
    ## 1     Fabaceae       Acacia       decurrens   Especie                   Willd.
    ## 2  Achatinidae     Achatina          fulica   Especie            Bowdich, 1822
    ## 3      Poaceae Anthoxanthum        odoratum   Especie                       L.
    ## 4      Poaceae       Arundo           donax   Especie                       L.
    ## 5 Salviniaceae       Azolla    filiculoides   Especie                     Lam.
    ##                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     references
    ## 1                                                                                                                                                                             Cárdenas D., Baptiste M.P., Castaño N. (2017). Plantas exóticas con alto potencial de invasión en Colombia. Instituto de Investigación de Recursos Biológicos Alexander von Humboldt. Bogotá, D. C., Colombia. 295 p. | Mora, M. F., Rubio J., Ocampo R. & Barrera J.I. (2015). Catálogo de especies invasoras del territorio CAR. Publicado por Pontificia Universidad Javeriana & Corporación Autónoma Regional de Cundinamarca – CAR, 238 pp.
    ## 2 Corporación Autónoma Regional (2018). Plan de Prevención, Control y Manejo (PPCM) de Caracol Gigante Africano (Achatina fulica) en la jurisdicción CAR. Dirección de Recursos Naturales. 61 pp. Disponible en: https://www.car.gov.co/uploads/files/5b9033f095d34.pdf | Invasive Species Specialist Group (2020). Achatina fulica. Disponible en: http://www.iucngisd.org/gisd/speciesname/Achatina+fulica | Garcés M., Patiño A., Gómez M., Giraldo A. & Bolívar G. (2016). Sustancias alternativas para el control del caracol africano (Achatina fulica) en el Valle del Cauca. Biota Colombiana. Vol. 17(1), 44 - 52 pp.
    ## 3                                                                                                                                                                                                                                                              Cárdenas D., Baptiste M.P., Castaño N. (2017). Plantas exóticas con alto potencial de invasión en Colombia. Instituto de Investigación de Recursos Biológicos Alexander von Humboldt. Bogotá, D. C., Colombia. 295 p. | Invasive Species Compendium (2019). Anthoxanthum odoratum (sweet vernal grass). Consultado en: https://www.cabi.org/isc/datasheet/93023
    ## 4                                                                                                                                                                                                                                                                                Cárdenas D., Baptiste M.P., Castaño N. (2017). Plantas exóticas con alto potencial de invasión en Colombia. Instituto de Investigación de Recursos Biológicos Alexander von Humboldt. Bogotá, D. C., Colombia. 295 p. | Invasive Species Compendium (2019). Arundo donax (giant reed). Consultado en: https://www.cabi.org/isc/datasheet/1940
    ## 5                                                                                                                                                                                                                                                                         Cárdenas D., Baptiste M.P., Castaño N. (2017). Plantas exóticas con alto potencial de invasión en Colombia. Instituto de Investigación de Recursos Biológicos Alexander von Humboldt. Bogotá, D. C., Colombia. 295 p. | Invasive Species Compendium (2019). Azolla filiculoides (water fern). Consultado en: https://www.cabi.org/isc/datasheet/8119

#### 1.1.0.1 Taxonomic information

The “taxon” file contains all the taxonomic information.

``` r
colnames(data[["taxon"]])
```

    ##  [1] "id"                       "taxonID"                 
    ##  [3] "scientificName"           "kingdom"                 
    ##  [5] "phylum"                   "class"                   
    ##  [7] "order"                    "family"                  
    ##  [9] "genus"                    "specificEpithet"         
    ## [11] "taxonRank"                "scientificNameAuthorship"
    ## [13] "references"

The “scientificName” is in fact a canonicalname

``` r
data$taxon$scientificName[1:10]
```

    ##  [1] "Acacia decurrens"      "Achatina fulica"       "Anthoxanthum odoratum"
    ##  [4] "Arundo donax"          "Azolla filiculoides"   "Bambusa vulgaris"     
    ##  [7] "Calotropis procera"    "Cenchrus clandestinus" "Cenchrus purpureus"   
    ## [10] "Columba livia"

However, associated with the field scientificNameAuthorship, we may
retrieve the scientificName.

``` r
data$taxon$scientificNameAuthorship[1:10]
```

    ##  [1] "Willd."                      "Bowdich, 1822"              
    ##  [3] "L."                          "L."                         
    ##  [5] "Lam."                        "Schrad. ex J.C. Wendl"      
    ##  [7] "(Ait.) Ait. f."              "(Hochst. ex Chiov.) Morrone"
    ##  [9] "(Schumach.) Morrone"         "Gmelin, 1789"

There is no information about the taxonomic status of the species, and
no infornation concerning the potential synonyms.

Our most simple way here to get the rank of the taxon is the column
“taxonRank”, even though 3 taxa do not have anything in this column.

``` r
ranks <- data$taxon$taxonRank
table(ranks)
```

    ## ranks
    ## Especie 
    ##      45

So all the taxa here are species, so the parents are extracted through
the genus field

``` r
parentCano <- data$taxon$genus
```

The gbifkey of the taxa may be found by:

``` r
gbifkey = rep(NA,nrow(data$taxon))
regexGbif <- "^https://www\\.gbif\\.org/species/([0-9]+)$"
grepl(data$taxon$id,pattern=regexGbif)
```

    ##  [1] TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE
    ## [16] TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE
    ## [31] TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE

``` r
gbifkey[grepl(data$taxon$id,pattern=regexGbif)] <- sub(regexGbif,"\\1",data$taxon$id)
```

###### 1.1.0.1.0.1 Taxonomic preformatting

``` r
pf_taxon <- data.frame(id = data$taxon$id, gbifkey = gbifkey, scientificname = paste(data$taxon$scientificName, data$taxon$scientificNameAuthorship,sep=" "), canonicalname=data$taxon$scientificName, rank = "SP", parentcanonicalname = parentCano)
head(pf_taxon)
```

    ##                                     id gbifkey
    ## 1 https://www.gbif.org/species/2979778 2979778
    ## 2 https://www.gbif.org/species/2295966 2295966
    ## 3 https://www.gbif.org/species/2705975 2705975
    ## 4 https://www.gbif.org/species/2703041 2703041
    ## 5 https://www.gbif.org/species/2650107 2650107
    ## 6 https://www.gbif.org/species/7661971 7661971
    ##                           scientificname         canonicalname rank
    ## 1                Acacia decurrens Willd.      Acacia decurrens   SP
    ## 2          Achatina fulica Bowdich, 1822       Achatina fulica   SP
    ## 3               Anthoxanthum odoratum L. Anthoxanthum odoratum   SP
    ## 4                        Arundo donax L.          Arundo donax   SP
    ## 5               Azolla filiculoides Lam.   Azolla filiculoides   SP
    ## 6 Bambusa vulgaris Schrad. ex J.C. Wendl      Bambusa vulgaris   SP
    ##   parentcanonicalname
    ## 1              Acacia
    ## 2            Achatina
    ## 3        Anthoxanthum
    ## 4              Arundo
    ## 5              Azolla
    ## 6             Bambusa

#### 1.1.0.2 Exotic status, Invasive status, occurrence status, references and comments

There are many information in this dataset, organized as repetitions of
rows:

``` r
table(data$measurementorfact$measurementType)
```

    ## 
    ##                              Altitud máxima 
    ##                                          45 
    ##                              Altitud mínima 
    ##                                          45 
    ##                         Asociación invasiva 
    ##                                          45 
    ##           Aspectos generales de invasividad 
    ##                                          45 
    ##                      Causas de introducción 
    ##                                          45 
    ##                   Distribución como exótica 
    ##                                          45 
    ##                         Distribución nativa 
    ##                                          45 
    ##                                     Estatus 
    ##                                          45 
    ## Factores limitantes para el establecimiento 
    ##                                          45 
    ##                                      Hábito 
    ##                                          45 
    ##                    Impactos de introducción 
    ##                                          45 
    ##                Introducida después de (año) 
    ##                                          45 
    ##                 Medidas de manejo y control 
    ##                                          45 
    ##                 Observaciones de ocurrencia 
    ##                                          45 
    ##                                          pH 
    ##                                          45 
    ##                        Precipitación máxima 
    ##                                          45 
    ##                        Precipitación mínima 
    ##                                          45 
    ##                  Puntaje-Riesgo de Invasión 
    ##                                          45 
    ##                          Riesgo de invasión 
    ##                                          45 
    ##                          Temperatura máxima 
    ##                                          45 
    ##                          Temperatura mínima 
    ##                                          45 
    ##                          Tipo de dispersión 
    ##                                          45 
    ##                        Tipo de introducción 
    ##                                          45 
    ##                        Tipo de reproducción 
    ##                                          45 
    ##                               Tipo de suelo 
    ##                                          45 
    ##                        Vías de introducción 
    ##                                          45

In order to see it clearer, we will reorganize the table:

``` r
sepTab <- by(INDICES = data$measurementorfact$measurementType,data = data$measurementorfact,function(x){
  tabRes <- x[c("measurementValue","measurementUnit","measurementRemarks")]
  rownames(tabRes) <- x$id
  measurement <- gsub("[- ]","_",unique(x$measurementType))
  colnames(tabRes)[1] <- measurement
  colnames(tabRes) <- gsub("measurement",paste0(measurement,"_"),colnames(tabRes))
  tabRes[which(tabRes=="",arr.ind=T)]<-NA
  #tabRes<-tabRes[,apply(tabRes,2,function(x)!all(is.na(x)|x==""))]
  return(tabRes)
})
reorganized <- Reduce(cbind,sepTab)
reorganized <- reorganized[!apply(reorganized,2,function(x)all(is.na(x)))]
```

Now, we have much data to put into the comment field of the database, I
will paste it all into the comments field, but we might want to filter
later…

``` r
colnames(reorganized)
```

    ##  [1] "Altitud_máxima"                             
    ##  [2] "Altitud_máxima_Unit"                        
    ##  [3] "Altitud_mínima"                             
    ##  [4] "Altitud_mínima_Unit"                        
    ##  [5] "Asociación_invasiva"                        
    ##  [6] "Aspectos_generales_de_invasividad"          
    ##  [7] "Causas_de_introducción"                     
    ##  [8] "Distribución_como_exótica"                  
    ##  [9] "Distribución_nativa"                        
    ## [10] "Estatus"                                    
    ## [11] "Factores_limitantes_para_el_establecimiento"
    ## [12] "Hábito"                                     
    ## [13] "Impactos_de_introducción"                   
    ## [14] "Introducida_después_de_(año)"               
    ## [15] "Medidas_de_manejo_y_control"                
    ## [16] "Observaciones_de_ocurrencia"                
    ## [17] "pH"                                         
    ## [18] "Precipitación_máxima"                       
    ## [19] "Precipitación_máxima_Unit"                  
    ## [20] "Precipitación_mínima"                       
    ## [21] "Precipitación_mínima_Unit"                  
    ## [22] "Puntaje_Riesgo_de_Invasión"                 
    ## [23] "Puntaje_Riesgo_de_Invasión_Remarks"         
    ## [24] "Riesgo_de_invasión"                         
    ## [25] "Temperatura_máxima"                         
    ## [26] "Temperatura_máxima_Unit"                    
    ## [27] "Temperatura_mínima"                         
    ## [28] "Temperatura_mínima_Unit"                    
    ## [29] "Tipo_de_dispersión"                         
    ## [30] "Tipo_de_introducción"                       
    ## [31] "Tipo_de_reproducción"                       
    ## [32] "Tipo_de_suelo"                              
    ## [33] "Vías_de_introducción"

When we read the “Impactos de introduction” column, it appears that all
species have a negative impact, I will then put them all as “invasive”.

Concerning their alien status, there are some that are not:

``` r
table(reorganized$Estatus)
```

    ## 
    ##               Exótica Exótica | Translocada     Nativa | Invasora 
    ##                    40                     2                     2 
    ##  Nativa | Translocada 
    ##                     1

``` r
df_status <- data.frame(id=rownames(reorganized),is_alien=!grepl("Nativa",reorganized$Estatus),is_invasive = T, occ_observed = T, cryptogenic =F )
```

``` r
reorganized$Distribución_como_exótica <- gsub("\\|",",",reorganized$Distribución_como_exótica)
reorganized$Distribución_nativa <- gsub("\\|",",",reorganized$Distribución_nativa)
df_status$comments<-apply(reorganized,1,function(x,title)paste(title,x,sep=": ",collapse=" | "),title=gsub("_"," ",colnames(reorganized)))
```

Concerning the references, there are in the taxon table.

First we separate the references:

``` r
listReferences <- strsplit(data$taxon$references," \\| ")
names(listReferences)<-data$taxon$id
```

Then we extract the links from the references

``` r
regex <- "^(.*) ((Consultado en)|(Disponible en))? ?: ?(http.*) *$"
listLinks<-lapply(listReferences,function(vec,r)
  {
    #grepl(r,vec)
    ifelse(grepl(r,vec),sub(r,"\\5",vec)," ")
  },r = regex)
listref_citation <- lapply(listReferences,function(vec,r){   
  ifelse(grepl(r,vec),sub(r,"\\1",vec),vec)
  },r = regex)
```

#### 1.1.0.3 Final preformatting

The goal here is to associate the taxonomic information, the exotic
statuses, the references, and the comments in lists that may be directly
transformed to json in order to send them to the API post method.

``` r
## First we prepare the global reference and link for the dataset, to add in each taxon
baseRef <- list(
  ref_citation = list(" Instituto de Investigación de Recursos Biológicos Alexander von Humboldt (2020). Base de datos de información ecológica e invasividad de especies exóticas prioritarias de flora y fauna de Colombia. 43 registros."),
  link = list("http://i2d.humboldt.org.co/ceiba/resource.do?r=lista_colombia_exoticas_2020")
  )
masterList <- list()
for(i in 1:nrow(pf_taxon))
{
  id <- pf_taxon[i,"id"]
  masterList[[i]] <- as.list(pf_taxon[i,colnames(pf_taxon) != "id" & !is.na(pf_taxon[i,])])
  masterList[[i]] <- append(masterList[[i]],as.list(df_status[df_status$id==id,colnames(df_status)!="id"]))
  masterList[[i]] <- append(masterList[[i]],baseRef)
  masterList[[i]]$ref_citation <-append(masterList[[i]]$ref_citation,listref_citation[[id]])
  masterList[[i]]$link <-append(masterList[[i]]$link,listLinks[[id]])
  ## Then we add the potential references already preformatted for this taxon
}
```

Now we insert all the list:

``` r
require(httr)
```

    ## Loading required package: httr

``` r
require(jsonify)
```

    ## Loading required package: jsonify

``` r
res = list()
for(i in 1:length(masterList))
{
  res[[i]] <- POST(paste(baseURL,baseResource,sep="/"),body=to_json(masterList[[i]],unbox=T), content_type("application/json"))
}
```

# 2 GRIIS

The most important dataset for exotic species is the species list from
the GRIIS (publicly available as a gbif dataset at
<https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91>)

## 2.1 Preformatting the dataset

The dataset downloaded from GBIF includes various files, that we need to
preformat (here in R), in order to extract the information that we may
send to the API and its database:

``` r
directory = "../../data/dwca-griis-colombia-v1.5/"
(files = dir(directory))
```

    ## [1] "distribution.txt"   "eml.xml"            "meta.xml"          
    ## [4] "speciesprofile.txt" "taxon.txt"

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

    ## $distribution
    ##      id countryCode occurrenceStatus establishmentMeans
    ## 1 31099          CO          Present              Alien
    ## 2 31100          CO          Present              Alien
    ## 3 31101          CO          Present              Alien
    ## 4 31102          CO          Present              Alien
    ## 5 31103          CO          Present              Alien
    ## 
    ## $speciesprofile
    ##      id isInvasive     habitat
    ## 1 31099       Null Terrestrial
    ## 2 31100   Invasive Terrestrial
    ## 3 31101       Null Terrestrial
    ## 4 31102       Null Terrestrial
    ## 5 31103       Null Terrestrial
    ## 
    ## $taxon
    ##      id taxonID                     scientificName
    ## 1 31099   31099       Acacia caven (Molina) Molina
    ## 2 31100   31100            Acacia decurrens Willd.
    ## 3 31101   31101      Acacia farnesiana (L.) Willd.
    ## 4 31102   31102 Acacia longifolia (Andrews) Willd.
    ## 5 31103   31103              Acacia mangium Willd.
    ##                            acceptedNameUsage kingdom       phylum         class
    ## 1 Vachellia caven (Molina) Seigler & Ebinger Plantae Tracheophyta Magnoliopsida
    ## 2                                            Plantae Tracheophyta Magnoliopsida
    ## 3     Vachellia farnesiana (L.) Wight & Arn. Plantae Tracheophyta Magnoliopsida
    ## 4                                            Plantae Tracheophyta Magnoliopsida
    ## 5                                            Plantae Tracheophyta Magnoliopsida
    ##     order   family taxonRank taxonomicStatus
    ## 1 Fabales Fabaceae   SPECIES         SYNONYM
    ## 2 Fabales Fabaceae   SPECIES        ACCEPTED
    ## 3 Fabales Fabaceae   SPECIES         SYNONYM
    ## 4 Fabales Fabaceae   SPECIES        ACCEPTED
    ## 5 Fabales Fabaceae   SPECIES        ACCEPTED

#### 2.1.0.1 Taxonomic information

The “taxon” file contains all the taxonomic information.

``` r
colnames(data[["taxon"]])
```

    ##  [1] "id"                "taxonID"           "scientificName"   
    ##  [4] "acceptedNameUsage" "kingdom"           "phylum"           
    ##  [7] "class"             "order"             "family"           
    ## [10] "taxonRank"         "taxonomicStatus"

The “scientificName” is well formatted, with the taxon names and the
authorship.

``` r
data$taxon$scientificName[1:10]
```

    ##  [1] "Acacia caven (Molina) Molina"       "Acacia decurrens Willd."           
    ##  [3] "Acacia farnesiana (L.) Willd."      "Acacia longifolia (Andrews) Willd."
    ##  [5] "Acacia mangium Willd."              "Acacia melanoxylon R.Br."          
    ##  [7] "Acalypha amentacea Roxb."           "Acalypha hispida Burm.f."          
    ##  [9] "Acalypha wilkesiana MÃ¼ll.Arg."     "Achatina fulica (Férussac, 1821)"

The taxonomic status of the species is written as specified in the
classical DarwinCore format of GBIF:

``` r
table(data[["taxon"]]['taxonomicStatus'])
```

    ## 
    ##          ACCEPTED DOUBTFUL  SYNONYM 
    ##        6      481        2       20

In case taxon names are synonyms, the column “acceptedNameUsage” gives
the accepted name of the taxon, in the form of a classical
“scientificName”, but we may see here that, sometimes the
taxonomicStatus does not mention “SYNONYM” even though there is an
“acceptedNameUsage”.

``` r
table(data[["taxon"]]$acceptedNameUsage,data[["taxon"]]$taxonomicStatus)
```

    ##                                                    
    ##                                                         ACCEPTED DOUBTFUL
    ##                                                       3      481        2
    ##   Agave vivipara L.                                   0        0        0
    ##   Brachiaria eminii (Mez) Robyns                      0        0        0
    ##   Celosia cristata L.                                 0        0        0
    ##   Cenchrus clandestinus (Hochst. ex Chiov.) Morrone   0        0        0
    ##   Cenchrus polystachios (L.) Morrone                  0        0        0
    ##   Chaetoceros rostratus Lauder                        0        0        0
    ##   Cnidoscolus aconitifolius I.M.Johnst.               0        0        0
    ##   Cornu aspersum (O.F.Müller, 1774)                   0        0        0
    ##   Eclipta prostrata                                   1        0        0
    ##   Erigeron canadensis L.                              0        0        0
    ##   Erythrura gouldiae (Gould, 1844)                    0        0        0
    ##   Eugenia uniflora                                    1        0        0
    ##   Helostoma temminckii Cuvier, 1829                   0        0        0
    ##   Lissachatina fulica (Férussac, 1821)                0        0        0
    ##   Lysimachia arvensis (L.) U.Manns & Anderb.          0        0        0
    ##   Newcastle disease virus                             1        0        0
    ##   Paratrechina pubens (Forel, 1893)                   0        0        0
    ##   Passiflora mollissima L.H.Bailey                    0        0        0
    ##   Pityrogramma tartarea (Cav.) Maxon                  0        0        0
    ##   Pseuderanthemum reticulatum Radlk.                  0        0        0
    ##   Sinapis arvensis L.                                 0        0        0
    ##   Vachellia caven (Molina) Seigler & Ebinger          0        0        0
    ##   Vachellia farnesiana (L.) Wight & Arn.              0        0        0
    ##                                                    
    ##                                                     SYNONYM
    ##                                                           0
    ##   Agave vivipara L.                                       1
    ##   Brachiaria eminii (Mez) Robyns                          1
    ##   Celosia cristata L.                                     1
    ##   Cenchrus clandestinus (Hochst. ex Chiov.) Morrone       1
    ##   Cenchrus polystachios (L.) Morrone                      1
    ##   Chaetoceros rostratus Lauder                            1
    ##   Cnidoscolus aconitifolius I.M.Johnst.                   1
    ##   Cornu aspersum (O.F.Müller, 1774)                       1
    ##   Eclipta prostrata                                       0
    ##   Erigeron canadensis L.                                  1
    ##   Erythrura gouldiae (Gould, 1844)                        1
    ##   Eugenia uniflora                                        0
    ##   Helostoma temminckii Cuvier, 1829                       1
    ##   Lissachatina fulica (Férussac, 1821)                    1
    ##   Lysimachia arvensis (L.) U.Manns & Anderb.              1
    ##   Newcastle disease virus                                 0
    ##   Paratrechina pubens (Forel, 1893)                       1
    ##   Passiflora mollissima L.H.Bailey                        1
    ##   Pityrogramma tartarea (Cav.) Maxon                      1
    ##   Pseuderanthemum reticulatum Radlk.                      1
    ##   Sinapis arvensis L.                                     1
    ##   Vachellia caven (Molina) Seigler & Ebinger              1
    ##   Vachellia farnesiana (L.) Wight & Arn.                  1

Our most simple way here to get the rank of the taxon is the column
“taxonRank”, even though 3 taxa do not have anything in this column.

``` r
ranks <- data$taxon$taxonRank
table(ranks)
```

    ## ranks
    ##               SPECIES SUBSPECIES    VARIETY 
    ##          3        497          3          6

``` r
ranks[ranks == ""] <- NA
```

In order to find the parents, we need to associate the taxonomic columns
and the ranks of the taxa.

``` r
parentCano <- rep(NA,nrow(data$taxon))
parentCano[data$taxon$taxonRank == "SPECIES"] <- gsub("^([A-Z][a-z]+) .+$","\\1",data$taxon$scientificName[data$taxon$taxonRank == "SPECIES"])
parentCano[data$taxon$taxonRank %in% c("SUBSPECIES","VARIETY")] <- gsub("^([A-Z][a-z]+ [a-z]+) .+$","\\1",data$taxon$scientificName[data$taxon$taxonRank %in% c("SUBSPECIES","VARIETY")])
```

###### 2.1.0.1.0.1 Taxonomic preformatting

``` r
syno <- data$taxon$acceptedNameUsage != "" | data$taxon$taxonomicStatus == "SYNONYM"
pf_taxon <- data.frame(id = data$taxon$id,scientificname = data$taxon$scientificName,rank=ranks,synoscientificname = ifelse(data$taxon$acceptedNameUsage == "", NA, data$taxon$acceptedNameUsage), parentcanonicalname = parentCano, syno = syno)
head(pf_taxon)
```

    ##      id                     scientificname    rank
    ## 1 31099       Acacia caven (Molina) Molina SPECIES
    ## 2 31100            Acacia decurrens Willd. SPECIES
    ## 3 31101      Acacia farnesiana (L.) Willd. SPECIES
    ## 4 31102 Acacia longifolia (Andrews) Willd. SPECIES
    ## 5 31103              Acacia mangium Willd. SPECIES
    ## 6 31104           Acacia melanoxylon R.Br. SPECIES
    ##                           synoscientificname parentcanonicalname  syno
    ## 1 Vachellia caven (Molina) Seigler & Ebinger              Acacia  TRUE
    ## 2                                       <NA>              Acacia FALSE
    ## 3     Vachellia farnesiana (L.) Wight & Arn.              Acacia  TRUE
    ## 4                                       <NA>              Acacia FALSE
    ## 5                                       <NA>              Acacia FALSE
    ## 6                                       <NA>              Acacia FALSE

#### 2.1.0.2 Exotic status, Invasive status, occurrence status, references and comments

I am not completely sure of the way to treat the status of the taxa,
depending on their establishmentMeans.

``` r
table(data$distribution$occurrenceStatus,data$distribution$establishmentMeans)
```

    ##          
    ##           Alien Cryptogenic|Uncertain
    ##   Present   490                    19

For now we will consider that all the taxa here are alien, all are
observed (all are noted as “Present” for Colombia), and some of them are
cryptogenic.

In the table “speciesprofile”, we find the following information about
the invasive status:

``` r
table(data$speciesprofile$isInvasive)
```

    ## 
    ## Invasive     Null 
    ##       96      413

As you can see the species are either invasive or null, so we will
consider that the species are invasive, or not (False), when the status
is null (we might have to go back on this decision later…)

In this dataset there are no information that we should include in the
comment, or extra references to include for the taxa.

``` r
tabStatus = data.frame(id=pf_taxon$id,is_alien=T, occ_observed=T)
m <- match(data$distribution$id,tabStatus$id)
tabStatus$cryptogenic[m] <- grepl("Cryptogenic",data$distribution$establishmentMeans)
m <- match(data$speciesprofile$id,tabStatus$id)
tabStatus$is_invasive[m] <- grepl("Invasive",data$speciesprofile$isInvasive)
head(tabStatus)
```

    ##      id is_alien occ_observed cryptogenic is_invasive
    ## 1 31099     TRUE         TRUE       FALSE       FALSE
    ## 2 31100     TRUE         TRUE       FALSE        TRUE
    ## 3 31101     TRUE         TRUE       FALSE       FALSE
    ## 4 31102     TRUE         TRUE       FALSE       FALSE
    ## 5 31103     TRUE         TRUE       FALSE       FALSE
    ## 6 31104     TRUE         TRUE       FALSE       FALSE

#### 2.1.0.3 Final preformatting

The goal here is to associate the taxonomic information, the exotic
statuses, the references, and the comments in lists that may be directly
transformed to json in order to send them to the API post method.

``` r
## First we prepare the global reference and link for the dataset, to add in each taxon
baseRef <- list(
  ref_citation = list("Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG."),
  link = list("https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91")
  )
masterList <- list()
for(i in 1:nrow(pf_taxon))
{
  id <- pf_taxon[i,"id"]
  masterList[[i]] <- as.list(pf_taxon[i,colnames(pf_taxon) != "id" & !is.na(pf_taxon[i,])])
  masterList[[i]] <- append(masterList[[i]],as.list(tabStatus[tabStatus$id==id,colnames(tabStatus)!="id"]))
  masterList[[i]] <- append(masterList[[i]],baseRef)
  ## Then we add the potential references already preformatted for this taxon
}
```

## 2.2 Basic usage : example of one only species

If we take the first example of the list that we formatted on the
previous part of the document, we obtain:

``` r
masterList[[1]]
```

    ## $scientificname
    ## [1] "Acacia caven (Molina) Molina"
    ## 
    ## $rank
    ## [1] "SPECIES"
    ## 
    ## $synoscientificname
    ## [1] "Vachellia caven (Molina) Seigler & Ebinger"
    ## 
    ## $parentcanonicalname
    ## [1] "Acacia"
    ## 
    ## $syno
    ## [1] TRUE
    ## 
    ## $is_alien
    ## [1] TRUE
    ## 
    ## $occ_observed
    ## [1] TRUE
    ## 
    ## $cryptogenic
    ## [1] FALSE
    ## 
    ## $is_invasive
    ## [1] FALSE
    ## 
    ## $ref_citation
    ## $ref_citation[[1]]
    ## [1] "Piedad Baptiste E M, Marcela García L. L, Acevedo-Charry O, Acosta A, Alarcón J, Arévalo E, Carolina Avella G, Blanco A, E. Botero J, Rancés Caicedo-Portilla J, Camelo Martínez C, Camelo-Calvo M P, Certuche-Cubillos K, Chasqui L, Cifuentes Y, Julián Contreras P, Córdoba S, Correa J, Fernanda Díaz M, DoNascimiento C, Alexandra Duque R, Victoria Flechas S, Dimitri Forero I, José Gómez Hoyos A, González Durán G, Guayara S, Carlos Guetiva J, Jiménez G, Larrahondo M, Maldonado Ocampo J, Medina-Rangel G F, Merino M C, Mesa L M, Millán M V, Mojica H, César Neita Moreno J, del Pilar Parrado M, Camilo Pérez S, Ramírez W, Rojas V, Rojas Z, Urbina-Cardona N, Paola Velásquez L, Wong L J, Pagad S (2020). Global Register of Introduced and Invasive Species - Colombia. Version 1.5. Invasive Species Specialist Group ISSG."
    ## 
    ## 
    ## $link
    ## $link[[1]]
    ## [1] "https://www.gbif.org/dataset/168568e7-eb5f-4ef6-8c59-f73ceaf57e91"

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
-   *is_alien* : whether the species considered as introduced in
    Colombia
-   *is_invasive* : whether the species considered as potentially
    harmful (in terms of biological invasion) in Colombia
-   *occ_observed*: observed occurrence in Colombia
-   *cryptogenic* whether the species is cryptogenic (or very rare)
-   *ref_citation* : a list of the references on which are based the
    inclusion of the taxon and its endemism status in the API
-   *link* : a list of the url links (corresponding in length and order
    to the *ref_citation*)
-   *comments* : comment on the endemism status of the taxon

#### 2.2.0.1 In R

``` r
sendJson <- to_json(masterList[[1]],unbox=T)
POST('http://localhost:5000/insertExot',body=sendJson, content_type("application/json"),verbose())
```

    ## Response [http://localhost:5000/insertExot]
    ##   Date: 2022-03-14 01:23
    ##   Status: 200
    ##   Content-Type: application/json
    ##   Size: 32 B
    ## {"cd_tax": 153, "cdRefs": [90]}

Now we do it for all the list:

``` r
res = list()
for(i in 1:length(masterList))
{
  res[[i]] <- POST(paste(baseURL,baseResource,sep="/"),body=to_json(masterList[[i]],unbox=T), content_type("application/json"))
}
```

##### 2.2.0.1.1 Problems

``` r
pbs <- !sapply(res,function(x)"cd_tax"%in%names(content(x)))
```

    ## Registered S3 method overwritten by 'jsonlite':
    ##   method     from   
    ##   print.json jsonify

Note: Canis lupus is twice in the list, with 2 different statuses:

``` r
data$taxon[grep("Canis",data$taxon$scientificName),]
```

    ##       id taxonID             scientificName acceptedNameUsage  kingdom   phylum
    ## 93 31191   31191 Canis lupus Linnaeus, 1758                   Animalia Chordata
    ## 94 31192   31192 Canis lupus Linnaeus, 1758                   Animalia Chordata
    ##       class     order  family taxonRank taxonomicStatus
    ## 93 Mammalia Carnivora Canidae   SPECIES        ACCEPTED
    ## 94 Mammalia Carnivora Canidae   SPECIES        ACCEPTED

``` r
data$speciesprofile[data$speciesprofile$id%in%c(31191,31192),]
```

    ##       id isInvasive     habitat
    ## 93 31191   Invasive Terrestrial
    ## 94 31192       Null Terrestrial

Note: Helix aspersa is a synonym to Cornu aspersum, but one is
considered invasive and the other no…

``` r
data$taxon[grepl("Helix",data$taxon$scientificName)|grepl("Cornu",data$taxon$scientificName),]
```

    ##        id taxonID                     scientificName
    ## 143 31241   31241 Cornu aspersum (O.F.MÃ¼ller, 1774)
    ## 238 31336   31336     Helix aspersa O.F.Müller, 1774
    ##                     acceptedNameUsage  kingdom   phylum      class
    ## 143                                   Animalia Mollusca Gastropoda
    ## 238 Cornu aspersum (O.F.Müller, 1774) Animalia Mollusca Gastropoda
    ##               order    family taxonRank taxonomicStatus
    ## 143 Stylommatophora Helicidae   SPECIES        ACCEPTED
    ## 238 Stylommatophora Helicidae   SPECIES         SYNONYM

``` r
data$speciesprofile[data$speciesprofile$id%in%c(31336,31241),]
```

    ##        id isInvasive     habitat
    ## 143 31241       Null Terrestrial
    ## 238 31336   Invasive Terrestrial

Note: same for Pennisetum clandestinum, synonym of Cenchrus clandestinum

``` r
data$taxon[grepl("Pennisetum c",data$taxon$scientificName)|grepl("Cenchrus cl",data$taxon$scientificName),]
```

    ##        id taxonID                                    scientificName
    ## 112 31210   31210 Cenchrus clandestinus (Hochst. ex Chiov.) Morrone
    ## 371 31469   31469         Pennisetum clandestinum Hochst. ex Chiov.
    ##                                     acceptedNameUsage kingdom       phylum
    ## 112                                                   Plantae Tracheophyta
    ## 371 Cenchrus clandestinus (Hochst. ex Chiov.) Morrone Plantae Tracheophyta
    ##          class  order  family taxonRank taxonomicStatus
    ## 112 Liliopsida Poales Poaceae   SPECIES        ACCEPTED
    ## 371 Liliopsida Poales Poaceae   SPECIES         SYNONYM

``` r
data$speciesprofile[data$speciesprofile$id%in%c(31210,31469),]
```

    ##        id isInvasive     habitat
    ## 112 31210       Null Terrestrial
    ## 371 31469   Invasive Terrestrial

The viruses are not taken well into account, we should see whether there
are solutions… There are not included for now…

``` r
griis_tax <- pf_taxon
```
