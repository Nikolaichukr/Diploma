from flask import Blueprint, render_template, request, make_response
from utils.SPT.generate_xml import generate_quiz_xml

spt_tasks = Blueprint("spt_tasks", __name__)


@spt_tasks.route("/handle_post", methods=["POST"])
def handle_post_request():
    jobs_amount_min = int(request.form.get("jobs_amount_min"))
    jobs_amount_max = int(request.form.get("jobs_amount_max"))
    jobs_duration_min = int(request.form.get("jobs_duration_min"))
    jobs_duration_max = int(request.form.get("jobs_duration_max"))
    tests_amount = int(request.form.get("tests_amount"))
    test_name = str(request.form.get("test_name"))

    xml_content = generate_quiz_xml(
        jobs_amount_min,
        jobs_amount_max,
        jobs_duration_min,
        jobs_duration_max,
        tests_amount,
        test_name,
    )

    # Create a response with appropriate headers to force file download
    response = make_response(xml_content)
    response.headers.set("Content-Type", "application/xml")
    response.headers.set(
        "Content-Disposition", "attachment", filename="generated_file.xml"
    )

    return response


@spt_tasks.route("/spt_F", methods=["GET"])
def spt_f_page():
    return render_template("spt_task.html", title="SPT F")
