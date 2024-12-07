import json
import re
from parse import fetch_recipe, extract_json_ld, parse_recipe, recipe_to_json

# Ingredient substitution mapping for Italian cuisine
ingredient_mapping = {
    "butter": "olive oil",
    "milk": "heavy cream",
    "cheddar": "parmesan",
    "cheddar cheese": "parmesan cheese",
    "chicken": "prosciutto",
    "ground beef": "Italian sausage",
    "sour cream": "mascarpone",
    "potatoes": "gnocchi",
    "corn": "polenta",
    "tomato ketchup": "marinara sauce",
    "vegetable oil": "olive oil",
    "green beans": "zucchini",
    "mushrooms": "porcini mushrooms",
    "bell peppers": "roasted red peppers",
    "cream cheese": "ricotta",
    "bacon": "pancetta",
    "ham": "speck",
    "pasta noodles": "fresh tagliatelle or fettuccine",
    "white rice": "risotto rice",
    "vinegar": "balsamic vinegar",
    "spinach": "arugula",
    "lettuce": "radicchio",
    "sausage": "salami or soppressata",
    "shrimp": "scampi",
    "onions": "shallots",
    "cabbage": "savoy cabbage",
}

# Tool substitution mapping for Italian cuisine
tool_mapping = {
    "wok": "saute pan",
    "deep fryer": "large padella",
    "griddle": "pizza stone",
    "skillet": "padella",
    "spatula": "wooden spoon",
    "oven mitts": "thick kitchen towels",
    "pot": "casseruola",
    "stockpot": "pentola",
    "baking tray": "terracotta baking dish",
    "whisk": "fork or balloon whisk",
    "colander": "mesh strainer",
    "rolling pin": "pasta rolling pin",
    "frying pan": "non-stick padella",
}

# Cooking method mapping for Italian cuisine
method_mapping = {
    "fry": "saute",
    "grill": "pan-sear",
    "bake": "roast",
    "steam": "blanch",
    "boil": "simmer",
    "stir-fry": "toss",
    "roast": "oven-roast",
    "barbecue": "grill",
    "poach": "simmer",
    "braise": "slow-cook",
    "stew": "simmer",
    "toast": "grill",
    "marinate": "season",
}


# mapping common Italian ingredients to associated cooking methods 
ingredient_to_method_mapping = {
    "olive oil": ["heat", "drizzle", "roast", "sauté"],
    "garlic": ["sauté", "prepare sauce", "simmer"],
    "parmesan": ["garnish", "serve", "combine with sauce"],
    "basil": ["garnish", "finish", "simmer"],
    "tomatoes": ["add to sauce", "roast", "blend"],
    "wine": ["deglaze", "simmer"],
    "oregano": ["season", "add to sauce"],
    "mozzarella": ["top", "bake"],
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

    # Apply missing ingredient transform

    
    return transformed_recipe

def suggest_missing_ingredients(steps, iconic_ingredients):
    """
    Identifies where iconic ingredients could/should be added in recipe steps.
    Should be applied to recipe AFTER initial ingredient, method, tool substitutions.
    For any steps with methods that do not have iconic ingredients after initial substitution but have associated cooking action(s), 
    suggest to add those ingredients.

    Args:
        steps (list): List of recipe steps (strings).
        iconic_ingredients (dict): Dictionary mapping iconic ingredients to cooking actions.
    Returns:
        list: Updated steps with suggestions for adding missing ingredients.
    """
    updated_steps = []
    for step in steps:
        # Analyze step and suggest iconic ingredients
        suggestions = []
        for ingredient, keywords in iconic_ingredients.items():
            if any(keyword in step.lower() for keyword in keywords):
                suggestions.append(ingredient)
        
        # Add suggestions to the step
        if suggestions:
            updated_steps.append(f"{step} (Consider adding: {', '.join(suggestions)})")
        else:
            updated_steps.append(step)
    return updated_steps

def main():

    # raw_steps = [
    #     "Preheat a nonstick skillet over medium heat. Generously butter one side of a slice of bread. Place bread butter-side down in the hot skillet; add 1 slice of cheese. Butter a second slice of bread on one side and place butter-side up on top of cheese.",
    #     "Cook until lightly browned on one side; flip over and continue cooking until cheese is melted. Repeat with remaining 2 slices of bread, butter, and slice of cheese."
    # ]

    # updated_steps = replace_items(raw_steps, tool_mapping)
    # print(updated_steps)
    
    # url = "https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/"

    # try:
    #     soup = fetch_recipe(url)
    #     json_data = extract_json_ld(soup)
    #     if not json_data:
    #         print("Could not find a valid recipe in the provided URL.")
    #         return
    #     # parse recipe
    #     recipe = parse_recipe(json_data)
    #     original_recipe = recipe_to_json(recipe)
        
    #     # Transform the recipe
    #     italian_recipe = transform_recipe_to_italian(original_recipe)

    #     original_file_path = "original_recipe.txt"
    #     with open(original_file_path, "w") as file:
    #         json.dump(original_recipe, file, indent=4)

    #     transformed_file_path = "transformed_recipe.txt"
    #     with open(transformed_file_path, "w") as file:
    #         json.dump(italian_recipe, file, indent=4)

    # except Exception as e:
    #     print(f"An error occurred: {e}")
    
    # Example recipe steps
    recipe_steps = [
        "Heat a pan over medium heat.",
        "Fry the chicken until golden brown.",
        "Add tomatoes and cook for 10 minutes.",
        "Serve the pasta with the sauce.",
    ]

    # Apply the function
    updated_recipe = suggest_missing_ingredients(recipe_steps, ingredient_to_method_mapping)

    # Display the updated recipe
    print("Original Steps:")
    print("\n".join(recipe_steps))
    print("\nUpdated Steps with Suggestions:")
    print("\n".join(updated_recipe))



if __name__ == "__main__":
    main()

