
from flask import Flask, render_template
from flask_app import app
from flask_app.controllers import users,recipes
if __name__ == '__main__':
  app.run(debug=True)
 
