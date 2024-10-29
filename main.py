import numpy as np
from constants import compounds_dict
import kinetik
from kinetik import custom_round
from pprint import pprint
import customtkinter as ctk

np.set_printoptions(precision=6, suppress=True)

root = ctk.CTk()  # инициализация главного окна
root.title("GAZO")
root.geometry('1200x800')
root.grid_columnconfigure(0, weight=1)
root.configure(fg_color="#34354a")

max_entry_value = 10

# Заголовок
header = ctk.CTkLabel(root, text='Розрахунок адіабатичного шару каталізатора'
                                 ' за моделлю ідеального витеснення\nдля процесів каталітичної очистки відходячих газів.\n\n'
                                 'Ведить початкові параметри',
                      font=ctk.CTkFont(family="Tahoma ", size=20, weight="bold", ), text_color='#c5c8ed', pady=20)
header.grid(row=0, column=0, sticky='n')

# Фрейм с вводными значениями
InputFrame = ctk.CTkFrame(root, fg_color='#3c3d54')  # Фрейм с вводными значениями
InputFrame.grid(row=1, column=0, sticky='ew', padx=30)
InputFrame.grid_columnconfigure((0, 1, 2, 3), weight=1)
InputFrame.grid_rowconfigure((0, 1), weight=1)

# Поля ввода
input_text_color = '#dee1fa'
compounds_input_label = ctk.CTkLabel(InputFrame, text='Речовина', text_color=input_text_color,
                                     font=ctk.CTkFont(family="Arial", size=16, weight="bold"), pady=10)
compounds_input_label.grid(row=0, column=0, sticky='n')
compounds_menu = ctk.CTkOptionMenu(InputFrame, values=["Оксид углеродa", "Метан", "Бутан", "Пентан",
                                                       "Гептан", "Декан", "Бензол", "Толуол", "Ксилол", "Стирол",
                                                       "Этанол", "Бутанол", "Фенол", "Ацетон", "Фурфурол",
                                                       "Акролеин", "Этилацетат", "Уксусная кислота"],
                                   fg_color='#212547', button_color='#212547', text_color=input_text_color,
                                   dropdown_fg_color='#212547', dropdown_hover_color="#616161",
                                   dropdown_text_color=input_text_color)
compounds_menu.grid(row=1, column=0, sticky='n', pady=(0, 20))

temp_input_label = ctk.CTkLabel(InputFrame, text='Температура входу, ℃', text_color=input_text_color,
                                font=ctk.CTkFont(family="Arial", size=16, weight="bold"), pady=10)
temp_input_label.grid(row=0, column=1, sticky='n')
temp_entry = ctk.CTkEntry(InputFrame, width=100, justify='center', fg_color='#212547', text_color=input_text_color)
temp_entry.insert(0, '300')
temp_entry.grid(row=1, column=1, sticky='n', pady=(0, 20))

concentration_input_label = ctk.CTkLabel(InputFrame, text="Концентрація, % об'єму", text_color=input_text_color,
                                         font=ctk.CTkFont(family="Arial", size=16, weight="bold"), pady=10)
concentration_input_label.grid(row=0, column=2, sticky='n')
concentration_entry = ctk.CTkEntry(InputFrame, width=100, justify='center' , fg_color='#212547', text_color=input_text_color)
concentration_entry.insert(0, '3')
concentration_entry.grid(row=1, column=2, sticky='n', pady=(0, 20))

time_input_label = ctk.CTkLabel(InputFrame, text='Час контакту, сек', text_color=input_text_color,
                                font=ctk.CTkFont(family="Arial", size=16, weight="bold"), pady=10)
time_input_label.grid(row=0, column=3, sticky='n')
time_entry = ctk.CTkEntry(InputFrame, width=100, justify='center' , fg_color='#212547', text_color=input_text_color)
time_entry.insert(0, '3')
time_entry.grid(row=1, column=3, sticky='n', pady=(0, 20))

# Фрейм для вывода
ResultsFrame = ctk.CTkFrame(root, fg_color='#3c3d54')
ResultsFrame.grid(row=2, column=0, sticky='ew', padx=30, pady=20)
ResultsFrame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
ResultsFrame.grid_rowconfigure((0, 1, 2), weight=1)
output_font_style = 'Segoe UI'

