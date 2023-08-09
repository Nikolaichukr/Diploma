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
from utils.solver import solve


def generate_durations(jobs_amount, jobs_duration_min, jobs_duration_max):
    """Ця функція генерує jobs_amount випадкових чисел з заданого діапазону [jobs_duration_min; jobs_duration_max]"""

    if jobs_amount > (jobs_duration_max - jobs_duration_min + 1):
        raise ValueError(
            f"Неможливо згенерувати {jobs_amount} робіт з унікальною тривалістю з діапазону [{jobs_duration_min}; {jobs_duration_max}]"
        )

    mu, sigma = calculate_mu_sigma(jobs_duration_min, jobs_duration_max)

    job_durations = []
    while len(job_durations) < jobs_amount:
        number = int(random.normalvariate(mu, sigma))
        if (
            jobs_duration_min <= number <= jobs_duration_max
            and number not in job_durations
        ):
            job_durations.append(number)

    return job_durations


def generate_ds(mu, sigma):
    """Ця функція генерує значення директивного строку з використанням нормального розподілу"""

    return int(np.random.normal(mu, sigma))


def calculate_mu_sigma(start_range, end_range):
    """Функція для генерації значень mu та sigma, де

    mu - середнє значення діапазону, навколо якого групуватимуться згенеровані числа;
    sigma - стандартне відхилення, визначає дисперсію (відхилення чисел від середнього значення).
    """

    mu = (start_range + end_range) / 2
    sigma = (end_range - start_range) / 6

    return mu, sigma


def generate_problem_data(
    jobs_amount_min, jobs_amount_max, jobs_duration_min, jobs_duration_max
):
    """Ця функція генерує дані для задачі - тривалості, директивний строк та тип задачі"""

    jobs_amount = random.randint(jobs_amount_min, jobs_amount_max)
    job_durations = generate_durations(
        jobs_amount, jobs_duration_min, jobs_duration_max
    )
    ds = generate_ds(*calculate_mu_sigma(jobs_duration_min, sum(job_durations)))
    is_min_task = random.choice([True, False])
    is_delayed = random.choice([True, False])

    return jobs_amount, job_durations, ds, is_min_task, is_delayed


if __name__ == "__main__":
    print(
        f"+{'-' * 102}+\n|{'Тривалості робіт':^20}|{'Дир. строк':^12}|{'Досягає':^12}|{'Запізнюється':^14}|{'Оптимальний розклад':^22}|{'Опт.знач.крит.':^17}|\n+{'-' * 102}+"
    )
    for _ in range(50):
        jobs_amount, job_durations, ds, is_min_task, is_delayed = generate_problem_data(
            jobs_amount_min=5, jobs_amount_max=7, jobs_duration_min=3, jobs_duration_max=10
        )
        res, crit_val = solve(job_durations, ds, is_min_task, is_delayed)
        print(
            f"|{' '.join(map(str, job_durations)):^20}|{ds:^12}|{('Максимум', 'Мінімум')[is_min_task]:^12}|{('Ні', 'Так')[is_delayed]:^14}|{res:^22}|{crit_val:^17}|"
        )
    print(f"+{'-' * 102}+")
