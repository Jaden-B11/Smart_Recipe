from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from API import fetch_random_recipes, get_recipe_details, clean_description, clean_instructions, API_KEY, requests
from pprint import pprint

app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/')
def home():
	cuisines = ["Any Cuisine", "African", "Asian", "American", "British", "Cajun", "Caribbean", "Chinese", "Eastern European", "European", "French", "German", "Greek", "Indian", "Irish", "Italian", "Japanese", "Jewish", "Korean", "Latin American", "Mediterranean", "Mexican", "Middle Eastern", "Nordic", "Southern", "Spanish", "Thai", "Vietnamese"]
	meal_types=["Any Course", "Main Course", "Side Dish", "Dessert", "Appetizer", "Salad", "Bread", "Beverage", "Soup", "Beverage", "Sauce", "Marinade", "Fingerfood", "Snack", "Drink"]
	recipes = fetch_random_recipes()
	return render_template('home.html', recipes=recipes, meal_types=meal_types, cuisines=cuisines)

@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
	recipe = get_recipe_details(recipe_id)
	if recipe:
		recipe['summary'] = clean_description(recipe.get('summary', 'No description available.'))
		recipe['instructions'] = clean_instructions(recipe.get('instructions', 'No instructions available.'))
		return render_template('random_recipes.html', recipe=recipe)
	else:
		return "Recipe no longer exists", 404

@app.route('/search', methods=['POST'])
def search_recipes():
	# Spoonacular API link
	url = "https://api.spoonacular.com/recipes/complexSearch"
	params = {
		"number": 6,	# Amount of recipes to be displayed (This can be changed) 
		"apiKey": API_KEY
	}
	if request.form.get("query"):
		if request.form.get("search")=="Matching Text In Title":
			params["titleMatch"]=request.form.get("query")
		else:
			params["query"]=request.form.get("query")
	if request.form.get("cuisine") != "Any%20Cuisine":
		params["cuisine"]=request.form.get("cuisine")
	if request.form.get("ingredients"):
		params["includeIngredients"]=request.form.get("ingredients")
	if request.form.get("diets"):
		params["diet"]=request.form.get("diets")
	if request.form.get("intolerances"):
		params["intolerances"]=request.form.get("intolerances")
	if request.form.get("equipment"):
		params["equipment"]=request.form.get("equipment")
	if request.form.get("avoid_ingredients"):
		params["excludeIngredients"]=request.form.get("avoid_ingredients")
	if request.form.get("meal_type") != "Any%20Course":
		params["type"]=request.form.get("meal_type")
	if request.form.get("max_time"):
		params["maxReadyTime"]=request.form.get("max_time")
	print(params)
	response = requests.get(url, params=params)
	if response.status_code == 200:
		recipes = response.json()
		pprint(recipes)
	else:
		recipes = {"Error":response.status_code}
	return render_template('recipe_search_results.html', recipes=recipes['results'])


if __name__ == "__main__":
	app.run(debug=True)