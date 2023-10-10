import random
import numpy as np
from typing import List


def generate_job_durations(
    jobs_amount: int, jobs_duration_min: int, jobs_duration_max: int
) -> List[int]:
    """Генерує список з N тривалостей робіт, де N-1 робіт мають унікальну тривалість, а одна інша повторюється"""

    if jobs_duration_max - jobs_duration_min + 1 < jobs_amount:
        raise ValueError(
            f"У діапазоні [{jobs_duration_min}, {jobs_duration_max}] недостатньо значень, аби згенерувати {jobs_amount} робіт."
        )

    mu = (jobs_duration_min + jobs_duration_max) / 2

    # sigma (std.dev) була обрана таким чином (max-min)/4, що ~95% значень знаходяться в межах [min, max]
    sigma = (jobs_duration_max - jobs_duration_min) / 4

    # Генеруємо N-1 тривалостей
    durations_set = set()
    durations = np.empty(0, dtype=int)

    while len(durations) < (jobs_amount - 1):
        new_durations = np.round(
            np.random.normal(mu, sigma, jobs_amount - len(durations))
        )
        for duration in new_durations:
            if (
                jobs_duration_min <= duration <= jobs_duration_max
                and duration not in durations_set
            ):
                durations = np.append(durations, int(duration))
                durations_set.add(duration)
            if len(durations) == (jobs_amount - 1):
                break

    # Додаємо дублікат
    if len(durations) > 0:
        duplicate_item_index = np.random.randint(0, len(durations))
        durations = np.append(durations, durations[duplicate_item_index])

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


def generate_job_weights(
    jobs_amount: int, weight_min: int = 1, weight_max: int = 3
) -> List[int]:
    """Повертає список ваг для N робіт"""

    return [random.randint(weight_min, weight_max) for _ in range(jobs_amount)]


def format_list_to_string(jobs_list):
    """Конвертує список кортежів до списку рядків формату '№i / ti / ui / di'"""

    formatted = []

    for job in jobs_list:
        job_string = f"№{job[0]} / {job[1]} / {job[2]} / {job[3]}"
        formatted.append(job_string)

    return formatted


def generate_problem_data(
    jobs_amount_min, jobs_amount_max, jobs_duration_min, jobs_duration_max
):
    """Функція генерує дані задачі - список робіт, представлених у вигляді кортежів (№i, ti, di, ui)"""
    jobs_amount = random.randint(jobs_amount_min, jobs_amount_max)

    jobs_indexes = list(range(1, jobs_amount + 1))
    jobs_durations = generate_job_durations(
        jobs_amount, jobs_duration_min, jobs_duration_max
    )
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
        lst = generate_problem_data(5, 7, 5, 25)
        print(format_list_to_string(lst))
