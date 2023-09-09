from flask import Blueprint, render_template

menu = Blueprint("menu", __name__)


@menu.route("/")
def main_menu():
    return render_template("index.html", title="Головне меню")


@menu.route("/delayed_tasks_menu")
def delayed_tasks_menu():
    return render_template(
        "delayed_tasks_menu.html", title="Меню задач, що запізнюються"
    )


@menu.route("/lpt_menu")
def lpt_menu():
    return render_template("lpt_menu.html", title="Меню LPT задач")


@menu.route("/spt_menu")
def spt_menu():
    return render_template("spt_menu.html", title="Меню SPT задач")


@menu.route("/lptu_menu")
def lptu_menu():
    return render_template("lptu_menu.html", title="Меню LPTu задач")


@menu.route("/sptu_menu")
def sptu_menu():
    return render_template("sptu_menu.html", title="Меню SPTu задач")
