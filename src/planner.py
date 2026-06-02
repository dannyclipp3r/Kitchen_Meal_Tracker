from src.storage import read_csv

COLUMNS = ["day", "meal_id"]


def load_weekly_plan():
    return read_csv("weekly_plan.csv", COLUMNS)
