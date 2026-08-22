from src.meals import load_meals, load_meal_ingredients
from src.planner import load_weekly_plan
from src.shopping_list import build_shopping_list, save_shopping_list
from src.email_service import send_shopping_list_email


def main():
    meals = load_meals()
    meal_ingredients = load_meal_ingredients()
    weekly_plan = load_weekly_plan()

    shopping_list = build_shopping_list(meals, meal_ingredients, weekly_plan)
    save_shopping_list(shopping_list)

    print("Weekly shopping list generated:")
    if not shopping_list:
        print("No items needed.")
        return

    for item in shopping_list:
        print(f"- {item['ingredient']}: {item['quantity']} {item['unit']}")


if __name__ == "__main__":
    main()
