"""Цей файл містить допоміжні функції"""


def get_description(rule, task_type, weighted):
    """Повертає текстовий опис розкладу на основі типу правила та типу задачі"""

    text_description = "розклад з "

    if rule == "SPT":
        text_description += "мінімальн"
    elif rule == "LPT":
        text_description += "максимальн"

    if task_type == "F":
        text_description += (
            f"ою сумарною {'зваженою ' if weighted else ''}тривалістю проходження"
        )
    elif task_type == "W":
        text_description += (
            f"ою сумарною {'зваженою ' if weighted else ''}тривалістю очікування"
        )
    elif task_type == "L":
        text_description += (
            f"им сумарним {'зваженим ' if weighted else ''}часовим зміщенням"
        )
    elif task_type == "T":
        text_description += (
            f"им сумарним {'зваженим ' if weighted else ''}часом закінчення"
        )

    return text_description + " робіт."
