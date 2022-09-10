import email
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt

bcrpyt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$')
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data ['created_at']

        
    @staticmethod
    def validate_input(user):
        is_valid=True
        if len(user['first_name']) < 2:
            flash('First name required.', "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name required.', "register")
            is_valid = False
        if len(user['email']) < 1:
            flash('Email address required.', "register")
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must contain at least 8 characters.', "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address.', "register")
            is_valid=False
        if not PW_REGEX.match(user['password']):
            flash('Make a better password plz', "register")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('login').query_db(query, data)
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('login').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
