import requests

# Replace with your actual Spoonacular API key
API_KEY = "b1520ada85e8455e92d4c51d187e092f"

# Function to fetch recipe details by ID
def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching details for Recipe ID {recipe_id}: {response.status_code} - {response.text}")
        return None

# Function to fetch recipes by meal type and ingredients
def fetch_recipes_by_meal_type(ingredients, meal_type):
    base_url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "includeIngredients": ingredients,
        "type": meal_type,
        "number": 3,  # Number of recipes to return
        "apiKey": API_KEY,
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Error fetching recipes: {response.status_code} - {response.text}")
        return []

# Function to fetch and display recipes
def find_recipes():
    print("Welcome to the Recipe Finder!")
    ingredients = input("Enter ingredients (comma-separated): ").strip()
    print("Choose a meal type:")
    print("1. Breakfast")
    print("2. Lunch")
    print("3. Dinner")

    choice = input("Enter your choice (1, 2, or 3): ").strip()
    meal_types = {"1": "breakfast", "2": "lunch", "3": "dinner"}
    meal_type = meal_types.get(choice)

    if not meal_type:
        print("Invalid choice. Please try again.")
        return

    print(f"\nSearching for {meal_type} recipes with ingredients: {ingredients}\n")
    recipes = fetch_recipes_by_meal_type(ingredients, meal_type)

    if recipes:
        for recipe in recipes:
            print(f"Recipe Title: {recipe['title']}")
            print(f"Recipe ID: {recipe['id']}")
            print(f"Image URL: {recipe['image']}\n")

            # Fetch recipe details
            details = get_recipe_details(recipe['id'])
            if details:
                print("Ingredients:")
                for ingredient in details.get('extendedIngredients', []):
                    print(f"- {ingredient['original']}")

                print("\nInstructions:")
                instructions = details.get('instructions', 'No instructions provided.')
                print(instructions)

            print("-" * 40)
    else:
        print(f"No {meal_type} recipes found for the given ingredients.")

# Run the function
if __name__ == "__main__":
    find_recipes()
