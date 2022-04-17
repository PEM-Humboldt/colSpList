"""
Security and user managements
"""
from flask import Flask, render_template, jsonify, current_app, g
from flask_restful import Resource, Api
import psycopg2
import psycopg2.extras
import os
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from errors_def import MissingArgError, AlreadyExistsDbError, DeleteMissingElementDbError, GrantExistingRightError, RevokeUnexistingRightError, UserNotFoundError 

def hash_password(password):
    """
    Return the 'hash' (encrypted version) of a password
    Parameter:
    ==========
    password: Str
        password of the user
    Returns:
    ========
    password_hash: Str 
        encrypted version of the password
    """
    password_hash = pwd_context.hash(password)
    return(password_hash)

def user_exists(cursor,username):
    """
    Test whether a user exists, from its username
    Parameters:
    ==========
    cursor: Psycopg2 cursor
        Cursor of type RealDict in the postgres database
    username: Str
        Name of the user
    """
    SQL = "SELECT count(*) AS nb FROM users WHERE username=%s"
    cursor.execute(SQL,[username])
    res = bool(cursor.fetchone()['nb'])
    return(res)
 
def get_user(cursor, get_hash=False, **user):
    """
    Get the user information about a user from its id or username.

    Parameters:
    -----------
    cursor: Psycopg2 cursor
        Cursor of type RealDict in the postgres database
    get_hash: Bool
        Whether to return the encrypted the encrypted version of the user password
    user: Dict
        dictionary with the following elements:
        id: Int
            identifier of the user (uid)
        username: Str
            name of the user
    Returns:
    -------
    user : Dict
        dictionary with the following elements:
        id: Int
            identifier of the user (uid)
        username: Str
            name of the user
        roles: List(Str)
            roles of the user (associated with permissions in the API)
        password_hash: Str
            encrypted version of the user password
    """
    if user.get('id') is not None:
        SQL = "SELECT * FROM users WHERE id=%s"
        cursor.execute(SQL,[user.get('id')])
    elif user.get('username') is not None: 
        SQL = "SELECT * FROM users WHERE username=%s"
        cursor.execute(SQL,[user.get('username')])
    else:
        raise MissingArgError(missingArg= "'id' or 'username'")
    res0 = cursor.fetchone()
    if len(res0)==0:
        userParts={k:v for (k,v) in user.items() if k in ['id','username']}
        raise UserNotFoundError(user=userParts)
    res=dict(res0)
    user= dict((k, res[k]) for k in ['id','username'] if k in res)
    user['roles'] = list()
    if res.get('apiuser'):
        user['roles'].append('user')
    if res.get('edit_auth'):
        user['roles'].append('edit')
    if res.get('admin'):
        user['roles'].append('admin')
    if(get_hash):
        user.update({"password_hash":res.get('password_hash')})
    return user

def valid_password(cursor,username,password):
    """
    Validate the password of the user and send a boolean (True if the password corresponds)

    Parameters:
    -----------
    cursor: Psycopg2 cursor
        Cursor of type RealDict in the postgres database
    username : Str
        name of the user
    password : Str 
        password of the user (to be tested against the encrypted password) 
    Returns:
    --------
        Bool
        if the password is the right one (when compared with the encrypted version kept in the database), send True
    """
    user = get_user(cursor=cursor, get_hash=True, username=username)
    return pwd_context.verify(password, user.get('password_hash'))

def insert_user(cursor,username,hash_pw):
    """
    Insert a new user in the database

    Parameters:
    -----------
    cursor: Psycopg2 cursor
        Cursor of type RealDict in the postgres database
    username : Str
        name of the user
    hash_pw : Str 
        encrypted password of the user (to be tested against the encrypted password) 

    Returns:
    --------
    id : Int
        identifier of the inserted user
    """
    SQL = "INSERT INTO users(username, password_hash) VALUES(%s,%s) RETURNING id"
    cursor.execute(SQL,[username,hash_pw])
    res = cursor.fetchone()['id']
    return res

def new_user(connection,**userArgs):
    """
    Create a new user in the database

    Parameters:
    -----------
    connection: Psycopg2 connection
        connection to the postgres database
    userArgs: Dict
        dictionary with the following parameters:
        username: Str
            name of the user
        password: Str
            password of the user
    Returns:
    --------
    newId: Int
        Identifier of the new user
    username: Str
        name of the user
    Errors:
    -------
    MissingArgError: Exception
        if the username or the password are missing, send this error with the corresponding missingArg argument
    AlreadyExistsDbError: Exception
        If the user already exists send this error
    """
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    username = userArgs.get('username')
    password = userArgs.get('password')
    if username is None:
        raise MissingArgError(missingArg="'username'")
    if password is None:
        raise MissingArgError(missingArg="'password'")
    if user_exists(cur,username):
        raise AlreadyExistsDbError(value=username, field='username')
    hash_pw = hash_password(password)
    newId = insert_user(cur,username,hash_pw)
    connection.commit()
    cur.close()
    return newId, username

