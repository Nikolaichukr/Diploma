import xml.etree.ElementTree as ET
from html import unescape
from lxml import etree

from utils.solver import solve
from utils.task_generator import generate_problem_data


def tab():
    return "\n\t\t\t"


def create_question_element(i, start_range, end_range, n):
    question = ET.Element('question', type='cloze')

    # Adding the 'name' element
    name = ET.SubElement(question, 'name')
    name_text = ET.SubElement(name, 'text')
    name_text.text = f'Згенероване_Питання_{i}'

    # Adding the 'questiontext' element
    questiontext = ET.SubElement(question, 'questiontext', format='html')
    questiontext_text = ET.SubElement(questiontext, 'text')

    durations, ds, is_min_task, is_delayed = generate_problem_data(n=n, start_range=start_range, end_range=end_range)
    res, crit_val = solve(durations, ds, is_min_task, is_delayed)

    questiontext_text.text = f"""
        <![CDATA[
        <p><span lang="uk"> 
        Для
        системи з&nbsp;</span><span lang="EN-US"><i>n</i> = {n}, <i>m</i> = 1</span><span lang="RU">&nbsp;скласти розклад у якого досягає <b>{['максимуму', 'мінімуму'][is_min_task]} кількість робіт, що {['НЕ ', ''][is_delayed]}запізнюються</b>.</span></p>
        <p><span lang="EN-US"></span></p>
        <table width="280" cellspacing="0" cellpadding="0" border="2">
            <colgroup>
                <col width="36" span="5">
            </colgroup>
            <tbody>

        <tr height="25">
            <td style="text-align: center;" width="36" height="25"><i><span><b>робота</b></span></i></td>
            {tab().join([f"<td style='text-align: center;' width='36'><span><b>{num}</b></span></td>" for num in range(1, n + 1)])}
        </tr>
        
        <tr height="25">
            <td style="text-align: center;" width="36" height="25"><i><span><b>тривалість</b></span></i></td>
            {tab().join([f"<td style='text-align: center;' width='36'><span><b>{d}</b></span></td>" for d in durations])}
        </tr>

        <tr height="25">
            <td style="text-align: center;" width="36" height="25"><i><span><b>дир. строк</b></span></i></td>
            {tab().join([f"<td style='text-align: center;' width='36'><span><b>{ds}</b></span></td>" for d in range(n)])}
        </tr>

            </tbody>
        </table>
        <span>
        <br>
        <i style="">У разі наявності альтернативних розкладів використовувати круглі дужки, в середині кожної групи номери робіт вказувати через пробіл за зрозтанням. Наприклад: (3 5) (1 2 4)</i>
        <span><br><b>Оптимальний р</b></span><b>озклад&nbsp;</b>(<span lang="uk">номери робіт через пробіл)</span>: {{1:SA:= {res} ~%100%{res}}}<br><br><b>Опт. значення критерія</b>:&nbsp;{{1:SA:= {crit_val}}}&nbsp;</span><br><br><br><br>
        <p></p>]]>
    """

    # Adding the 'generalfeedback' element
    generalfeedback = ET.SubElement(question, 'generalfeedback', format='html')
    generalfeedback_text = ET.SubElement(generalfeedback, 'text')
    generalfeedback_text.text = ''

    # Adding the 'penalty' element
    penalty = ET.SubElement(question, 'penalty')
    penalty.text = '0.3333333'

    # Adding the 'hidden' element
    hidden = ET.SubElement(question, 'hidden')
    hidden.text = '0'

    # Adding the 'idnumber' element
    idnumber = ET.SubElement(question, 'idnumber')
    idnumber.text = ''

    return question


def generate_quiz_xml(amount, start_range, end_range):
    quiz = ET.Element('quiz')

    for i in range(amount):
        question = create_question_element(i + 1, start_range, end_range, n=5)
        quiz.append(question)

    xml_string = ET.tostring(quiz, encoding='UTF-8').decode('utf-8')

    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.fromstring(xml_string, parser)
    return unescape(etree.tostring(tree, encoding='utf-8', pretty_print=True, xml_declaration=True).decode('utf-8'))


if __name__ == "__main__":
    xml_output = generate_quiz_xml(1, 1, 15)
    print(xml_output)
