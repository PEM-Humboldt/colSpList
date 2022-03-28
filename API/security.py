from flask import Flask, render_template, jsonify, current_app, g
from flask_restful import Resource, Api
import psycopg2
import psycopg2.extras
import os
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer                          as Serializer, BadSignature, SignatureExpired)

def hash_password(password):
    password_hash = pwd_context.hash(password)
    return(password_hash)

def user_exists(cursor,username):
    SQL = "SELECT count(*) AS nb FROM users WHERE username=%s"
    cursor.execute(SQL,[username])
    res = bool(cursor.fetchone()['nb'])
    return(res)
    
def get_user(cursor, get_hash=False, **user):
    if user.get('id') is not None:
        SQL = "SELECT * FROM users WHERE id=%s"
        cursor.execute(SQL,[user.get('id')])
    elif user.get('username') is not None: 
        SQL = "SELECT * FROM users WHERE username=%s"
        cursor.execute(SQL,[user.get('username')])
    else:
        raise Exception("Impossible to get the user information without id or username")
    res = dict(cursor.fetchone())
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
    user = get_user(cursor=cursor, get_hash=True, username=username)
    return pwd_context.verify(password, user.get('password_hash'))

def insert_user(cursor,username,hash_pw):
    SQL = "INSERT INTO users(username, password_hash) VALUES(%s,%s) RETURNING id"
    cursor.execute(SQL,[username,hash_pw])
    res = cursor.fetchone()['id']
    return res

def new_user(connection,**userArgs):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    username = userArgs.get('username')
    password = userArgs.get('password')
    if username is None:
        raise Exception("No username provided")
    if password is None:
        raise Exception("No password provided")
    if user_exists(cur,username):
        raise Exception("User already exists")
    hash_pw = hash_password(password)
    newId = insert_user(cur,username,hash_pw)
    connection.commit()
    cur.close()
    return newId, username

def delete_user(connection, **userArgs):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    username = userArgs.get('username')
    if(not user_exists(cur,username)):
        raise Exception("Attempt to deleting an inexisting user")
    user = get_user(cur, get_hash=False, **userArgs)
    SQL = "DELETE FROM users WHERE id=%s RETURNING id"
    cur.execute(SQL,[user.get('id')])
    res = cur.fetchone()['id']
    connection.commit()
    cur.close()
    return res, username

def grant_user(cursor, **userArgs):
    user=get_user(cursor, get_hash=False, **userArgs)
    if 'user' in user.get('roles'):
        raise Exception("This user was already an API user")
    uid=user.get('id')
    SQL = "UPDATE users SET apiuser = TRUE WHERE id=%s RETURNING id"
    cursor.execute(SQL,[uid])
    uidUpdated = cursor.fetchone()['id']
    return uidUpdated

def revoke_user(cursor, **userArgs):
    user=get_user(cursor, get_hash=False, **userArgs)
    if 'user' in user.get('roles'):
        raise Exception("This user was not an API user")
    uid=user.get('id')
    SQL = "UPDATE users SET apiuser = FALSE WHERE id=%s RETURNING id"
    cursor.execute(SQL,[uid])
    uidUpdated = cursor.fetchone()['id']
    return uidUpdated

def grant_edit(cursor, **userArgs):
    user=get_user(cursor, get_hash=False, **userArgs)
    if 'edit' in user.get('roles'):
        raise Exception("This user had already been granted edition rights")
    uid=user.get('id')
    SQL = "UPDATE users SET edit_auth = TRUE WHERE id=%s RETURNING id"
    cursor.execute(SQL,[uid])
    uidUpdated = cursor.fetchone()['id']
    return uidUpdated

def revoke_edit(cursor, **userArgs):
    user=get_user(cursor, get_hash=False, **userArgs)
    if not 'edit' in user.get('roles'):
        raise Exception("This user had no edition rights")
    uid=user.get('id')
    SQL = "UPDATE users SET edit_auth = FALSE WHERE id=%s RETURNING id"
    cursor.execute(SQL,[uid])
    uidUpdated = cursor.fetchone()['id']
    return uidUpdated

def grant_admin(cursor, **userArgs):
    user=get_user(cursor, get_hash=False, **userArgs)
    if 'admin' in user.get('roles'):
        raise Exception("This user was already an API user")
    uid=user.get('id')
    SQL = "UPDATE users SET admin = TRUE WHERE id=%s RETURNING id"
    cursor.execute(SQL,[uid])
    uidUpdated = cursor.fetchone()['id']
    return uidUpdated

def revoke_admin(cursor, **userArgs):
    user=get_user(cursor, get_hash=False, **userArgs)
    if not 'admin' in user.get('roles'):
        raise Exception("This user was already an API user")
    uid=user.get('id')
    SQL = "UPDATE users SET admin = FALSE WHERE id=%s RETURNING id"
    cursor.execute(SQL,[uid])
    uidUpdated = cursor.fetchone()['id']
    return uidUpdated

def change_password(cursor, **userArgs):
    user=get_user(cursor, **userArgs)
    if userArgs.get('newPassword') is None:
        raise Exception("Impossible to change the password without a new password")
    new_hash=hash_password(userArgs.get('newPassword'))
    SQL = "UPDATE users SET password_hash=%s WHERE id=%s RETURNING id"
    cursor.execute(SQL,[user.get('id'),new_hash])
    uidUpdated= cursor.fetchone()['id']
    return uidUpdated

def generate_auth_token(connection,userId):
    cur= connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sc=os.environ.get('SECRET_KEY')
    cur.close()
    s = Serializer(sc,expires_in = 240)
    return s.dumps({'id':userId})

def verify_auth_token(token,cur):
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
    SQL = "SELECT id, username,apiuser,edit_auth,admin FROM users"
    cursor.execute(SQL)
    res=cursor.fetchall()
    return res
