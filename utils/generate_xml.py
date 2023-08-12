import xml.etree.ElementTree as ET
from html import unescape
from lxml import etree
from utils.solver import solve
from utils.task_generator import generate_problem_data
from math import factorial


def tab():
    """Повертає комбінацію перенесення каретки та табуляції, потрібна виключно для візуального відображення"""

    return "\n\t\t\t"


def add_tag(parent_element, tag, value):
    """Створює теги зі значенням, використовується для уникнення дублювання"""

    new_tag = ET.SubElement(parent_element, tag)
    new_tag.text = value


def add_dragbox(parent_tag, symbol, group):
    """Додає dragbox блоки (перетягування) до тесту"""

    dragbox = ET.SubElement(parent_tag, "dragbox")
    dragbox_text = ET.SubElement(dragbox, "text")
    dragbox_text.text = str(symbol)
    dragbox_group = ET.SubElement(dragbox, "group")
    dragbox_group.text = str(group)
    ET.SubElement(dragbox, "infinite")


def create_question_element(
    test_name,
    jobs_amount_min,
    jobs_amount_max,
    jobs_duration_min,
    jobs_duration_max,
    is_min_task,
    is_delayed,
    i,
):
    """Генерує одне тестове питання в xml-форматі, на основі вхідних даних"""

    jobs_amount, job_durations, ds = generate_problem_data(
        jobs_amount_min,
        jobs_amount_max,
        jobs_duration_min,
        jobs_duration_max,
        is_min_task,
        is_delayed,
    )
    res, crit_val, opt_count = solve(job_durations, ds, is_min_task, is_delayed)
    opt_solution_options = "(" + "".join([str(i + 1) for i in range(jobs_amount)]) + ")"
    opt_crit_val_options = "".join(map(str, range(jobs_amount + 1)))
    alter_amount_options = list(
        sorted(
            set(
                [
                    factorial(i - j) * factorial(j)
                    for i in range(jobs_amount + 1)
                    for j in range(i // 2 + 1)
                ]
            )
        )
    )
    question = ET.Element("question", type="ddwtos")

    name = ET.SubElement(question, "name")
    add_tag(name, "text", f"{test_name}_{i:03}")

    questiontext = ET.SubElement(question, "questiontext", format="html")
    questiontext_text = ET.SubElement(questiontext, "text")

    questiontext_text.text = f"""
        <![CDATA[
        <p dir="ltr"">Для системи з <i>n</i> = {jobs_amount}, <i>m</i> = 1 скласти розклад у якого досягає <b>{['максимуму', 'мінімуму'][is_min_task]} кількість робіт, що {['НЕ ', ''][is_delayed]}запізнюються</b>.</p>

        <table width="280" cellspacing="0" cellpadding="0" border="2">
            <colgroup>
                <col width="36" span="5">
            </colgroup>
            <tbody>

        <tr height="25">
            <td style="text-align: center;" width="36" height="25"><i><span><b>робота</b></span></i></td>
            {tab().join([f"<td style='text-align: center;' width='36'><span><b>{num}</b></span></td>" for num in range(1, jobs_amount + 1)])}
        </tr>
        
        <tr height="25">
            <td style="text-align: center;" width="36" height="25"><i><span><b>тривалість</b></span></i></td>
            {tab().join([f"<td style='text-align: center;' width='36'><span><b>{d}</b></span></td>" for d in job_durations])}
        </tr>

        <tr height="25">
            <td style="text-align: center;" width="36" height="25"><i><span><b>дир. строк</b></span></i></td>
            {tab().join([f"<td style='text-align: center;' width='36'><span><b>{ds}</b></span></td>" for _ in range(jobs_amount)])}
        </tr>

            </tbody>
        </table>
        <br>
        <p dir="ltr" style="text-align: left;">Оптимальний розклад: {' '.join([f'[[{opt_solution_options.index(i) + 1}]]' for i in res.replace(' ', '')])}</p>
        <p dir="ltr" style="text-align: left;">Опт. значення критерія: [[{len(opt_solution_options) + opt_crit_val_options.index(str(crit_val)) + 1}]]</p>
        <p dir="ltr" style="text-align: left;">Кількість оптимальних розкладів: [[{len(opt_solution_options) + len(opt_crit_val_options) + alter_amount_options.index(opt_count) + 1}]]</p>
        ]]>
    """

    # Adding the 'generalfeedback' element
    generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
    add_tag(generalfeedback, "text", "")
    add_tag(question, "penalty", "0.3333333")
    add_tag(question, "hidden", "0")
    add_tag(question, "idnumber", "")
    add_tag(question, "shuffleanswers", "0")

    for option in opt_solution_options:
        add_dragbox(parent_tag=question, symbol=option, group=1)

    for symbol in opt_crit_val_options:
        add_dragbox(parent_tag=question, symbol=symbol, group=2)

    for option in alter_amount_options:
        add_dragbox(parent_tag=question, symbol=option, group=3)

    return question


def generate_quiz_xml(
    jobs_amount_min,
    jobs_amount_max,
    jobs_duration_min,
    jobs_duration_max,
    tests_amount,
    test_name,
    is_min_task,
    is_delayed,
):
    """Генерує xml з тестовими питаннями"""

    quiz = ET.Element("quiz")

    for i in range(1, tests_amount + 1):
        question = create_question_element(
            test_name,
            jobs_amount_min,
            jobs_amount_max,
            jobs_duration_min,
            jobs_duration_max,
            is_min_task,
            is_delayed,
            i,
        )
        quiz.append(question)

    xml_string = ET.tostring(quiz, encoding="UTF-8").decode("utf-8")

    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.fromstring(xml_string, parser)
    return unescape(
        etree.tostring(
            tree, encoding="utf-8", pretty_print=True, xml_declaration=True
        ).decode("utf-8")
    )


if __name__ == "__main__":
    xml_output = generate_quiz_xml(
        jobs_amount_min=5,
        jobs_amount_max=7,
        jobs_duration_min=3,
        jobs_duration_max=10,
        tests_amount=1,
        test_name="GeneratedQuestion",
        is_min_task=True,
        is_delayed=True,
    )
    print(xml_output)
