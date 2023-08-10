from flask import Flask, render_template
from views import *

app = Flask(__name__)

app.register_blueprint(main, url_prefix="/")
app.register_blueprint(task1, url_prefix="/task1")


@app.errorhandler(500)
def app_internal_server_error(error):
    return (
        render_template(
            "app_error.html", error_message=error.original_exception, title="Помилка"
        ),
        500,
    )


if __name__ == "__main__":
    app.run(debug=True)
