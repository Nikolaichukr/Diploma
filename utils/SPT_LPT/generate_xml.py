"""Цей файл генерує XML-код, що описує набір задач"""

import xml.etree.ElementTree as ET
from random import shuffle, uniform

from utils.SPT_LPT.helper import get_description
from utils.SPT_LPT.solver import get_seeking_criteria, solve_SPT_LPT
from utils.SPT_LPT.task_generator import (format_job_tuple_to_string,
                                          generate_problem_data)
from utils.xml_utils import add_dragbox, add_tag, prettify


def create_question_element(
    test_name,
    i,
    jobs_amount_min,
    jobs_amount_max,
    jobs_duration_min,
    jobs_duration_max,
    task_type,
    rule,
    weighted,
):
    """Генерує одне тестове питання в xml-форматі, на основі вхідних даних"""

    # Початок генерації XML-файлу
    question = ET.Element("question", type="ddwtos")

    name = ET.SubElement(question, "name")
    add_tag(name, "text", f"{test_name}_{i:03}")

    questiontext = ET.SubElement(question, "questiontext", format="html")
    questiontext_text = ET.SubElement(questiontext, "text")

    # Генерація даних для наповнення тесту
    schedule_items = generate_problem_data(
        jobs_amount_min, jobs_amount_max, jobs_duration_min, jobs_duration_max
    )

    formatted_blocks = [format_job_tuple_to_string(item) for item in schedule_items]
    additional_blocks = ["(", ")", "-"]
    option_blocks = formatted_blocks + additional_blocks

    sorted_solved_jobs, alt_opts = solve_SPT_LPT(
        schedule_items, rule=rule, weighted=weighted
    )
    seeking_criteria = get_seeking_criteria(task_type, weighted, sorted_solved_jobs)

    sorted_solved_jobs += ["-"] * (10 - len(sorted_solved_jobs))
    alternate_optimums = list(range(1, 37))

    # Генерація варіантів для значення критерію
    crit_values = [int(seeking_criteria * uniform(0.5, 1.5)) for _ in range(20)]

    if seeking_criteria not in crit_values:
        crit_values.append(seeking_criteria)

    shuffle(crit_values)  # Перемішуємо згенеровані варіанти

    # Продовження генерації XML-файлу
    questiontext_text.text = f"""
        <![CDATA[
        <p dir="ltr"">Для системи з \( n={len(schedule_items)}, m=1 \) скласти <strong>{get_description(rule, task_type, weighted)}</strong></p>
        <p></p>
        Результуючий розклад: {' '.join([f"[[{option_blocks.index(format_job_tuple_to_string(item)) + 1}]]" for item in sorted_solved_jobs])}
        <br>
        <p></p>
        Кількість альтернативних оптимумів: [[{len(option_blocks) + 1 + alternate_optimums.index(alt_opts)}]]
        <br>
        Значення критерію: [[{1 + len(option_blocks) + len(alternate_optimums) + crit_values.index(seeking_criteria)}]]
        <br>
        <em>Перетягнути наступні елементи на відповідні їм місця.</em>
        <br>
        Позначення \( №i / t _i / d _i/ u _i\<br>\), де \( i \) - номер роботи, \( t_i \) - її тривалість,
        \( d_i \) - її директивний строк, \( u_i \) - її вага.
        <br>
        <em>У випадку альтернативних оптимумів використовувати дужки "(" та ")". В дужках номери робіт упорядковувати за зростанням.</em><br>
        <em>Зайві поля заповнити блоком з символом "-".</em><br>]]>
    """

    # Adding the 'generalfeedback' element
    generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
    add_tag(generalfeedback, "text", "")
    add_tag(question, "defaultgrade", "3")
    add_tag(question, "penalty", "0.3333333")
    add_tag(question, "hidden", "0")
    add_tag(question, "idnumber", "")
    add_tag(question, "shuffleanswers", "0")
    add_tag(question, "shownumcorrect", "")

    for symbol in option_blocks:
        add_dragbox(parent_tag=question, symbol=symbol, group=1)

    for option in alternate_optimums:
        add_dragbox(parent_tag=question, symbol=option, group=2)

    for option in crit_values:
        add_dragbox(parent_tag=question, symbol=option, group=3)

    return question


def generate_quiz_xml(
    jobs_amount_min,
    jobs_amount_max,
    jobs_duration_min,
    jobs_duration_max,
    tests_amount,
    test_name,
    task_type,
    rule,
    weighted,
):
    """Генерує xml з тестовими питаннями"""

    quiz = ET.Element("quiz")

    for i in range(1, tests_amount + 1):
        question = create_question_element(
            test_name,
            i,
            jobs_amount_min,
            jobs_amount_max,
            jobs_duration_min,
            jobs_duration_max,
            task_type,
            rule,
            weighted,
        )
        quiz.append(question)

    return prettify(quiz)


if __name__ == "__main__":
    xml_output = generate_quiz_xml(5, 7, 5, 25, 1, "SPT_F", "F", "SPT", True)
    print(xml_output)
