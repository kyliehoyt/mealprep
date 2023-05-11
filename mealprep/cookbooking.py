"""Class based module for maintaining a cookbook of recipes with ingredients and nutrition"""
import os
import pandas as pd
import numpy as np


class Cookbook:
    """a mutable collection of recipe objects"""

    def __init__(self, title):
        # check that the cookbook is in the cwd and is a string
        self.title = title
        self.folderpath = os.getcwd() + "\\" + self.title
        # instantiate the recipes and contain in self.recipes
        recipe_files = [f for f in os.listdir(
            self.folderpath) if f.endswith(".txt")]
        self.num_recipes = len(recipe_files)
        self.recipes = []
        self.index = 0
        for recipe_name in recipe_files:
            # get cals and macros of recipe
            recipe_filepath = self.folderpath + '\\' + recipe_name
            self.recipes.append(Recipe(recipe_filepath))
        print(self)

    def __str__(self):
        """return name of cookbook and number of recipes"""
        return f'{self.title} has {self.num_recipes} recipes'

    def __len__(self):
        """return number of recipes in the cookbook"""
        return self.num_recipes

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == self.num_recipes:
            raise StopIteration
        self.index += 1
        return self.recipes[self.index]


class Recipe:
    """a recipe containing servings, nutrition information, ingredients, and instructions"""

    def __init__(self, filepath):
        self.filepath = filepath
        with open(self.filepath, 'r', encoding='utf-8') as recipe:
            self.name = recipe.readline()
            servings_line = recipe.readline()
            # check that servings line is correct format
            self.servings = eval(servings_line[0])
            nutrition_line = recipe.readline().split('|')
            self.calories = eval(nutrition_line[0].strip()[0])
            self.protein = eval(nutrition_line[1].strip()[0])
            self.carbs = eval(nutrition_line[2].strip()[0])
            self.fat = eval(nutrition_line[3].strip()[0])
            # find ingredients range
            # read ingredients into a dataframe with field names
            # find recipe range
            # read recipe into a list of fstrings?

    @property
    def nutrition_info(self):
        """return the calories, protein, carbs, and fat in the format found in recipe files"""
        return f'{self.calories} cals | {self.protein} P | {self.carbs} C | {self.fat} F'

    @staticmethod
    def calculate_nutrition(recipe_ingredients, servings):
        """calculates the nutrition of a recipe given the ingredients list"""
        # import ingredients
        ingredients_file = os.getcwd() + "\\Ingredients.csv"
        ingredient_bank = pd.read_csv(ingredients_file)
        ingredient_bank.set_index(['ingredient'], inplace=True)
        # go through recipe ingredients list and find them in ingredient bank csv
        ingredient_info = ingredient_bank.loc[list(recipe_ingredients.index)]
        # if ingredient doesn't exist throw an error
        # convert ingredient quantities and nutrition
        # collect nutrition for all ingredients
        recipe_nutrition = {}
        for nut in ['cal', 'P', 'C', 'F']:
            # Nutrition in recipe = (Quantity in recipe/Quantity in ingredient info)*Nutrition in ingredient info
            recipe_ingredients[nut] = np.array(
                recipe_ingredients['Q'].values)/ingredient_info['Q'].values*np.array(ingredient_info[nut].values)
            # Total nutrition = Sum of nutrition of all ingredients/Number of Servings in Recipe
            recipe_nutrition[nut] = int(
                np.sum(np.array(recipe_ingredients[nut].values))//servings)
        # format nutrition
        nutrition = [f' {v:d} {k} ' for k, v in recipe_nutrition.items()]
        nutrition = '|'.join(nutrition)
        # print and return nutrition
        print(f'Recipe Nutrition: {nutrition}')
        return nutrition

    @classmethod
    def write(cls, cookbook, recipe_name):
        """alternative constructor to write a text file and create a recipe instance through the console"""
        cookbook_folder = cookbook.folderpath
        recipe_filepath = cookbook_folder + "\\" + recipe_name + ".txt"
        with open(recipe_filepath, 'w', encoding='utf-8') as new_recipe:
            new_recipe.write(f'{recipe_name}\n')
            servings = eval(input("Enter the number of servings: "))
            new_recipe.write(f'{servings} Servings\n')
            new_recipe.write(
                "X cal | X P | X C | X F\nIngredients\nQ\tunit\tingredient\n")
            print('Enter ingredients (quantity\tunit\tingredient)\nor "Q" to finish:')
            # collect ingredients in a df
            ingredient_info = []
            while 1:
                ingredient = input()
                if ingredient.upper() == 'Q':
                    break
                new_recipe.write(f'{ingredient}\n')
                ingredient_info.append(ingredient.split('\t'))
                # convert quantity to number type
                ingredient_info[-1][0] = eval(ingredient_info[-1][0])
            recipe_ingredients = pd.DataFrame(
                ingredient_info, columns=['Q', 'un', 'ingredient'])
            recipe_ingredients.set_index(['ingredient'], inplace=True)
            new_recipe.write("Recipe\n")
            step_num = 1
            print('\nEnter recipe directions or "Q" to finish:')
            while 1:
                step = input(f'{step_num} . ')
                if step.upper() == 'Q':
                    break
                new_recipe.write(f'{step_num}. {step}\n')
                step_num += 1
            # calculate macros
            nutrition = cls.calculate_nutrition(recipe_ingredients, servings)
        # read entire recipe
        with open(recipe_filepath, 'r', encoding='utf-8') as new_recipe:
            recipe = new_recipe.readlines()
        # replace nutrition line with calculated nutrition
        with open(recipe_filepath, 'w', encoding='utf-8') as new_recipe:
            recipe[2] = nutrition
            new_recipe.writelines(recipe)
        print(f'{recipe_name} created!')
        return cls(recipe_filepath)


my_cookbook = Cookbook('Cookbook')
