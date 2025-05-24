import xml.etree.ElementTree as ET
from models import Object
from xml_utils import create_xml_tree, prettyfy_xml
import json


def build_xml_config(path: str, root: Object):
    """генерирует внутреннюю конфигурацию базовой станции
    в config.xml

    Args:
        path (str): путь к файлу
        root (Object): корневой объект
    """
    root_xml = root.create_xml_element(None)
    create_xml_tree(root_xml, root.children)

    pretty_xml = prettyfy_xml(root_xml)

    with open(path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)


def build_json_meta(path: str, classes: dict[str, Object]):
    """Генерирует файл meta.json с
    мета-информацию о классах и их атрибутах

    Args:
        path (str): путь к файлу
        classes (dict[str, Object]): словарь классов(ключ - тег класса, значение - экземпляр класса)
    """
    json_list = [cls_obj.to_dict() for cls_obj in classes.values() if not cls_obj.isRoot]
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(json_list, f, indent=4)
