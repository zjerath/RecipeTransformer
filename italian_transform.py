import json
import re
from parse import fetch_recipe, extract_json_ld, parse_recipe, recipe_to_json
from fractions import Fraction

# Ingredient substitution mapping for Italian cuisine
ingredient_mapping = {
    "butter": "olive oil",
    "milk": "heavy cream",
    "cheddar": "parmesan",
    "cheddar cheese": "parmesan cheese",
    "chicken": "prosciutto",
    "ground beef": "Italian sausage",
    "beef": "Italian sausage",
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
    # "sausage": "salami or soppressata",
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



# Mapping common Italian ingredients to associated cooking methods. 
# If a recipe step mentions any of these methods, a suggestion will be added to the current recipe step to include the associated ingredient.
common_ingredient_to_method_mapping = {
    "olive oil": ["heat", "drizzle", "roast", "saute"],
    "garlic": ["saute", "prepare sauce", "simmer"],
    "parmesan": ["garnish", "serve", "combine with sauce"],
    "basil": ["garnish", "finish", "simmer"],
    "tomatoes": ["add to sauce", "roast", "blend"],
    "wine": ["deglaze", "simmer"],
    "oregano": ["season", "add to sauce"],
    "mozzarella": ["top", "bake"],
}

# Italian ingredient defaults based on common Italian cooking practices
# Used for initializing ingredients to append to recipe["ingredients"] list
common_ingredient_defaults = {
    "olive oil": {"quantity": "2", "measurement": "tablespoons"},
    "garlic": {"quantity": "2", "measurement": "cloves"},
    "parmesan": {"quantity": "1/4", "measurement": "cup"},
    "basil": {"quantity": "1/4", "measurement": "cup (packed leaves)"},
    "tomatoes": {"quantity": "3", "measurement": "medium (or whole)"},
    "wine": {"quantity": "1/2", "measurement": "cup"},
    "oregano": {"quantity": "1", "measurement": "teaspoon (dried)"},
    "mozzarella": {"quantity": "8", "measurement": "ounces"}
}

def aggregate_raw_ingredients(raw_ingredients):
    """
    Combines common ingredients in raw_ingredients list to one entry with updated quantity. 

    Ex:
    raw_ingredients = [
        "1 egg",
        "1 tablespoon olive oil",
        "1 tablespoon olive oil",
        "1 onion, chopped",
        "2 tablespoons olive oil"
    ]

    is converted to 

    raw_ingredients = [
        "1 egg",
        "4 tablespoons olive oil",
        "1 onion, chopped"
    ]
    """
    def parse_raw_ingredient(ingredient):
        # Regular expression to extract quantity, measurement, and ingredient name
        pattern = r"(?P<quantity>[\d/]+(?:\.\d+)?|\d+)?\s*(?P<measurement>\b\w+\b)?\s*(?P<name>.+)"
        match = re.match(pattern, ingredient.strip())
        if match:
            quantity = match.group("quantity") or "1"  # Default to 1 if no quantity
            measurement = match.group("measurement") or ""
            name = match.group("name").strip(",").lower()
            return {
                "name": name,
                "quantity": quantity,
                "measurement": measurement
            }
        return None

    aggregated = {}
    
    for raw in raw_ingredients:
        parsed = parse_raw_ingredient(raw)
        if not parsed:
            continue
        name = parsed["name"]
        
        if name not in aggregated:
            aggregated[name] = parsed  # Start with the first occurrence
        else:
            # Combine quantities if possible
            current_quantity = aggregated[name]["quantity"]
            new_quantity = parsed["quantity"]
            
            try:
                # Attempt to parse and add quantities as numbers
                current_quantity = float(Fraction(current_quantity))
                new_quantity = float(Fraction(new_quantity))
                aggregated[name]["quantity"] = str(current_quantity + new_quantity)
            except ValueError:
                # Concatenate quantities if they can't be added numerically
                aggregated[name]["quantity"] += f" + {parsed['quantity']}"
            
            # Retain measurement or append if there's a mismatch
            if aggregated[name]["measurement"] != parsed["measurement"]:
                aggregated[name]["measurement"] = aggregated[name]["measurement"] or parsed["measurement"]
    
    # Combine into readable strings
    return [
        f"{info['quantity']} {info['measurement']} {info['name']}".strip()
        for info in aggregated.values()
    ]

def aggregate_ingredients(ingredients):
    """
    Combines common ingredients in ingredients list to one entry with updated quantity. 
    
    Ex:
    {
        "name": "olive oil",
        "quantity": "1",
        "measurement": "tablespoon",
        "descriptor": None,
        "preparation": None
    },
    {
        "name": "olive oil",
        "quantity": "2",
        "measurement": "tablespoons",
        "descriptor": None,
        "preparation": None
    },

    is converted to
    
    {
        "name": "olive oil",
        "quantity": "2",
        "measurement": "tablespoons",
        "descriptor": None,
        "preparation": None
    }
    """
    # Helper to convert string quantities to numeric for addition
    def parse_quantity(q):
        try:
            return float(Fraction(q))
        except ValueError:
            return None
    
    # Aggregated result
    aggregated = {}
    
    for ingredient in ingredients:
        name = ingredient["name"].strip().lower()  # Normalize name (strip and lowercase)
        
        if name not in aggregated:
            aggregated[name] = ingredient.copy()  # Start with a copy of the first occurrence
        else:
            # Combine quantities if possible
            current_quantity = parse_quantity(aggregated[name]["quantity"])
            new_quantity = parse_quantity(ingredient["quantity"])
            
            if current_quantity is not None and new_quantity is not None:
                aggregated[name]["quantity"] = str(current_quantity + new_quantity)
            else:
                # If quantities are not summable, default to appending the new one
                aggregated[name]["quantity"] = aggregated[name]["quantity"] + " + " + ingredient["quantity"]
            
            # Merge other fields if they are not already set
            for key in ["measurement", "descriptor", "preparation"]:
                if not aggregated[name][key] and ingredient[key]:
                    aggregated[name][key] = ingredient[key]
    
    return list(aggregated.values())

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

def suggest_enhancing_ingredients(step, iconic_ingredients, current_ingredients):
    """
    Identifies whether any common Italian ingredients could be added to enhance current recipe step.
    Applied to recipe step AFTER initial ingredient substitution.
    If step does not have any common Italian ingredients after initial ingredient substitution but mentions associated cooking method(s), 
    ingredients are suggested as enhancement.

    Args:
        step (string): Current recipe step.
        iconic_ingredients (dict): Dictionary mapping iconic ingredients to cooking actions.
        current_ingredients (list of strings): ingredients included in current recipe step
    Returns:
        updated_step (string): Updated step with suggestions for adding missing ingredients.
        suggestions (list of strings): suggestions for optional ingredients to enhance recipe step.
    """
    
    updated_step = step
    # Analyze step and suggest iconic ingredients
    suggestions = []
    for ingredient, keywords in iconic_ingredients.items():
        if ingredient in current_ingredients: # if ingredient suggestion is already included in step ingredient list, no need to suggest 
            continue
        if any(keyword in step.lower() for keyword in keywords):
            suggestions.append(ingredient)
    
    # Add suggestions to the step
    if suggestions:
        updated_step += f" (Consider adding: {', '.join(suggestions)})"
    
    return updated_step, suggestions

def transform_recipe_to_italian(recipe):
    """
    Transforms a parsed JSON recipe representation into an Italian-style recipe.
    """
    transformed_recipe = recipe.copy()

    # Transform recipe title
    transformed_recipe["title"] = "Italian-Style " + recipe["title"]

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

    # Transform raw_steps: replace ingredients, methods, tools w/ Italian equivalents
    transformed_recipe["raw_steps"] = replace_items(recipe["raw_steps"], [ingredient_mapping, method_mapping, tool_mapping])
    
    # Transform steps 
    additional_optional_ingredients = set() # set of optional ingredient suggestions to append to recipe ingredient list
    for i, step in enumerate(transformed_recipe["steps"]):
        step["text"] = replace_items([step["text"]], [ingredient_mapping, tool_mapping, method_mapping])[0]
        step["ingredients"] = replace_items(step["ingredients"], [ingredient_mapping])
        step["tools"] = replace_items(step["tools"], [tool_mapping])
        step["methods"] = replace_items(step["methods"], [method_mapping])
        
        # check for optional ingredient enhancements for current step
        step["text"], step_ingredient_suggestions = suggest_enhancing_ingredients(step["text"], common_ingredient_to_method_mapping, step["ingredients"])
        
        # if optional ingredients were suggested, add to ingredients list for the step & overall recipe
        step["ingredients"].extend(step_ingredient_suggestions)
        additional_optional_ingredients.update(step_ingredient_suggestions)

    # update recipe raw ingredients and ingredients list if additional ingredients were suggested
    for optional_ingredient in list(additional_optional_ingredients):
        raw_ingredient_components = [
            common_ingredient_defaults[optional_ingredient]["quantity"],
            common_ingredient_defaults[optional_ingredient]["measurement"],
            optional_ingredient
        ]
        raw_ingredient_to_add = " ".join(raw_ingredient_components)
        transformed_recipe["raw_ingredients"].append(raw_ingredient_to_add)

        transformed_recipe["ingredients"].append({
            "name": optional_ingredient,
            "quantity": common_ingredient_defaults[optional_ingredient]["quantity"],
            "measurement": common_ingredient_defaults[optional_ingredient]["measurement"],
            "descriptor": None,
            "preparation": None
        })
    
    # aggregate common ingredients into single entries with updated quantities
    transformed_recipe["raw_ingredients"] = aggregate_raw_ingredients(transformed_recipe["raw_ingredients"])
    transformed_recipe["ingredients"] = aggregate_ingredients(transformed_recipe["ingredients"])

    return transformed_recipe