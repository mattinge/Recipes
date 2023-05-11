from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

db="recipes_schema"

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def create_recipe(cls, data):
        if not cls.valid_recipe(data):
            return False
        
        query = """INSERT INTO recipes (name, description, instructions, data_made, under_30, user_id)
        VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s);"""
        results = connectToMySQL(db).query_db(query, data)
        recipe = cls.get_recipe_by_id(results)

        return recipe

    @classmethod
    def get_all_recipes(cls):
        query = """SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"""
        results = connectToMySQL(db).query_db(query)
        all_recipes = []
        for row in results:
            a_recipe = cls(row)

            a_recipe.user = user.User({
                'id': row['users.id'],
                'first_name': row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            })
            all_recipes.append(a_recipe)
        return all_recipes


    @classmethod
    def get_recipe_by_id(cls, recipe_id):
        data = {"id": recipe_id}
        query = """SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"""
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        result = results[0]
        recipe = cls(result)

        recipe.user = user.User({
            "id": result["user_id"],
            "first_name": result["first_name"],
            "last_name": result["last_name"],
            "email": result["email"],
            "created_at": result["users.created_at"],
            "updated_at": results["users.updated_at"]
        })
        return recipe

    
    @classmethod
    def edit_recipe(cls, data, session_id):
        recipe = cls.get_recipe_by_id(data['id'])
        if recipe.user.id != session_id:
            return False
        
        if not cls.valid_recipe(data):
            return False

        query = """UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s,
        date_made = %(date_made)s, under_30 = %(under_30)s WHERE id = %(id)s;"""
        result = connectToMySQL(db).query_db(query, data)
        recipe = cls.get_recipe_by_id(data['id'])
        return recipe

    @classmethod
    def delete_recipe(cls, recipe_id):
        data = {"id": recipe_id}
        query = """DELETE FROM recipes WHERE id = %(id)s;"""
        connectToMySQL(db).query_db(query, data)
        return recipe_id

    @staticmethod
    def valid_recipe(data):
        is_valid=True

        if len(data['name']) < 3:
            flash('Name field must be at least 3 characters long.')
            is_valid = False
        if len(data['description']) < 3:
            flash('Description field must be at least 3 characters long.')
            is_valid = False
        if len(data['instructions']) < 3:
            flash('Instructions field must be at least 3 characters long')
            is_valid = False
        if len(data['data_made']) <= 0:
            flash('Date is required')
            is_valid = False
        if "under_30" not in data:
            flash("Is recipe less than 30 min?")
            is_valid = False
        
        return is_valid