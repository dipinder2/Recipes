
from ..configs.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
from ..models import recipe
import re

bcrypt = Bcrypt(app)

class User:
	def __init__(self,data):
		for k,v in data.items():
			setattr(self,k,v)
		self.recipes = []

	@classmethod
	def get_all(cls):
		query = "SELECT * FROM users;"
		results = connectToMySQL().query_db(query)
		obj_list = []
		for res in results:
			obj_list.append(cls(res))
		return obj_list


	@classmethod
	def get_by_email(cls,data):
		query = "SELECT * FROM users WHERE email = %(email)s;"
		result = connectToMySQL().query_db(query, data)
		if len(result)<1:
			return []
		return cls(result[0])	


	@classmethod
	def get_by_id(cls,data):
		query = "SELECT * FROM users WHERE id = %(id)s;"
		result = connectToMySQL().query_db(query, data)
		return cls(result[0])



	@classmethod
	def get_one(cls,data):
		query = "SELECT * FROM users "\
		"LEFT JOIN recipes "\
		"ON users.id = recipes.user_id "\
		"WHERE users.id = %(id)s;"
		results = connectToMySQL().query_db(query,data)
		user = cls(results[0])

		if results[0]["recipes.id"] is not None:
			for res in results:
				rows = {}
				rows.update(res)
				rows["id"] = res["recipes.id"]
				rows["created_at"] = res["recipes.created_at"]
				rows["updated_at"] = res["recipes.updated_at"]
				user.recipes.append(recipe.Recipe(rows))

		return user


	@classmethod
	def create(cls, data):
		query = "INSERT INTO users " \
		"VALUES(NULL, %(first_name)s, %(last_name)s, "\
		"%(email)s, %(password)s, NOW(), NOW());"
		return connectToMySQL().query_db(query,data)


	@classmethod
	def delete_one(cls,data):
		query = "DELETE FROM users WHERE id = %(id)s;"
		connectToMySQL().query_db(query, data)


	@staticmethod
	def register_validator(post_data):
	    is_valid = True

	    if len(post_data['first_name']) < 2:
	        flash("First name must be at least 2 characters.")
	        is_valid = False
	    if len(post_data['last_name']) < 2:
	        flash("Last name must be at least 2 characters.")
	        is_valid = False

	    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
	    if not EMAIL_REGEX.match(post_data['email']):
	        flash("Email is in invalid format")
	        is_valid = False

	    if len(post_data['password']) < 4:
	        flash("Password must be at least 4 characters.")
	        is_valid = False
	    else:
	        if post_data['password'] != post_data['confirm_password']:
	            flash("Password and Confirm password must match")
	            is_valid = False

	    return is_valid


	@staticmethod
	def login_validator(post_data):
	    user_from_db = User.get_by_email({'email': post_data['email']})
	    # user_form_db will be None if that email is not in the DB
	    if not user_from_db:
	        flash("Invalid Credentials.")
	        return False

	    if not bcrypt.check_password_hash(user_from_db.password, post_data['password']):
	        flash("Invalid Credentials")
	        return False
	    
	    return True