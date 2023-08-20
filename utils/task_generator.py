# Має генеруватись певна кількість чисел (5 за замовчуванням). Числа мають бути різними.
# Та значення директивного строку.
# Додатково має бути можливість обрати тип задачі (мін/макс).
# Можливо, є сенс проаналізувати наявні завдання, перед написанням власного алгоритму генерації.

# Виходячи з наявних даних:
# a) тривалості від 1 до 30.
# b) кожна задача містить 5 унікальних чисел, що представляють тривалість.
# c) дир. строки від 11 до 77.
# d) дир. строк менший від суми тривалостей від 1.17 до 3.36 разів.


import random
from typing import List, Union
import numpy as np
from utils.solver import solve


def generate_durations(
    jobs_amount: int, jobs_duration_min: int, jobs_duration_max: int
):
    """Ця функція генерує jobs_amount випадкових чисел з заданого діапазону [jobs_duration_min; jobs_duration_max]"""

    if jobs_amount > (jobs_duration_max - jobs_duration_min + 1):
        raise ValueError(
            f"Неможливо згенерувати {jobs_amount} робіт(оти) з унікальною тривалістю з діапазону [{jobs_duration_min}; {jobs_duration_max}]"
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


def generate_ds(
    mu: Union[int, float], sigma: Union[int, float], min_val: int, max_val: int
):
    """Ця функція генерує значення директивного строку з використанням нормального розподілу"""

    ds = int(np.random.normal(mu, sigma))

    while not min_val < ds < max_val:
        ds = int(np.random.normal(mu, sigma))

    return ds


def calculate_mu_sigma(start_range: int, end_range: int):
    """Функція для генерації значень mu та sigma, де

    mu - середнє значення діапазону, навколо якого групуватимуться згенеровані числа;
    sigma - стандартне відхилення, визначає дисперсію (відхилення чисел від середнього значення).
    """

    mu = (start_range + end_range) / 2
    sigma = (end_range - start_range) / 6

    return mu, sigma


def get_parts(job_durations: List[int], ds: int, is_min_task: bool, is_delayed: bool):
    """Повертає ліву та праву частини, тобто множину робіт що не запізнюються та запізнюються"""

    job_durations = list(sorted(job_durations, reverse=is_min_task ^ is_delayed))
    accum_list = [sum(job_durations[: i + 1]) for i in range(len(job_durations))]
    split_index = list(map(lambda x: x <= ds, accum_list)).index(False)

    return job_durations[:split_index], job_durations[split_index:]


def is_min_max_a_not_a(
    non_delayed_part: List[int], delayed_part: List[int], is_min_task: bool
):
    """Перевірка умови min(pj) < max(pj), де min(pj) працює з множиною робіт, що не запізнюються, а max(pj) з множиною робіт, що запізнюються"""

    if is_min_task:
        return min(non_delayed_part) < max(delayed_part)
    else:
        return min(non_delayed_part) > max(delayed_part)


def is_valid_data(
    job_durations: List[int], ds: int, is_min_task: bool, is_delayed: bool
):
    """Перевірка відповідності задачі всім необхідним умовам"""

    non_delayed_part, delayed_part = get_parts(
        job_durations, ds, is_min_task, is_delayed
    )

    if is_delayed and is_min_task:
        return all(
            [
                min(job_durations) < ds < sum(job_durations),
                is_min_max_a_not_a(non_delayed_part, delayed_part, is_min_task),
            ]
        )

    if is_delayed and not is_min_task:
        return all(
            [
                max(job_durations) < ds < sum(job_durations),
                ds - sum(non_delayed_part) < min(delayed_part),
                is_min_max_a_not_a(non_delayed_part, delayed_part, is_min_task),
            ]
        )

    if not is_delayed and is_min_task:
        return True

    if not is_delayed and not is_min_task:
        return True

    return False


def generate_raw_data(
    jobs_amount_min: int,
    jobs_amount_max: int,
    jobs_duration_min: int,
    jobs_duration_max: int,
    is_min_task: bool,
):
    """Ця функція генерує дані для задачі - тривалості робіт та директивний строк, проте вони потребують додаткових перевірок"""

    jobs_amount = random.randint(jobs_amount_min, jobs_amount_max)
    job_durations = generate_durations(
        jobs_amount, jobs_duration_min, jobs_duration_max
    )
    ds = generate_ds(
        *calculate_mu_sigma(
            (max(job_durations), min(job_durations))[is_min_task] + 1,
            sum(job_durations) - 1,
        ),
        (max(job_durations), min(job_durations))[is_min_task],
        sum(job_durations),
    )

    return jobs_amount, job_durations, ds


def generate_problem_data(
    jobs_amount_min: int,
    jobs_amount_max: int,
    jobs_duration_min: int,
    jobs_duration_max: int,
    is_min_task: bool,
    is_delayed: bool,
):
    """Ця функція генерує дані для задачі з урахуванням всіх потрібних умов"""

    jobs_amount, job_durations, ds = generate_raw_data(
        jobs_amount_min,
        jobs_amount_max,
        jobs_duration_min,
        jobs_duration_max,
        is_min_task,
    )

    while not is_valid_data(job_durations, ds, is_min_task, is_delayed):
        jobs_amount, job_durations, ds = generate_raw_data(
            jobs_amount_min,
            jobs_amount_max,
            jobs_duration_min,
            jobs_duration_max,
            is_min_task,
        )

    return jobs_amount, job_durations, ds


if __name__ == "__main__":
    _is_min_task, _is_delayed = False, True
    print(
        f"+{'-' * 120}+\n|{'Тривалості робіт':^20}|{'Дир. строк':^12}|{'Досягає':^12}|{'Запізнюється':^14}|{'Оптимальний розклад':^22}|{'Опт.знач.крит.':^17}|{'К-ть.опт.розкл.':^17}|\n+{'-' * 120}+"
    )
    for _ in range(10):
        _jobs_amount, _job_durations, _ds = generate_problem_data(
            jobs_amount_min=5,
            jobs_amount_max=7,
            jobs_duration_min=3,
            jobs_duration_max=10,
            is_min_task=_is_min_task,
            is_delayed=_is_delayed,
        )
        res, crit_val, opt_count = solve(_job_durations, _ds, _is_min_task, _is_delayed)
        print(
            f"|{' '.join(map(str, _job_durations)):^20}|{_ds:^12}|{('Максимум', 'Мінімум')[_is_min_task]:^12}|{('Ні', 'Так')[_is_delayed]:^14}|{res:^22}|{crit_val:^17}|{opt_count:^17}|"
        )
    print(f"+{'-' * 120}+")
