import json
from parse import fetch_recipe, extract_json_ld, parse_recipe, recipe_to_json

# Ingredient substitution mapping for non-vegetarian to vegetarian
ingredient_mapping = {
    # Fats and Oils
    "tallow": "vegetable oil",
    "lard": "vegetable oil",
    "beef tallow": "vegetable oil",
    "rendered fat": "vegetable oil",
    "bacon fat": "olive oil",
    "duck fat": "olive oil",
    "schmaltz": "vegetable oil",
    "ghee": "vegan butter",
    "butter": "vegan butter",
    "margarine": "vegan butter",
    
    # Dairy
    "milk": "soy milk",
    "heavy cream": "coconut cream",
    "half and half": "oat milk",
    "whipping cream": "coconut cream",
    "buttermilk": "plant-based buttermilk",
    "sour cream": "cashew sour cream",
    "cream cheese": "vegan cream cheese",
    "ricotta": "tofu ricotta",
    "mozzarella": "vegan mozzarella",
    "parmesan": "nutritional yeast",
    "cheese": "vegan cheese",
    "yogurt": "coconut yogurt",
    "cottage cheese": "crumbled tofu",
    "mascarpone": "cashew mascarpone",
    "provolone": "vegan provolone",
    "cheddar": "vegan cheddar",
    "brie": "vegan brie",
    "gouda": "vegan gouda",
    "feta": "tofu feta",
    "blue cheese": "cultured cashew cheese",
    "romano": "nutritional yeast",
    "asiago": "vegan parmesan",
    
    # Eggs
    "egg": "flax egg",
    "eggs": "flax eggs",
    "egg white": "aquafaba",
    "egg whites": "aquafaba",
    "egg yolk": "silken tofu",
    "egg yolks": "silken tofu",
    "egg wash": "plant milk wash",
    "meringue": "aquafaba meringue",
    
    # Meat - Basic
    "chicken": "seitan",
    "beef": "beyond beef",
    "ground beef": "impossible meat",
    "pork": "jackfruit",
    "bacon": "tempeh bacon",
    "ham": "plant-based ham",
    "turkey": "tofurky",
    "lamb": "seitan",
    "veal": "young jackfruit",
    "goat": "seitan",
    "duck": "seitan duck",
    "rabbit": "king oyster mushrooms",
    
    # Processed Meats
    "sausage": "beyond sausage",
    "hot dog": "vegan hot dog",
    "bratwurst": "vegan bratwurst",
    "pepperoni": "vegan pepperoni",
    "salami": "vegan salami",
    "spam": "vegan spam",
    "bologna": "vegan bologna",
    "chorizo": "soyrizo",
    "prosciutto": "mushroom prosciutto",
    "pancetta": "mushroom bacon",
    "pastrami": "seitan pastrami",
    "corned beef": "seitan corned beef",
    "liverwurst": "mushroom pate",
    "mortadella": "vegan mortadella",
    "kielbasa": "vegan kielbasa",
    "hot dogs": "vegan hot dogs",
    "vienna sausages": "vegan vienna sausages",
    "breakfast sausage": "beyond breakfast sausage",
    "italian sausage": "beyond italian sausage",
    
    # Seafood
    "fish": "hearts of palm",
    "salmon": "marinated carrot lox",
    "tuna": "chickpea tuna",
    "shrimp": "king oyster mushrooms",
    "anchovies": "capers",
    "crab": "hearts of palm",
    "lobster": "hearts of palm",
    "scallops": "king oyster mushrooms",
    "clams": "oyster mushrooms",
    "mussels": "oyster mushrooms",
    "oysters": "oyster mushrooms",
    "calamari": "breaded hearts of palm",
    "cod": "tofu fish",
    "tilapia": "tofu fish",
    "sardines": "marinated artichokes",
    "caviar": "seaweed caviar",
    "roe": "seaweed caviar",
    
    # Stock/Broth
    "chicken stock": "vegetable stock",
    "beef stock": "mushroom stock",
    "chicken broth": "vegetable broth",
    "beef broth": "mushroom broth",
    "bone broth": "mushroom broth",
    "fish stock": "seaweed stock",
    "dashi": "kombu dashi",
    
    # Miscellaneous
    "honey": "maple syrup",
    "gelatin": "agar agar",
    "worcestershire sauce": "vegan worcestershire sauce",
    "fish sauce": "coconut aminos",
    "oyster sauce": "mushroom sauce",
    "bone marrow": "roasted mushrooms",
    "suet": "vegetable shortening",
    "rennet": "vegetable rennet",
    "isinglass": "agar agar",
    "carmine": "beetroot powder",
    "cochineal": "beetroot powder",
    "lactic acid": "citric acid",
    "shellac": "zein",
    "albumen": "aquafaba",
    
    # Organ Meats
    "liver": "mushroom pate",
    "foie gras": "mushroom pate",
    "sweetbreads": "seasoned seitan",
    "tripe": "oyster mushrooms",
    "heart": "seitan",
    "kidney": "mushrooms",
    "tongue": "seitan",
    
    # Meat Preparations
    "meatballs": "beyond meatballs",
    "meatloaf": "beyond meatloaf",
    "beef jerky": "mushroom jerky",
    "pate": "mushroom pate",
    "terrine": "vegetable terrine",
    "head cheese": "vegetable terrine",
}

