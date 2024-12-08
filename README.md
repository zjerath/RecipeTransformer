# Project 3 CS 337: RecipeTransformer

GitHub Repo: https://github.com/zjerath/RecipeTransformer

## File Structure:
- main.py: script used to run our program locally.
- parse.py: logic for recipe retrieval and parsing into appropriate data structure defined in representation.py.
- representation.py: defines the data structure where we store the parsed information about the recipe.
- transformation.py: handles transformation logic for healthy and amount changes.
- veg_transform.py: handles transformation logic for vegetarian changes.
- italian_transform.py: handles transformation logic for transforming recipe to Italian style cuisine.
- speed_transform.py: handles transformation logic for speed changes.
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
     - To vegetarian: https://www.allrecipes.com/recipe/246481/slow-cooked-red-braised-pork-belly/
     - From vegetarian: https://www.allrecipes.com/recipe/277953/air-fryer-beyond-meat-brats-onions-and-peppers/
2. Healthy 
   - To: "Transform the recipe to healthy." From: "Transform the recipe from healthy."
   - Recipes:
     - To healthy: https://www.allrecipes.com/recipe/220895/old-charleston-style-shrimp-and-grits/
     - From healthy: https://www.allrecipes.com/recipe/272849/healthy-chicken-salad/
3. Style of cuisine (Italian)
   - "Transform the recipe to Italian cuisine."
   - Recipes:
      - https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/
      - https://www.allrecipes.com/recipe/258947/mushroom-beef-burgers/
   - Note: some popular Italian ingredients are associated with certain cooking methods. In the parsed representation, additional Italian ingredients are suggested as optional enhancements for a step, if that step contains any cooking methods that are typically associated with those ingredients.
4. Double or half 
   - "Double the recipe size." or "Reduce the amount by half."
   - Recipes:
     - https://www.allrecipes.com/recipe/218091/classic-and-simple-meat-lasagna/
     - https://www.allrecipes.com/recipe/232227/million-dollar-spaghetti/
5. Sped up 
   - "Make the recipe faster."
   - Recipes:
     - https://www.allrecipes.com/recipe/21766/roasted-pork-loin/
     - https://www.allrecipes.com/recipe/246481/slow-cooked-red-braised-pork-belly/
