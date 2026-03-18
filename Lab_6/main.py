from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

from geometry import parallelepiped, tetrahedron, sphere
from exporter import save_to_excel

try:
    from database import save_to_db, init_db
    DB_AVAILABLE = True
except Exception:
    DB_AVAILABLE = False

Window.size = (480, 640)

# Плотности материалов (кг/м³)
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


class GeometryLayout(BoxLayout):
    """
    Application Core 
    """

    label = Label(
        text="Геометрические тела",
        font_size="22sp",
        size_hint_y=None,
        height=40
    )
    shape = Spinner(
        text="Параллелепипед",
        values=list(FIGURE.keys()),
        size_hint_y=None,
        height=50
    )
    material = Spinner(
        text="Сталь",
        values=list(MATERIAL.keys()),
        size_hint_y=None,
        height=50
    )
    hint = Label(
        text=FIGURE["Параллелепипед"],
        size_hint_y=None,
        height=30,
        font_size="13sp"
    )
    input_a = TextInput(
        hint_text="a",
        multiline=False,
        size_hint_y=None,
        height=50
    )
    input_b = TextInput(
        hint_text="b",
        multiline=False,
        size_hint_y=None, 
        height=50
    )
    input_c = TextInput(
        hint_text="c",
        multiline=False,
        size_hint_y=None,
        height=50
    )
    compute = Label(
        text="Результат появится здесь",
        font_size="15sp",
        size_hint_y=None,
        height=150,
        halign="center",
        valign="middle"
    )
    # compute.bind(size=compute.setter("text_size"))
    btn_xls = Button(
        text="Сохранить в Excel",
        size_hint_y=None,
        height=50
    )
    btn_calc = Button(
        text="Рассчитать",
        size_hint_y=None,
        height=50
    )
    btn_db = Button(
        text="Сохранить в БД (PostgreSQL)",
        size_hint_y=None,
        height=50
    )
    last = None

    def __init__(self, **kwargs):
        """
        Add objects to the App
        """
        super().__init__(orientation="vertical", padding=16, spacing=8, **kwargs)

        CALCULATOR_OBJ = [
            self.label,
            self.shape,
            self.material,
            self.hint,
            self.input_a,
            self.input_b,
            self.input_c,
            self.compute,
            self.btn_calc,
            self.btn_xls
        ]

        ####################
        # Actions
        ####################
        self.shape.bind(text=self.on_shape)
        self.btn_xls.bind(on_press=self.save_excel)
        self.btn_calc.bind(on_press=self.calculate)

        # Check db exist and extend widget
        if DB_AVAILABLE:
            CALCULATOR_OBJ.append(self.btn_db)         
            self.btn_db.bind(on_press=self.save_db)

        # Add objects to widget
        for item in CALCULATOR_OBJ:
            self.add_widget(item)


    def on_shape(self, spinner, text):
        """
        Show the Hint text based on figure 
        """
        self.hint.text = FIGURE[text]

    def _parse_float(self, widget, name):
        """
        Check the 
        """
        try:
            return float(widget.text)
        except ValueError:
            raise ValueError(f"Введите число в поле \"{name}\"")

    def _check_constraints(self, *_):
        """
        """
        try:
            float(self.input_a.text)
            float(self.input_b.text)
            float(self.input_c.text)
        except:
            self.compute.text = "Для рассчета используйте только числа!"
            return True


    def calculate(self, *_):
        """
        Perform claculation or raise an error
        """
        not_valid = self._check_constraints()
        if not_valid:
            return
        shape    = self.shape.text
        material = self.material.text
        density  = MATERIAL[material]
        try:
            a = self._parse_float(self.input_a, "a")
            if shape == "Параллелепипед":
                b = self._parse_float(self.input_b, "b")
                c = self._parse_float(self.input_c, "c")
                v = parallelepiped.volume(a, b, c)
                s = parallelepiped.surface(a, b, c)
                m = parallelepiped.mass(density, a, b, c)
            elif shape == "Тетраэдр":
                v = tetrahedron.volume(a)
                s = tetrahedron.surface(a)
                m = tetrahedron.mass(density, a)
            else:  # Шар
                v = sphere.volume(a)
                s = sphere.surface(a)
                m = sphere.mass(density, a)
        except ValueError as e:
            self.compute.text = str(e)
            return

        self.last = {"shape": shape, "material": material,
                     "volume": v, "surface": s, "mass": m}
        self.compute.text = (f"Объём:    {v:.4f} м³\n"
                            f"Площадь: {s:.4f} м²\n"
                            f"Масса:    {m:.4f} кг")

    def _check_compute(self, *_):
        """
        Check the computation performed
        and raise an error
        """
        if not self.last:
            self.compute.text = "Сначала выполните расчёт!"; 
            return True

    def save_excel(self, *_):
        """
        Export computation to xls file
        """
        not_valid = self._check_compute()
        if not_valid:
            return

        save_to_excel(self.last)
        self.compute.text += "\n✓ Сохранено в results.xlsx"

    def save_db(self, *_):
        """
        Save data to the DB
        """
        not_valid = self._check_compute()
        if not_valid:
            return

        try:
            save_to_db(self.last)
            self.compute.text += "\n✓ Сохранено в PostgreSQL"
        except Exception as e:
            self.compute.text += f"\nОшибка БД: {e}"


class GeometryApp(App):
    """
    Init DB and run the App
    """

    title = "Рассчет геометрических тел"

    def build(self):
        if DB_AVAILABLE:
            init_db()
        return GeometryLayout()


if __name__ == "__main__":
    GeometryApp().run()
