from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user

from flask import flash

class Date:
    db = 'healthcare_inc_2'

    def __init__(self, data):
        self.id = data['id']
        self.care_date = data['care_date']
        self.provider_name = data['provider_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def create_one(cls, data ):
        query = """
        INSERT INTO dates ( care_date, provider_name, created_at, updated_at, users_id) 
        VALUES ( %(care_date)s , %(provider_name)s, NOW() , NOW(), %(users_id)s )
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        flash("Account creation successful")
        print(results)
        return results

    @classmethod
    def validate_create(cls, data):
        is_valid = True
        if not data:
            flash("Please enter a date")
            is_valid = False
        return is_valid

    @classmethod
    def get_all_with_creator(cls):
        query = """
        SELECT * FROM dates 
        LEFT JOIN users ON dates.users_id = users.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        all_dates = []
        for one_date in results:
            date_data = {
                "id": one_date['id'],
                "care_date": one_date['care_date'],
                "provider_name": one_date['provider_name'],
                "created_at": one_date['created_at'],
                "updated_at": one_date['updated_at']
            }
            single_date = cls(date_data)
            user_data = {
                "id": one_date['users.id'],
                "first_name": one_date['first_name'],
                "last_name": one_date['last_name'],
                "email": one_date['email'],
                "insurance_name": one_date['insurance_name'],
                "password": one_date['password'],
                "created_at": one_date['users.created_at'],
                "updated_at": one_date['users.updated_at']
            }
            single_user = user.User(user_data)
            single_date.creator = single_user
            all_dates.append(single_date)
        return all_dates

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM dates WHERE dates.id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return results

    @classmethod
    def sort_by_date(cls):
        query = """
        SELECT * FROM dates 
        LEFT JOIN users ON dates.users_id = users.id
        ORDER BY care_date ASC
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        all_dates = []
        for one_date in results:
            date_data = {
                "id": one_date['id'],
                "care_date": one_date['care_date'],
                "provider_name": one_date['provider_name'],
                "created_at": one_date['created_at'],
                "updated_at": one_date['updated_at']
            }
            single_date = cls(date_data)
            user_data = {
                "id": one_date['users.id'],
                "first_name": one_date['first_name'],
                "last_name": one_date['last_name'],
                "email": one_date['email'],
                "insurance_name": one_date['insurance_name'],
                "password": one_date['password'],
                "created_at": one_date['users.created_at'],
                "updated_at": one_date['users.updated_at']
            }
            single_user = user.User(user_data)
            single_date.creator = single_user
            all_dates.append(single_date)
        return all_dates

    @classmethod
    def sort_by_provider_name(cls):
        query = """
        SELECT * FROM dates 
        LEFT JOIN users ON dates.users_id = users.id
        ORDER BY provider_name ASC
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        all_dates = []
        for one_date in results:
            date_data = {
                "id": one_date['id'],
                "care_date": one_date['care_date'],
                "provider_name": one_date['provider_name'],
                "created_at": one_date['created_at'],
                "updated_at": one_date['updated_at']
            }
            single_date = cls(date_data)
            user_data = {
                "id": one_date['users.id'],
                "first_name": one_date['first_name'],
                "last_name": one_date['last_name'],
                "email": one_date['email'],
                "insurance_name": one_date['insurance_name'],
                "password": one_date['password'],
                "created_at": one_date['users.created_at'],
                "updated_at": one_date['users.updated_at']
            }
            single_user = user.User(user_data)
            single_date.creator = single_user
            all_dates.append(single_date)
        return all_dates