# hello_flask.py
from flask import Flask, render_template

# create an instance of Flask
app = Flask(__name__)

# route decorator binds a function to a URL
@app.route('/')
def search():
  return render_template('search.html')

@app.route('/recipe')
def recipe():
  return render_template('recipe.html')