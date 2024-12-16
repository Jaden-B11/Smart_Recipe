import requests
import re  #imported this to help parse thrhough text but we can just parse through it ourselves 

# Replace with your actual Spoonacular API key
API_KEY = "666dcfdbceb44a50ba2c6f5801ee4de5"
# API_KEY = "666dcfdbceb44a50ba2c6f5801ee4de5"


#Function to fetch random recipes for homepage
def fetch_random_recipes():
    url = "https://api.spoonacular.com/recipes/random"
    params = {"number": 3, "apiKey": API_KEY}
    response = requests.get(url, params=params)
    return response.json().get("recipes", [])
    

# Function to fetch recipe details by ID
def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": API_KEY}
    response = requests.get(url, params=params)
    return response.json()
    
   

def clean_description(description):
    # Removes any HTML tags that would display occassionally
    description = re.sub(r'<.*?>', '', description)
    description = re.sub(r'spoonacular', '', description) #just wanted to remove spoonacular
    # I wanted to remove unnessesary parts of the Description
    sentences = description.split('. ')    
    sentences = sentences[:-1]   #removed unnecessary links at the end of the description
    description = '. '.join(sentences)
    description += '. Enjoy!'
    return description

def clean_instructions(instructions): #I had this common issue where pulling from the API would display HTMI tags and this funciton helps remove that
    instructions = re.sub(r'<.*?>', '', instructions)
    return instructions