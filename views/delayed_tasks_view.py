"""
Цей файл відповідає за views (відображення) для задач,
які враховують кількість робіт, що запізнюються (не запізнюються)
"""

from flask import Blueprint, render_template, request, abort

from utils.delayed_tasks.generate_xml import generate_quiz_xml
from utils.common.request_utils import get_job_values, respond_with_file

delayed_tasks = Blueprint("delayed_tasks", __name__)


@delayed_tasks.route("/handle_post", methods=["POST"])
def handle_delayed_post_request():
    """Обробляє POST-запит на генерацію XML-файлу для задач на запізнення"""
    (jobs_amount_min, jobs_amount_max, jobs_duration_min, jobs_duration_max, tests_amount, test_name) = get_job_values()
    is_min_task = bool(int(request.form.get("is_min_task")))
    is_delayed = bool(int(request.form.get("is_delayed")))

    xml_content = generate_quiz_xml(
        jobs_amount_min,
        jobs_amount_max,
        jobs_duration_min,
        jobs_duration_max,
        tests_amount,
        test_name,
        is_min_task,
        is_delayed,
    )

    return respond_with_file(xml_content=xml_content, custom_filename=test_name)


@delayed_tasks.route("/<string:min_max>_<string:delayed>", methods=["GET"])
def delayed_task_page(min_max, delayed):
    """Динамічно обробляє маршрути для задач на запізнення"""

    if min_max not in ["min", "max"] or delayed not in ["delayed", "nondelayed"]:
        return abort(404)

    is_min = min_max == "min"
    is_delayed = delayed == "delayed"
    title = f"{min_max.capitalize()} {'Delayed' if is_delayed else 'Non-Delayed'}"

    return render_template("delayed_task.html", title=title, is_min=is_min, is_delayed=is_delayed)


@delayed_tasks.route("/complicated_task", methods=["GET"])
def complicated_task():
    return "To be implemented"
