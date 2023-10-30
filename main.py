import flet as ft
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from flet.matplotlib_chart import MatplotlibChart
from matplotlib.patches import FancyArrowPatch


class Configuration:
    matplotlib.use("svg")
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = "Arial"
    matplotlib.rcParams["text.latex.preamble"] = r"\usepackage{cmbright}"
    COLOR_LINE = "#111111"
    COLOR_TEXT = "#111111"


class Visualization:
    def __init__(self):
        self.prev_fig = None

    def create_graph(self, v):
        if self.prev_fig is not None:
            plt.close(self.prev_fig)
        fig, ax = plt.subplots(figsize=(17.5, 7))
        ax.clear()
        ax.set_aspect("equal", "box")
        self.prev_fig = fig

        v = (v / 299792.458) * 10
        percentage = v / 0.1

        c_start, c_end = (0, 0), (0, -10)
        v_start, v_end = c_start, (v, 0)

        d_start = (0, 0)
        d_side = np.sqrt(abs(c_end[1]) ** 2 - v_end[0] ** 2)
        d_end = (v_end[0], -d_side)
        dd_start, dd_end = (v_end[0], 0), (v_end[0], -d_side)

        dt_start, dt_end = (-0.2, d_end[1]), (v_end[0] + 0.2, d_end[1]) if percentage != 100 else (v_start[1], d_end[1])

        t_start, t_end = (-0.2, c_end[1]), (v_end[0] + 0.2, c_end[1])

        td_start, td_end = (v_end[0], d_end[1]), (v_end[0], c_end[1])

        ax.fill_between(
            [v_start[0], v_end[0]], [dt_start[1], dt_end[1]], [t_start[1], t_end[1]], color="lightgray", alpha=0.5
        )
        # ax.plot([c_start[0], c_end[0]], [c_start[1], c_end[1]], color=color_line, lw=2, label="c")
        adjusted_c_end = (c_end[0], c_end[1] - 0.05)
        ax.add_patch(
            FancyArrowPatch(
                c_start,
                adjusted_c_end,
                mutation_scale=20,
                lw=2,
                arrowstyle="-|>",
                color=Configuration.COLOR_LINE,
                label="c",
            )
        )
        # Backup: ax.plot([v_start[0], v_end[0]], [v_start[1], v_end[1]], color=Configuration.COLOR_LINE, lw=2, label="v")
        # The endpoint of the Arrow needs to be adjusted for some reason as its shorter with an arrow than without
        adjusted_v_start = (v_start[0] - 0.05, v_start[1])
        if v_end[0] > 0:
            adjusted_v_end = (v_end[0] + 0.05, v_end[1])
            ax.add_patch(
                FancyArrowPatch(
                    adjusted_v_start,
                    adjusted_v_end,
                    mutation_scale=20,
                    lw=2,
                    arrowstyle="-|>",
                    color=Configuration.COLOR_LINE,
                    label="v",
                )
            )
        else:
            ax.add_patch(
                FancyArrowPatch(
                    v_start, v_end, mutation_scale=20, lw=2, arrowstyle="-|>", color=Configuration.COLOR_LINE, label="v"
                )
            )
        # ax.plot([d_start[0], d_end[0]], [d_start[1], d_end[1]], color=Configuration.COLOR_LINE, lw=1.5, label="d")
        ax.add_patch(
            FancyArrowPatch(
                d_start,
                d_end,
                mutation_scale=20,
                linestyle="dotted",
                lw=2,
                arrowstyle="-",
                color=Configuration.COLOR_LINE,
                label="d1",
            )
        )
        ax.add_patch(
            FancyArrowPatch(
                d_start,
                d_end,
                mutation_scale=20,
                linestyle="solid",
                lw=0,
                arrowstyle="-|>",
                color=Configuration.COLOR_LINE,
                label="d2",
            )
        )
        ax.plot([dd_start[0], dd_end[0]], [dd_start[1], dd_end[1]], color=Configuration.COLOR_LINE, lw=1.5, label="dd")
        ax.plot([dt_start[0], dt_end[0]], [dt_start[1], dt_end[1]], color=Configuration.COLOR_LINE, lw=2, label="dt")
        if v_end[0] >= (0.33 * abs(c_end[1])):
            ax.add_patch(
                FancyArrowPatch(
                    td_start,
                    td_end,
                    mutation_scale=20,
                    lw=2,
                    arrowstyle="-|>",
                    color=Configuration.COLOR_LINE,
                    label="td1",
                )
            )
            ax.add_patch(
                FancyArrowPatch(
                    td_end,
                    td_start,
                    mutation_scale=20,
                    lw=2,
                    arrowstyle="-|>",
                    color=Configuration.COLOR_LINE,
                    label="td2",
                )
            )
        ax.plot([t_start[0], t_end[0]], [t_start[1], t_end[1]], color=Configuration.COLOR_LINE, lw=2, label="t")
        ax.text(c_start[0] - 0.5, (c_start[1] + c_end[1]) / 2, "c", color=Configuration.COLOR_TEXT, fontsize=14)
        ax.text(
            (v_start[0] + v_end[0]) / 2,
            (v_start[1] + v_end[1]) / 2 + 0.5,
            f"v ({percentage:.5f}% of c)",
            ha="center",
            va="center",
            color=Configuration.COLOR_TEXT,
            fontsize=14,
        )
        ax.text(
            (t_start[0] + t_end[0]) / 2,
            (t_start[1] + t_end[1]) / 2 - 0.5,
            f"$\gamma$ = {abs(c_end[1]) / d_side:.10f}",
            ha="center",
            va="center",
            color=Configuration.COLOR_TEXT,
            fontsize=14,
        )
        ax.set_axis_off()
        return MatplotlibChart(fig, expand=True, transparent=True)


