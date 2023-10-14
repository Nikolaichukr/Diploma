"""
Цей файл відповідає за views (відображення) для задач,
які враховують кількість робіт, що запізнюються (не запізнюються)
"""

from flask import Blueprint, render_template, request
from utils.delayed_tasks.generate_xml import generate_quiz_xml
from utils.request_utils import respond_with_file, get_job_values

delayed_tasks = Blueprint("delayed_tasks", __name__)


@delayed_tasks.route("/handle_post", methods=["POST"])
def handle_post_request():
    (
        jobs_amount_min,
        jobs_amount_max,
        jobs_duration_min,
        jobs_duration_max,
        tests_amount,
        test_name,
    ) = get_job_values()
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


@delayed_tasks.route("/min_delayed", methods=["GET"])
def min_delayed_page():
    return render_template(
        "delayed_task.html", title="Min Delayed", is_min=True, is_delayed=True
    )


@delayed_tasks.route("/max_delayed", methods=["GET"])
def max_delayed_page():
    return render_template(
        "delayed_task.html", title="Max Delayed", is_min=False, is_delayed=True
    )


@delayed_tasks.route("/min_non_delayed", methods=["GET"])
def min_non_delayed_page():
    return render_template(
        "delayed_task.html", title="Min Non-Delayed", is_min=True, is_delayed=False
    )


@delayed_tasks.route("/max_non_delayed", methods=["GET"])
def max_non_delayed_page():
    return render_template(
        "delayed_task.html", title="Max Non-Delayed", is_min=False, is_delayed=False
    )


@delayed_tasks.route("/complicated_task", methods=["GET"])
def complicated_task():
    return "To be implemented"
