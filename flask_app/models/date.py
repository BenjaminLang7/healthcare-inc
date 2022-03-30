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