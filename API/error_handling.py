"""
In this file we redirect the errors before passing them to the endpoints
We manage here 2 types of errors:
1. if the error is due to user input, the functions should returns a result consisting of a dictionary with a key 'error' and the explicative message for the user
2. if the error is due to a problem in the api code or database, the function raises a "Abort500Error" in order to indicate to the endpoint that it should use the abort method with the "500" html error code and the message from the initial error code
"""

from errors_def import MissingArgError, DatabaseUncompatibilityValueError, DatabaseUncompatibilityError, AlreadyExistsDbError, DeleteMissingElementDbError, ModifyMissingStatusDbError, TaxonNotFoundDbError, GrantExistingRightError, RevokeUnexistingRightError, UncompatibilityGbifKeyCanonicalname, DbIntegrityError, UncompatibleStatusError, UnauthorizedValueError,UncompatibilityCdTaxInputTaxError, ModifyMissingRefDbError, Abort500Error
from taxo import manageInputTax, get_gbif_parsed_from_sci_name,childrenList,deleteTaxo, checkCdTax
from flask import abort, g
from getStatus import testEndemStatus, testExotStatus, testThreatStatus, getListTax,getListExot, getListEndem, getListThreat, getTax, getListReferences
from manageStatus import manageSource,deleteRef,mergeRefs, modifyRef, deleteExot, deleteEndem,deleteThreat,modifyEndem,modifyThreat,modifyExot,manageInputEndem,manageInputThreat,manageInputExot
from security import new_user, delete_user, valid_password, user_exists, get_user, generate_auth_token, verify_auth_token, grant_user, revoke_user, grant_edit, revoke_edit, grant_admin, revoke_admin,change_password, get_user_list
import psycopg2
from psycopg2 import sql
import psycopg2.extras
from io import BytesIO
from flask import send_file

