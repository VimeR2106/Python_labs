from pathlib import Path

import openpyxl

RESULTS_FILE = Path("results.xlsx")
HEADERS = ["Фигура", "Материал", "Объём (м³)", "Площадь (м²)", "Масса (кг)"]


def save_to_excel(result: dict) -> None:
    if RESULTS_FILE.exists():
        workbook = openpyxl.load_workbook(RESULTS_FILE)
        sheet = workbook.active
    else:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(HEADERS)

    sheet.append([
        result["shape"],
        result["material"],
        round(result["volume"]),
        round(result["surface"]),
        round(result["mass"]),
    ])
    workbook.save(RESULTS_FILE)
