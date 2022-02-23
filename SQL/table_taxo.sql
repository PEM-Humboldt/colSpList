CREATE TABLE tax_rank
(
    id_rank varchar(6) PRIMARY KEY,
    rank_name text NOT NULL,
    rank_level integer,
    gbif_bb_marker varchar(10) UNIQUE
);

CREATE TABLE tax_status
(
    status varchar(15) PRIMARY KEY,
    descri text
);

CREATE TABLE refer
(
    cd_ref serial PRIMARY KEY,
    citation text UNIQUE NOT NULL,
    link text
);

CREATE TABLE taxon 
(
    id_tax serial PRIMARY KEY,
    name text NOT NULL,
    name_auth text,
    auth text,
    tax_rank varchar(6) NOT NULL  REFERENCES tax_rank(id_rank) ON DELETE SET NULL ON UPDATE CASCADE DEFERRABLE,
    cd_sup integer REFERENCES taxon(id_tax)  ON UPDATE CASCADE DEFERRABLE,
    cd_syno integer REFERENCES taxon(id_tax)  ON UPDATE CASCADE DEFERRABLE,
    status varchar(15) REFERENCES tax_status(status),
    gbifkey bigint UNIQUE,
    source integer REFERENCES refer(cd_ref)
);
CREATE INDEX taxon_cd_sup_idx ON taxon(cd_sup);
CREATE INDEX taxon_cd_syno_idx ON taxon(cd_syno);

INSERT INTO tax_rank 
VALUES
    ('FORM', 'FORM', 1,'f.'),
    ('SUBVAR', 'SUBVARIETY', 2,'subvar.'),
    ('VAR', 'VARIETY', 3,'var.'),
    ('SUBSP', 'SUBSPECIES', 4, 'subsp.'),
    ('SP', 'SPECIES', 5, 'sp.'),
    ('SPSP', 'SUPERSPECIES', 6, NULL),
    ('SGN', 'SUBGENUS',7, 'subgen.'),
    ('GN', 'GENUS', 8,'gen.'),
    ('TR', 'TRIBE', 9, NULL),
    ('SFAM', 'SUBFAMILY', 10,'subfam.'),
    ('FAM', 'FAMILY', 11,'fam.'),
    ('SPFAM', 'SUPERFAMILY', 12,NULL),
    ('SOR', 'SUBORDER', 13,NULL),
    ('OR', 'ORDER', 14,'ord.'),
    ('LEG', 'LEGION', 15,NULL),
    ('SCL', 'SUBCLASS', 17,NULL),
    ('CL', 'CLASS', 18, 'cl.'),
    ('SPCL', 'SUPERCLASS', 19,NULL),
    ('SPHY', 'SUBPHYLUM', 20,NULL),
    ('PHY', 'PHYLUM', 21,'phyl.'),
    ('SPPHY', 'SUPERPHYLUM', 22,NULL),
    ('SKG', 'SUBKINGDOM', 23,NULL),
    ('KG', 'KINGDOM', 24,NULL),
    ('SPKG', 'SUPERKINGDOM', 25,NULL),
    ('SREA', 'SUBREALM', 26,NULL),
    ('REA', 'REALM', 27,NULL),
    ('SDOM', 'SUBDOMAIN', 28,NULL),
    ('DOM', 'DOMAIN', 29,NULL);

INSERT INTO tax_status
VALUES
    ('ACCEPTED','taxon accepted'),
    ('SYNONYM','taxon non accepted, should reference an accepted taxon, note that doubtful synonym are noted SYNONYM'),
    ('DOUBTFUL','taxon non completely accepted, need more information, note that doubtful synonym are noted SYNONYM');

/*
INSERT INTO tax_source
VALUES
    ('GRIIS','','');
*/

CREATE TABLE pres_status
(
    id_pres varchar(15) PRIMARY KEY,
    descr_pres text
);

CREATE TABLE habito
(
    id_habito varchar(15) PRIMARY KEY,
    descr_type text
);

CREATE TABLE type_intro
(
    id_type varchar(15) PRIMARY KEY,
    descr_intro text
);

CREATE TABLE uso
(
    cd_uso varchar(15) PRIMARY KEY,
    descr_uso text
);

CREATE TABLE habito
(
    cd_tax integer REFERENCES taxon("id_tax") NOT NULL
    habito varchar(25) NOT NULL
)
;

CREATE TABLE exot
(
    cd_tax integer PRIMARY KEY REFERENCES taxon(id_tax),
    is_alien boolean,
    is_invasive boolean,
    occ_observed boolean,
    cryptogenic boolean,
    comments text
);



CREATE TABLE threat_status
(
    id_status varchar(15) PRIMARY KEY,
    level int NOT NULL,
    status_descr text
);

INSERT INTO threat_status
VALUES 
('NE',0,'Not Evaluated'),
('DD',1,'Data Deficient'),
('LC',2,'Least Concern'),
('NT',3,'Near Threatened'),
('VU',4,'Vulnerable'),
('EN',5,'Endangered'),
('CR',6,'Critically endangered'),
('EW',7,'Extinct in the wild'),
('EX',8,'Extinct');


    
CREATE TABLE threat
(
    cd_tax integer PRIMARY KEY REFERENCES taxon(id_tax),
    cd_status varchar(15) REFERENCES threat_status(id_status),
    comments text,
    comment text
);

CREATE TABLE nivel_endem
(
    cd_nivel integer PRIMARY KEY,
    descr_endem_en text,
    descr_endem_es text
);

INSERT INTO nivel_endem
VALUES
(0, 'Unsuficient information', 'Información insuficient'), 
(1, 'Species of interest', 'Especie de interés'),
(2, 'Almost endemic by area', 'Casi endémica por area'),
(3, 'Almost endemic', 'Casi endémica'),
(4, 'Endemic', 'Endémica');


CREATE TABLE endemic
(
    cd_tax integer PRIMARY KEY REFERENCES taxon(id_tax),
    cd_nivel integer REFERENCES nivel_endem(cd_nivel),
    comments text
);


CREATE TABLE ref_endem 
(
    id serial PRIMARY KEY,
    cd_ref integer REFERENCES refer(cd_ref) ON DELETE CASCADE ON UPDATE CASCADE,
    cd_tax integer REFERENCES endemic(cd_tax) ON DELETE CASCADE ON UPDATE CASCADE,
    comment text,
    UNIQUE (cd_ref, cd_tax)
);

CREATE TABLE ref_exot
(
    id serial PRIMARY KEY,
    cd_ref integer REFERENCES refer(cd_ref) ON DELETE CASCADE ON UPDATE CASCADE,
    cd_tax integer REFERENCES exot(cd_tax)  ON DELETE CASCADE ON UPDATE CASCADE,
    comment text,
    UNIQUE (cd_ref,cd_tax)
);

CREATE TABLE ref_threat
(
    id serial PRIMARY KEY,
    cd_ref integer REFERENCES refer(cd_ref) ON DELETE CASCADE ON UPDATE CASCADE,
    cd_tax integer REFERENCES threat(cd_tax) ON DELETE CASCADE ON UPDATE CASCADE,
    comment text,
    UNIQUE (cd_ref, cd_tax)
);
