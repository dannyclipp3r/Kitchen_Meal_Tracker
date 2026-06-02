from src.storage import read_csv

COLUMNS = ["ingredient", "quantity", "unit"]


def load_inventory():
    return read_csv("inventory.csv", COLUMNS)
