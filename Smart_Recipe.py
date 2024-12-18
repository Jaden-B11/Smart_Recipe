#Course: CST 205
#Title: Smart Recipe
#Abstract: This project uses an API to pull in a large amount of recipes, in which the user can view, like, and search for recipes. 
#Authors: Alan Eckhaus, Zainab Abbasi, Jaden Bartram, Joseph Bravo
#Date: November - December 18



#added my liked recipes button on homepage

from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap5
from API import fetch_random_recipes, get_recipe_details, clean_description, clean_instructions, API_KEY, requests


app = Flask(__name__)
app.secret_key = "CSUMB_OTTER" 
bootstrap = Bootstrap5(app)

# def fetch_image():
#     response = requests.get('https://foodish-api.com/api/')
#     if response.status_code == 200:
#         results = response.json()
#         print(results) 
#         img = results.get('image') 
#         print(img)  
#         return img


@app.route('/')
def home():
    recipes = fetch_random_recipes()
    # background_image = fetch_image()
    background_image = url_for('static', filename='images/background.jpg')
    return render_template('home.html', recipes=recipes, background_image=background_image)


@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    # background_image = fetch_image()
    background_image = url_for('static', filename='images/background_recipe_details.jpg')

    recipe = get_recipe_details(recipe_id)
    isLiked = request.args.get('isLiked', 'no') #Get the isLiked value from query parameters

    previous_page = request.args.get('previous_page', 'home')
    print(f"Previous page: {previous_page}")  #testing

    if recipe:
        recipe['summary'] = clean_description(recipe.get('summary', 'No description available.'))
        recipe['instructions'] = clean_instructions(recipe.get('instructions', 'No instructions available.'))
        return render_template('random_recipes.html', recipe=recipe, previous_page=previous_page, isLiked=isLiked, background_image=background_image)
    else:
        return "Recipe no longer exists", 404

        
@app.route('/search', methods=['POST', 'GET']) #added the possibility a GET request if user wants to go back to search results if clicked on a recipe through search function
def search_recipes():
    if request.method == 'POST':
        # Get form data
        ingredients = request.form.get('ingredients')
        meal_type = request.form.get('meal_type')

        # (imported Session) Save the data in the session to reuse during GET requests
        session['ingredients'] = ingredients
        session['meal_type'] = meal_type

    else:  # Handle the GET request here

        # Retrieve saved data from the session
        ingredients = session.get('ingredients', '')
        meal_type = session.get('meal_type', '')


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

    # background_image = fetch_image()
    background_image = url_for('static', filename='images/background_search_results.jpg')
    
    return render_template('recipe_search_results.html', recipes=recipes, background_image=background_image)

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
    background_image = url_for('static', filename='images/background.jpg')
    return render_template('liked_recipes.html', liked_recipes=liked_recipes, background_image=background_image)

# Route to remove a recipe from the liked list
@app.route('/unlike/<int:recipe_id>', methods=['POST'])
def unlike_recipe(recipe_id):
    liked_recipes = session['liked_recipes']
    session['liked_recipes'] = [r for r in liked_recipes if r['id'] != recipe_id]
    return redirect(url_for('liked_recipes'))

if __name__ == "__main__":
    app.run(debug=True)
