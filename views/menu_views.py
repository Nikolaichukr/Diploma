"""Цей файл відповідає за views (відображення) для меню та підменю"""

from flask import Blueprint, render_template

menu = Blueprint("menu", __name__)


@menu.route("/")
def main_menu():
    return render_template("index.html", title="Головне меню")


@menu.route("/delayed_tasks_menu")
def delayed_tasks_menu():
    return render_template(
        "menu_templates/delayed_tasks_menu.html", title="Меню задач, що запізнюються"
    )


@menu.route("/<string:menu_type>_menu")
def menu_view(menu_type):
    allowed_routes = ["lpt", "spt", "lptu", "sptu"]
    if menu_type not in allowed_routes:
        return "Invalid page.", 404

    template = f"menu_templates/{menu_type}_menu.html"

    return render_template(template, title=f"Меню {menu_type.upper()} задач")
