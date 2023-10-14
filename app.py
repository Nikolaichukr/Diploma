"""Основний файл - запускає веб-сервер"""

from flask import Flask, render_template
from views import *

app = Flask(__name__)

app.register_blueprint(menu, url_prefix="/")
app.register_blueprint(delayed_tasks, url_prefix="/delayed_task")
app.register_blueprint(spt_tasks, url_prefix="/spt_task")


@app.errorhandler(500)
def app_internal_server_error(error):
    """При виникненні помилок, виводимо інформацію у браузері"""

    return (
        render_template(
            "app_error.html", error_message=error.original_exception, title="Помилка"
        ),
        500,
    )


if __name__ == "__main__":
    app.run(debug=True)
