
from ..configs.mysqlconnection import connectToMySQL
from ..models import user
from flask import flash
class Recipe:
	def __init__(self,data):
		for k,v in data.items():
			setattr(self,k,v)	
		self.user = user.User.get_by_id({"id":data["user_id"]})


	@classmethod
	def get_all(cls):
		query = "SELECT * FROM recipes;"
		results = connectToMySQL().query_db(query)
		obj_list = []
		for res in results:
			obj_list.append(cls(res))
		return obj_list


	@classmethod
	def get_one(cls,data):
		query = "SELECT * FROM recipes "\
		"LEFT JOIN users "\
		"ON recipes.user_id = users.id "\
		"WHERE recipes.id = %(id)s;"
		results = connectToMySQL().query_db(query,data)
		recipe = cls(results[0])
		if results[0]["users.id"] is not None:
			rows = {}
			for res in results:
				rows = {}
				rows.update(res)
				rows["id"] = res["users.id"]
		return recipe


	@classmethod
	def add_one(cls, data):
		query = "INSERT INTO recipes " \
		"VALUES(NULL, %(name)s, %(underthirty)s, %(description)s, %(instructions)s, "\
		"%(created_at)s, NOW(), %(user_id)s);"
		return connectToMySQL().query_db(query,data)


	@classmethod
	def delete_one(cls,data):
		query = "DELETE FROM recipes WHERE id = %(id)s;"
		connectToMySQL().query_db(query, data)


	@classmethod
	def update(cls, data):
		query = "UPDATE recipes "\
		"SET name = %(name)s, underthirty = %(underthirty)s, description= %(description)s, " \
		"instructions = %(instructions)s, created_at = %(created_at)s ,updated_at = NOW() WHERE id = %(id)s;"
		connectToMySQL().query_db(query, data)


	@staticmethod
	def validate(data):
		is_valid=True
		if len(data['name'])<2:
			flash("Name needs more characters")
			is_valid = False		
		if len(data['description'])<10:
			flash("description needs more characters")
			is_valid = False		
		if len(data['instructions'])<10:
			flash("instructions needs more characters")
			is_valid = False

		return is_valid