from src.storage import read_csv

MEAL_COLUMNS = ["meal_id", "meal_name"]
INGREDIENT_COLUMNS = ["meal_id", "ingredient", "quantity", "unit"]


def load_meals():
    return read_csv("meals.csv", MEAL_COLUMNS)


def load_meal_ingredients():
    return read_csv("meal_ingredients.csv", INGREDIENT_COLUMNS)
