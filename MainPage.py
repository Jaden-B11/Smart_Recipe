# hello_flask.py
from flask import Flask, render_template, request
import requests, json
from pprint import pprint

# create an instance of Flask
app = Flask(__name__)

spoonacular = "https://api.spoonacular.com/recipes/complexSearch?apiKey=d81ccf44766f404da43f003dccc46f61"

# route decorator binds a function to a URL
@app.route("/", methods=["GET", "POST"])
def search():
  cuisines = ["Any Cuisine", "African", "Asian", "American", "British", "Cajun", "Caribbean", "Chinese", "Eastern European", "European", "French", "German", "Greek", "Indian", "Irish", "Italian", "Japanese", "Jewish", "Korean", "Latin American", "Mediterranean", "Mexican", "Middle Eastern", "Nordic", "Southern", "Spanish", "Thai", "Vietnamese"]
  courses=["Any Course", "Main Course", "Side Dish", "Dessert", "Appetizer", "Salad", "Bread", "Beverage", "Soup", "Beverage", "Sauce", "Marinade", "Fingerfood", "Snack", "Drink"]
  recipes=[]
  if request.method == "POST":
    search=spoonacular
    if request.form.get("query") != "":
      search = f"{search}&"
      if request.form.get("search")=="Matching Text In Title":
        search = f"{search}titleMatch"
      else:
        search = f"{search}query"
      search = f"{search}={request.form.get("query")}"
    if request.form.get("cuisine") != "Any%20Cuisine":
      search = f"{search}&cuisine={request.form.get("cuisine")}"
    if request.form.get("ingredients") != "":
      search = f"{search}&eincludeIngredients={request.form.get("ingredients")}"
    if request.form.get("diets") != "":
      search = f"{search}&diet={request.form.get("diets")}"
    if request.form.get("intolerances") != "":
      search = f"{search}&intolerances={request.form.get("cuisine")}"
    if request.form.get("equipment") != "":
      search = f"{search}&equipment={request.form.get("equipment")}"
    if request.form.get("avoidIngredients") != "":
      search = f"{search}&excludeIngredients={request.form.get("avoidIngredients")}"
    if request.form.get("courses") != "Any%20Course":
      search = f"{search}&type={request.form.get("courses")}"
    if request.form.get("maxTime").isdigit():
      search = f"{search}&maxReadyTime={request.form.get("maxTime")}"
    try:
      print(f"API:{search}")
      r = requests.get(search)
      data = r.json()
      pprint(data)
      recipes=data["results"]
    except:
      print("please try again")
  return render_template("search.html", cuisines=cuisines,courses=courses,method=request.method,recipes=recipes)

@app.route("/recipe")
def recipe():
  ingredients = {"Ingredient1","Ingredient2","Ingredient3"}
  instructions = ["Instruction1","Instruction2","Instruction3"]
  return render_template("recipe.html",ingredients=ingredients,instructions=instructions)