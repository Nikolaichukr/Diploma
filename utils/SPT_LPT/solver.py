"""Цей файл містить увесь потрібний код для розв'язання завдання"""

from collections import Counter
from math import factorial, prod

from utils.SPT_LPT.task_generator import (
    format_job_tuple_to_string,
    generate_problem_data,
)


def check_next_job(problem_list, i, weighted):
    """
    Допоміжна функція для пошуку альтернативних оптимумів

    Якщо шукаємо альтернативні оптимуму для зваженої задачі - порівнюємо чи однакові значення відношень ti/ui
    у поточної та наступної роботи, інакше - порівнюємо лише тривалості (ti)
    """

    if weighted:
        return round(problem_list[i][1] / problem_list[i][3], 9) == round(
            problem_list[i + 1][1] / problem_list[i + 1][3], 9
        )
    return problem_list[i][1] == problem_list[i + 1][1]


def get_value_list(problem_list, weighted):
    """
    Допоміжна функція, основна ціль якої витягнути значення для пошуку кількості альтернативних оптимумів

    Якщо задача зважена - повертаємо список відношень ti/ui, якщо ні - список тривалостей ti
    """

    if weighted:
        return [round(item[1] / item[3], 9) for item in problem_list]
    return [item[1] for item in problem_list]


def identify_alternative_optimums(problem_list, weighted):
    """
    Функція, для додавання дужок, що свідчать про наявність альтернативних оптимумів

    Повертає розклад (з дужками) та кількість альтернативних оптимумів
    """

    # Додаємо дужки
    result_list = []  # Ініціалізація фінального списку робіт з дужками
    i = 0  # Вказівник для перевірки списку робіт

    while i < len(problem_list):  # Ітеруємось списком робіт
        # Створюємо тимчасову групу робіт, починаючи з поточної
        temp = [problem_list[i]]
        while i + 1 < len(  # Дивимось на наступну роботу, якщо в неї така ж тривалість (або відношення тривалості та ваги) - додаємо до групи
            problem_list
        ) and check_next_job(
            problem_list, i, weighted
        ):
            temp.append(problem_list[i + 1])
            i += 1
        # Якщо в тимчасовій групі більше одного елемента - додаємо ці елементи до результату з дужками
        if len(temp) > 1:
            result_list.extend(["(", *temp, ")"])
        else:  # Інакше, додаємо лише саму роботу, без дужок
            result_list.append(temp[0])
        i += 1

    # Обраховуємо кількість альтернативних оптимумів

    # Витягаємо значення тривалостей (або відношень ti/ui)
    values = get_value_list(problem_list, weighted)

    # Рахуємо скільки разів зустрічаються тривалості (або відношення ti/ui)
    counts = Counter(values)
    multi_occurrences = [num for dur, num in counts.items() if num > 1]

    alt_opt_count = prod([factorial(num) for num in multi_occurrences])

    return result_list, alt_opt_count


def clean(lst):
    """Функція видаляє дужки, що відповідають за альтернативні оптимуми зі списку"""

    return [item for item in lst if isinstance(item, tuple)]


def get_Wi(lst):
    """
    Приймає на вхід уже відсортований список кортежів
    та обраховує для них список тривалостей очікування (Wi)
    """

    clean_lst = clean(lst)

    return [
        sum([int(item[1]) for item in clean_lst[:i]]) for i in range(len(clean_lst))
    ]


def get_TiFi(lst):
    """
    Приймає на вхід уже відсортований список кортежів
    і обраховує для них список моментів закінчення (Ti)
    та список тривалостей проходження (Fi),
    при чому вважається що усі роботи надходять одночасно.
    """

    clean_lst = clean(lst)

    return [
        sum([int(item[1]) for item in clean_lst[: i + 1]])
        for i in range(len(clean_lst))
    ]


def get_Li(lst):
    """
    Приймає на вхід уже відсортований список кортежів
    та обраховує для них список часових зміщень (Li)
    """

    clean_lst = clean(lst)
    Ti = get_TiFi(clean_lst)

    return list(map(lambda x: x[0] - x[1], zip(Ti, [item[2] for item in clean_lst])))


def get_sort_key(weighted):
    """
    Допоміжна функція для визначення способу сортування робіт

    Якщо задача зважена - сортуємо за відношенням ti/ui, інакше - просто за ti
    """

    if weighted:
        return lambda x: round(x[1] / x[3], 9)
    return lambda x: x[1]


def solve_SPT_LPT(problem_list, rule, weighted):
    """
    Сортує роботи за неспаданням тривалостей (SPT), а якщо тривалості однакові,
    то за зростанням порядкового номера роботи
    """

    reversed_flag = True if rule == "LPT" else False
    sort_key = get_sort_key(weighted)

    sorted_problem_list = sorted(problem_list, key=sort_key, reverse=reversed_flag)

    return identify_alternative_optimums(sorted_problem_list, weighted)


def get_seeking_criteria(task_type, weighted, sorted_solved_jobs):
    if task_type == "F":
        return sum(get_TiFi(sorted_solved_jobs))
    elif task_type == "L":
        return sum(get_Li(sorted_solved_jobs))
    elif task_type == "T":
        return sum(get_TiFi(sorted_solved_jobs))
    elif task_type == "W":
        return sum(get_Wi(sorted_solved_jobs))


if __name__ == "__main__":
    gen_lst = generate_problem_data(5, 7, 5, 25)

    print("Generated data:")
    for k in gen_lst:
        print(format_job_tuple_to_string(k))

    print("\nSolved data:")
    solved, alt_opts = solve_SPT_LPT(gen_lst, rule="SPT", weighted=True)
    for k in solved:
        print(format_job_tuple_to_string(k))

    print(alt_opts)