# Ingredient substitution mapping for vegetarian to non-vegetarian
inv_ingredient_mapping = {
    # Plant-based Meats
    "beyond beef": "ground beef",
    "impossible meat": "ground beef",
    "beyond sausage": "sausage",
    "beyond meatballs": "meatballs",
    "beyond burger": "hamburger",
    "beyond breakfast sausage": "breakfast sausage",
    "beyond italian sausage": "italian sausage",
    "tofurky": "turkey",
    "seitan": "chicken",
    "tempeh bacon": "bacon",
    "soyrizo": "chorizo",
    "vegan spam": "spam",
    "vegan hot dog": "hot dog",
    "vegan hot dogs": "hot dogs",
    "vegan bratwurst": "bratwurst",
    "vegan pepperoni": "pepperoni",
    "vegan salami": "salami",
    "vegan bologna": "bologna",
    "vegan mortadella": "mortadella",
    "vegan kielbasa": "kielbasa",
    "vegan vienna sausages": "vienna sausages",
    
    # Vegan Dairy
    "vegan butter": "butter",
    "vegan cheese": "cheese",
    "vegan mozzarella": "mozzarella",
    "vegan cheddar": "cheddar",
    "vegan provolone": "provolone",
    "vegan brie": "brie",
    "vegan gouda": "gouda",
    "vegan parmesan": "parmesan",
    "nutritional yeast": "parmesan",
    "vegan cream cheese": "cream cheese",
    "cashew sour cream": "sour cream",
    "tofu ricotta": "ricotta",
    "tofu feta": "feta",
    "cultured cashew cheese": "blue cheese",
    "cashew mascarpone": "mascarpone",
    
    # Plant Milks & Creams
    "soy milk": "milk",
    "almond milk": "milk",
    "oat milk": "milk",
    "coconut milk": "milk",
    "cashew milk": "milk",
    "coconut cream": "heavy cream",
    "plant-based buttermilk": "buttermilk",
    "coconut yogurt": "yogurt",
    
    # Egg Replacers
    "flax egg": "egg",
    "flax eggs": "eggs",
    "aquafaba": "egg whites",
    "aquafaba meringue": "meringue",
    "plant milk wash": "egg wash",
    
    # Seafood Alternatives
    "hearts of palm fish": "fish",
    "marinated carrot lox": "salmon",
    "chickpea tuna": "tuna",
    "seaweed caviar": "caviar",
    
    # Stocks & Sauces
    "vegan worcestershire sauce": "worcestershire sauce",
    "coconut aminos": "fish sauce",
    "mushroom sauce": "oyster sauce",
    "vegetable stock": "chicken stock",
    "mushroom stock": "beef stock",
    "vegetable broth": "chicken broth",
    "mushroom broth": "beef broth",
    "seaweed stock": "fish stock",
    "kombu dashi": "dashi",
    
    # Miscellaneous
    "agar agar": "gelatin",
    "vegetable rennet": "rennet",
    "beetroot powder": "carmine",
    "zein": "shellac",
}

def replace_items(strings, mappings):
    """
    Replace all occurrences of items in strings based on given mappings.
    Intended to be used to update all ingredients, tools, methods referenced in recipe steps with transformed equivalent.
    
    Args:
        strings (list): List of strings to process i.e. recipe steps.
        mappings (list of dicts): List of dictionaries, where each dictionary contains items to replace as keys and their replacements as values.
                                  Ex: replace ingredients, methods, tools.
        
    Returns:
        updated_strings: List of strings with replacements applied.
    """
    updated_strings = []
    for string in strings:
        for mapping in mappings:
            for key, new in mapping.items():
                string = string.replace(key, new)  # Replace each old item with the new one, non case sensitive
        updated_strings.append(string)
    return updated_strings

