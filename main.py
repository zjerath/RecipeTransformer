import re
from parse import fetch_recipe, extract_json_ld, parse_recipe, recipe_to_json
from transformation import transform, to_from_veg, to_from_healthy, style_cuisine, double_or_half

def is_valid_allrecipes_url(url):
    """Validate if the URL is from allrecipes.com"""
    return re.match(r'^https?://(www\.)?allrecipes\.com/recipe/\d+/[^/]+/?$', url)

def main():
    # prompt for user input
    print("Please specify a URL.")
    url = input().strip()
    # validate url
    if not is_valid_allrecipes_url(url):
        print("The URL must be from allrecipes.com.")
        return
    # attempt to fetch and parse url
    try:
        soup = fetch_recipe(url)
        json_data = extract_json_ld(soup)
        if not json_data:
            print("Could not find a valid recipe in the provided URL.")
            return
        # parse recipe
        recipe = parse_recipe(json_data)
        jsn = recipe_to_json(recipe)
        # ask for transformation
        transformation = input(f"How would you like to transform the recipe for {recipe.title}?")
        # transform
        transformed = transform(transformation, jsn) # using parsed json format for now
        with open("output.txt", "w") as file:
            file.write(f"Transformation: {transformation}\n")
            file.write("\nInput Recipe:\n")
            file.write(recipe.raw_ingredients)
            file.write(recipe.raw_steps)
            file.write("\n\nTransformed Recipe:\n")
            file.write(transformed)
        print("Transformation saved to output.txt.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()