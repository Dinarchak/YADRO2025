import xml.etree.ElementTree as ET
from models import Object
import xml.dom.minidom


def create_xml_tree(root_xml: ET.Element, children: list[Object]):
    """Создает представление xml дерева

    Args:
        root_xml (ET.Element): корневой элеменент xml дерева
        children (list[Object]): дети корневого элемента
    """
    for child in children:
        child_xml = child.create_xml_element(root_xml)
        create_xml_tree(child_xml, child.children)


def prettyfy_xml(root_xml: ET.Element) -> str:
    """форматирует xml строку

    Args:
        root_xml (ET.Element): корневой элемент xml дерева

    Returns:
        str: отворматированный xml текст
    """
    rough_string = ET.tostring(root_xml, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
