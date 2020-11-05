import PySimpleGUI as sg
import textFunc
import numpy as np
import simple_code_text as sct

# Условие третьей лабораторной работы
H = np.array([
    [0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 1, 1, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1],
])
# n - кол-во информативных бит, k - проверочных
n, k = (5, 4)
# 0 -> 00000, ..., 31 -> 11111
dict_coded = dict(zip([str(i) for i in range(32)], [bin(i)[2:].zfill(n) for i in range(32)]))
ham_dict_coded = textFunc.get_coded_hamming(H)

layout_research = '''d0: {0}
Граница Хэмминга: {1}
Граница Плоткина: {2}
Граница Варшамова-Гильберта: {3}'''

code_text = sg.InputText(size=(55, 1))
code_Hamming = sg.Output(size=(25, 10))
decode_Hamming = sg.Output(size=(25, 10))
errors_Hamming = sg.Output(size=(25, 10))
research = sg.Output(size=(25, 10))
research_haffman = sg.Output(size=(25, 10))

code_Haffman = sg.Output(size=(25, 10))
decode_Haffman = sg.Output(size=(25, 10))
errors_Haffman = sg.Output(size=(25, 10))

layout = [
    [sg.Text('Input text from file:')],
    [sg.InputText(), sg.FileBrowse(), sg.Submit('Input')],
    [sg.Text('Введите текст для шифрования')],
    [code_text],
    [sg.Text('Закодированный кодом Хэмминга', size=(30, 1), justification='left'), sg.Text('Хаффмана', size=(15, 1), justification='right')],
    [code_Hamming, code_Haffman],
    [sg.Text('Декодированный Хэмминг', size=(20, 1), justification='left'), sg.Text('Хаффман', size=(25, 1), justification='right')],
    [sg.Submit('Decode')],
    [decode_Hamming, decode_Haffman],
    [sg.Text('Список исправленных ошибок  /  обнаруженных (Хаффман)', size=(50, 1), justification='left')],
    [errors_Hamming, errors_Haffman],
    [sg.Text('Исследования', size=(20, 1), justification='left')],
    [research, research_haffman],
    [sg.Submit('Run', size=(25, 1))],
]

window = sg.Window('3 Lab', layout)
while True:
    event, values = window.read()

    try:
        if event in (None, 'Exit', 'Cancel'):
            break
        elif event == 'Input':
            if values[0]:
                with open(values[0], 'r') as fileIn:
                    code_text.update(fileIn.read())

        elif event == 'Run':
            if len(code_text.Get()) > 0:
                source_text = code_text.Get().split()
                coded_str = textFunc.hamming_code(source_text, ham_dict_coded, k)
                code_Haffman.update(textFunc.encode(source_text, dict_coded))
                code_Hamming.update(coded_str)

                text_decoded_str, err_list = textFunc.decode(code_Haffman.Get().split(), dict_coded)
                decode_Haffman.update(text_decoded_str)
                errors_Haffman(str(err_list))

                text_decoded_str, err_list = textFunc.hamming_decode(coded_str, ham_dict_coded, H, k)
                decode_Hamming.update(text_decoded_str)
                errors_Hamming.update(str(err_list))

                d0 = textFunc.min_hamming_metrics(ham_dict_coded)
                research.update(layout_research.format(
                    d0,
                    textFunc.hamming_boundary(n, k, 1),
                    textFunc.plotkin_boundary(d0, n, k),
                    textFunc.varshamov_gilbert_boundary(n, k, d0),
                ))

                d0 = textFunc.min_hamming_metrics(dict_coded)
                research_haffman.update(layout_research.format(
                    d0,
                    0,
                    0,
                    textFunc.varshamov_gilbert_boundary(n, n, d0),
                ))
            else:
                errors_Hamming.update('Введите текст в соотстветствующее поле')
        elif event == 'Decode':
            if len(code_Haffman.Get()) > 0 and len(code_Hamming.Get()) > 0:
                text_decoded_str, err_list = textFunc.decode(code_Haffman.Get().split(), dict_coded)
                decode_Haffman.update(text_decoded_str)
                errors_Haffman(str(err_list))
                text_decoded_str, err_list = textFunc.hamming_decode(code_Hamming.Get().split(), ham_dict_coded, H, k)
                decode_Hamming.update(text_decoded_str)
                errors_Hamming.update(str(err_list))

    except BaseException as e:
        print(e)
