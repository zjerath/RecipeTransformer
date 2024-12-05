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
                ingredient['quantity'] = int(ingredient['quantity']) * 2
    else:
        print(f"Halving amounts for {recipe['title']}...")
        for ingredient in recipe['ingredients']:
            if ingredient['quantity']:
                ingredient['quantity'] = int(ingredient['quantity']) / 2
    return recipe

# make the recipe faster
def faster(recipe)
    print(f"Speeding up Recipe for {recipe['title']}...")
    return recipe
