import PySimpleGUI as sg

from geometry import Parallelepiped, Sphere, Tetrahedron
from exporter import save_to_excel

try:
    from database import save_to_db, init_db
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

Window = getattr(sg, "Window")
Text = getattr(sg, "Text")
Combo = getattr(sg, "Combo")
Input = getattr(sg, "Input")
Multiline = getattr(sg, "Multiline")
Button = getattr(sg, "Button")
WIN_CLOSED = getattr(sg, "WIN_CLOSED")

MATERIAL = {
    "Сталь":      7800,
    "Алюминий":   2700,
    "Медь":       8900,
    "Дерево":      600,
    "Пластик":    1200,
}

FIGURE = {
    "Параллелепипед": "Введите a, b, c (стороны в метрах)",
    "Тетраэдр":       "Введите a (ребро в метрах); b и c не нужны",
    "Шар":            "Введите a (радиус в метрах); b и c не нужны",
}


class GeometryApp:
    """PySimpleGUI app for geometry calculations."""

    def __init__(self) -> None:
        self.last = None
        self.window = Window(
            "Расчёт геометрических тел",
            self._build_layout(),
            finalize=True,
            resizable=False,
            element_justification="left",
        )
        self._apply_shape_rules("Параллелепипед")

    def __str__(self) -> str:
        return f"GeometryApp(last={self.last is not None})"

    def __repr__(self) -> str:
        return f"GeometryApp(last={self.last!r})"

    @staticmethod
    def _build_layout():
        return [
            [Text("Геометрические тела", font=("Helvetica", 18, "bold"))],
            [Text("Фигура", size=(14, 1)), Combo(list(FIGURE.keys()), default_value="Параллелепипед", readonly=True, key="-SHAPE-")],
            [Text("Материал", size=(14, 1)), Combo(list(MATERIAL.keys()), default_value="Сталь", readonly=True, key="-MATERIAL-")],
            [Text(FIGURE["Параллелепипед"], key="-HINT-", size=(52, 2), text_color="blue")],
            [Text("a", size=(2, 1)), Input(key="-A-", size=(18, 1))],
            [Text("b", size=(2, 1)), Input(key="-B-", size=(18, 1))],
            [Text("c", size=(2, 1)), Input(key="-C-", size=(18, 1))],
            [Multiline("Результат появится здесь", key="-RESULT-", size=(56, 7), disabled=True, autoscroll=True)],
            [Button("Рассчитать", key="-CALC-"), Button("Сохранить в Excel", key="-XLS-")],
            [Button("Сохранить в БД (PostgreSQL)", key="-DB-", visible=DB_AVAILABLE)],
            [Text("PostgreSQL недоступен: кнопка сохранения в БД скрыта", visible=not DB_AVAILABLE, text_color="red")],
        ]

    def _set_result(self, message: str) -> None:
        self.window["-RESULT-"].update(message)

    def _append_result(self, message: str) -> None:
        old = self.window["-RESULT-"].get()
        self.window["-RESULT-"].update(f"{old}\n{message}")

    def _apply_shape_rules(self, shape: str) -> None:
        self.window["-HINT-"].update(FIGURE[shape])
        is_parallelepiped = shape == "Параллелепипед"
        self.window["-B-"].update(disabled=not is_parallelepiped)
        self.window["-C-"].update(disabled=not is_parallelepiped)

    @staticmethod
    def _parse_positive(value: str, name: str) -> float:
        try:
            number = float(value)
        except ValueError as exc:
            raise ValueError(f"Введите число в поле '{name}'") from exc

        if number <= 0:
            raise ValueError(f"Поле '{name}' должно быть больше нуля")
        return number

    def _build_shape(self, values: dict):
        shape = values["-SHAPE-"]
        material = values["-MATERIAL-"]
        density = MATERIAL[material]

        a = self._parse_positive(values["-A-"], "a")
        if shape == "Параллелепипед":
            b = self._parse_positive(values["-B-"], "b")
            c = self._parse_positive(values["-C-"], "c")
            return Parallelepiped(a=a, b=b, c=c, density=density, material=material)
        if shape == "Тетраэдр":
            return Tetrahedron(a=a, density=density, material=material)
        return Sphere(a=a, density=density, material=material)

    def calculate(self, values: dict) -> None:
        try:
            shape = self._build_shape(values)
        except ValueError as exc:
            self._set_result(str(exc))
            return

        print(f"str: {shape}")
        print(f"repr: {repr(shape)}")

        volume = shape.volume()
        surface = shape.surface()
        mass = shape.mass()
        self.last = {
            "shape": shape.shape_name,
            "material": shape.material,
            "volume": volume,
            "surface": surface,
            "mass": mass,
        }

        self._set_result(
            f"Объём:    {volume:.4f} м³\n"
            f"Площадь: {surface:.4f} м²\n"
            f"Масса:    {mass:.4f} кг"
        )

    def save_excel(self) -> None:
        if not self.last:
            self._set_result("Сначала выполните расчёт!")
            return

        save_to_excel(self.last)
        self._append_result("✓ Сохранено в results.xlsx")

    def save_db(self) -> None:
        if not self.last:
            self._set_result("Сначала выполните расчёт!")
            return

        try:
            save_to_db(self.last)
            self._append_result("✓ Сохранено в PostgreSQL")
        except (OSError, RuntimeError, ValueError) as exc:
            self._append_result(f"Ошибка БД: {exc}")

    def run(self) -> None:
        while True:
            event, values = self.window.read()
            if event in (WIN_CLOSED, "Exit"):
                break
            if event == "-SHAPE-":
                self._apply_shape_rules(values["-SHAPE-"])
            elif event == "-CALC-":
                self.calculate(values)
            elif event == "-XLS-":
                self.save_excel()
            elif event == "-DB-":
                self.save_db()

        self.window.close()


if __name__ == "__main__":
    if DB_AVAILABLE:
        init_db()
    GeometryApp().run()
