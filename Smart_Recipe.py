from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from API import fetch_random_recipes, get_recipe_details, clean_description, clean_instructions, API_KEY, requests

app = Flask(__name__)
bootstrap = Bootstrap5(app)

def fetch_image():
        response = requests.get('https://foodish-api.com/api/')
        if response.status_code == 200:
            results = response.json()
            print(results) 
            img = results.get('image') 
            print(img)  
            return img

@app.route('/')
def home():
    recipes = fetch_random_recipes()
    background_image = fetch_image()
    return render_template('home.html', recipes=recipes, background_image=background_image)


@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    background_image = fetch_image()

    recipe = get_recipe_details(recipe_id)
    if recipe:
        recipe['summary'] = clean_description(recipe.get('summary', 'No description available.'))
        recipe['instructions'] = clean_instructions(recipe.get('instructions', 'No instructions available.'))
        return render_template('random_recipes.html', recipe=recipe, background_image=background_image)
    else:
        return "Recipe no longer exists", 404

        
@app.route('/search', methods=['POST'])
def search_recipes():
    # Get form data
    ingredients = request.form.get('ingredients')
    meal_type = request.form.get('meal_type')
    cuisine = request.form.get('cuisine')
    
    # Convert ingredients into a list
    ingredients_list = [ingredient.strip() for ingredient in ingredients.split(',')]

    # Spoonacular API link
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ','.join(ingredients_list),
        "type": meal_type,
        "cuisine": cuisine,  # New parameter for cuisine type
        "number": 6,  # Amount of recipes to be displayed (This can be changed) 
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)
    recipes = response.json()

    background_image = fetch_image()

    return render_template('recipe_search_results.html', recipes=recipes, background_image=background_image)


if __name__ == "__main__":
    app.run(debug=True)