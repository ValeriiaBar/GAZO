import numpy as np
from constants import compounds_dict
import kinetik
from kinetik import custom_round
from pprint import pprint
import customtkinter as ctk
np.set_printoptions(precision=6, suppress=True)

# предположим, что следующие значения ввёл пользователь
compound = 'Акролеин'
t = 200 + 273.15  # КЕЛЬВИНОВ, НЕ ЦЕЛЬСИЙ
c = 3  # доли объёма
tau = 3  # секунды
X = 0  # степень превращения


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
max_step = 0.01    # Максимальное значение шага
threshold_increase = 0.00002  # Порог для увеличения шага
threshold_decrease = 0.00004

result = np.array([[coord, t, c, X, tau * coord]])

while coord < 1 and c > 0:
    c_previous = result[-1][2]
    t_previous = result[-1][1]

    # k1 расчёт
    w_k1 = velocity_eq(c, t)

    c_del = -tau * (step/2) * w_k1
    t_del = -c_del * ad_raz
    # Точка B
    c_k1 = c_previous + c_del
    t_k1 = t_previous + t_del

    # k2 расчёт
    w_k2 = velocity_eq(c_k1, t_k1)
    c_del = -tau * (step/2) * w_k2
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
    w_final = 1/6 * (w_k1 + 2 * w_k2 + 2 * w_k3 + w_k4)
    c_del = -tau * step * w_final
    t_del = -c_del * ad_raz
    c = c_previous + c_del  # конечная концентрация
    t = t_previous + t_del  # конечная температура Кельвины
    X = (c_start - c)/c_start
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

print(result)
