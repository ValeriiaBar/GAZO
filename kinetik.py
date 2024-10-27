import math
from functools import wraps


def CO_velocity(c: float,  # "концентрация",
                temp: float,  # "температура",
                constants: 'sequence',  # "список с константами, которые используются в уравнении Аррениуса
                ) -> float:
    """Функция вычисления скорости р-ции для оксида углерода;
    возвращает скорость реакции, в зависимости от
    температуры и концентрации"""
    if c < 1e-10:
        w = 0
        return w
    else:
        w = pow(c, 0.69) * constants[1] * math.exp(constants[2] / (1.987 * temp))
    return w


def AEU_velocity(c: float,  # "концентрация"
                 temp: float,  # "температура"
                 constants: 'sequence',  # "список с константами, которые используются в уравнении Аррениуса
                 ) -> float:
    # название AEU соответствует первым буквам трёх соединений, для которых она используется
    """Функция вычисления скорости р-ции для акролеина,
    этилацетата и уксусной к-ты; возвращает скорость реакции,
     в зависимости от температуры и концентрации"""
    if c < 1e-10:
        w = 0
    else:
        w = (c * constants[1] * math.exp(constants[2] / (1.987 * temp))) / \
            (1 + constants[3] * math.exp(constants[4] / (1.987 * temp)) * c)
    return w


def others_velocity(c: float,  # "концентрация"
                    temp: float,  # "температура"
                    constants: 'sequence',  # "список с константами, которые используются в уравнении Аррениуса
                    ) -> float:
    """Функция вычисления скорости р-ции остальных соединений;
     возвращает скорость реакции, в зависимости от температуры
     и концентрации"""
    if c < 1e-10:
        w = 0
    else:
        w = c * constants[1] * math.exp(constants[2] / (1.987 * temp))
    return w


def constants_fixator(kinetic_eq,  # кинетическое уравнение (CO_velocity, AEU_velocity или others_velocity)
                      constants_  # нужные константы из compounds_dict (см модуль constants)
                      ):
    """Этот декоратор нужен исключительно для того, чтобы запоминать константы
     для соответствующего кинетического уравнения, согласно выбранному элементу
     (смотри уравнения расчёта скорости выше)"""

    @wraps(kinetic_eq)
    def inner(*args, **kwargs):
        return kinetic_eq(*args, constants=constants_, **kwargs, )

    return inner


def custom_round(arg, prec=8):
    return round(arg, prec)