def delete_user(connection, **userArgs):
    """
    Delete a user from the database

    Parameters:
    ----------
    connection: Psycopg2 connection
        connection to the postgres database
    userArgs: Dict
        dictionary with the following elements
        username: Str
            name of the user
        id: Str
            identifier of the user
    Returns:
    --------
    id: Int
        Identifier of the user
    username: Str
        name of the user
    Errors:
    -------
    DeleteMissingElementDbError: Exception
        If the user do not exists, send this error and stop execution before applying change in the database
    """
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    username = userArgs.get('username')
    if(not user_exists(cur,username)):
        raise DeleteMissingElementDbError(value=username, field='username')
    user = get_user(cur, get_hash=False, **userArgs)
    SQL = "DELETE FROM users WHERE id=%s RETURNING id"
    cur.execute(SQL,[user.get('id')])
    res = cur.fetchone()['id']
    connection.commit()
    cur.close()
    return res, username

def grant_user(cursor, **userArgs):
    """
    Grant the "user" role to a user
    
    Parameters:
    -----------
    cursor: Psycopg2 cursor
        Cursor of type RealDict in the postgres database
    userArgs: Dict
        dictionary with the different element:
        username: Str
            name of the user
        id: Int
            Identifier of the user
    Returns:
    --------
    uidUpdated: Int
        identifier of the updated user
    Errors:
    -------
    GrantExistingRightError: Exception
        If the user does not have the user permission and role, send this error and stops
    """
    user=get_user(cursor, get_hash=False, **userArgs)
    if 'user' in user.get('roles'):
        raise GrantExistingRightError(user=user.get('username'), right='user')
    uid=user.get('id')
    SQL = "UPDATE users SET apiuser = TRUE WHERE id=%s RETURNING id"
    cursor.execute(SQL,[uid])
    uidUpdated = cursor.fetchone()['id']
    return uidUpdated

def revoke_user(cursor, **userArgs):
    """
    Revoke the "user" role to a user
    
    Parameters:
    -----------
    cursor: Psycopg2 cursor
        Cursor of type RealDict in the postgres database
    userArgs: Dict
        dictionary with the different element:
        username: Str
            name of the user
        id: Int
            Identifier of the user
    Returns:
    --------
    uidUpdated: Int
        identifier of the updated user
    Errors:
    -------
    RevokeExistingRightError: Exception
        If the user already has the user permission and role, send this error and stops
    """
    user=get_user(cursor, get_hash=False, **userArgs)
    if not 'user' in user.get('roles'):
        raise RevokeUnexistingRightError(user=user.get('username'),right='user')
    uid=user.get('id')
    SQL = "UPDATE users SET apiuser = FALSE WHERE id=%s RETURNING id"
    cursor.execute(SQL,[uid])
    uidUpdated = cursor.fetchone()['id']
    return uidUpdated

def grant_edit(cursor, **userArgs):
    """
    Grant the "edit" role to a user
    
    Parameters:
    -----------
    cursor: Psycopg2 cursor
        Cursor of type RealDict in the postgres database
    userArgs: Dict
        dictionary with the different element:
        username: Str
            name of the user
        id: Int
            Identifier of the user
    Returns:
    --------
    uidUpdated: Int
        identifier of the updated user
    Errors:
    -------
    GrantExistingRightError: Exception
        If the user does not have the edit permission and role, send this error and stops
    """
    user=get_user(cursor, get_hash=False, **userArgs)
    if 'edit' in user.get('roles'):
        raise GrantExistingRightError(user=user.get('username'), right='edit')
    uid=user.get('id')
    SQL = "UPDATE users SET edit_auth = TRUE WHERE id=%s RETURNING id"
    cursor.execute(SQL,[uid])
    uidUpdated = cursor.fetchone()['id']
    return uidUpdated

def revoke_edit(cursor, **userArgs):
    """
    Revoke the "edit" role to a user
    
    Parameters:
    -----------
    cursor: Psycopg2 cursor
        Cursor of type RealDict in the postgres database
    userArgs: Dict
        dictionary with the different element:
        username: Str
            name of the user
        id: Int
            Identifier of the user
    Returns:
    --------
    uidUpdated: Int
        identifier of the updated user
    Errors:
    -------
    RevokeExistingRightError: Exception
        If the user does not have the edit permission and role, send this error and stops
    """
    user=get_user(cursor, get_hash=False, **userArgs)
    if not 'edit' in user.get('roles'):
        raise RevokeUnexistingRightError(user=user.get('username'),right='edit')
    uid=user.get('id')
    SQL = "UPDATE users SET edit_auth = FALSE WHERE id=%s RETURNING id"
    cursor.execute(SQL,[uid])
    uidUpdated = cursor.fetchone()['id']
    return uidUpdated