class LorentzFactorMath:
    @staticmethod
    def calculate(speed_value, const_value, unit):
        v = float(speed_value) if speed_value else 0.0
        c = float(const_value)

        if v == 0.0:
            return "1.0"

        try:
            if unit == "km/s":
                graph_v_value = v
            elif unit == "% of c":
                graph_v_value = (v / 100) * c
            elif unit == "m/s":
                graph_v_value = v / 1000
            elif unit == "km/h":
                graph_v_value = v / 3600
            result = c / ((c**2 - graph_v_value**2) ** 0.5)
        except ZeroDivisionError:
            result = float("inf")
        return result, graph_v_value


class TimeDilationMath:
    @staticmethod
    def calculate(result_t_value, years_value):
        t = float(result_t_value) if result_t_value else 0.0
        j = float(years_value) if years_value else 0.0

        if t == 0.0:
            return None

        result = round(t * j, 4)
        return f"{result}"


class TimeDilationApp:
    def __init__(self):
        self.visualization = Visualization()
        self.graph_v_value = 0
        self.chart_ref = [self.visualization.create_graph(self.graph_v_value)]
        self.slider_text = ft.Text("Velocity-Slider:")
        self.slider = ft.Slider(min=0, max=100, divisions=10, width=330, on_change=self.slider_changed)
        self.const = ft.TextField(
            label="Speed of Light", text_align=ft.TextAlign.CENTER, width=150, dense=True, value="299792.458"
        )
        self.speed = ft.TextField(
            label="Given Velocity", text_align=ft.TextAlign.CENTER, width=310, dense=True, autofocus=True
        )
        self.units = ft.Dropdown(
            label="Unit",
            options=[
                ft.dropdown.Option("km/s"),
                ft.dropdown.Option("% of c"),
                ft.dropdown.Option("m/s"),
                ft.dropdown.Option("km/h"),
            ],
            dense=True,
            width=100,
            value="% of c",
        )
        self.calc_time_delta = ft.ElevatedButton(width=100, text="Run", on_click=self.lorentz_factor)
        self.result_t = ft.TextField(
            label="Lorentz-Factor", text_align=ft.TextAlign.CENTER, width=310, dense=True, read_only=True
        )
        self.time_delta = ft.TextField(
            label="Dilated Time", text_align=ft.TextAlign.CENTER, width=150, dense=True, read_only=True
        )
        self.years = ft.TextField(label="Proper Time", text_align=ft.TextAlign.CENTER, width=150, dense=True)
        self.calc_time_diff = ft.ElevatedButton(width=100, text="Get", on_click=self.time_dilation)

    def lorentz_factor(self, e):
        result, self.graph_v_value = LorentzFactorMath.calculate(self.speed.value, self.const.value, self.units.value)
        self.chart_ref[0] = self.visualization.create_graph(self.graph_v_value)
        self.result_t.value = f"{result}"

        v = float(self.speed.value)
        c = float(self.const.value)

        match self.units.value:
            case "km/s":
                percentage = (v / c) * 100
            case "% of c":
                percentage = v
            case "m/s":
                percentage = ((v * 0.001) / c) * 100
            case "km/h":
                percentage = ((v / 3600) / c) * 100
        self.slider.value = round(int(percentage) / 10.0) * 10

        self.page.update()

    def time_dilation(self, e):
        result = TimeDilationMath.calculate(self.result_t.value, self.years.value)
        self.time_delta.value = result
        self.page.update()

    def slider_changed(self, e):
        v = (float(e.control.value) / 100) * 299792.458
        self.chart_ref[0] = self.visualization.create_graph(v)

        match self.units.value:
            case "km/s":
                self.speed.value = f"{v:.3f}"
            case "% of c":
                self.speed.value = f"{float(e.control.value)}"
            case "m/s":
                self.speed.value = f"{(v * 1000):.3f}"
            case "km/h":
                self.speed.value = f"{(v * 3600):.3f}"
        self.result_t.value,_ = LorentzFactorMath.calculate(self.speed.value, self.const.value, self.units.value)
        self.page.update()

    def layout_app(self, page):
        row1 = ft.Row(
            [
                self.slider_text,
                self.slider
            ]
        )
        row2 = ft.Row([self.speed, self.units])
        row3 = ft.Row([self.result_t, self.calc_time_delta])
        row4 = ft.Row([self.time_delta, self.years, self.calc_time_diff])

        rows_column = ft.Column([row1, row2, row3, ft.Divider(), row4], alignment=ft.MainAxisAlignment.CENTER)

        page.add(
            ft.Row(
                [
                    ft.Container(
                        content=rows_column,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Row(self.chart_ref),
                        alignment=ft.alignment.center,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        )

    def main(self, page):
        self.page = page
        page.title = "Time Dilation-Calculator"
        page.window_height = 500
        page.window_width = 866
        page.window_resizable = False
        self.layout_app(page)
        page.theme_mode = ft.ThemeMode.LIGHT
        page.update()


app = TimeDilationApp()
ft.app(target=app.main)