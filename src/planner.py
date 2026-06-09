from itertools import cycle
from src.storage import read_csv, write_csv

COLUMNS = ["day", "meal_type", "meal_name", "meal_id"]
DEFAULT_DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
DEFAULT_MEAL_TYPES = ["Breakfast", "Lunch", "Dinner"]


def load_weekly_plan():
    return read_csv("weekly_plan.csv", COLUMNS)


def build_meal_plan(meals, days=None, meal_types=None):
    """Build a simple meal plan using day, meal type, and meal name.

    The rows include meal_id so shopping-list generation can still connect the
    selected meals to their ingredients.
    """
    days = days or DEFAULT_DAYS
    meal_types = meal_types or DEFAULT_MEAL_TYPES

    if not meals:
        raise ValueError("At least one meal is required to build a meal plan.")

    available_meals = [
        {
            "meal_id": str(meal["meal_id"]),
            "meal_type": meal.get("meal_type", "Dinner") or "Dinner",
            "meal_name": meal["meal_name"],
        }
        for meal in meals
        if meal.get("meal_id") and meal.get("meal_name")
    ]

    if not available_meals:
        raise ValueError("Meals must include meal_id and meal_name values.")

    all_meals = cycle(available_meals)
    meals_by_type = {
        meal_type: cycle([meal for meal in available_meals if meal["meal_type"] == meal_type])
        for meal_type in meal_types
        if any(meal["meal_type"] == meal_type for meal in available_meals)
    }

    plan = []
    for day in days:
        for meal_type in meal_types:
            meal_source = meals_by_type.get(meal_type, all_meals)
            meal = next(meal_source)
            plan.append(
                {
                    "day": day,
                    "meal_type": meal_type,
                    "meal_name": meal["meal_name"],
                    "meal_id": meal["meal_id"],
                }
            )

    return plan


def save_weekly_plan(weekly_plan):
    return write_csv(weekly_plan, "weekly_plan.csv", COLUMNS)
