"""
Base class:
1.Exception: Base class for all exceptions
2. StopIteration: Raised when the next() method of an iterator does not point to any object.
3. SystemExit: Raised by the sys.exit() function.
4. StandardError: Base class for all built-in exceptions except StopIteration and SystemExit.
5. ArithmeticError: Base class for all errors that occur for numeric calculation.
6. OverflowError: Raised when a calculation exceeds maximum limit for a numeric type.
7. FloatingPointError: Raised when a floating point calculation fails.
8. ZeroDivisionError: Raised when division or modulo by zero takes place for all numeric types.
9. AssertionError: Raised in case of failure of the Assert statement.
10. AttributeError: Raised in case of failure of attribute reference or assignment.
11. EOFError: Raised when there is no input from either the raw_input() or input() function and the end of file is reached.
12.ImportError: Raised when an import statement fails.
13. KeyboardInterrupt: Raised when the user interrupts program execution, usually by pressing Ctrl+c.
14. LookupError: Base class for all lookup errors.
15. IndexError: Raised when an index is not found in a sequence.
16. KeyError: Raised when the specified key is not found in the dictionary.
17. NameError: Raised when an identifier is not found in the local or global namespace.
18. UnboundLocalError: Raised when trying to access a local variable in a function or method but no value has been assigned to it.
19. EnvironmentError: Base class for all exceptions that occur outside the Python environment.
20. IOError: Raised when an input/ output operation fails, such as the print statement or the open() function when trying to open a file that does not exist.
21. IOError: Raised for operating system-related errors.
22. SyntaxError: Raised when there is an error in Python syntax.
23. IndentationError: Raised when indentation is not specified properly.
24. SystemError: Raised when the interpreter finds an internal problem, but when this error is encountered the Python interpreter does not exit.
25. SystemExit: Raised when Python interpreter is quit by using the sys.exit() function. If not handled in the code, causes the interpreter to exit.
26. TypeError: Raised when an operation or function is attempted that is invalid for the specified data type.
27. ValueError: Raised when the built-in function for a data type has the valid type of arguments, but the arguments have invalid values specified.
28. RuntimeError: Raised when a generated error does not fall into any category.
29.NotImplementedError: Raised when an abstract method that needs to be implemented in an inherited class is not actually implemented.
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
    def __init__(self, cd_tax, statustype, message="impossible to modify"):
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
        return f'{self.message} (database status: {str(self.dbStatus)}, canonicalname: {str(self.providedStatus)})'
    
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
            


