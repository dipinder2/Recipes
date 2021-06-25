from flask import render_template, request, session, redirect
from flask_bcrypt import Bcrypt

from flask_app import app
from ..models import user,recipe
bcrypt = Bcrypt(app) #instantiating the Bcrypt class passing the flask app


@app.route("/")
def index():
	if "uuid" in session:
	    return redirect("/dashboard")
	return render_template("index.html")


@app.route("/register", methods = ["POST"])
def register():
	if not user.User.register_validator(request.form):
	    return redirect("/")
	hash_browns = bcrypt.generate_password_hash(request.form['password'])
	data = {
	    "first_name": request.form['first_name'],
	    "last_name": request.form['last_name'],
	    "email": request.form['email'],
	    "password": hash_browns
	}
	user_id = user.User.create(data)
	session['uuid'] = user_id
	return redirect("/dashboard")


@app.route("/login", methods = ["POST"])
def login():
	if not user.User.login_validator(request.form):
	    return redirect("/")
	userx = user.User.get_by_email({"email": request.form['email']})
	session['uuid'] = userx.id
	return redirect("/dashboard")


@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")


	
@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html', user = user.User.get_one({"id":session["uuid"]}), recipes = recipe.Recipe.get_all())

