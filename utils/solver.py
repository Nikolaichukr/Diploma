# Максимум  (MIN = False)   +   НЕ ЗАПІЗНЮЄТЬСЯ (DELAYED = False)  ->  Спочатку йдуть коротші (сортування за зростанням)  (reverse = False)
# Мінімуму  (MIN = True)    +   НЕ ЗАПІЗНЮЄТЬСЯ (DELAYED = False)  ->  Спочатку йдуть довші   (сортування за спаданням)   (reverse = True)
# Максимуму (MIN = False)   +   ЗАПІЗНЮЄТЬСЯ    (DELAYED = True)   ->  Спочатку йдуть довші   (сортування за спаданням)   (reverse = True)
# Мінімуму  (MIN = True)    +   ЗАПІЗНЮЄТЬСЯ    (DELAYED = True)   ->  Спочатку йдуть коротші (сортування за зростанням)  (reverse = False)
from typing import List
from math import factorial

MIN = False  # Досягає максимуму - False, мінімуму - True
DELAYED = False  # Запізнюється - True, НЕ запізнюється - FALSE

# Згенеровані значення мають бути різними!!!
# durations = [11, 8, 4, 4, 4]
# ds = 8
# В подібному випадку можуть виникнути непорозуміння.

_durations = [11, 8, 7, 4, 14]
_ds = 21

# Оптимальний розклад: (2 3 4)(1 5)
# Опт. значення критерія: 3


def normalize_schedule_string(opt_schedule: str):
    """
    Видалення пробілів між дужками порівняння результатів з мудла з результатами роботи скрипта
    Приклад: (2 5) (1 3 4) --> (2 5)(1 3 4)
    """

    return opt_schedule.replace(") ", ")").replace(" (", "(")


def format_output(lst: List[tuple]):
    """Функція для форматування результату"""

    return " ".join(sorted(map(lambda x: str(x[0]), lst)))


def solve(durations: List[int], ds: int, is_min_task: bool, is_delayed: bool):
    """Алгоритм розв'язання задачі, на основі вхідних даних (тривалостей робіт, директивного строку та типу задачі - макс/мін)"""

    # нумерація робіт та сортування в залежності від типу задачі (макс/мін)
    slist = list(
        sorted(
            [(i, x) for i, x in enumerate(durations, start=1)],
            key=lambda x: (x[1], x[0]),
            reverse=is_min_task ^ is_delayed,
        )
    )
    # Визначення опт. значення критерія
    current_sum, num_elements = 0, 0
    for num in list(map(lambda x: x[1], slist)):
        if current_sum + num <= ds:
            current_sum += num
            num_elements += 1
        else:
            break

    # Формування результату, в залежності від опт. знач. критерія
    if num_elements == 0 or num_elements == len(slist):
        res = f"({format_output(slist)})"
    elif num_elements == 1:
        res = f"{slist[0][0]} ({format_output(slist[num_elements:])})"
    elif num_elements == len(slist) - 1:
        res = f"({format_output(slist[:num_elements])}) {slist[-1][0]}"
    else:
        res = f"({format_output(slist[:num_elements])}) ({format_output(slist[num_elements:])})"

    opt_count = factorial(num_elements) * factorial(len(durations) - num_elements)

    return res, (num_elements, len(durations) - num_elements)[is_delayed], opt_count


if __name__ == "__main__":
    _opt_schedule, _opt_crit_val, _opt_count = solve(_durations, _ds, MIN, DELAYED)
    print("Оптимальний розклад:", _opt_schedule)
    print("Опт. знач. критерія:", _opt_crit_val)
    print("Кількість оптимальних розкладів:", _opt_count)
