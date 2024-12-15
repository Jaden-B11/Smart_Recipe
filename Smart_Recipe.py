from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from API import fetch_random_recipes, get_recipe_details, clean_description, clean_instructions, API_KEY, requests


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
    # Get form data
    ingredients = request.form.get('ingredients')
    meal_type = request.form.get('meal_type')

    # Convert ingredients into a list
    ingredients_list = [ingredient.strip() for ingredient in ingredients.split(',')]

    # Spoonacular API link
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ','.join(ingredients_list),
        "type": meal_type,
        "number": 6,  # Amount of recipes to be displayed (This can be changed) 
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)
    recipes = response.json()
    
    return render_template('recipe_search_results.html', recipes=recipes)


if __name__ == "__main__":
    app.run(debug=True)