def transform_recipe_to_veg(recipe):
    """
    Transforms a parsed JSON recipe representation into a vegetarian recipe.
    """
    transformed_recipe = recipe.copy()

    # Transform raw_ingredients
    transformed_recipe["raw_ingredients"] = replace_items(recipe["raw_ingredients"], [ingredient_mapping])

    # Transform ingredients
    transformed_ingredients = []
    for ingredient in recipe["ingredients"]:
        # Clean the ingredient name by removing punctuation and whitespace
        clean_name = ingredient["name"].lower().strip().rstrip(',.')
        
        for key in ingredient_mapping:
            if key in clean_name:
                transformed_ingredients.append({
                    "name": clean_name.replace(key, ingredient_mapping[key]),
                    "quantity": ingredient["quantity"],
                    "measurement": ingredient["measurement"],
                    "descriptor": ingredient["descriptor"],
                    "preparation": ingredient["preparation"]
                })
                break
        else:
            transformed_ingredients.append(ingredient)
    transformed_recipe["ingredients"] = transformed_ingredients

    # Transform raw_steps -> replace ingredients, methods, tools w/ vegetarian equivalents
    transformed_recipe["raw_steps"] = replace_items(recipe["raw_steps"], [ingredient_mapping])
    
    return transformed_recipe

def transform_recipe_from_veg(recipe):
    """
    Transforms a parsed JSON recipe representation from vegetarian to non-vegetarian.
    """
    transformed_recipe = recipe.copy()

    # Transform raw_ingredients
    transformed_recipe["raw_ingredients"] = replace_items(recipe["raw_ingredients"], [inv_ingredient_mapping])


    # Transform ingredients
    transformed_ingredients = []
    for ingredient in recipe["ingredients"]:
        # Clean the ingredient name by removing punctuation and whitespace
        clean_name = ingredient["name"].lower().strip().rstrip(',.')
        
        for key in inv_ingredient_mapping:
            if key in clean_name:
                transformed_ingredients.append({
                    "name": clean_name.replace(key, inv_ingredient_mapping[key]).replace('vegan', '').replace('vegetarian', ''),
                    "quantity": ingredient["quantity"],
                    "measurement": ingredient["measurement"],
                    "descriptor": ingredient["descriptor"],
                    "preparation": ingredient["preparation"]
                })
                break
        else:
            transformed_ingredients.append({
                "name": ingredient["name"].replace('vegetarian', '').replace('vegan', ''),
                "quantity": ingredient["quantity"],
                "measurement": ingredient["measurement"],
                "descriptor": ingredient["descriptor"],
                "preparation": ingredient["preparation"]
            })
    transformed_recipe["ingredients"] = transformed_ingredients

    # Transform raw_steps -> replace ingredients, methods, tools w/ vegetarian equivalents
    transformed_recipe["raw_steps"] = replace_items(recipe["raw_steps"], [inv_ingredient_mapping])
    
    return transformed_recipe

def main():

    # raw_steps = [
    #     "Preheat a nonstick skillet over medium heat. Generously butter one side of a slice of bread. Place bread butter-side down in the hot skillet; add 1 slice of cheese. Butter a second slice of bread on one side and place butter-side up on top of cheese.",
    #     "Cook until lightly browned on one side; flip over and continue cooking until cheese is melted. Repeat with remaining 2 slices of bread, butter, and slice of cheese."
    # ]

    # updated_steps = replace_items(raw_steps, tool_mapping)
    # print(updated_steps)
    
    url = "https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/"

    try:
        soup = fetch_recipe(url)
        json_data = extract_json_ld(soup)
        if not json_data:
            print("Could not find a valid recipe in the provided URL.")
            return
        # parse recipe
        recipe = parse_recipe(json_data)
        original_recipe = recipe_to_json(recipe)
    except Exception as e:
        print(f"An error occurred: {e}")
        return
        
    # Transform the recipe
    vegetarian_recipe = transform_recipe_to_veg(original_recipe)
    non_vegetarian_recipe = transform_recipe_from_veg(vegetarian_recipe)
    original_file_path = "original_recipe.txt"
    with open(original_file_path, "w") as file:
        json.dump(original_recipe, file, indent=4)

    transformed_file_path = "transformed_recipe.txt"
    with open(transformed_file_path, "w") as file:
        json.dump(vegetarian_recipe, file, indent=4)

    non_vegetarian_file_path = "non_vegetarian_recipe.txt"
    with open(non_vegetarian_file_path, "w") as file:
        json.dump(non_vegetarian_recipe, file, indent=4)

if __name__ == "__main__":
    main()
