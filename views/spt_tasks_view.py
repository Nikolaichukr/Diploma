"""Цей файл відповідає за views (відображення) для SPT-задач"""

from flask import Blueprint, render_template, request
from utils.SPT.generate_xml import generate_quiz_xml
from utils.request_utils import respond_with_file, get_job_values

spt_tasks = Blueprint("spt_tasks", __name__)


@spt_tasks.route("/handle_post", methods=["POST"])
def handle_post_request():
    """Обробка запиту на генерацію XML-файлу"""

    (
        jobs_amount_min,
        jobs_amount_max,
        jobs_duration_min,
        jobs_duration_max,
        tests_amount,
        test_name,
    ) = get_job_values()
    task_type = str(request.form.get("task_type"))

    xml_content = generate_quiz_xml(
        jobs_amount_min,
        jobs_amount_max,
        jobs_duration_min,
        jobs_duration_max,
        tests_amount,
        test_name,
        task_type,
    )

    return respond_with_file(xml_content=xml_content, custom_filename=test_name)


@spt_tasks.route("/spt_F", methods=["GET"])
def spt_f_page():
    return render_template("spt_task.html", task_type="F", title="SPT F")


@spt_tasks.route("/spt_L", methods=["GET"])
def spt_l_page():
    return render_template("spt_task.html", task_type="L", title="SPT L")


@spt_tasks.route("/spt_T", methods=["GET"])
def spt_t_page():
    return render_template("spt_task.html", task_type="T", title="SPT T")


@spt_tasks.route("/spt_W", methods=["GET"])
def spt_w_page():
    return render_template("spt_task.html", task_type="W", title="SPT W")
