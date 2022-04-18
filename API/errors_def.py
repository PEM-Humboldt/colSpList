"""
Definition of the exceptions classes for the API.
In order to understand how they are used please search for explanations in the documentation of the functions which uses them
"""

class MissingArgError(Exception):
    def __init__(self, missingArg, message="Missing arguments which would be necessary for the proper functioning of the current process"):
        self.missingArg = missingArg
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}, missing argument: {self.missingArg}'

class DatabaseUncompatibilityValueError(ValueError):
    pass

class DatabaseUncompatibilityError(Exception):
    pass

class AlreadyExistsDbError(DatabaseUncompatibilityError):
    def __init__(self, value, field, message="already exists in the database"):
        self.value = value
        self.field = field
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.field} {self.value} {self.message}'

class DeleteMissingElementDbError(DatabaseUncompatibilityError):
    def __init__(self, value, field, message="does not exist in the database: impossible to delete"):
        self.value = value
        self.field = field
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.field} {self.value} {self.message}'

class ModifyMissingStatusDbError(DatabaseUncompatibilityError):
    def __init__(self, cd_ref, statustype, message="impossible to modify"):
        self.cd_ref = cd_ref
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Reference {self.cd_ref} does not exist: {self.message}'

class ModifyMissingRefDbError(DatabaseUncompatibilityError):
    def __init__(self, cd_ref, statustype, message="impossible to modify"):
        self.cd_tax = cd_tax
        self.statustype = statustype
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Taxon {self.cd_tax} does not have a {self.statustype} status in the database: {self.message}'

class TaxonNotFoundDbError(DatabaseUncompatibilityError):
    def __init__(self, tax, message="Taxon not recognized"):
        self.tax = tax
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: taxon {self.tax} was not found in the database'

class GrantExistingRightError(DatabaseUncompatibilityError):
    def __init__(self, user, right, message="Attempt to grant existing right"):
        self.user = user
        self.right = right
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: user {self.user} already has {self.right} rights'

class RevokeUnexistingRightError(DatabaseUncompatibilityError):
    def __init__(self, user, right, message="Attempt to revoke unexisting right"):
        self.user = user
        self.right = right
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: user {self.user} has not the {self.right} rights'

class UncompatibilityGbifKeyCanonicalname(DatabaseUncompatibilityError):
    def __init__(self, gbifkey, canonicalname, name_gbifkey, message= "The name corresponding to the gbifkey and the canonical name are not compatible"):
        self.gbifkey = gbifkey
        self.canonicalname = canonicalname
        self.name_gbifkey = name_gbifkey
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} (gbifkey: {self.gbifkey}, canonicalname: {self.canonicalname}, name found from gbifkey: {self.name_gbifkey})'

class DbIntegrityError(Exception):
    def __init__(self, value=None, field=None ,message="Database integrity Error"):
        self.value = value
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        if self.value is not None:
            return f'{self.message} (field: {self.field}, value: {self.value})'
        else:
            return f'{self.message}'

class UncompatibleStatusError(ValueError):
    def __init__(self, dbStatus, providedStatus, message= "Database status and status provided are not compatible, you might want to provide 'priority'"):
        self.dbStatus = dbStatus
        self.providedStatus = providedStatus
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} (database status: {str(self.dbStatus)}, provided status: {str(self.providedStatus)})'
    
class UnauthorizedValueError(ValueError):
    def __init__(self, value=None, var=None, acceptable=[], message="Variable value out of authorized range"):
        self.value=value
        self.var=var
        self.acceptable=acceptable
        self.message=message
        super().__init__(self.message)

    def __str__(self):
        if self.value and self.var and self.acceptable:
            return f'{self.message} (variable: {self.var}, value: {self.value}, acceptable:{str(self.acceptable)})'
        elif self.var and self.value:
            return f'{self.message} (variable: {self.var}, value: {self.value})'
        elif self.value and self.acceptable:
            return f'{self.message} (value: {self.value}, acceptable:{str(self.acceptable)})'
        elif self.var and self.acceptable:
            return f'{self.message} (variable: {self.var}, acceptable:{str(self.acceptable)}))'
        elif self.var :
            return f'{self.message} (variable: {self.var})'
        elif self.acceptable:
            return f'{self.message} (acceptable:{str(self.acceptable)})'
        else :
            return f'{self.message}'

class UncompatibilityCdTaxInputTaxError(DatabaseUncompatibilityValueError):
    def __init__(self, cd_tax, inputTax, message= "The name provided and the cd_tax do not correspond"):
        self.cd_tax = cd_tax
        self.inputTax = inputTax
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} (cd_tax: {str(self.cd_tax)}, inputTax: {str(self.inputTax)})'

class DbIntegrityError(Exception):
    def __init__(self, value=None, field=None ,message="Database integrity Error"):
        self.value = value
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        if self.value is not None:
            return f'{self.message} (field: {self.field}, value: {self.value})'

class UserNotFoundError(DatabaseUncompatibilityError):
    def __init__(self, user=None, message="User not found"):
        self.user = value
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        if self.value is not None:
            return f'{self.message} (user: {str(self.user)})'

class Abort500Error(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}'

