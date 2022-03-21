from flask import Flask, render_template, jsonify
from flask_restful import Resource, Api
import psycopg2
import os
from passlib.apps import custom_app_context as pwd_context



def hash_password(password):
    password_hash = pwd_context.encrypt(password)
    return(password_hash)

def user_exists(cursor,username):
    SQL = "SELECT count(*) AS nb FROM users WHERE username=%s"
    cursor.execute(SQL,[username])
    res = bool(cursor.fetchone()['nb'])
    return(res)
    
def get_user(cursor,username):
    SQL = "SELECT * FROM users WHERE username=%s"
    cursor.execute(SQL,[username])
    res = dict(cursor.fetchone())
    return(res)

def verify_password(cursor,username,password):
    user = get_user(cursor,username)
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
    if username is None
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


def delete_user(connection, username):
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if(not user_exists(cur,username)):
        raise Exception("Attempt to deleting an inexisting user")
    user = get_user(cursor, username)
    SQL = "DELETE FROM user WHERE id=%s RETURNING id"
    cursor.execute(SQL,[user.get('id')])
    res = cursor.fetchone()['id']
    return res
    
    
