from csv import DictReader, DictWriter
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
EXPORTS_DIR = ROOT_DIR / "exports"


def read_csv(filename: str, columns: list[str]) -> list[dict[str, str]]:
    path = DATA_DIR / filename
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(DictReader(file))


def write_csv(rows: list[dict[str, object]], filename: str, columns: list[str], export: bool = False) -> Path:
    directory = EXPORTS_DIR if export else DATA_DIR
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / filename

    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    return path

