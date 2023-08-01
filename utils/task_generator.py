# Має генеруватись певна кількість чисел (5 за замовчуванням). Числа мають бути різними.
# Та значення директивного строку.
# Додатково має бути можливість обрати тип задачі (мін/макс).
# Можливо, є сенс проаналізувати наявні завдання, перед написанням власного алгоритму генерації.

# Виходячи з наявних даних:
# a) тривалості від 1 до 30.
# b) кожна задача містить 5 унікальних чисел в якості тривалості.
# c) дир. строки від 11 до 77.
# d) дир. строк менший від суми тривалостей від 1.17 до 3.36 разів.


import random
import numpy as np
from solver import solve


def generate_durations(n, start_range, end_range):
    """Ця функція генерує n випадкових чисел з заданого діапазону"""

    if n > (end_range - start_range + 1):
        raise ValueError(f"Cannot generate {n} unique numbers in the given range")

    return [int(i // 1.4) for i in random.sample(range(start_range, end_range + 1), n)]


def generate_ds(start_range=1, end_range=30):
    """Ця функція генерує значення директивного строку з використанням нормального розподілу"""

    loc = (start_range + end_range) / 2
    scale = (end_range - start_range) / 6

    return int(np.random.normal(loc, scale))


def generate_proble_data(n=5, start_range=1, end_range=30):
    """Ця функція генерує дані для задачі - тривалості, директивний строк та тип задачі"""

    durations = generate_durations(n, start_range, end_range)
    ds = generate_ds(start_range, end_range)
    is_min_task = random.choice([True, False])
    is_delayed = random.choice([True, False])

    return durations, ds, is_min_task, is_delayed


if __name__ == "__main__":
    print(
        f"+{'-' * 102}+\n|{'Тривалості робіт':^20}|{'Дир. строк':^12}|{'Досягає':^12}|{'Запізнюється':^14}|{'Оптимальний розклад':^22}|{'Опт.знач.крит.':^17}|\n+{'-' * 102}+")
    for _ in range(50):
        durations, ds, is_min_task, is_delayed = generate_proble_data(n=5, start_range=1, end_range=15)
        res, crit_val = solve(durations, ds, is_min_task, is_delayed)
        print(
            f"|{' '.join(map(str, durations)):^20}|{ds:^12}|{('Максимум', 'Мінімум')[is_min_task]:^12}|{('Ні', 'Так')[is_delayed]:^14}|{res:^22}|{crit_val:^17}|")
    print(f"+{'-' * 102}+")
