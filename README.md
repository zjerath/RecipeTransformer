# Project 3 CS 337: RecipeTransformer

GitHub Repo: https://github.com/zjerath/RecipeTransformer

## File Structure:
- main.py: script used to run our program locally.
- parse.py: logic for recipe retrieval and parsing into appropriate data structure defined in representation.py.
- representation.py: defines the data structure where we store the parsed information about the recipe.
- transformation.py: handles transformation logic for vegetarian, healthy, style of cuisine, amount, and speed changes.
- requirements.txt: contains dependencies required to set up an environment to run our code.
- output.txt: contains output displaying transformation, original recipe, and transformed recipe after running main.

## Getting Started:
1. Clone the repository.
2. Create a virtual environment (python 3.10/3.11).
3. Install the dependencies with pip install -r requirements.txt.
4. Find a recipe and run main.py.

## Example Inputs and Recipes for Transformation:
1. Vegetarian 
   - To: "Transform the recipe to vegetarian." From: "Transform the recipe from vegetarian."
   - Recipes:
     - To vegetarian:
     - From vegetarian:
2. Healthy 
   - To: "Transform the recipe to healthy." From: "Transform the recipe from healthy."
   - Recipes:
     - To healthy: https://www.allrecipes.com/recipe/220895/old-charleston-style-shrimp-and-grits/
     - From healthy: https://www.allrecipes.com/recipe/272849/healthy-chicken-salad/
3. Style of cuisine 
   - "Transform the recipe to Italian cuisine."
   - Recipes:
4. Double or half 
   - "Double the recipe size." or "Reduce the amount by half."
   - Recipes:
     - https://www.allrecipes.com/recipe/218091/classic-and-simple-meat-lasagna/
     - https://www.allrecipes.com/recipe/232227/million-dollar-spaghetti/
5. Sped up 
   - "Make the recipe faster."
   - Recipes:
