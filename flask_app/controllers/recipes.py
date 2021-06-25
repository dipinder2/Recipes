from flask import render_template, request, session, redirect
from flask_app import app
from flask_app.models import recipe
	
@app.route('/add', methods=['POST','GET'])
def add_recipe():
	if request.method == 'GET':
		return render_template('recipe.html')

	if not recipe.Recipe.validate(request.form):
		return redirect('/add')
	data = {}
	data.update(request.form)
	data["user_id"] = session["uuid"]
	recipe.Recipe.add_one(data)
	return redirect("/dashboard")

	
@app.route('/delete/<int:id>')
def delete_recipe(id):
	recipe.Recipe.delete_one({"id":id})
	return redirect('/dashboard')


	
@app.route('/update/<int:id>', methods=['POST','GET'])
def update_recipe(id):
	if request.method == 'GET':
		recipex = recipe.Recipe.get_one({"id":id})
		created_at = str(recipex.created_at).split(" ")
		return render_template('edit.html', recipe = recipex, created_at=created_at[0])

	if not recipe.Recipe.validate(request.form):
		return redirect(f'/update/{id}')
	data = {}
	data.update(request.form)
	data["id"] = id
	data["user_id"] = session["uuid"]
	recipe.Recipe.update(data)
	return redirect('/dashboard')


	
@app.route('/view/<int:id>')
def view_recipe(id):

	return render_template('show.html', recipe = recipe.Recipe.get_one({'id':id}))


