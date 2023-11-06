"""Цей файл відповідає за views (відображення) для SPT та LPT-задач"""

from flask import Blueprint, render_template, request, abort
from utils.SPT_LPT.generate_xml import generate_quiz_xml
from utils.request_utils import respond_with_file, get_job_values

spt_lpt_tasks = Blueprint("spt_lpt_tasks", __name__)

RULE_TYPE = ["SPT", "LPT", "SPTu", "LPTu"]
TASK_TYPE = ["F", "L", "T", "W"]


@spt_lpt_tasks.route("/handle_post", methods=["POST"])
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
    rule = str(request.form.get("rule"))
    weighted = bool(int(request.form.get("is_weighted")))

    xml_content = generate_quiz_xml(
        jobs_amount_min,
        jobs_amount_max,
        jobs_duration_min,
        jobs_duration_max,
        tests_amount,
        test_name,
        task_type,
        rule,
    )

    return respond_with_file(xml_content=xml_content, custom_filename=test_name)


@spt_lpt_tasks.route("/<rule>_<task>", methods=["GET"])
def task_page(rule, task):
    """Використовуємо динамічну маршрутизацію для уніфікації коду"""

    if "u" in rule:
        rule, weighted = rule.strip("u"), True
    else:
        weighted = False
    if rule in RULE_TYPE and task in TASK_TYPE:
        return render_template(
            "spt_lpt.html", task_type=task, rule=rule.upper(), weighted=weighted
        )
    else:
        abort(404)
