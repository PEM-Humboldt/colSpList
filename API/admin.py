from taxo import synosAndParents
def delTaxo_no_status(connection):
    deleted=[]
    cur = connection.cursor()
    SQL="SELECT cd_tax FROM exot UNION SELECT cd_tax FROM endemic UNION SELECT cd_tax FROM threat"
    cur.execute(SQL)
    res = cur.fetchall()
    all_tax_status = [r[0] for r in res]
    all_tax_status_syno_parents = synosAndParents(cur,all_tax_status)
    SQL = "WITH a AS (SELECT UNNEST(%s) AS cd_tax) SELECT cd_tax FROM taxon LEFT JOIN a USING (cd_tax) WHERE a.cd_tax IS NULL"
    cur.execute(SQL,[all_tax_status_syno_parents['all']])
    res = cur.fetchall()
    to_delete = [r[0] for r in res]
    if len(to_delete)>0:
        SQL = "WITH a AS (SELECT UNNEST(%s) AS cd_tax) DELETE FROM taxon WHERE taxon.cd_tax IN  (SELECT cd_tax FROM a) RETURNING cd_tax"
        cur.execute(SQL,[to_delete])
        res=cur.fetchall()
        deleted=[r[0] for r in res]
    cur.close()
    connection.commit()
    return deleted

def delReference_no_status(connection):
    cur=connection.cursor()
    SQL= "WITH a AS(SELECT cd_ref FROM refer WHERE cd_ref NOT IN (SELECT source FROM taxon UNION SELECT cd_ref FROM ref_endem UNION SELECT cd_ref FROM ref_exot UNION SELECT cd_ref FROM ref_threat)) DELETE FROM refer WHERE cd_ref IN (SELECT cd_ref FROM a) RETURNING cd_ref"
    cur.execute(SQL)
    res = cur.fetchall()
    deleted=[r[0] for r in res]
    cur.close()
    connection.commit()
    return deleted

def delStatus_no_reference(connection):
    cur=connection.cursor()
    SQL= "WITH a AS(SELECT cd_tax/*, BOOL_AND(cd_ref IS NULL) no_ref */FROM exot e LEFT JOIN ref_exot re USING (cd_tax) GROUP BY cd_tax HAVING BOOL_AND(cd_ref IS NULL)) DELETE FROM exot WHERE cd_tax IN (SELECT cd_tax FROM a) RETURNING cd_tax"
    cur.execute(SQL)
    res=cur.fetchall()
    deletedExot=[r[0] for r in res]
    SQL= "WITH a AS(SELECT cd_tax/*, BOOL_AND(cd_ref IS NULL) no_ref */FROM endemic e LEFT JOIN ref_endem re USING (cd_tax) GROUP BY cd_tax HAVING BOOL_AND(cd_ref IS NULL)) DELETE FROM endemic WHERE cd_tax IN (SELECT cd_tax FROM a) RETURNING cd_tax"
    cur.execute(SQL)
    res= cur.fetchall()
    deletedEndem = [r[0] for r in res]
    SQL= "WITH a AS(SELECT cd_tax/*, BOOL_AND(cd_ref IS NULL) no_ref */FROM threat t LEFT JOIN ref_threat rt USING (cd_tax) GROUP BY cd_tax HAVING BOOL_AND(cd_ref IS NULL)) DELETE FROM threat WHERE cd_tax IN (SELECT cd_tax FROM a) RETURNING cd_tax"
    cur.execute(SQL)
    res=cur.fetchall()
    deletedThreat=[r[0] for r in res]
    cur.close()
    connection.commit()
    return deletedExot+deletedEndem+deletedThreat

def delSyno_no_tax(connection):
    cur=connection.cursor()
    SQL= "WITH a AS (SELECT t.cd_tax FROM taxon t LEFT JOIN taxon ta ON t.cd_syno=ta.cd_tax WHERE t.status='SYNONYM' AND ta.cd_tax IS NULL) DELETE FROM taxon WHERE cd_tax IN (SELECT cd_tax FROM a) RETURNING cd_tax"
    cur.execute(SQL)
    res=cur.fetchall()
    deleted=[r[0] for r in res]
    cur.close()
    connection.commit()
    return deleted

    
    
