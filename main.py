import numpy as np
from constants import compounds_dict
import mat_models
from mat_models import custom_round
from pprint import pprint
# from scipy.integrate import solve_ivp
from decimal import Decimal
import matplotlib.pyplot as plt


R = 1.987

# предположим, что следующие значения ввёл пользователь
compound = 'Оксид углеродa'
t = 200 + 273.15  # КЕЛЬВИНОВ, НЕ ЦЕЛЬСИЙ
c = 3  # доли объёма
tau = 3  # секунды
X = 0  # степень превращения

# Для начала инициализируем всё (а может быть пока что и не всё) что нужно:

# Начальная концентрация, которую нужно будет запомнить
c_start = c

# Константы, согласно выбранному соединению
constants = list(compounds_dict[compound].values())
print(constants[1], constants[2])

# Температура адибатического разогрева
ad_raz = constants[0]
coord = 0  # начальная координата

# шаг по координате
step = 0.001  # пусть пока будет такой

# Определение формулы расчёта скорости:
if compound == 'Оксид углеродa':
    velocity_eq = mat_models.CO_velocity
elif compound in {'Акролеин', 'Этилацетат', 'Уксусная кислота'}:
    velocity_eq = mat_models.AEU_velocity
else:
    velocity_eq = mat_models.others_velocity

# Попытка написать кастомный метод Рунгге-Кутта (или как там правильно его имя пишется)
# для конкретно этой задачи, наша независимая переменная - КООРДИНАТА и по ней мы шагаем,
# то есть это своего рода значение оси абсцисс, а изменяется у нас всё остальное,
# Время контакта изменяется пропорционально координате, то есть
# какой процент был пройден по координате - столько процентов прошло и времени


result = [(coord, t - 273.15, c, X, tau * coord)]
coord_range = np.arange(0, 1, step)  # количество координат

k1, k2, k3 = [], [], []
# имитация метода Эйлера

# tau_step = tau * step
# for z in coord_range:
#     # print(f'tau: {tau_current}')
#     # расчёт скорости:
#     w = velocity_eq(c, t, constants)  # скорость в текущей координате
#     # print(w)
#
#     c_del = -tau_step * w  # приращение по концентрации в точке coord
#     t_del = -c_del * ad_raz  # приращение по температуре в точке коорд
#     # print(c_del)
#     # print(t_del)
#     c = result[-1][2] + c_del  # новая концентрация (по методу Эйлера)
#     if c < 1e-10:
#         break
#     t = result[-1][1] + t_del + 273.15  # новая температура (по методу Эйлера)
#     # print(c)
#     # print(t - 273.15)
#     X = (c_start-c)/c_start  # степень превращения в точке
#     coord = coord + step  # рассчитываемая координата
#     tau_current = tau * coord  # текущее время
#     result.append(tuple(map(custom_round, (coord, t - 273.15, c, X, tau_current))))  # фиксация результата итерации в массив result

min_step = 0.0001  # Минимальное значение шага
max_step = 0.01    # Максимальное значение шага
threshold_increase = 0.00002  # Порог для увеличения шага
threshold_decrease = 0.00004

while coord < 1:
    c_previous = result[-1][2]
    t_previous = result[-1][1]

    # k1 расчёт
    w_k1 = velocity_eq(c, t, constants)
    c_del = -tau * (step/2) * w_k1
    t_del = -c_del * ad_raz
    c_k1 = c_previous + c_del
    t_k1 = t_previous + t_del + 273.15
    k1.extend((c_k1, t_k1))  # Точка B

    # k2 расчёт
    w_k2 = velocity_eq(c_k1, t_k1, constants)
    c_del = -tau * (step/2) * w_k2
    t_del = -c_del * ad_raz
    c_k2 = c_previous + c_del
    t_k2 = t_previous + t_del + 273.15
    k2.extend((c_k2, t_k2))  # точка C

    # k3 расчёт
    w_k3 = velocity_eq(c_k2, t_k2, constants)
    c_del = -tau * step * w_k3
    t_del = -c_del * ad_raz
    c_k3 = c_previous + c_del
    t_k3 = t_previous + t_del + 273.15
    k3.extend((c_k3, t_k3))  # точка D

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

    # if coord > 0.003:
    #     if abs(c_previous - c) > 0.000004:
    #         step /= 2
    #         continue
    #     elif abs(c_previous - c) < 0.000002:
    #         step *= 2
    #         continue
    #     else:
    concentration_change = abs(c - c_previous)

    if concentration_change > threshold_decrease and step > min_step:
        # Уменьшаем шаг, если изменение концентрации слишком большое
        step /= 2
    elif concentration_change < threshold_increase and step < max_step:
        # Увеличиваем шаг, если изменение концентрации слишком маленькое
        step *= 2

    result.append(tuple(map(custom_round, (coord, t - 273.15, c, X, tau_current))))  # точка Е


for i in range(1, len(result)):
    print(result[i])





































