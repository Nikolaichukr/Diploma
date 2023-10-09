import xml.etree.ElementTree as ET
from utils.general_purpose import add_tag, add_dragbox, prettify
from utils.SPT.task_generator import generate_problem_data


def create_question_element(test_name, i, jobs_amount):
    """Генерує одне тестове питання в xml-форматі, на основі вхідних даних"""

    question = ET.Element("question", type="ddwtos")

    name = ET.SubElement(question, "name")
    add_tag(name, "text", f"{test_name}_{i:03}")

    questiontext = ET.SubElement(question, "questiontext", format="html")
    questiontext_text = ET.SubElement(questiontext, "text")

    schedule_items = generate_problem_data()

    questiontext_text.text = f"""
        <![CDATA[
        <p dir="ltr"">Для системи з \( n={jobs_amount}, m=1 \) скласти розклад <strong>мінімальною сумарною тривалістю проходження</strong></p>
        <p></p>
        Результуючий розклад: [[1]] [[4]] [[5]] [[2]] [[3]] [[7]] [[6]] 
        <br>
        <p></p>
        Кількість альтернативних оптимумів: [[8]]
        <br>
        <em>Перетягнути наступні елементи на відповідні їм місця.</em>
        <br>
        Позначення \( №i / t _i / d _i/ u _i\<br>\), де \( i \) - номер роботи, \( t_i \) - її тривалість,
        \( d_i \) - її директивний строк, \( u_i \) - її вага.
        <br>
        <em>У випадку альтернативних оптимумів використовувати дужки "(" та ")". В дужках номери робіт упорядковувати за зростанням.</em><br>]]>
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

    for symbol in schedule_items:
        add_dragbox(parent_tag=question, symbol=symbol, group=1)

    for option in ["(", ")", "-"]:
        add_dragbox(parent_tag=question, symbol=option, group=1)

    for option in [8, 10, 19, 18, 21, 2]:
        add_dragbox(parent_tag=question, symbol=option, group=2)

    return question


def generate_quiz_xml(tests_amount, test_name, jobs_amount):
    """Генерує xml з тестовими питаннями"""

    quiz = ET.Element("quiz")

    for i in range(1, tests_amount + 1):
        question = create_question_element(test_name, i, jobs_amount)
        quiz.append(question)

    return prettify(quiz)


if __name__ == "__main__":
    xml_output = generate_quiz_xml(tests_amount=1, test_name="SPT_F", jobs_amount=5)
    print(xml_output)
