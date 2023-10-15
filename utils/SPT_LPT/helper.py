"""Цей файл містить допоміжні функції"""


def get_description(rule, task_type):
    """Повертає текстовий опис розкладу на основі типу правила та типу задачі"""

    text_description = "розклад з "

    if rule == "SPT":
        text_description += "мінімальн"
    elif rule == "LPT":
        text_description += "максимальн"

    if task_type == "F":
        text_description += "ою сумарною тривалістю проходження"
    elif task_type == "W":
        text_description += "ою сумарною тривалістю очікування"
    elif task_type == "L":
        text_description += "им сумарним часовим зміщенням"
    elif task_type == "T":
        text_description += "им сумарним часом закінчення"

    return text_description + " робіт."