def testEndemGet_err_hand(connection, **testEndemArgs):
    try:
        res = manageInputTax(connection=connection, insert=False, **testEndemArgs)
        if res.get('alreadyInDb'):
            res.update(testEndemStatus(connection,res.get('cd_tax_acc')))
        else:
            res.update({'hasEndemStatus':False,'cd_status':None,'comments':None,'references':list(),'links':list()})
    except (MissingArgError, UncompatibilityGbifKeyCanonicalname) as e:
        return {'error':str(e)}
    except UnauthorizedValueError as e:
        if e.var=='gbifMatchMode':
           raise Abort500Error(str(e)) from e
        else:
            return {'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res


def testExotGet_err_hand(connection, **testExotArgs):
    try:
        res = manageInputTax(connection=connection, insert=False, **testExotArgs)
        if res.get('alreadyInDb'):
            res.update(testExotStatus(connection,res.get('cd_tax_acc')))
        else:
            res.update({'hasExotStatus':False,'is_alien':None,'is_invasive':None,'comments':None,'references':list(),'links':list()})
    except (MissingArgError, UncompatibilityGbifKeyCanonicalname) as e:
        return {'error':str(e)}
    except UnauthorizedValueError as e:
        if e.var=='gbifMatchMode':
           raise Abort500Error(str(e)) from e
        else:
            return {'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def testThreatGet_err_hand(connection, **testThreatArgs):
    try:
        res = manageInputTax(connection=connection, insert=False, **testThreatArgs)
        if res.get('alreadyInDb'):
            res.update(testThreatStatus(connection,res.get('cd_tax_acc')))
        else:
            res.update({'hasThreatStatus':False,'cd_status':None,'comments':None,'references':list(),'links':list()})
    except (MissingArgError, UncompatibilityGbifKeyCanonicalname) as e:
        return {'error':str(e)}
    except UnauthorizedValueError as e:
        if e.var=='gbifMatchMode':
           raise Abort500Error(str(e)) from e
        else:
            return {'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res


def ListEndem_err_hand(connection, **listEndemArgs):
    try:
        if listEndemArgs.get('childrenOf'):
            parsed = get_gbif_parsed_from_sci_name(listEndemArgs.get('childrenOf'))
            if parsed.get('scientificName') and parsed.get('canonicalNameComplete') and parsed.get('scientificName')==parsed.get('canonicalNameComplete'):
                parent=manageInputTax(connection=connection, insert=False,canonicalname=listEndemArgs.get('childrenOf'))
            else:
                parent=manageInputTax(connection=connection, insert=False,scientificname=listEndemArgs.get('childrenOf'))
            if parent.get('alreadyInDb'):
                cursor=connection.cursor()
                listChildren=childrenList(cursor,parent.get('cd_tax_acc'))
                cursor.close()
                res=getListEndem(connection=connection, listChildren=listChildren, formatExport=listEndemArgs.get('format'))
            else:
                raise TaxonNotFoundDbError(tax=listEndemArgs.get('childrenOf'), message='\'childrenOf\' taxon not recognized')
                #raise Exception("childrenOfNotFound")
        else:
            res = getListEndem(connection=connection, listChildren=[], formatExport=listEndemArgs.get('format'))
    except (TaxonNotFoundDbError, MissingArgError) as e:
        return {'error':str(e)}
    except (DbIntegrityError, UnauthorizedValueError) as e:
        raise Abort500Error(str(e)) from e
    else:
        if listEndemArgs.get('format')=="CSV":
            response_stream = BytesIO(res.to_csv().encode())
            return send_file(response_stream, mimetype = "text/csv", attachment_filename = "endemic.csv")
        else:
            return res

def ListExot_err_hand(connection, **listExotArgs):
    try:
        if listExotArgs.get('childrenOf'):
            parsed = get_gbif_parsed_from_sci_name(listExotArgs.get('childrenOf'))
            if parsed.get('scientificName') and parsed.get('canonicalNameComplete') and parsed.get('scientificName')==parsed.get('canonicalNameComplete'):
                parent=manageInputTax(connection=connection, insert=False,canonicalname=listExotArgs.get('childrenOf'))
            else:
                parent=manageInputTax(connection=connection, insert=False,scientificname=listExotArgs.get('childrenOf'))
            if parent.get('alreadyInDb'):
                cursor=connection.cursor()
                listChildren=childrenList(cursor,parent.get('cd_tax_acc'))
                cursor.close()
                res=getListExot(connection=connection, listChildren=listChildren, formatExport=listExotArgs.get('format'))
            else:
                raise TaxonNotFoundDbError(tax=listExotArgs.get('childrenOf'), message='\'childrenOf\' taxon not recognized')
                #raise Exception("childrenOfNotFound")
        else:
            res = getListExot(connection=connection, listChildren=[], formatExport=listExotArgs.get('format'))
    except (TaxonNotFoundDbError, MissingArgError) as e:
        return {'error':str(e)}
    except (DbIntegrityError, UnauthorizedValueError) as e:
        raise Abort500Error(str(e)) from e
    else:
        if listExotArgs.get('format')=="CSV":
            response_stream = BytesIO(res.to_csv().encode())
            return send_file(response_stream, mimetype = "text/csv", attachment_filename = "exot.csv")
        else:
            return res

def ListThreat_err_hand(connection, **listThreatArgs):
    try:
        if listThreatArgs.get('childrenOf'):
            parsed = get_gbif_parsed_from_sci_name(listThreatArgs.get('childrenOf'))
            if parsed.get('scientificName') and parsed.get('canonicalNameComplete') and parsed.get('scientificName')==parsed.get('canonicalNameComplete'):
                parent=manageInputTax(connection=connection, insert=False,canonicalname=listThreatArgs.get('childrenOf'))
            else:
                parent=manageInputTax(connection=connection, insert=False,scientificname=listThreatArgs.get('childrenOf'))
            if parent.get('alreadyInDb'):
                cursor=connection.cursor()
                listChildren=childrenList(cursor,parent.get('cd_tax_acc'))
                cursor.close()
                res=getListThreat(connection=connection, listChildren=listChildren, formatExport=listThreatArgs.get('format'))
            else:
                raise TaxonNotFoundDbError(tax=listThreatArgs.get('childrenOf'), message='\'childrenOf\' taxon not recognized')
                #raise Exception("childrenOfNotFound")
        else:
            res = getListThreat(connection=connection, listChildren=[], formatExport=listThreatArgs.get('format'))
    except (TaxonNotFoundDbError, MissingArgError) as e:
        return {'error':str(e)}
    except (DbIntegrityError, UnauthorizedValueError) as e:
        raise Abort500Error(str(e)) from e
    else:
        if listThreatArgs.get('format')=="CSV":
            response_stream = BytesIO(res.to_csv().encode())
            return send_file(response_stream, mimetype = "text/csv", attachment_filename = "threat.csv")
        else:
            return res

def GetTaxon_err_hand(connection, **taxInput):
    try:
        if not taxInput.get('cd_tax'):
            taxInput.update(manageInputTax(connection=connection,insert=False,**taxInput))
        taxOutput = getTax(connection,taxInput.get('cd_tax'))
    except (MissingArgError, UncompatibilityGbifKeyCanonicalname) as e:
        return {'error':str(e)}
    except (DbIntegrityError, UnauthorizedValueError) as e:
        raise Abort500Error(str(e)) from e
    else:
        return taxOutput


def ListTax_err_hand(connection, **listTaxArgs):
    try:
        if listTaxArgs.get('childrenOf'):
            parsed = get_gbif_parsed_from_sci_name(listTaxArgs.get('childrenOf'))
            if parsed.get('scientificName') and parsed.get('canonicalNameComplete') and parsed.get('scientificName')==parsed.get('canonicalNameComplete'):
                parent=manageInputTax(connection=connection, insert=False,canonicalname=listTaxArgs.get('childrenOf'))
            else:
                parent=manageInputTax(connection=connection, insert=False,scientificname=listTaxArgs.get('childrenOf'))
            if parent.get('alreadyInDb'):
                cursor=connection.cursor()
                listChildren=childrenList(cursor,parent.get('cd_tax_acc'))
                cursor.close()
                res=getListTax(connection=connection, listChildren=listChildren, formatExport=listTaxArgs.get('format'))
            else:
                raise TaxonNotFoundDbError(tax=listTaxArgs.get('childrenOf'), message='\'childrenOf\' taxon not recognized')
                #raise Exception("childrenOfNotFound")
        else:
            res = getListTax(connection=connection, listChildren=[], formatExport=listTaxArgs.get('format'))
    except (TaxonNotFoundDbError, MissingArgError) as e:
        return {'error':str(e)}
    except (DbIntegrityError, UnauthorizedValueError) as e:
        raise Abort500Error(str(e)) from e
    else:
        if listTaxArgs.get('format')=="CSV":
            response_stream = BytesIO(res.to_csv().encode())
            return send_file(response_stream, mimetype = "text/csv", attachment_filename = "taxonomy.csv")
        else:
            return res

def ListRef_err_hand(connection, **listRefArgs):
    try:
        listRef = getListReferences(connection=connection, formatExport= listRefArgs.get('format'), onlyEndem= listRefArgs.get('onlyEndem'), onlyExot= listRefArgs.get('onlyExot'), onlyThreat= listRefArgs.get('onlyThreat'))
    except (MissingArgError) as e:
        return {'error':str(e)}
    except (DbIntegrityError, UnauthorizedValueError) as e:
        raise Abort500Error(str(e)) from e
    else:
        if listRefArgs.get('format')=="CSV":
            response_stream = BytesIO(listRef.to_csv().encode())
            return send_file(response_stream, mimetype = "text/csv", attachment_filename = "references.csv")
        else:
            return listRef

def cleanDbDel_err_hand(connection,**cdbArgs):
        try:
            cd_taxs=[]
            cd_refs=[]
            cd_status=[]
            if cdbArgs.get('status_no_ref'):
                cd_status+=delStatus_no_reference(conn)
            if cdbArgs.get('ref_no_status'):
                cd_refs+=delReference_no_status(conn)
            if cdbArgs.get('syno_no_tax'):
                cd_taxs+=delSyno_no_tax(conn)
            if cdbArgs.get('tax_no_status'):
                cd_taxs+=delTaxo_no_status(conn)
        except (MissingArgError,DeleteMissingElementDbError) as e:
            return {'error':str(e)}
        else:
            return {'cd_taxs': cd_taxs, 'cd_refs':cd_refs,'cd_status':cd_status}

def userPost_err_hand(connection, **userArgs):
    try:
        uid,username=new_user(connection,**userArgs)
    except (AlreadyExistsDbError) as e:
        return {'error':str(e)}
    else:
        return{'uid':uid, 'username':username}


def userPut_err_hand(connection,**userArgs):
    try:
        user=g.get('user')
        user.update(**userArgs)
        cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        uid = change_password(cur,**user)
    except MissingArgError as e:
        return {'error':str(e)}
    else:
        connection.commit()
        return uid
    finally: 
        cur.close()
    
def adminUserDel_err_hand(connection,**userArgs):
    try:
        uid, delUsername = delete_user(connection,**userArgs)
    except DeleteMissingElementDbError as e:
        return {'error':str(e)}
    else:
        connection.commit()
        return{'uid':uid, 'username':delUsername}

def adminUserPut_err_hand(connection,**modifyArgs):
    try:
        res={'grant_edit':None,'grant_user':None,'grant_admin':None,'revoke_edit':None,'revoke_admin':None,'revoke_user':None,'newPassword':None}
        cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if modifyArgs.get('grant_user'):
            res['grant_user']=grant_user(cur,**modifyArgs)
        if modifyArgs.get('grant_edit'):
            res['grant_edit']=grant_edit(cur,**modifyArgs)
        if modifyArgs.get('grant_admin'):
            res['grant_admin']=grant_admin(cur,**modifyArgs)
        if modifyArgs.get('revoke_user'):
            res['revoke_user']=revoke_user(cur,**modifyArgs)
        if modifyArgs.get('revoke_edit'):
            res['revoke_edit']=revoke_edit(cur,**modifyArgs)
        if modifyArgs.get('revoke_admin'):
            res['revoke_admin']=revoke_admin(cur,**modifyArgs)
        if modifyArgs.get('newPassword'):
            res['newPassword']=change_password(cur,**modifyArgs)
    except (GrantExistingRightError,RevokeUnexistingRightError) as e:
        return {'error':str(e)}
    else:
        connection.commit()
        return res
    finally:
        cur.close()


def adminUserGet_err_hand(connection):
    try:
        cur=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        user_list=get_user_list(cur)
        return user_list
    finally:
        cur.close()

def manageTaxPost_err_hand(connection, **inputTax):
    try:
        res = manageInputTax(connection=connection, insert=True,**inputTax)
    except (MissingArgError,UncompatibilityGbifKeyCanonicalname) as e:
        return{'error':str(e)}
    except (UnauthorizedValueError, DbIntegrityError) as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageTaxDel_err_hand(connection,**delTaxArgs):
    try:
        cd_tax = delTaxArgs.get('cd_tax')
        if delTaxArgs.get('canonicalname') or delTaxArgs.get('scientificname') or delTaxArgs.get('gbifkey'):
            if not checkCdTax(connection=connection, cd_tax=cd_tax, **delTaxArgs):
                raise UncompatibilityCdTaxInputTaxError(cd_tax=cd_tax,inputTax={key:value for (key,value) in delTaxArgs.items() if key in ('canonicalname','scientificname','gbifkey')})
        res = deleteTaxo(connection, cd_tax)
    except (MissingArgError,UncompatibilityGbifKeyCanonicalname,UncompatibilityCdTaxInputTaxError) as e:
        return{'error':str(e)}
    except (UnauthorizedValueError, DbIntegrityError) as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageTaxPut_err_hand(connection,**putTaxArgs):
    try:
        cd_tax = putTaxArgs.get('cd_tax')
        res = modifyTaxo(connection=connection, cd_tax=cd_tax,**putTaxArgs)
    except (MissingArgError,UncompatibilityGbifKeyCanonicalname,AlreadyExistsDbError) as e:
        return{'error':str(e)}
    except (UnauthorizedValueError, DbIntegrityError) as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageEndemPost_err_hand(connection,**inputEndem):
    try:
        res = manageInputTax(connection=connection, insert=True,**inputEndem)
        res.update(manageInputEndem(res.get('cd_tax_acc'), connection = connection, **inputEndem))
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageEndemDel_err_hand(connection,**delEndemArgs):
    try:
        res= deleteEndem(cd_tax=delEndemArgs.get('cd_tax'),connection=connection,**delEndemArgs)
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageEndemPut_err_hand(connection, **putEndemArgs):
    try:
        res= modifyEndem(cd_tax=delEndemArgs.get('cd_tax'),connection=connection,**putEndemArgs)
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res


def manageExotPost_err_hand(connection,**inputExot):
    try:
        res = manageInputTax(connection=connection, insert=True,**inputExot)
        res.update(manageInputExot(res.get('cd_tax_acc'), connection = connection, **inputExot))
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageExotDel_err_hand(connection,**delExotArgs):
    try:
        res= deleteExot(cd_tax=delExotArgs.get('cd_tax'),connection=connection,**delExotArgs)
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageExotPut_err_hand(connection, **putExotArgs):
    try:
        res= modifyExot(cd_tax=delExotArgs.get('cd_tax'),connection=connection,**putExotArgs)
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res


def manageThreatPost_err_hand(connection,**inputThreat):
    try:
        res = manageInputTax(connection=connection, insert=True,**inputThreat)
        res.update(manageInputThreat(res.get('cd_tax_acc'), connection = connection, **inputThreat))
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageThreatDel_err_hand(connection,**delThreatArgs):
    try:
        res= deleteThreat(cd_tax=delThreatArgs.get('cd_tax'),connection=connection,**delThreatArgs)
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageThreatPut_err_hand(connection, **putThreatArgs):
    try:
        res= modifyThreat(cd_tax=delThreatArgs.get('cd_tax'),connection=connection,**putThreatArgs)
    except UnauthorizedValueError as e:
        if e.var in ('threatstatus','priority','endemstatus'):
            return {'error':str(e)}
        else:
            raise Abort500Error(str(e)) from e
    except (UncompatibilityGbifKeyCanonicalname,UncompatibleStatusError,ModifyMissingStatusDbError,MissingArgError) as e:
        return{'error':str(e)}
    except DbIntegrityError as e:
        raise Abort500Error(str(e)) from e
    else:
        return res

def manageRefDel_err_hand(connection, **delRefArgs):
    try:
        if delRefArgs.get('mergeInto'):
            mergeRefs(connection=connection,into_ref=delRefArgs.get('mergeInto'),from_ref=delRefArgs.get('cd_ref'))
        deleteRef(connection,delRefArgs.get('cd_ref'))
    except (UnauthorizedValueError,DeleteMissingElementDbError) as e:
        return {'error':str(e)}
    else:
        connection.commit()

def manageRefPut_err_hand(connection, **putRefArgs):
    try:
        modifyRef(connection, **putRefArgs)
    except ModifyMissingRefDbError as e:
        return {'error':str(e)}
    else:
        connection.commit()
