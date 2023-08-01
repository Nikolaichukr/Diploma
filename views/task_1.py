from flask import Blueprint, render_template, request, make_response
from utils.generate_xml import generate_file

task1 = Blueprint('task1', __name__)


@task1.route("/", methods=["GET", "POST"])
def task1_page():
    if request.method == "POST":
        amount = int(request.form["amount"])
        start_range = int(request.form["start_range"])
        end_range = int(request.form["end_range"])

        xml_content = generate_file(amount, start_range, end_range)

        # Create a response with appropriate headers to force file download
        response = make_response(xml_content)
        response.headers.set("Content-Type", "application/xml")
        response.headers.set("Content-Disposition", "attachment", filename="generated_file.xml")

        return response

    return render_template("task1.html")
