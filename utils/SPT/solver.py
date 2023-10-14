"""Цей файл містить увесь потрібний код для розв'язання завдання"""

from utils.SPT.task_generator import generate_problem_data, format_job_tuple_to_string
from collections import Counter
from math import factorial, prod


def identify_alternative_optimums(problem_list):
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
        while (  # Дивимось на наступну роботу, якщо в неї така ж тривалість - додаємо до групи
            i + 1 < len(problem_list) and problem_list[i][1] == problem_list[i + 1][1]
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

    # Витягаємо значення тривалостей
    durations = [item[1] for item in problem_list]
    counts = Counter(durations)  # Рахуємо скільки разів зустрічаються тривалості
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


def solve_SPT(problem_list):
    """
    Сортує роботи за неспаданням тривалостей (SPT), а якщо тривалості однакові,
    то за зростанням порядкового номера роботи
    """
    sorted_problem_list = sorted(problem_list, key=lambda x: (x[1], x[0]))

    return identify_alternative_optimums(sorted_problem_list)


if __name__ == "__main__":
    gen_lst = generate_problem_data(5, 7, 5, 25)

    print("Generated data:")
    for k in gen_lst:
        print(format_job_tuple_to_string(k))

    print("\nSolved data:")
    solved, alt_opts = solve_SPT(gen_lst)
    for k in solved:
        print(format_job_tuple_to_string(k))

    print(alt_opts)