output_label = ctk.CTkLabel(ResultsFrame, text="Вихідні значення", text_color='#c5c8ed',
                            font=ctk.CTkFont(family="Arial", size=25, weight="bold"))
output_label.grid(row=0, column=0, columnspan=5, sticky='ew', pady=10)

values_output_label_color = '#dee1fa'
coord_label_output = ctk.CTkLabel(ResultsFrame, text='Координата, частки', text_color=values_output_label_color,
                                  font=ctk.CTkFont(size=15, family=output_font_style))
coord_label_output.grid(row=1, column=0, pady=(0, 5))

temp_label_output = ctk.CTkLabel(ResultsFrame, text='Поточна температура, ℃', text_color=values_output_label_color,
                                 font=ctk.CTkFont(size=15, family=output_font_style))
temp_label_output.grid(row=1, column=1, pady=(0, 5))

concentration_label_output = ctk.CTkLabel(ResultsFrame, text='Поточна концентрація, %', text_color=values_output_label_color,
                                          font=ctk.CTkFont(size=15, family=output_font_style))
concentration_label_output.grid(row=1, column=2, pady=(0, 5))

conversion_label_output = ctk.CTkLabel(ResultsFrame, text='Ступінь перетворення, частки', text_color=values_output_label_color,
                                       font=ctk.CTkFont(size=15, family=output_font_style))
conversion_label_output.grid(row=1, column=3, pady=(0, 5))

time_label_output = ctk.CTkLabel(ResultsFrame, text='Час контакту, сек', text_color=values_output_label_color,
                                       font=ctk.CTkFont(size=15, family=output_font_style))
time_label_output.grid(row=1, column=4, pady=(0, 5))

# Поля для вывода
text_box_field_color = '#212547'
text_text_color = '#dee1fa'
coord_text_output = ctk.CTkTextbox(ResultsFrame, width=150, height=280, fg_color=text_box_field_color,
                                   font=ctk.CTkFont(size=16, family='Arial'), text_color=text_text_color)
coord_text_output.grid(row=2, column=0, pady=(0, 20))
coord_text_output.configure(state='disabled')

temp_text_output = ctk.CTkTextbox(ResultsFrame, width=150, fg_color=text_box_field_color, text_color=text_text_color,
                                  height=280, font=ctk.CTkFont(size=16, family='Arial'))
temp_text_output.grid(row=2, column=1, pady=(0, 20))
temp_text_output.configure(state='disabled')

cooncentration_text_output = ctk.CTkTextbox(ResultsFrame, width=150, fg_color=text_box_field_color, text_color=text_text_color,
                                            height=280, font=ctk.CTkFont(size=16, family='Arial'))
cooncentration_text_output.grid(row=2, column=2, pady=(0, 20))
cooncentration_text_output.configure(state='disabled')

conversion_text_output = ctk.CTkTextbox(ResultsFrame, width=150, fg_color=text_box_field_color, text_color=text_text_color,
                                        height=280, font=ctk.CTkFont(size=16, family='Arial'))
conversion_text_output.grid(row=2, column=3, pady=(0, 20))
conversion_text_output.configure(state='disabled')

time_text_output = ctk.CTkTextbox(ResultsFrame, width=150, fg_color=text_box_field_color, text_color=text_text_color,
                                  height=280, font=ctk.CTkFont(size=16, family='Arial'))
time_text_output.grid(row=2, column=4, pady=(0, 20))
time_text_output.configure(state='disabled')
# --------------------------------------------------------------------
FooterFrame = ctk.CTkFrame(root, fg_color='#3c3d54')
FooterFrame.grid(row=3, column=0, sticky='ew', padx=30)
FooterFrame.grid_columnconfigure(0, weight=1)
FooterFrame.grid_rowconfigure((0, 1), weight=1)


