"""Цей файл містить набір функцій, які використовуються при обробці запиту на генерацію XML-файлу"""

from flask import make_response, request


def respond_with_file(xml_content: str, custom_filename: str = None):
    """Ця функція отримує на вхід XML-файл у вигляді рядка та повертає його як файл у відповідь на запит користувача"""

    filename = "generated_file.xml"
    if custom_filename:
        filename = f"{custom_filename.lower()}.xml"

    # Створюємо відповідь з відповідними заголовками, аби браузер почав завантаження файлу
    response = make_response(xml_content)
    response.headers.set("Content-Type", "application/xml")
    response.headers.set("Content-Disposition", "attachment", filename=filename)

    return response


def get_job_values():
    """Ця функція витягає з форми основний набір параметрів"""

    jobs_amount_min = int(request.form.get("jobs_amount_min"))
    jobs_amount_max = int(request.form.get("jobs_amount_max"))
    jobs_duration_min = int(request.form.get("jobs_duration_min"))
    jobs_duration_max = int(request.form.get("jobs_duration_max"))
    tests_amount = int(request.form.get("tests_amount"))
    test_name = str(request.form.get("test_name"))

    return (
        jobs_amount_min,
        jobs_amount_max,
        jobs_duration_min,
        jobs_duration_max,
        tests_amount,
        test_name,
    )
