import xml.etree.ElementTree as ET
from html import unescape
from lxml import etree

from utils.solver import solve
from utils.task_generator import generate_problem_data


def tab():
    return "\n\t\t\t"


def add_tag(parent_element, tag, value):
    new_tag = ET.SubElement(parent_element, tag)
    new_tag.text = value


def add_dragbox(parent_tag, symbol, group):
    dragbox = ET.SubElement(parent_tag, "dragbox")
    dragbox_text = ET.SubElement(dragbox, "text")
    dragbox_text.text = symbol
    dragbox_group = ET.SubElement(dragbox, "group")
    dragbox_group.text = group
    ET.SubElement(dragbox, "infinite")


def create_question_element(
    test_name, jobs_amount_min, jobs_amount_max, jobs_duration_min, jobs_duration_max, i
):
    question = ET.Element("question", type="ddwtos")

    name = ET.SubElement(question, "name")
    add_tag(name, "text", f"{test_name}_{i:03}")

    questiontext = ET.SubElement(question, "questiontext", format="html")
    questiontext_text = ET.SubElement(questiontext, "text")

    jobs_amount, job_durations, ds, is_min_task, is_delayed = generate_problem_data(
        jobs_amount_min, jobs_amount_max, jobs_duration_min, jobs_duration_max
    )
    res, crit_val = solve(job_durations, ds, is_min_task, is_delayed)
    options = "(" + "".join([str(i + 1) for i in range(jobs_amount)]) + ")"
    group_b = "".join(map(str, range(jobs_amount + 1)))

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
        <p dir="ltr" style="text-align: left;">Оптимальний розклад: {' '.join([f'[[{options.index(i) + 1}]]' for i in res.replace(' ', '')])}</p>
        <p dir="ltr" style="text-align: left;">Опт. значення критерія: [[{len(options) + group_b.index(str(crit_val)) + 1}]]</p>
        ]]>
    """

    # Adding the 'generalfeedback' element
    generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
    add_tag(generalfeedback, "text", "")
    add_tag(question, "penalty", "0.3333333")
    add_tag(question, "hidden", "0")
    add_tag(question, "idnumber", "")
    add_tag(question, "shuffleanswers", "0")

    for option in options:
        add_dragbox(parent_tag=question, symbol=option, group="1")

    for symbol in group_b:
        add_dragbox(parent_tag=question, symbol=symbol, group="2")

    return question


def generate_quiz_xml(
    jobs_amount_min,
    jobs_amount_max,
    jobs_duration_min,
    jobs_duration_max,
    tests_amount,
    test_name,
):
    quiz = ET.Element("quiz")

    for i in range(1, tests_amount + 1):
        question = create_question_element(
            test_name,
            jobs_amount_min,
            jobs_amount_max,
            jobs_duration_min,
            jobs_duration_max,
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
    )
    print(xml_output)
