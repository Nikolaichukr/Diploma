"""Цей файл містить увесь потрібний код для генерації завдання"""

import random
from typing import List

import numpy as np


def generate_job_durations(jobs_amount: int, jobs_duration_min: int, jobs_duration_max: int) -> List[int]:
    """Генерує список з N тривалостей робіт, де N-1 робіт мають унікальну тривалість, а одна інша повторюється"""

    if jobs_duration_max - jobs_duration_min + 1 < jobs_amount:
        raise ValueError(
            f"У діапазоні [{jobs_duration_min}, {jobs_duration_max}] недостатньо значень, аби згенерувати {jobs_amount} робіт."
        )

    mu = (jobs_duration_min + jobs_duration_max) / 2

    # sigma (std.dev) була обрана таким чином (max-min)/4, що ~95% значень знаходяться в межах [min, max]
    sigma = (jobs_duration_max - jobs_duration_min) / 4

    # Визначаємо скільки наборів повторів буде, тобто один з варіантів:
    # 1 2 3 4 5 6       - в 20% випадків
    # 1 (2 3) 4 5 6     - в 50% випадків
    # 1 (2 3) (4 5) 6   - в 30% випадків

    duplicates_sets = np.random.choice([0, 0, 1, 1, 1, 1, 1, 2, 2, 2])

    # Визначаємо скільки дублікатів буде в самих дужках, один з двох сценаріїв:
    # 1) (7, 7)
    # 2) (9, 9, 9)

    if jobs_amount > 5:
        duplicate_amounts = [np.random.choice([1, 2]) for _ in range(duplicates_sets)]
    else:
        duplicate_amounts = [1 for _ in range(duplicates_sets)]

    # Ініціалізуємо масив тривалостей та допоміжну множину
    durations_set = set()
    durations = np.empty(0, dtype=int)

    # Генеруємо початковий набір унікальних тривалостей (без дублікатів)
    while len(durations) < (jobs_amount - sum(duplicate_amounts)):
        new_durations = np.round(np.random.normal(mu, sigma, jobs_amount - len(durations)))
        for duration in new_durations:
            duration = int(duration)
            if jobs_duration_min <= duration <= jobs_duration_max and duration not in durations_set:
                durations = np.append(durations, duration)
                durations_set.add(duration)
            if len(durations) == (jobs_amount - sum(duplicate_amounts)):
                break

    # Додаємо дублікати до списку тривалостей
    duplicate_values = random.sample(list(durations), duplicates_sets)
    for dup_duration, dup_times in zip(duplicate_values, duplicate_amounts):
        for _ in range(dup_times):
            durations = np.append(durations, dup_duration)

    return list(durations)


def generate_dis(jobs_amount, jobs_durations):
    """Функція для генерації директивних строків"""

    total_duration = sum(jobs_durations)
    deadlines = []
    for _ in range(jobs_amount):
        multiplier = random.uniform(0.5, 0.9)
        proposed_deadline = int(total_duration * multiplier)

        deadlines.append(proposed_deadline)

    return deadlines


def generate_job_weights(jobs_amount: int, weight_min: int = 1, weight_max: int = 3) -> List[int]:
    """Повертає список ваг для N робіт"""

    return [random.randint(weight_min, weight_max) for _ in range(jobs_amount)]


def format_job_tuple_to_string(job):
    """Конвертує кортеж до рядка формату '№i / ti / ui / di'"""
    if isinstance(job, tuple):
        return f"№{job[0]} / {job[1]} / {job[2]} / {job[3]}"
    return job


def generate_order_problem_data(jobs_amount_min, jobs_amount_max, jobs_duration_min, jobs_duration_max):
    """Функція генерує дані задачі - список робіт, представлених у вигляді кортежів (№i, ti, di, ui)"""
    jobs_amount = random.randint(jobs_amount_min, jobs_amount_max)

    jobs_indexes = list(range(1, jobs_amount + 1))
    jobs_durations = generate_job_durations(jobs_amount, jobs_duration_min, jobs_duration_max)
    jobs_dis = generate_dis(jobs_amount, jobs_durations)
    jobs_weights = generate_job_weights(jobs_amount)

    # Список робіт [(№i, ti, di, ui), ..., (№i, ti, di, ui)]
    jobs_list = list(zip(jobs_indexes, jobs_durations, jobs_dis, jobs_weights))

    return jobs_list

    # return [
    #     "№1 / 16 / 34 / 3",
    #     "№2 / 20 / 42 / 3",
    #     "№3 / 20 / 33 / 1",
    #     "№4 / 9 / 48 / 3",
    #     "№5 / 15 / 41 / 3",
    # ]


if __name__ == "__main__":
    for _ in range(5):
        lst = generate_order_problem_data(5, 7, 5, 25)
        for j in lst:
            print(format_job_tuple_to_string(j))
        print()
