"""Цей файл містить набір функцій, які використовуються при роботі генерації XML-файлу"""

import xml.etree.ElementTree as ET
from html import unescape
from lxml import etree


def tab():
    """Повертає комбінацію перенесення каретки та табуляції, потрібна виключно для візуального відображення"""

    return "\n\t\t\t"


def add_tag(parent_element, tag, value):
    """Створює теги зі значенням, використовується для уникнення дублювання"""

    new_tag = ET.SubElement(parent_element, tag)
    new_tag.text = value


def add_dragbox(parent_tag, symbol, group):
    """Додає dragbox блоки (перетягування) до тесту"""

    dragbox = ET.SubElement(parent_tag, "dragbox")
    dragbox_text = ET.SubElement(dragbox, "text")
    dragbox_text.text = str(symbol)
    dragbox_group = ET.SubElement(dragbox, "group")
    dragbox_group.text = str(group)
    ET.SubElement(dragbox, "infinite")


def prettify(xml_string):
    """Форматує XML-код до більш читабельного формату"""

    xml_string = ET.tostring(xml_string, encoding="UTF-8").decode("utf-8")

    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.fromstring(xml_string, parser)
    return unescape(
        etree.tostring(
            tree, encoding="utf-8", pretty_print=True, xml_declaration=True
        ).decode("utf-8")
    )
