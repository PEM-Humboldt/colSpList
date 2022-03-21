UPDATE pg_database set encoding = pg_char_to_encoding('UTF8') where datname='sp_list';

CREATE TABLE tax_rank
(
    cd_rank varchar(6) PRIMARY KEY,
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
    cd_tax serial PRIMARY KEY,
    name text NOT NULL,
    name_auth text,
    auth text,
    tax_rank varchar(6) NOT NULL  REFERENCES tax_rank(cd_rank) ON DELETE SET NULL ON UPDATE CASCADE DEFERRABLE,
    cd_sup integer REFERENCES taxon(cd_tax)  ON UPDATE CASCADE DEFERRABLE,
    cd_syno integer REFERENCES taxon(cd_tax)  ON UPDATE CASCADE DEFERRABLE,
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

CREATE TABLE def_habito
(
    cd_hab varchar(50) PRIMARY KEY,
    descr_hab text
);

CREATE TABLE habito
(
    id serial PRIMARY KEY,
    cd_tax integer REFERENCES taxon(cd_tax) NOT NULL,
    cd_hab varchar(50) REFERENCES def_habito(cd_hab) NOT NULL,
    UNIQUE (cd_tax, cd_hab)
);

/* These tables might be useful later if we want to categorize more precisely the species
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
*/

CREATE TABLE exot
(
    cd_tax integer PRIMARY KEY REFERENCES taxon(cd_tax),
    is_alien boolean,
    is_invasive boolean,
    -- occ_observed boolean,
    -- cryptogenic boolean,
    comments text
);



CREATE TABLE threat_status
(
    cd_status varchar(15) PRIMARY KEY,
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
    cd_tax integer PRIMARY KEY REFERENCES taxon(cd_tax),
    cd_status varchar(15) REFERENCES threat_status(cd_status),
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
(0, 'Unsuficient information', 'Información insuficiente'), 
(1, 'Species of interest', 'Especie de interés'),
(2, 'Almost endemic by area', 'Casi endémicas por área'),
(3, 'Almost endemic', 'Casi endémica'),
(4, 'Endemic', 'Endémica');


CREATE TABLE endemic
(
    cd_tax integer PRIMARY KEY REFERENCES taxon(cd_tax),
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

-----------------------------------------
/* Security and users */
CREATE TABLE users
(
    id serial PRIMARY KEY,
    username varchar(100) UNIQUE,
    password_hash varchar(128),
    admin boolean DEFAULT FALSE,
    edit_auth boolean DEFAULT FALSE
);
------------------------------------------

CREATE VIEW exotList AS(
    SELECT 
        t.name_auth,
        t_par.name_auth parentname,
        t.tax_rank,
        t.gbifkey,
        STRING_AGG (t_synos.name_auth, ' | ') synonyms,
        --ARRAY_AGG(t_synos.name_auth) synonyms_list,
        e.is_alien,
        e.is_invasive,
        --e.occ_observed,
        --e.cryptogenic,
        e.comments,
        STRING_AGG(r.citation, ' | ' ORDER BY r.cd_ref) AS references,
        STRING_AGG(r.link, ' | ' ORDER BY r.cd_ref) AS links 
    FROM exot e
    LEFT JOIN taxon t ON e.cd_tax=t.cd_tax
    LEFT JOIN taxon t_par ON t.cd_sup=t_par.cd_tax
    LEFT JOIN taxon t_synos ON t_synos.cd_syno=t.cd_tax
    LEFT JOIN ref_exot re ON e.cd_tax=re.cd_tax
    LEFT JOIN refer r ON re.cd_ref=r.cd_ref 
    GROUP BY t.name_auth, t_par.name_auth,t.tax_rank,t.gbifkey,e.is_alien, e.is_invasive, /*e.occ_observed,e.cryptogenic,*/ e.comments
);
