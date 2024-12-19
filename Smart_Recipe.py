#added my liked recipes button on homepage

from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap5
from API import fetch_random_recipes, get_recipe_details, clean_description, clean_instructions, API_KEY, requests
from pprint import pprint

app = Flask(__name__)
app.secret_key = "CSUMB_OTTER" 
bootstrap = Bootstrap5(app)


@app.route('/')
def home():
    cuisines = ["Any Cuisine", "African", "Asian", "American", "British", "Cajun", "Caribbean", "Chinese", "Eastern European", "European", "French", "German", "Greek", "Indian", "Irish", "Italian", "Japanese", "Jewish", "Korean", "Latin American", "Mediterranean", "Mexican", "Middle Eastern", "Nordic", "Southern", "Spanish", "Thai", "Vietnamese"]
    meal_types = ["Any Course", "Main Course", "Side Dish", "Dessert", "Appetizer", "Salad", "Bread", "Beverage", "Soup", "Beverage", "Sauce", "Marinade", "Fingerfood", "Snack", "Drink"]
    recipes = fetch_random_recipes()


    return render_template('home.html', recipes=recipes, meal_types=meal_types, cuisines=cuisines)

@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    recipe = get_recipe_details(recipe_id)
    isLiked = request.args.get('isLiked', 'no') #Get the isLiked value from query parameters

    previous_page = request.args.get('previous_page', 'home')
    print(f"Previous page: {previous_page}")  #testing

    if recipe:
        recipe['summary'] = clean_description(recipe.get('summary', 'No description available.'))
        recipe['instructions'] = clean_instructions(recipe.get('instructions', 'No instructions available.'))
        return render_template('random_recipes.html', recipe=recipe, previous_page=previous_page, isLiked=isLiked)
    else:
        return "Recipe no longer exists", 404

@app.route('/search', methods=['POST', 'GET']) #added the possibility a GET request if user wants to go back to search results if clicked on a recipe through search function
def search_recipes():
    # Spoonacular API link
    url = "https://api.spoonacular.com/recipes/complexSearch"
    if request.method == 'POST':
        session['params'] = {
            "number": 6,	# Amount of recipes to be displayed (This can be changed) 
            "apiKey": API_KEY
        }
        if request.form.get("query"):
            if request.form.get("search")=="Matching Text In Title":
                session['params']["titleMatch"]=request.form.get("query")
            else:
                session['params']["query"]=request.form.get("query")
        if request.form.get("cuisine") != "Any%20Cuisine":
            session['params']["cuisine"]=request.form.get("cuisine")
        if request.form.get("ingredients"):
            session['params']["includeIngredients"]=request.form.get("ingredients")
        if request.form.get("diets"):
            session['params']["diet"]=request.form.get("diets")
        if request.form.get("intolerances"):
            session['params']["intolerances"]=request.form.get("intolerances")
        if request.form.get("equipment"):
            session['params']["equipment"]=request.form.get("equipment")
        if request.form.get("avoid_ingredients"):
            session['params']["excludeIngredients"]=request.form.get("avoid_ingredients")
        if request.form.get("meal_type") != "Any%20Course":
            session['params']["type"]=request.form.get("meal_type")
        if request.form.get("max_time"):
            session['params']["maxReadyTime"]=request.form.get("max_time")

    params = session.get('params', {})
    print(params)
    response = requests.get(url, params=params)
    recipes = response.json()
    pprint(recipes)

    return render_template('recipe_search_results.html', recipes=recipes.get('results',[]))

@app.route('/like/<int:recipe_id>', methods=['POST'])
def like_recipe(recipe_id):
    # Initialize 'liked_recipes' in the session if it doesn't exist
    if 'liked_recipes' not in session:
        session['liked_recipes'] = []

    recipe = get_recipe_details(recipe_id)
    if recipe:
        liked_recipes = session['liked_recipes']
        # Check if the recipe is already liked
        if recipe_id not in [r['id'] for r in liked_recipes]:
            # Add the recipe details to the liked recipes
            liked_recipes.append({'id': recipe['id'], 'title': recipe['title'], 'image': recipe['image']})
            session['liked_recipes'] = liked_recipes  # Save the updated list to the session
            return redirect(url_for('recipe_details', recipe_id=recipe_id, isLiked='yes'))
    # (add to liked recipes was not clicked) will redirect back to recipe details without showing added to liked recipes alert        
    return redirect(url_for('recipe_details', recipe_id=recipe_id, isLiked='no'))


# Route to view liked recipes
@app.route('/liked_recipes')
def liked_recipes():
    liked_recipes = session.get('liked_recipes', [])

    return render_template('liked_recipes.html', liked_recipes=liked_recipes)

# Route to remove a recipe from the liked list
@app.route('/unlike/<int:recipe_id>', methods=['POST'])
def unlike_recipe(recipe_id):
    liked_recipes = session['liked_recipes']
    session['liked_recipes'] = [r for r in liked_recipes if r['id'] != recipe_id]
    return redirect(url_for('liked_recipes'))

if __name__ == "__main__":
	app.run(debug=True)