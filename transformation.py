# parse user input to get transformation
def transform(transformation, jsn):
    if 'vegetarian' in transformation:
        return to_from_veg(jsn)
    elif 'healthy' in transformation:
        return to_from_healthy(jsn)
    elif 'italian' in transformation: # placeholder, can change cuisine style we want
        return style_cuisine(jsn)
    elif 'double' in transformation:
        return double_or_half(2, jsn)
    elif 'half' in transformation:
        return double_or_half(0.5, jsn)
    else:
        print('Invalid transformation request.')
        return None

# make the recipe vegetarian
def to_from_veg(recipe):
    pass

# make the recipe healthy
def to_from_healthy(recipe):
    pass

# make the recipe italian (or something else)
def style_cuisine(recipe):
    pass

# increase or reduce the recipe size
def double_or_half(factor, recipe):
    pass