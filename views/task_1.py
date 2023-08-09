from flask import Blueprint, render_template, request, make_response
from utils.generate_xml import generate_quiz_xml

task1 = Blueprint('task1', __name__)


@task1.route("/", methods=["GET", "POST"])
def task1_page():
    if request.method == "POST":
        jobs_amount_min = int(request.form["jobs_amount_min"])
        jobs_amount_max = int(request.form["jobs_amount_max"])
        jobs_duration_min = int(request.form["jobs_duration_min"])
        jobs_duration_max = int(request.form["jobs_duration_max"])
        tests_amount = int(request.form["tests_amount"])
        test_name = int(request.form["test_name"])

        # xml_content = generate_quiz_xml(amount, start_range, end_range)
        xml_content = generate_quiz_xml(5, 1, 15)

        # Create a response with appropriate headers to force file download
        response = make_response(xml_content)
        response.headers.set("Content-Type", "application/xml")
        response.headers.set("Content-Disposition", "attachment", filename="generated_file.xml")

        return response

    return render_template("task1.html")
