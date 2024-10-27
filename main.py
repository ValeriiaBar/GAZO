import numpy as np
from constants import compounds_dict
import kinetik
from kinetik import custom_round
from pprint import pprint

# предположим, что следующие значения ввёл пользователь
compound = 'Метан'
t = 300 + 273.15  # КЕЛЬВИНОВ, НЕ ЦЕЛЬСИЙ
c = 1  # доли объёма
tau = 2.0  # секунды
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

result = [(coord, t - 273.15, c, X, tau * coord)]

min_step = 0.0001  # Минимальное значение шага
max_step = 0.01    # Максимальное значение шага
threshold_increase = 0.00002  # Порог для увеличения шага
threshold_decrease = 0.00004

while coord < 1 and c > 0:
    c_previous = result[-1][2]
    t_previous = result[-1][1]

    # k1 расчёт
    w_k1 = velocity_eq(c, t, constants)
    c_del = -tau * (step/2) * w_k1
    t_del = -c_del * ad_raz
    # Точка B
    c_k1 = c_previous + c_del
    t_k1 = t_previous + t_del + 273.15

    # k2 расчёт
    w_k2 = velocity_eq(c_k1, t_k1, constants)
    c_del = -tau * (step/2) * w_k2
    t_del = -c_del * ad_raz
    # точка C
    c_k2 = c_previous + c_del
    t_k2 = t_previous + t_del + 273.15

    # k3 расчёт
    w_k3 = velocity_eq(c_k2, t_k2, constants)
    c_del = -tau * step * w_k3
    t_del = -c_del * ad_raz
    # точка D
    c_k3 = c_previous + c_del
    t_k3 = t_previous + t_del + 273.15

    # k4 расчёт
    w_k4 = velocity_eq(c_k3, t_k3, constants)

    # final
    w_final = 1/6 * (w_k1 + 2 * w_k2 + 2 * w_k3 + w_k4)
    c_del = -tau * step * w_final
    t_del = -c_del * ad_raz
    c = c_previous + c_del  # конечная концентрация
    t = t_previous + t_del + 273.15  # конечная температура
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

    result.append(tuple(map(custom_round, (coord, t - 273.15, c, X, tau_current))))  # точка Е

    if result[-1][0] > 1:
        result.pop()


print(np.linspace(0, len(result) - 1, 12, dtype=np.int64))
for i in np.linspace(0, len(result) - 1, 12, dtype=np.int64):
    print(result[i])

# pprint(result)
# pprint(final_result)


































