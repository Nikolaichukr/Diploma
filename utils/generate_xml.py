import xml.etree.ElementTree as ET


def generate_file(amount, start_range, end_range):
    # Your XML generation code here
    # Replace this placeholder code with your actual XML generation logic
    xml_root = ET.Element("data")
    for i in range(amount):
        element = ET.SubElement(xml_root, "item")
        element.text = str(i + start_range)

    return ET.tostring(xml_root, encoding="utf-8")
