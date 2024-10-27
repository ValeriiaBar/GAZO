import math
import numpy as np
print(np.linspace(1, 10, 10, dtype=np.uint32))

# Словарь с константами для различных соединений
compounds_dict = {'Оксид углеродa': {'ad_raz': 91, 'c1': 600, 'c2': -7600, 'c3': None, 'c4': None},
                  'Метан': {'ad_raz': 297, 'c1': 1140000, 'c2': -19017, 'c3': None, 'c4': None},
                  'Бутан': {'ad_raz': 868, 'c1': 770000, 'c2': -16600, 'c3': None, 'c4': None},
                  'Пентан': {'ad_raz': 1179, 'c1': 118000, 'c2': -13700, 'c3': None, 'c4': None},
                  'Гептан': {'ad_raz': 1495, 'c1': 43800, 'c2': -10300, 'c3': None, 'c4': None},
                  'Декан': {'ad_raz': 2050, 'c1': 1450000, 'c2': -15000, 'c3': None, 'c4': None},
                  'Бензол': {'ad_raz': 1101, 'c1': 120000, 'c2': -11000, 'c3': None, 'c4': None},
                  'Толуол': {'ad_raz': 1318, 'c1': 25100, 'c2': -11430, 'c3': None, 'c4': None},
                  'Ксилол': {'ad_raz': 1413, 'c1': 1450000, 'c2': -15000, 'c3': None, 'c4': None},
                  'Стирол': {'ad_raz': 1483, 'c1': 120000, 'c2': -11000, 'c3': None, 'c4': None},
                  'Этанол': {'ad_raz': 410, 'c1': 1090000, 'c2': -14900, 'c3': None, 'c4': None},
                  'Бутанол': {'ad_raz': 907, 'c1': 160000, 'c2': -11610, 'c3': None, 'c4': None},
                  'Фенол': {'ad_raz': 996, 'c1': 120000, 'c2': -11000, 'c3': None, 'c4': None},
                  'Ацетон': {'ad_raz': 597, 'c1': 160000, 'c2': -11900, 'c3': None, 'c4': None},
                  'Фурфурол': {'ad_raz': 775, 'c1': 1900, 'c2': -7200, 'c3': None, 'c4': None},
                  'Акролеин': {'ad_raz': 428, 'c1': 1470, 'c2': -5300, 'c3': 5.5, 'c4': 5100},
                  'Этилацетат': {'ad_raz': 751, 'c1': 205, 'c2': -4830, 'c3': 2.35e-16, 'c4': -10730},
                  'Уксусная кислота': {'ad_raz': 291, 'c1': 403000, 'c2': -13600, 'c3': 6.06, 'c4': 4530}
}


def velocity(c: float, temp: float, compound_type: str) -> float:
    """Функция вычисления скорости р-ции для различных соединений;
    возвращает скорость реакции в зависимости от температуры и концентрации."""

    # Получение констант из словаря
    constants = compounds_dict[compound_type]['constants']

    if c < 1e-10:
        return 0

    if compound_type == "CO":
        return pow(c, 0.69) * constants[1] * math.exp(constants[2] / (1.987 * temp))

    elif compound_type == "AEU":
        return (c * constants[1] * math.exp(constants[2] / (1.987 * temp))) / \
            (1 + constants[3] * math.exp(constants[4] / (1.987 * temp)) * c)

    elif compound_type == "others":
        return c * constants[1] * math.exp(constants[2] / (1.987 * temp))

    raise ValueError("Неизвестный тип реакции.")

