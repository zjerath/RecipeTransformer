GitHub Repo: https://github.com/zjerath/RecipeTransformer

Project 3 CS 337: RecipeTransformer

File Structure:
- main.py: script used to run our program locally.
- parse.py: logic for recipe retrieval and parsing into appropriate data structure defined in representation.py.
- representation.py: defines the data structure where we store the parsed information about the recipe.
- transformation.py: handles transformation logic for vegetarian, healthy, style of cuisine, and amount changes.
- requirements.txt: contains dependencies required to set up an environment to run our code.

Getting Started:
1. Clone the repository.
2. Create a virtual environment (python 3.10/3.11).
3. Install the dependencies with pip install -r requirements.txt.
4. Find a recipe and run main.py.

Example Inputs for Transformation:
1. Vegetarian - To: "Transform the recipe to vegetarian." From: "Transform the recipe from vegetarian."
2. Healthy - To: "Transform the recipe to healthy." From: "Transform the recipe from healthy."
3. Style of cuisine - "Transform the recipe to Italian cuisine."
4. Double or half - "Double the recipe size." or "Reduce the amount by half."
