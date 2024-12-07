import re
from transformation import transform
from parse import fetch_recipe, extract_json_ld, parse_recipe, recipe_to_json
import json

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
        print("You can transform the recipe in the following ways:")
        print("1. To make the recipe vegetarian, type 'to vegetarian'.")
        print("2. To make the recipe non-vegetarian, type 'from vegetarian'.")
        print("3. To make the recipe healthy, type 'to healthy'.")
        print("4. To make the recipe unhealthy, type 'from healthy'.")
        print("5. To make the recipe Italian, type 'italian'.")
        print("6. To double the recipe, type 'double'.")
        print("7. To halve the recipe, type 'half'.")
        print("8. To make the recipe faster, type 'faster' or 'speed'.")
        print()
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

        with open("full_original_recipe.txt", "w") as file:
            json.dump(jsn, file, indent=4)
        print("Original parsed recipe saved to full_original_recipe.txt.")
        
        with open("full_transformed_recipe.txt", "w") as file:
            json.dump(transformed, file, indent=4)
        print("Transformed parsed recipe saved to full_transformed_recipe.txt.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()