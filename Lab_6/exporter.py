import os
import openpyxl

FILE = "results.xlsx"
HEADERS = ["Фигура", "Материал", "Объём (м³)", "Площадь (м²)", "Масса (кг)"]


def save_to_excel(result: dict):
    if os.path.exists(FILE):
        wb = openpyxl.load_workbook(FILE)
        ws = wb.active
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(HEADERS)

    ws.append([
        result["shape"],
        result["material"],
        round(result["volume"]),
        round(result["surface"]),
        round(result["mass"]),
    ])
    wb.save(FILE)
