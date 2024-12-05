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
        return style_cuisine(jsn)
    elif 'double' in transformation:
        return double_or_half(2, jsn)
    elif 'half' in transformation:
        return double_or_half(0.5, jsn)
    elif 'faster' in transformation:
        return faster(jsn)
    else:
        print('Invalid transformation request.')
        return None

# make the recipe vegetarian
def to_veg(recipe):
    print(f"Transforming {recipe['title']} to vegetarian...")
    return recipe

# make the recipe non-vegetarian
def from_veg(recipe):
    print(f"Transforming {recipe['title']} from vegetarian...")
    return recipe

# make the recipe healthy
def to_healthy(recipe):
    print(f"Transforming {recipe['title']} to healthy...")
    return recipe

# make the recipe unhealthy
def from_healthy(recipe):
    print(f"Transforming {recipe['title']} from healthy...")
    return recipe

# make the recipe italian (or something else)
def style_cuisine(recipe):
    print(f"Transforming {recipe['title']} to Italian...")
    return recipe

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
    return recipe