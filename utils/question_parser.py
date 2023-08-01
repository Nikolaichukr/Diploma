import xml.etree.ElementTree as ET
import html
from bs4 import BeautifulSoup
from solver import solve, normalize_schedule_string


def extract_quiz_tags(xml_file):
    """Функція для витягнення всіх частин, що зберігають тестову інформацію з XML-файлу"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        quiz_tags = root.findall('question')

        return quiz_tags
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return []


def extract_data_from_quiz(quiz):
    """Фунція для витягнення всієї потрібної інформації з тіла тесту в xml та html форматах"""

    quiz_text = quiz.find('questiontext/text')
    if quiz_text is not None:
        text = html.unescape(ET.tostring(quiz_text).decode("utf-8"))
        soup = BeautifulSoup(text, 'html.parser')
        tds = soup.find_all("td")
        raw_data_list = list(map(lambda td: td.text, tds))
        ds = int(raw_data_list[-1].strip())
        job_durations = list(map(int, raw_data_list[-11:-6]))
        opt_schedule = text[text.index(":=") + 2:text.rindex("~%")].strip()
        opt_crit_value = int(text[text.rindex(":=") + 2:text.rindex("}")].strip())
        is_min_task = "мінімуму" in text
        return job_durations, ds, opt_schedule, opt_crit_value, is_min_task
    else:
        print("No <text> found.")


def display_problem_info(job_durations, ds, opt_schedule, opt_crit_value, solver_opt_schedule, solver_opt_crit_value,
                         is_min_task):
    """Функція для виведення всієї інформації про проблемний тест. Використовується у процесі перевірки."""

    print("\n" + "=" * 50)
    print(
        f"Умова: Скласти розклад у якого досягає {('максимуму', 'мінімуму')[is_min_task]} кількість робіт, що НЕ запізнюються.\n")
    print(f"Номери робіт:     {[i + 1 for i in range(len(job_durations))]}")
    print(f"Тривалості робіт: {job_durations}")
    print(f"Директивний строк: {ds}")

    print("\nPезультати з Moodle:\n")
    print(f"Оптимальний розклад: {opt_schedule}")
    print(f"Опт. значення критерія: {opt_crit_value}")

    print(f"\nРезультати роботи коду:\n")
    print(f"Оптимальний розклад: {solver_opt_schedule}")
    print(f"Опт. значення критерія: {solver_opt_crit_value}")

    print("=" * 50)


if __name__ == "__main__":
    xml_file_path = "60_питань.xml"
    quiz_tags = extract_quiz_tags(xml_file_path)
    if quiz_tags:
        quiz_amount, ok_quizes = len(quiz_tags), 0
        for quiz in quiz_tags:
            job_durations, ds, opt_schedule, opt_crit_value, is_min_task = extract_data_from_quiz(quiz)
            solver_opt_schedule, solver_opt_crit_value = solve(job_durations, ds, is_min_task, is_delayed=False)
            if solver_opt_crit_value == opt_crit_value and normalize_schedule_string(
                    solver_opt_schedule) == normalize_schedule_string(opt_schedule):
                ok_quizes += 1
            else:
                display_problem_info(job_durations, ds, opt_schedule, opt_crit_value, solver_opt_schedule,
                                     solver_opt_crit_value, is_min_task)
        print(f"\nЗагальний результат: {ok_quizes}/{quiz_amount}\n")
    else:
        print("No <quiz> tags found in the XML file.")
