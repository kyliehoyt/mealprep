"""Generates and track weekly meal plans using cookbooking.py module"""
import cookbooking as cb
import numpy as np


def generate(targetcal=None):
    """generates a weekly meal plan that meets a certain nutrition target and minimizes produce waste"""
    # if target is None: get last target from meallog.csv
    if targetcal is None:
        targetcal = 1900  # RECPLACE with last target
    # else calc P/C/F from target cal and macro distribution
    # change to choose macro distribution from training mode
    prot_rate = 0.35
    carb_rate = 0.45
    fat_rate = 0.20
    targetnut = [round(x*targetcal)
                 for x in [1, prot_rate/4, carb_rate/4, fat_rate/9]]
    # set constants: meal distribution nutrition tolerance
    target_deviation = [50, 10, 10, 7]
    # load cookbook
    my_cookbook = cb.Cookbook('Cookbook')
    print(calc_average_breakfast(my_cookbook))
    print("Hello")


def calc_average_breakfast(cookbook):
    """computes the mean calories, protein, carbs, and fat of all the breakfast recipes in cookbook"""
    breakfast_names = cookbook.type["Breakfast"]
    nutrition = []
    for breakfast in breakfast_names:
        rec = cookbook.recipes[breakfast]
        nutrition.append([rec.calories, rec.protein, rec.carbs, rec.fat])
    return np.mean(nutrition, 0)


generate()
