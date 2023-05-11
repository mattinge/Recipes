from flask_app.config.mysqlconnection import connectToMySQL
from flask import  flash, request
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = "recipes_schema"


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


#classmethods
    @classmethod
    def save_user(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_user_by_id(cls, data):
        
        query = """SELECT * FROM users WHERE id = %(id)s;"""
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_user_by_email(cls, data):
        query = """SELECT * FROM users WHERE email = %(email)s;"""
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

#staticmethods
    @staticmethod
    def validate_registration(data):
        is_valid = True
        query = """SELECT * FROM users WHERE email = %(email)s;"""
        results = connectToMySQL(db).query_db(query, data)

        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters long.", "register")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters long.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Email not valid format.", "register")
            is_valid = False
        if len(results) >= 1:
            flash('')
            is_valid = False
        if len(data['email']) < 2:
            flash('Email must be at least 2 characters long.', "register")
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be 8 characters.', "register")
            is_valid = False
        if data['password'] != data['c_password']:
            flash('Passwords do no match.' "register")
            is_valid = False
        
        
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        
        query = """SELECT * FROM users WHERE email = %(email)s;"""
        results = connectToMySQL(db).query_db(query, user)

        if len(results) == 0 or not EMAIL_REGEX.match(user['email']):
            flash("Invalid email", 'login')
            is_valid = False
        if results is False:
            flash("Incorrect Email or Password", 'login')
            is_valid = False
        if len(user['password']) < 8 or not bcrypt.check_password_hash(request.form['password'], user['password']):
            flash('Incorrect Email or Password')
            is_valid = False
        
        return is_valid