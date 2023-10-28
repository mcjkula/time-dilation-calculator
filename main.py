import flet as ft

def main(page: ft.Page):
    page.title = "Time Dilation Calculator"
    page.window_resizable = False
    page.window_width = 450
    page.window_height = 250

    const = ft.TextField(label="Speed of Light", text_align=ft.TextAlign.CENTER, width=150, dense=True, value='299792.458')
    speed = ft.TextField(label="Given Velocity", text_align=ft.TextAlign.CENTER, width=150, dense=True, autofocus=True)
    units = ft.Dropdown(
        label="Unit",
        options=[
            ft.dropdown.Option("km/s"),
            ft.dropdown.Option("% of c"),
            ft.dropdown.Option("m/s"),
            ft.dropdown.Option("km/h"),
        ],
        dense=True,
        width=100
    )

    def lorentz_factor(e):
        v = float(speed.value) if speed.value else 0.0
        c = float(const.value)

        if v == 0.0:
            # TODO
            page.update()
            return

        match units.value:
            case "km/s":
                result = c / ((c**2 - v**2)**0.5)
            case "% of c":
                result = c / ((c**2 - ((v / 100) * c)**2)**0.5)
            case "m/s":
                result = c / ((c**2 - (v / 1000)**2)**0.5)
            case "km/h":
                result = c / ((c**2 - (v / 3600)**2)**0.5)

        result_t.value = f"{result}"
        page.update()

    calc_time_delta = ft.ElevatedButton(width=100 ,text='Run', on_click=lorentz_factor)
    result_t = ft.TextField(label="Lorentz-Factor", text_align=ft.TextAlign.CENTER, width=310, dense=True, read_only=True)

    time_delta = ft.TextField(label="Dilated Time", text_align=ft.TextAlign.CENTER, width=150, dense=True, read_only=True)
    years = ft.TextField(label="Proper Time", text_align=ft.TextAlign.CENTER, width=150, dense=True)

    def time_dilation(e):
        t = float(result_t.value) if result_t.value else 0.0
        j = float(years.value) if years.value else 0.0

        if t == 0.0:
            # TODO
            page.update()
            return

        result = round(t * j, 4)
        time_delta.value = f"{result}"
        page.update()

    calc_time_diff = ft.ElevatedButton(width=100, text='Run', on_click=time_dilation)

    # Layout
    layout = ft.Column(
        [
            ft.Row([const, speed, units]),
            ft.Row([result_t, calc_time_delta]),
            ft.Divider(thickness=2.5),
            ft.Row([time_delta, years, calc_time_diff]),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(layout)
    page.update()

ft.app(target=main)
