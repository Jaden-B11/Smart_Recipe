from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary data to simulate recipes
recipes = {
    'Breakfast': {
        'Most Nutrition': ['Oatmeal', 'Omelette', 'Smoothie'],
        'Balanced': ['Avocado Toast', 'Yogurt with Granola', 'Pancakes'],
        'Least Nutrition': ['Bacon and Eggs', 'Cereal', 'Doughnut']
    },
    'Lunch': {
        'Most Nutrition': ['Chicken Salad', 'Veggie Bowl', 'Soup'],
        'Balanced': ['Turkey Sandwich', 'Chicken Wrap', 'Tuna Sandwich'],
        'Least Nutrition': ['Cheeseburger', 'Hot Dog', 'Pizza']
    },
    'Dinner': {
        'Most Nutrition': ['Grilled Salmon', 'Chicken and Rice', 'Steak and Veggies'],
        'Balanced': ['Spaghetti', 'Grilled Chicken', 'Fajitas'],
        'Least Nutrition': ['Fried Chicken', 'Mac and Cheese', 'Burrito']
    }
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/category', methods=['POST'])
def category():
    food_category = request.form.get('food_category')
    if food_category in recipes.keys():
        options = recipes[food_category].keys()
        return render_template('category.html', category=food_category, options=options)
    return redirect(url_for('home'))

@app.route('/recipes', methods=['POST'])
def show_recipes():
    category_name = request.form.get('category_name')
    selected_option = request.form.get('selected_option')
    category_recipes = recipes.get(category_name, {})
    recipe_list = category_recipes.get(selected_option, [])
    return render_template('recipes.html', category=category_name, option=selected_option, recipes=recipe_list)

if __name__ == '__main__':
    app.run(debug=True)
