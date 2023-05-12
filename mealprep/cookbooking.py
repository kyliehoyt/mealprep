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

    @classmethod
    def write(cls, cookbook, recipe_name):
        """alternative constructor to write a text file and create a recipe instance through the console"""
        cookbook_folder = cookbook.folderpath
        recipe_filepath = cookbook_folder + "\\" + recipe_name + ".txt"
        with open(recipe_filepath, 'w', encoding='utf-8') as new_recipe:
            print(f'Writing {recipe_name} recipe...')
            new_recipe.write(f'{recipe_name}\n')
            servings = eval(input("Enter the number of servings: "))
            new_recipe.write(f'{servings} Servings\n')
            new_recipe.write(
                "X cal | X P | X C | X F\nIngredients\nquantity\tunit\tingredient\n")
            print('Enter ingredients (quantity\tunit\tingredient)\nor "Q" to finish:')
            # collect ingredients in a df
            recipe_ingredients = IngredientList()
            while 1:
                raw_ingredient = input().lower()
                if raw_ingredient.upper() == 'Q':
                    break
                new_recipe.write(f'{raw_ingredient}\n')
                recipe_ingredients.add_ingredient(
                    Ingredient.from_recipe(raw_ingredient))
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
            recipe_ingredients.calculate_nutrition(servings)
        # read entire recipe
        with open(recipe_filepath, 'r', encoding='utf-8') as new_recipe:
            recipe = new_recipe.readlines()
        # replace nutrition line with calculated nutrition
        with open(recipe_filepath, 'w', encoding='utf-8') as new_recipe:
            recipe[2] = recipe_ingredients.nutrition
            new_recipe.writelines(recipe)
        print(f'{recipe_name} created!')
        # refresh cookbook
        Cookbook(cookbook.title)
        return cls(recipe_filepath)


class IngredientList:
    # init ingredients from csv or init empty dataframe
    def __init__(self, filepath=None):
        self.filepath = filepath
        self.total_nutrition = {}
        if self.filepath is None:
            self.ingredients = pd.DataFrame(
                columns=["quantity", "unit", "ingredient", "cal", "prot", "carb", "fat", "itype"])
        else:
            self.ingredients = pd.read_csv(filepath)
        self.ingredients.set_index(['ingredient'], inplace=True)

    def add_ingredient(self, ingredient):
        new_ingredient = pd.DataFrame(ingredient.as_dict())
        new_ingredient.set_index(['ingredient'], inplace=True)
        self.ingredients = pd.concat([self.ingredients, new_ingredient], ignore_index=False)

    def __len__(self):
        return len(self.ingredients.index)

    def calculate_nutrition(self, servings):
        """calculates the nutrition of a recipe given the ingredients list"""
        for nut in ['cal', 'prot', 'carb', 'fat']:
            self.total_nutrition[nut] = int(
                np.sum(np.array(self.ingredients[nut].values))//servings)
        return self.total_nutrition

    @property
    def nutrition(self):
        nutrition = [f' {v:d} {k} ' for k, v in self.total_nutrition.items()]
        return '|'.join(nutrition)


class Ingredient:
    """container for ingredient information"""

    def __init__(self, quantity, unit, name, cal, prot, carb, fat, itype):
        self.quantity = quantity
        self.unit = unit
        self.name = name
        self.calories = cal
        self.protein = prot
        self.carb = carb
        self.fat = fat
        self.itype = itype

    def pack(self):
        return pd.Series([self.quantity, self.unit, self.name, self.calories, self.protein, self.carb, self.fat, self.itype])
    
    def as_dict(self):
        return {k:[v] for k, v in zip(["quantity", "unit", "ingredient", "cal", "prot", "carb", "fat", "itype"], self.pack())}

    @classmethod
    def create_ingredient(cls):
        """add ingredient to ingredient csv"""

    @classmethod
    def from_recipe(cls, raw_ingredient):
        ingredient_info = raw_ingredient.split('\t')
        # convert quantity to number type
        ingredient_info[0] = eval(ingredient_info[0])
        # go through recipe ingredients list and find them in ingredient bank csv
        full_ingredient_info = bank.ingredients.loc[ingredient_info[2]]
        ingredient_info[3:7] = ingredient_info[0] / \
            full_ingredient_info['quantity'] * \
            full_ingredient_info['cal':'f'].values
        ingredient_info.append(full_ingredient_info['itype'])
        return cls(*tuple(ingredient_info))

    @staticmethod
    def peek(ingredient):
        print(bank.ingredients.loc[ingredient])


my_cookbook = Cookbook('Cookbook')
bankpath = os.getcwd() + "\\Ingredients.csv"
bank = IngredientList(bankpath)
