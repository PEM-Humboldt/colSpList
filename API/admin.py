"""
Functions for the administration of the database, with a performance focus
"""

from taxo import synosAndParents

def delTaxo_no_status(connection):
    """
    Suppresses the taxa which have no status (exotic, endemic or threatened). To use only when the database reaches its limits, because the presence of taxa even without statuses makes the API more efficient

    Parameters:
    -----------
    connection: psycopg2 Connection
        connection to the database
    Returns:
    --------
    List of suppressed taxon identifiers
    """
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
    """
    Suppresses the references which are not associated with any status

    Parameters:
    -----------
    connection: psycopg2 Connection
        connection to the database
    Returns:
    --------
    List of suppressed reference identifiers
    """
    cur=connection.cursor()
    SQL= "WITH a AS(SELECT source AS cd_ref FROM taxon UNION SELECT cd_ref FROM ref_endem UNION SELECT cd_ref FROM ref_exot UNION SELECT cd_ref FROM ref_threat), b AS (SELECT r.cd_ref, a.cd_ref IS NOT NULL refed FROM refer r LEFT JOIN a USING(cd_ref)) DELETE FROM refer AS r USING b WHERE r.cd_ref=b.cd_ref AND NOT b.refed RETURNING r.cd_ref"
    cur.execute(SQL)
    res = cur.fetchall()
    deleted=[r[0] for r in res]
    cur.close()
    connection.commit()
    return deleted

def delStatus_no_reference(connection):
    """
    Suppresses the statuses (endemism, alien/invasive or threatened) of species which are not associated with any bibliographic reference. If the API is used consistently, that should never happen...

    Parameters:
    -----------
    connection: psycopg2 Connection
        connection to the database
    Returns:
    --------
    List of suppressed status identifiers (note: the status identifiers correspond to the taxon identifiers cd_tax
    """
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
    """
    Suppresses the synonyms which are not associated with any accepted taxa

    Parameters:
    -----------
    connection: psycopg2 Connection
        connection to the database
    Returns:
    --------
    List of suppressed taxon identifiers
    """
    cur=connection.cursor()
    SQL= "WITH a AS (SELECT t.cd_tax FROM taxon t LEFT JOIN taxon ta ON t.cd_syno=ta.cd_tax WHERE t.status='SYNONYM' AND ta.cd_tax IS NULL) DELETE FROM taxon WHERE cd_tax IN (SELECT cd_tax FROM a) RETURNING cd_tax"
    cur.execute(SQL)
    res=cur.fetchall()
    deleted=[r[0] for r in res]
    cur.close()
    connection.commit()
    return deleted

