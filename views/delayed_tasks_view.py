from flask import Blueprint, render_template, request, make_response
from utils.generate_xml import generate_quiz_xml

delayed_tasks = Blueprint("delayed_tasks", __name__)


@delayed_tasks.route("/handle_post", methods=["POST"])
def handle_post_request():
    jobs_amount_min = int(request.form.get("jobs_amount_min"))
    jobs_amount_max = int(request.form.get("jobs_amount_max"))
    jobs_duration_min = int(request.form.get("jobs_duration_min"))
    jobs_duration_max = int(request.form.get("jobs_duration_max"))
    tests_amount = int(request.form.get("tests_amount"))
    test_name = str(request.form.get("test_name"))
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

    # Create a response with appropriate headers to force file download
    response = make_response(xml_content)
    response.headers.set("Content-Type", "application/xml")
    response.headers.set(
        "Content-Disposition", "attachment", filename="generated_file.xml"
    )

    return response


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