def calculate(event=None):  # добавляем параметр event для работы с bind
    print("Кнопка РОЗРАХУВАТИ нажата")
    global compound, t, c, tau
    compound = compounds_menu.get()
    t = float(temp_entry.get()) + 273.15
    c = float(concentration_entry.get())
    tau = float(time_entry.get())
    print(compound, t, c, tau)
    X = 0

    c_start = c  # Начальная концентрация, которую нужно будет запомнить
    constants = list(compounds_dict[compound].values())  # Константы, согласно выбранному соединению
    ad_raz = constants[0]  # Температура адибатического разогрева
    coord = 0  # начальная координата

    # шаг по координате
    step = 0.001

    # Определение формулы расчёта скорости:
    if compound == 'Оксид углеродa':
        velocity_eq = kinetik.CO_velocity
    elif compound in {'Акролеин', 'Этилацетат', 'Уксусная кислота'}:
        velocity_eq = kinetik.AEU_velocity
    else:
        velocity_eq = kinetik.others_velocity

    velocity_eq = kinetik.constants_fixator(velocity_eq, constants)

    min_step = 0.0001  # Минимальное значение шага
    max_step = 0.01  # Максимальное значение шага
    threshold_increase = 0.00002  # Порог для увеличения шага
    threshold_decrease = 0.00004

    result = np.array([[coord, t, c, X, tau * coord]])
    print(result, '\n', '-' * 10)

    while coord < 1 and c > 0:
        c_previous = result[-1][2]
        t_previous = result[-1][1]

        # k1 расчёт
        w_k1 = velocity_eq(c, t)

        c_del = -tau * (step / 2) * w_k1
        t_del = -c_del * ad_raz
        # Точка B
        c_k1 = c_previous + c_del
        t_k1 = t_previous + t_del

        # k2 расчёт
        w_k2 = velocity_eq(c_k1, t_k1)
        c_del = -tau * (step / 2) * w_k2
        t_del = -c_del * ad_raz
        # точка C
        c_k2 = c_previous + c_del
        t_k2 = t_previous + t_del  # Кельвины

        # k3 расчёт
        w_k3 = velocity_eq(c_k2, t_k2)
        c_del = -tau * step * w_k3
        t_del = -c_del * ad_raz
        # точка D
        c_k3 = c_previous + c_del
        t_k3 = t_previous + t_del  # Кельвины

        # k4 расчёт
        w_k4 = velocity_eq(c_k3, t_k3)

        # final
        w_final = 1 / 6 * (w_k1 + 2 * w_k2 + 2 * w_k3 + w_k4)
        c_del = -tau * step * w_final
        t_del = -c_del * ad_raz
        c = c_previous + c_del  # конечная концентрация
        t = t_previous + t_del  # конечная температура Кельвины
        X = (c_start - c) / c_start
        coord = coord + step
        tau_current = tau * coord

        concentration_change = abs(c - c_previous)

        if concentration_change > threshold_decrease and step > min_step:
            # Уменьшаем шаг, если изменение концентрации слишком большое
            step /= 2
        elif concentration_change < threshold_increase and step < max_step:
            # Увеличиваем шаг, если изменение концентрации слишком маленькое
            step *= 2

        result = np.vstack((result, np.array(list(map(custom_round, (coord, t, c, X, tau_current))))))

    if result[-1][0] > 1:  # достаточно топорное решение проблемы
        # того, что последняя расчётная координата может быть больше 1, тем не менее...
        result = result[:-1]

    result = np.array([result[i] for i in
                       np.linspace(0, len(result) - 1, 12, dtype=np.int64)])  # равноудалённое распределение
    # значений координат

    result[:, 1] -= 273.15  # перевод Кельвинов в цельсии

    for i, decimals in enumerate((3, 2, 3, 4, 4)):  # округление чисел
        result[:, i] = np.round(result[:, i], decimals)

    for i, destination in zip(range(5), (coord_text_output,
                                         temp_text_output,
                                         cooncentration_text_output,
                                         conversion_text_output,
                                         time_text_output)):

        parameter_values = result[:, i]
        destination.configure(state='normal')
        destination.delete('1.0', 'end')

        for value in parameter_values:
            destination.insert('end', f"{value}\n")

        destination.configure(state='disabled')



calculate_button = ctk.CTkButton(FooterFrame, text='РОЗРАХУВАТИ', fg_color='#212547', text_color="white",
                                 font=ctk.CTkFont(weight='bold', size=20), command=calculate)
calculate_button.grid(row=0, column=0, sticky='n', pady=10)

root.bind('<Return>', calculate)

root.mainloop()
