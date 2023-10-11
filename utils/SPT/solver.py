from utils.SPT.task_generator import generate_problem_data, format_job_tuple_to_string
from collections import Counter
from math import factorial


def identify_alternative_optimums(problem_list):
    """
    Функція, для додавання дужок, що свідчать про наявність альтернативних оптимумів

    Повертає розклад та кількість альтернативних оптимумів
    """

    durations = [item[1] for item in problem_list]  # Витягаємо тривалості

    # Витягаємо неунікальне значення, та кількість разів, які воно зустрічається
    value, times = Counter(durations).most_common()[0]

    start, end = None, None
    for i in range(len(problem_list)):
        if problem_list[i][1] == value:
            if start is None:
                start = i
            end = i

    if start is not None:
        problem_list.insert(start, "(")
        problem_list.insert(end + times, ")")

    return problem_list, factorial(times)


def solve_SPT(problem_list):
    """
    Сортує роботи за неспаданням тривалостей (SPT), а якщо тривалості однакові,
    то за зростанням порядкового номера роботи
    """
    sorted_problem_list = sorted(problem_list, key=lambda x: (x[1], x[0]))

    return identify_alternative_optimums(sorted_problem_list)


if __name__ == "__main__":
    lst = generate_problem_data(5, 7, 5, 25)

    print("Generated data:")
    for k in lst:
        print(format_job_tuple_to_string(k))

    print("\nSolved data:")
    solved, alt_opts = solve_SPT(lst)
    for k in solved:
        print(format_job_tuple_to_string(k))
