import json
import re

from parse import fetch_recipe, extract_json_ld, parse_recipe, recipe_to_json

ingredient_mapping = {
    # Meats (replace slow-cooking cuts with quick-cooking alternatives)
    "brisket": "strip loin",
    "chuck roast": "ribeye",
    "short ribs": "flat iron steak",
    "pork shoulder": "pork tenderloin",
    "pork butt": "pork chops",
    "pork loin": "pork tenderloin",
    "lamb shank": "lamb chops",
    "oxtail": "sirloin",
    "beef stew meat": "sirloin tips",
    "whole chicken": "chicken breasts",
    "turkey": "turkey breast",
    
    # Dried ingredients (use pre-cooked/canned versions)
    "dried beans": "canned beans",
    "dried chickpeas": "canned chickpeas",
    "dried lentils": "canned lentils",
    "dried peas": "canned peas",
    "dried black beans": "canned black beans",
    "dried kidney beans": "canned kidney beans",
    
    # Vegetables (quick-cooking alternatives)
    "russet potatoes": "baby potatoes",
    "whole potatoes": "diced potatoes",
    "butternut squash": "zucchini",
    "acorn squash": "summer squash",
    "whole carrots": "shredded carrots",
    "brown rice": "instant rice",
    "wild rice": "instant rice",
    "steel cut oats": "quick oats",
}

tool_mapping = {
    # Transform traditional tools to faster alternatives
    "dutch oven": "pressure cooker",
    "slow cooker": "pressure cooker",
    "crock pot": "pressure cooker",
    "stock pot": "pressure cooker",
    "oven": "air fryer",
    "baking dish": "microwave-safe dish",
    "steamer": "microwave steamer",
    "double boiler": "microwave",
}

method_mapping = {
    # Cooking methods from slow to fast
    "braise": "pressure cook",
    "slow cook": "pressure cook",
    "roast": "air fry",
    "bake": "air fry",
    "steam": "microwave steam",
    "stew": "pressure cook",
    "smoke": "grill",
    "ferment": "use store-bought",
    "proof": "quick proof",
    "rest": "quick rest",
    "marinate": "quick marinate",
    "soak": "quick soak",

    "Preheat": "Set",
    "preheated": "",
    "Braise": "Pressure cook",
    "Slow cook": "Pressure cook",
    "Roast": "Air fry",
    "Bake": "Air fry",
    "Steam": "Microwave steam",
    "Stew": "Pressure cook",
    "Smoke": "Grill",
    "Ferment": "Use store-bought",
    "Proof": "Quick proof",
    "Rest": "Quick rest",
    "Marinate": "Quick marinate",
    "Soak": "Quick soak",
    
    # Time modifiers to add to instructions
    "overnight": "2 hours",
    "for 8 hours": "for 4 hours",
    "for 6 hours": "for 3 hours",
    "for 4 hours": "for 2 hours",
    "for 3 hours": "for 90 minutes",
    "for 2 hours": "for 1 hour",
    "for 1 hour": "for 30 minutes",
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

def transform_recipe_faster(recipe):
    """
    Transforms a parsed JSON recipe representation into a recipe that cooks faster.
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

    # Transform raw_steps -> replace ingredients, methods, tools w/ faster equivalents
    transformed_recipe["raw_steps"] = replace_items(recipe["raw_steps"], [ingredient_mapping, tool_mapping, method_mapping])

    # Halve cooking times
    def halve_time(match):
        time_value = int(match.group(1))
        if "minutes" in match.group(2) and time_value >= 30:
            halved_time = time_value // 2
            return f"{halved_time} {match.group(2)}"
        elif "hours" in match.group(2) and time_value >= 1:
            halved_time = time_value // 2
            return f"{halved_time} {match.group(2)}"
        return match.group(0)
    for i, step in enumerate(transformed_recipe["raw_steps"]):
        step = re.sub(r"(\d+)\s*(minutes?|hours?)", halve_time, step)
        transformed_recipe["raw_steps"][i] = step
    
    # Transform steps 
    for i, step in enumerate(transformed_recipe["steps"]):
        if step["time"]["duration"]:
            step["time"]["duration"] = re.sub(r"(\d+)\s*(minutes?|hours?)", halve_time, step["time"]["duration"])
        step["text"] = re.sub(r"(\d+)\s*(minutes?|hours?)", halve_time, step["text"])
        step["text"] = replace_items([step["text"]], [ingredient_mapping, tool_mapping, method_mapping])
        step["ingredients"] = replace_items(step["ingredients"], [ingredient_mapping])
        step["tools"] = replace_items(step["tools"], [tool_mapping])
        step["methods"] = replace_items(step["methods"], [method_mapping])
    return transformed_recipe

def main():
    url = "https://www.allrecipes.com/recipe/21766/roasted-pork-loin/"

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
    faster_recipe = transform_recipe_faster(original_recipe)
    original_file_path = "original_recipe.txt"
    with open(original_file_path, "w") as file:
        json.dump(original_recipe, file, indent=4)

    transformed_file_path = "transformed_recipe.txt"
    with open(transformed_file_path, "w") as file:
        json.dump(faster_recipe, file, indent=4)

if __name__ == "__main__":
    main()
