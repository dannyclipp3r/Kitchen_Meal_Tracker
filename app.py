from src.inventory import load_inventory
from src.meals import load_meals, load_meal_ingredients
from src.planner import load_weekly_plan
from src.shopping_list import build_shopping_list, save_shopping_list


def main():
    inventory = load_inventory()
    meals = load_meals()
    meal_ingredients = load_meal_ingredients()
    weekly_plan = load_weekly_plan()

    shopping_list = build_shopping_list(inventory, meals, meal_ingredients, weekly_plan)
    save_shopping_list(shopping_list)

    print("Weekly shopping list generated:")
    if not shopping_list:
        print("No items needed.")
        return

    for item in shopping_list:
        print(f"- {item['ingredient']}: {item['quantity']} {item['unit']}")


if __name__ == "__main__":
    main()
