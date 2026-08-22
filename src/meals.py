from src.storage import read_csv, write_csv

MEAL_COLUMNS = ["meal_id", "meal_type", "meal_name"]
INGREDIENT_COLUMNS = ["meal_id", "ingredient", "quantity", "unit"]
MEAL_TYPES = ["Breakfast", "Lunch", "Dinner"]
DEFAULT_MEAL_TYPE = "Dinner"


def load_meals():
    meals = read_csv("meals.csv", MEAL_COLUMNS)
    for meal in meals:
        meal.setdefault("meal_type", DEFAULT_MEAL_TYPE)
        if not meal["meal_type"]:
            meal["meal_type"] = DEFAULT_MEAL_TYPE
    return meals


def load_meal_ingredients():
    return read_csv("meal_ingredients.csv", INGREDIENT_COLUMNS)


def _next_meal_id(meals):
    meal_ids = [int(meal["meal_id"]) for meal in meals if meal.get("meal_id", "").isdigit()]
    if not meal_ids:
        return "1"
    return str(max(meal_ids) + 1)


def _format_name(value):
    words = value.strip().split()
    formatted_words = []
    for word in words:
        if len(word) <= 2:
            formatted_words.append(word.upper())
        else:
            formatted_words.append(word[0].upper() + word[1:].lower())
    return " ".join(formatted_words)


def add_meal(meal_name, meal_type=DEFAULT_MEAL_TYPE):
    meal_name = _format_name(meal_name)
    meal_type = meal_type.strip()

    if not meal_name:
        raise ValueError("Meal name is required.")
    if meal_type not in MEAL_TYPES:
        raise ValueError("Meal type must be Breakfast, Lunch, or Dinner.")

    meals = load_meals()
    existing_names = {meal["meal_name"].strip().lower() for meal in meals}
    if meal_name.lower() in existing_names:
        raise ValueError("That meal already exists.")

    meal = {
        "meal_id": _next_meal_id(meals),
        "meal_type": meal_type,
        "meal_name": meal_name,
    }
    meals.append(meal)
    write_csv(meals, "meals.csv", MEAL_COLUMNS)
    return meal


def add_ingredient_to_meal(meal_id, ingredient, quantity, unit):
    meal_id = str(meal_id).strip()
    ingredient = _format_name(ingredient)
    quantity = str(quantity).strip()
    unit = unit.strip()

    if not meal_id:
        raise ValueError("Meal is required.")
    if not ingredient:
        raise ValueError("Ingredient name is required.")
    if not quantity:
        raise ValueError("Quantity is required.")
    if not unit:
        raise ValueError("Unit is required.")

    try:
        float(quantity)
    except ValueError as exc:
        raise ValueError("Quantity must be a number.") from exc

    meals = load_meals()
    meal_ids = {meal["meal_id"] for meal in meals}
    if meal_id not in meal_ids:
        raise ValueError("Selected meal does not exist.")

    meal_ingredients = load_meal_ingredients()
    row = {
        "meal_id": meal_id,
        "ingredient": ingredient,
        "quantity": quantity,
        "unit": unit,
    }
    meal_ingredients.append(row)
    write_csv(meal_ingredients, "meal_ingredients.csv", INGREDIENT_COLUMNS)
    return row


def update_meal_type(meal_id, meal_type):
    meal_id = str(meal_id).strip()
    meal_type = meal_type.strip()

    if not meal_id:
        raise ValueError("Meal is required.")
    if meal_type not in MEAL_TYPES:
        raise ValueError("Meal type must be Breakfast, Lunch, or Dinner.")

    meals = load_meals()
    for meal in meals:
        if meal["meal_id"] == meal_id:
            meal["meal_type"] = meal_type
            write_csv(meals, "meals.csv", MEAL_COLUMNS)
            return meal

    raise ValueError("Selected meal does not exist.")


def _validate_ingredient_fields(meal_id, ingredient, quantity, unit):
    meal_id = str(meal_id).strip()
    ingredient = _format_name(ingredient)
    quantity = str(quantity).strip()
    unit = unit.strip()

    if not meal_id:
        raise ValueError("Meal is required.")
    if not ingredient:
        raise ValueError("Ingredient name is required.")
    if not quantity:
        raise ValueError("Quantity is required.")
    if not unit:
        raise ValueError("Unit is required.")

    try:
        float(quantity)
    except ValueError as exc:
        raise ValueError("Quantity must be a number.") from exc

    return meal_id, ingredient, quantity, unit


def update_meal_ingredient(meal_id, row_index, ingredient, quantity, unit):
    meal_id, ingredient, quantity, unit = _validate_ingredient_fields(meal_id, ingredient, quantity, unit)
    row_index = int(row_index)
    meal_ingredients = load_meal_ingredients()
    matching_indexes = [
        index for index, row in enumerate(meal_ingredients)
        if row["meal_id"] == meal_id
    ]

    if row_index < 0 or row_index >= len(matching_indexes):
        raise ValueError("Selected ingredient does not exist.")

    target_index = matching_indexes[row_index]
    meal_ingredients[target_index] = {
        "meal_id": meal_id,
        "ingredient": ingredient,
        "quantity": quantity,
        "unit": unit,
    }
    write_csv(meal_ingredients, "meal_ingredients.csv", INGREDIENT_COLUMNS)
    return meal_ingredients[target_index]


def remove_meal_ingredient(meal_id, row_index):
    meal_id = str(meal_id).strip()
    row_index = int(row_index)
    meal_ingredients = load_meal_ingredients()
    matching_indexes = [
        index for index, row in enumerate(meal_ingredients)
        if row["meal_id"] == meal_id
    ]

    if row_index < 0 or row_index >= len(matching_indexes):
        raise ValueError("Selected ingredient does not exist.")

    target_index = matching_indexes[row_index]
    removed = meal_ingredients.pop(target_index)
    write_csv(meal_ingredients, "meal_ingredients.csv", INGREDIENT_COLUMNS)
    return removed

def delete_meal(meal_id):
    meal_id = str(meal_id).strip()

    if not meal_id:
        raise ValueError("Meal is required.")

    meals = load_meals()

    removed_meal = None
    remaining_meals = []

    for meal in meals:
        if meal["meal_id"] == meal_id:
            removed_meal = meal
        else:
            remaining_meals.append(meal)

    if removed_meal is None:
        raise ValueError("Selected meal does not exist.")

    write_csv(remaining_meals, "meals.csv", MEAL_COLUMNS)

    meal_ingredients = load_meal_ingredients()

    remaining_ingredients = [
        row for row in meal_ingredients
        if row["meal_id"] != meal_id
    ]

    write_csv(
        remaining_ingredients,
        "meal_ingredients.csv",
        INGREDIENT_COLUMNS
    )

    return removed_meal