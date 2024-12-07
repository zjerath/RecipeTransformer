from italian_transform import transform_recipe_to_italian
from veg_transform import transform_recipe_to_veg, transform_recipe_from_veg
from speed_transform import transform_recipe_faster
import re

# parse user input to get transformation
def transform(transformation, jsn):
    if 'to vegetarian' in transformation:
        return to_veg(jsn)
    elif 'from vegetarian' in transformation:
        return from_veg(jsn)
    elif 'to healthy' in transformation:
        return to_healthy(jsn)
    elif 'from healthy' in transformation:
        return from_healthy(jsn)
    elif 'italian' in transformation: # placeholder, can change cuisine style we want
        return to_italian(jsn)
    elif 'double' in transformation:
        return double_or_half(2, jsn)
    elif 'half' in transformation:
        return double_or_half(0.5, jsn)
    elif 'faster' in transformation or 'speed' in transformation:
        return faster(jsn)
    else:
        print('Invalid transformation request.')
        return None

# make the recipe vegetarian
def to_veg(recipe):
    print(f"Transforming {recipe['title']} to vegetarian...")
    return transform_recipe_to_veg(recipe)

# make the recipe non-vegetarian
def from_veg(recipe):
    print(f"Transforming {recipe['title']} from vegetarian...")
    return transform_recipe_from_veg(recipe)

# make the recipe healthy
def to_healthy(recipe):
    print(f"Transforming {recipe['title']} to healthy...")
    ing_substitutions = {
        'butter': 'unsalted butter',
        'white sugar': 'honey or maple syrup',
        'brown sugar': 'honey or maple syrup',
        'sugar': 'honey or maple syrup',
        'cream': 'low-fat yogurt',
        'yogurt': 'low-fat yogurt',
        'cottage cheese': 'low-fat cottage cheese',
        'whole milk': 'almond milk or fat-free milk',
        'white flour': 'whole wheat flour',
        'flour': 'whole wheat flour',
        'salt': 'low-sodium salt or herbs',
        'cheese': 'low-fat cheese',
        'chocolate': 'dark chocolate',
        'mayonnaise': 'greek yogurt',
        'olive oil': 'avocado oil',
        'bacon': 'turkey bacon or ham',
        'half-and-half': 'almond or skim milk',
        'fried': 'baked'
    }
    step_substitutions = {
        'deep fry': 'bake',
        'fry': 'bake',
        'cream': 'low-fat yogurt',
        'boil in cream': 'steam'
    }
    replacements = {}
    for i, text in enumerate(recipe['raw_ingredients']):
        for unhealthy, healthy in ing_substitutions.items():
            if unhealthy in text.lower():
                text = re.sub(rf'\b{unhealthy}\b', healthy, text, flags=re.IGNORECASE)
                replacements[unhealthy] = healthy
        recipe['raw_ingredients'][i] = text
    for i, step in enumerate(recipe['raw_steps']):
        for unhealthy, healthy in step_substitutions.items():
            if unhealthy in text.lower():
                step = re.sub(rf'\b{unhealthy}\b', healthy, step, flags=re.IGNORECASE)
        for unhealthy, healthy in replacements.items():
            if unhealthy in step.lower():
                step = re.sub(rf'\b{unhealthy}\b', healthy, step, flags=re.IGNORECASE)
        recipe['raw_steps'][i] = step
    return recipe

# make the recipe unhealthy
def from_healthy(recipe):
    print(f"Transforming {recipe['title']} from healthy...")
    descriptors = ['low-fat', 'fat-free', 'reduced-fat', 'light']
    ing_substitutions = {
        'greek yogurt': 'mayonnaise',
        'low-fat yogurt': 'cream',
        'cottage cheese': 'cream cheese',
        'fat-free milk': 'whole milk',
        'almond milk': 'whole milk',
        'stevia': 'sugar',
        'honey': 'sugar',
        'maple syrup': 'sugar',
        'whole wheat flour': 'white flour',
        'quinoa': 'white rice',
        'baked': 'fried',
        'grilled': 'fried',
        'olive oil': 'butter',
        'low-sodium salt': 'salt',
        'dark chocolate': 'milk chocolate'
    }
    step_substitutions = {
        'bake': 'deep fry',
        'grill': 'pan fry',
        'saute in olive oil': 'fry in butter',
        'steam': 'boil in cream'
    }
    replacements = {}
    for i, text in enumerate(recipe['raw_ingredients']):
        for descriptor in descriptors:
            if descriptor in text.lower():
                text = re.sub(rf'\b{descriptor}\b', '', text, flags=re.IGNORECASE).strip()
        for healthy, unhealthy in ing_substitutions.items():
            if healthy in text.lower():
                text = re.sub(rf'\b{healthy}\b', unhealthy, text, flags=re.IGNORECASE)
                replacements[healthy] = unhealthy
        recipe['raw_ingredients'][i] = text
    for i, step in enumerate(recipe['raw_steps']):
        for healthy, unhealthy in step_substitutions.items():
            if healthy in step.lower():
                step = re.sub(rf'\b{healthy}\b', unhealthy, step, flags=re.IGNORECASE)
        for healthy, unhealthy in replacements.items():
            if healthy in step.lower():
                step = re.sub(rf'\b{healthy}\b', unhealthy, step, flags=re.IGNORECASE)
        recipe['raw_steps'][i] = step
    return recipe

# make the recipe italian (or something else)
def to_italian(recipe):
    print(f"Transforming {recipe['title']} to Italian...")
    # assumes recipe is in JSON format
    return transform_recipe_to_italian(recipe)
    
# increase or reduce the recipe size
def double_or_half(factor, recipe):
    if factor == 2:
        print(f"Doubling amounts for {recipe['title']}...")
        for ingredient in recipe['ingredients']:
            if ingredient['quantity']:
                if ingredient['quantity'] not in ['to taste', 'or to taste']:
                    ingredient['quantity'] = float(ingredient['quantity']) * 2
    else:
        print(f"Halving amounts for {recipe['title']}...")
        for ingredient in recipe['ingredients']:
            if ingredient['quantity']:
                if ingredient['quantity'] not in ['to taste', 'or to taste']:
                    ingredient['quantity'] = float(ingredient['quantity']) / 2
    for i, text in enumerate(recipe['raw_ingredients']):
        ing = recipe['ingredients'][i]
        match = re.match(r"(\d+/\d+|\d+\.\d+|\d+)", text)
        if match:
            original_quantity = float(eval(match.group(1)))
            if factor == 2 and ing['quantity'] == original_quantity * 2:
                recipe['raw_ingredients'][i] = text.replace(match.group(1), str(ing['quantity']), 1)
            elif factor == 0.5 and ing['quantity'] == original_quantity / 2:
                recipe['raw_ingredients'][i] = text.replace(match.group(1), str(ing['quantity']), 1)
    return recipe

# make the recipe faster
def faster(recipe):
    print(f"Speeding up Recipe for {recipe['title']}...")
    transform_recipe_faster(recipe)