def grant_admin(cursor, **userArgs):
    """
    Grant the "admin" role to a user
    
    Parameters:
    -----------
    cursor: Psycopg2 cursor
        Cursor of type RealDict in the postgres database
    userArgs: Dict
        dictionary with the different element:
        username: Str
            name of the user
        id: Int
            Identifier of the user
    Returns:
    --------
    uidUpdated: Int
        identifier of the updated user
    Errors:
    -------
    GrantExistingRightError: Exception
        If the user does not have the admin permission and role, send this error and stops
    """
    user=get_user(cursor, get_hash=False, **userArgs)
    if 'admin' in user.get('roles'):
        raise GrantExistingRightError(user=user.get('username'), right='admin')
    uid=user.get('id')
    SQL = "UPDATE users SET admin = TRUE WHERE id=%s RETURNING id"
    cursor.execute(SQL,[uid])
    uidUpdated = cursor.fetchone()['id']
    return uidUpdated

def revoke_admin(cursor, **userArgs):
    """
    Revoke the "admin" role to a user
    
    Parameters:
    -----------
    cursor: Psycopg2 cursor
        Cursor of type RealDict in the postgres database
    userArgs: Dict
        dictionary with the different element:
        username: Str
            name of the user
        id: Int
            Identifier of the user
    Returns:
    --------
    uidUpdated: Int
        identifier of the updated user
    Errors:
    -------
    RevokeExistingRightError: Exception
        If the user does not have the admin permission and role, send this error and stops
    """
    user=get_user(cursor, get_hash=False, **userArgs)
    if not 'admin' in user.get('roles'):
        raise RevokeUnexistingRightError(user=user.get('username'),right='admin')
    uid=user.get('id')
    SQL = "UPDATE users SET admin = FALSE WHERE id=%s RETURNING id"
    cursor.execute(SQL,[uid])
    uidUpdated = cursor.fetchone()['id']
    return uidUpdated

def change_password(cursor, **userArgs):
    """
    Change the password of the user (keep the new encrypted version in the database

    Parameters:
    -----------
    cursor: Psycopg2 cursor
        Cursor of type RealDict in the postgres database
    userArgs: Dict
        dictionary with the different element:
        username: Str
            name of the user
        newPassword: Str
            new password of the user
    Returns:
    --------
    uidUpdated: Int
        identifier of the updated user
    Errors:
    -------
    MissingArgError: Exception
        If the new password is not given, send this error
    """
    user=get_user(cursor, **userArgs)
    if userArgs.get('newPassword') is None:
        raise MissingArgError(missingArg="'newPassword'")
    new_hash=hash_password(userArgs.get('newPassword'))
    SQL = "UPDATE users SET password_hash=%s WHERE id=%s RETURNING id"
    cursor.execute(SQL,[new_hash,user.get('id')])
    uidUpdated= cursor.fetchone()['id']
    return uidUpdated

def generate_auth_token(userId):
    """
    Generate a time-limited (15000 seconds) token, with the user id encrypted version inside
    
    Parameters:
    -----------
    userId: Int
        Identifier of the user in the database
    (SECRET_KEY): Str
        Environment variable containing the encryption key
    Returns:
    --------
    token: Str
        Token containing the user id and the validity time
    """
    sc=os.environ.get('SECRET_KEY')
    s = Serializer(sc,expires_in = 15000)
    return s.dumps({'id':userId})

def verify_auth_token(token,cur):
    """
    Verify the validity of a token, extract the user and send back the user information

    Parameters:
    -----------
    (SECRET_KEY): Str
        Environment variable containing the encryption key
    cur: Psycopg2 cursor
        Cursor of type RealDict in the postgres database
    Returns
    -------
    None if the token does not correspond to any user, or the signature is expired, or is invalid, send the user information otherwise
    """
    sc=os.environ.get('SECRET_KEY')
    s = Serializer(sc)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token
    user=get_user(cur, get_hash=False,id=data['id'])
    return user

def get_user_list(cursor):
    """
    Get the list of the users and their roles/permissions

    Parameters:
    -----------
    cursor: Psycopg2 cursor
        cursor in the connection to the postgres database
    Returns:
    --------
    res: List
        List of dictionaries with the following elements:
        uid: Int
            identifier of the user in the database
        username: Str
            name of the user
        roles: List(Str)
            roles/permissions of the user (admin, edit, user)
    """
    SQL = "SELECT id as uid, username,apiuser AS user,edit_auth AS edit, admin FROM users"
    cursor.execute(SQL)
    res=cursor.fetchall()
    for i in res:
        i['roles']=[]
        if i.pop('user'):
            i['roles']+=['user']
        if i.pop('admin'):
            i['roles']+=['admin']
        if i.pop('edit'):
            i['roles']+=['edit']
    return res

