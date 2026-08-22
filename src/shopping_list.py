from collections import defaultdict
from src.storage import write_csv

COLUMNS = ["ingredient", "quantity", "unit"]


def _number(value):
    return float(value or 0)


def build_shopping_list(meal_ingredients, weekly_plan):
    planned_meal_ids = [row["meal_id"] for row in weekly_plan]

    needed_by_item = defaultdict(float)
    for meal_id in planned_meal_ids:
        for ingredient in meal_ingredients:
            if ingredient["meal_id"] == meal_id:
                key = (ingredient["ingredient"], ingredient["unit"])
                needed_by_item[key] += _number(ingredient["quantity"])

    shopping_list = []
    for (ingredient, unit), needed_quantity in needed_by_item.items():
        quantity = needed_quantity

        if quantity > 0:
            shopping_list.append({
                "ingredient": ingredient,
                "quantity": f"{quantity:g}",
                "unit": unit,
            })

    return sorted(shopping_list, key=lambda row: row["ingredient"])


def save_shopping_list(shopping_list):
    write_csv(shopping_list, "shopping_list.csv", COLUMNS)
    write_csv(shopping_list, "weekly_shopping_list.csv", COLUMNS, export=True)
