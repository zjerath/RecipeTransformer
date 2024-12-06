import re
from transformation import transform
from parse import fetch_recipe, extract_json_ld, parse_recipe, recipe_to_json

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
        transformation = input(f"How would you like to transform the recipe for {recipe.title}? ")
        # transform
        transformed = transform(transformation, jsn) # using parsed json format
        with open("output.txt", "w") as file:
            file.write(f"Transformation: {transformation}\n")
            file.write("\nInput Recipe:\n")
            file.write("\nIngredients:\n")
            file.write("\n".join(recipe.raw_ingredients) + "\n")
            file.write("\nSteps:\n")
            for num, step in enumerate(recipe.raw_steps, start=1):
                file.write(f"{num}. {step}\n")
            file.write("\n\nTransformed Recipe:\n")
            file.write("\nIngredients:\n")
            file.write("\n".join(transformed['raw_ingredients']) + "\n")
            file.write("\nSteps:\n")
            for num, step in enumerate(transformed['raw_steps'], start=1):
                file.write(f"{num}. {step}\n")
        print("Transformation saved to output.txt.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()