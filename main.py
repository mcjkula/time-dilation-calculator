import PySimpleGUI as sg

sg.theme('Reddit')
layout = [[sg.Input(default_text='299792.458', justification='center', key='-INPUT1-', readonly=True),
           sg.Text('c in km/s', key='-UNIT-')],
          [sg.Input(default_text='299792.458', size=(22, 1), pad=((5, 0), (0, 0)), justification='center',
                    key='-INPUT2-', readonly=True),
           sg.Input(default_text='', size=(22, 1), pad=(3, 0), justification='center', focus=True, key='-INPUT3-'),
           sg.Spin(('km/s', '% of c', 'm/s', 'km/h'), size=(7, 1), key='-LIST1-')],
          [sg.Button('Berechnen', size=(39, 1), key='-BUTTON1-')],
          [sg.Input(justification='center', size=(45, 1), key='-INPUT4-', readonly=True), sg.Text("= t'")],
          [sg.HorizontalSeparator()],
          [sg.Input(default_text='0', size=(22, 1), pad=((5, 0), (0, 0)), justification='center',
                    key='-INPUT5-', readonly=True),
           sg.Input(default_text='', size=(22, 1), pad=(3, 0), justification='center', key='-INPUT6-'),
           sg.Text('Jahre')],
          [sg.Button('Umwandeln', size=(39, 1), key='-BUTTON2-')]
          ]

window = sg.Window('Zeitdilatationsrechner', layout)

while True:
    event, values = window.read()

    if event == '-BUTTON1-':
        v = values['-INPUT3-']
        c = values['-INPUT2-']
        if v.isnumeric():
            match values['-LIST1-']:

                case 'km/s':
                    output = float(c) / ((float(c) ** 2 - float(v) ** 2) ** 0.5)
                    window['-INPUT4-'].update(output)

                case '% of c':
                    output = float(c) / ((float(c) ** 2 - ((float(v) / 100) * float(c)) ** 2) ** 0.5)
                    window['-INPUT4-'].update(output)

                case 'm/s':
                    output = float(c) / ((float(c) ** 2 - (float(v) / 1000) ** 2) ** 0.5)
                    window['-INPUT4-'].update(output)

                case 'km/h':
                    output = float(c) / ((float(c) ** 2 - (float(v) / 3600) ** 2) ** 0.5)
                    window['-INPUT4-'].update(output)

    if event == '-BUTTON2-':
        t = values['-INPUT4-']
        j = values['-INPUT6-']
        j_output = round(float(j) / float(t), 4)
        window['-INPUT5-'].update(j_output)

    if event == sg.WINDOW_CLOSED:
        break

window.close()
