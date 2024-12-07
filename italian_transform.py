import json
from parse import fetch_recipe, extract_json_ld, parse_recipe, recipe_to_json

# Ingredient substitution mapping for Italian cuisine
ingredient_mapping = {
    "butter": "olive oil",
    "milk": "heavy cream",
    "cheddar": "parmesan",
    "chicken": "prosciutto",
    "ground beef": "Italian sausage",
    "sour cream": "mascarpone",
    "potatoes": "gnocchi",
    "corn": "polenta",
    "tomato ketchup": "marinara sauce",
    "white bread": "x",
    "butter,": "y",
    "cheddar cheese": "z"
}

# Tool substitution mapping for Italian cuisine
tool_mapping = {
    "wok": "saute pan",
    "deep fryer": "large padella",
    "griddle": "pizza stone",
    "skillet": "padella"
}

# Cooking method mapping for Italian cuisine
method_mapping = {
    "fry": "saute in olive oil",
    "grill": "pan-sear",
    "bake": "roast with herbs",
    "steam": "blanch",
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
            for old, new in mapping.items():
                string = string.replace(old, new)  # Replace each old item with the new one
        updated_strings.append(string)
    return updated_strings

def transform_recipe_to_italian(recipe):
    """
    Transforms a parsed JSON recipe representation into an Italian-style recipe.
    """
    transformed_recipe = recipe.copy()

    # Transform raw_ingredients
    transformed_recipe["raw_ingredients"] = replace_items(recipe["raw_ingredients"], [ingredient_mapping])

    # Transform ingredients
    transformed_ingredients = []
    for ingredient in recipe["ingredients"]:
        # Clean the ingredient name by removing punctuation and whitespace
        clean_name = ingredient["name"].lower().strip().rstrip(',.')
        
        transformed_ingredients.append({
            "name": ingredient_mapping.get(clean_name, ingredient["name"]), # keep the current ingredient name if no substitution exists
            "quantity": ingredient["quantity"],
            "measurement": ingredient["measurement"],
            "descriptor": ingredient["descriptor"],
            "preparation": ingredient["preparation"]
        })
    transformed_recipe["ingredients"] = transformed_ingredients

    # Transform tools
    transformed_tools = []
    for tool in recipe["tools"]:
        clean_tool = tool.lower().strip().rstrip(',.')
        transformed_tools.append(tool_mapping.get(clean_tool, tool))
    transformed_recipe["tools"] = transformed_tools

    # Transform methods
    transformed_methods = []
    for method in recipe["methods"]:
        clean_method = method.lower().strip().rstrip(',.')
        transformed_methods.append(method_mapping.get(clean_method, method))
    transformed_recipe["methods"] = transformed_methods

    # Transform raw_steps -> replace ingredients, methods, tools w/ Italian equivalents
    transformed_recipe["raw_steps"] = replace_items(recipe["raw_steps"], [ingredient_mapping, method_mapping, tool_mapping])
    
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
        
        # Transform the recipe
        italian_recipe = transform_recipe_to_italian(original_recipe)

        original_file_path = "original_recipe.txt"
        with open(original_file_path, "w") as file:
            json.dump(original_recipe, file, indent=4)

        transformed_file_path = "transformed_recipe.txt"
        with open(transformed_file_path, "w") as file:
            json.dump(italian_recipe, file, indent=4)

    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    main()

