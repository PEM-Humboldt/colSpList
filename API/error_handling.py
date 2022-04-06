from errors_def import MissingArgError, DatabaseUncompatibilityValueError, DatabaseUncompatibilityError, AlreadyExistsDbError, DeleteMissingElementDbError, ModifyMissingStatusDbError, TaxonNotFoundDbError, GrantExistingRightError, RevokeUnexistingRightError, UncompatibilityGbifKeyCanonicalname, DbIntegrityError, UncompatibleStatusError, UnauthorizedValueError
from taxo import manageInputTax
from flask import abort
from getStatus import testEndemStatus
import psycopg2
from psycopg2 import sql
import psycopg2.extras

def testEndemCatching(connection, **testEndemArgs):
    try:
        res = manageInputTax(connection=conn, insert=False, **testEndemArgs)
        if res.get('alreadyInDb'):
            res.update(testEndemStatus(conn,res.get('cd_tax_acc')))
        else:
            res.update({'hasEndemStatus':False,'cd_status':None,'comments':None,'references':list(),'links':list()})
    except MissingArgError, UncompatibilityGbifKeyCanonicalname as e:
        return {'error':str(e)}
    except UnauthorizedValueError as e:
        if e.var='gbifMatchMode':
            abort(500,str(e))
        else:
            raise
    except DbIntegrityError as e:
        abort(500,str(e))
    else:
        return res
