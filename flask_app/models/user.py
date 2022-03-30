from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)

class User:
    db = 'healthcare_inc_2'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.insurance_name = data['insurance']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

## CREATE ##
    @classmethod
    def register(cls, data ):
        query = """
        INSERT INTO users ( first_name, last_name, email, password, insurance_providers_id, created_at, updated_at ) 
        VALUES ( %(first_name)s , %(last_name)s , %(email)s, %(password)s, %(insurance_providers_id)s, NOW() , NOW() )
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        flash("Account creation successful")
        print(results)
        return results

## READ ##
    @classmethod
    def get_user_by_email(cls, data):
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_user_by_id(cls, data):
        query = """
        SELECT *
        FROM users
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        users = []
        for user in results:
            users.append(cls(user))
        return users

## UPDATE ##
# Add update methods here #

    @classmethod
    def update_one(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s, WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return results

## DELETE ##
# Add delete methods here #
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM users WHERE users.id=%(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        return results

## VALIDATE ##
# Below is what I did for validation logic on my project. We can change it up, delete it, or use any parts.

    @classmethod
    def validate_account(cls, data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        # Check to make sure everything is submitted
        if not data['first_name']:
            flash("First name field must be submitted.")
            is_valid = False
        if not data['last_name']:
            flash("Last name field must be submitted.")
            is_valid = False
        if not data['email']:
            flash("Email field must be submitted.")
            is_valid = False
        if not data['password']:
            flash("Password field must be submitted.")
            is_valid = False
        if not data['confirm_password']:
            flash("Confirm password field must be submitted.")
            is_valid = False
        # Check names for proper length
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 letters")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 letters")
            is_valid = False
        # Verify names are alphabetical only
        for character in data['first_name']:
            if character.isalpha():
                continue
            else:
                flash("Names can only be alphabetical")
                is_valid = False
        for character in data['last_name']:
            if character.isalpha():
                continue
            else:
                flash("Names can only be alphabetical")
                is_valid = False
        # Validate email format
        if not EMAIL_REGEX.match(data['email']):
            flash("Email format is invalid")
            is_valid = False
        # Check if email is already present in database
        query = """
        SELECT email
        FROM users
        WHERE email = %(email)s
        ;"""
        result = connectToMySQL(cls.db).query_db( query, data )
        if result:
            flash("Email address already in use.")
            is_valid = False
        #Validate password length
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        #Verify password matches confirmation
        if not data['password'] == data['confirm_password']:
            flash("Passwords do not match")
            is_valid = False
        print("Validation completed successfully, no errors found.")
        return is_valid


## HASH ##
# This is just for hashing/salting our user passwords before storing them in the DB. Can delete the below code if we wanna do it another way. 

    @staticmethod
    def prep_data(data):
        parsed_data = {
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
            'email' : data['email'],
            'password' : bcrypt.generate_password_hash(data['password'])
        }
        return parsed_data