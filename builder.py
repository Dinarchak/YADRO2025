from models import Object
from xml_utils import create_xml_tree, prettyfy_xml
import json


class ConfigBuilder:
    def __init__(
            self,
            root: Object,
            classes: dict[str, Object],
            config_path: str,
            meta_path: str):
        """Класс для генерации выходных файлов

        Args:
            root (Object): корневой класс
            config_path (str): путь до config.xml
            meta_path (str): путь до meta.json
        """
        self.root: Object = root
        self.classes: dict[str, Object] = classes
        self.config_path: str = config_path
        self.meta_path: str = meta_path

    def build_xml_config(self):
        """генерирует внутреннюю конфигурацию базовой станции
        в config.xml

        Args:
            path (str): путь к файлу
            root (Object): корневой объект
        """
        root_xml = self.root.create_xml_element(None)
        create_xml_tree(root_xml, self.root.children)

        pretty_xml = prettyfy_xml(root_xml)

        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

    def build_json_meta(self):
        """Генерирует файл meta.json с
        мета-информацию о классах и их атрибутах

        Args:
            path (str): путь к файлу
            classes (dict[str, Object]): словарь классов
            (ключ - тег класса, значение - экземпляр класса)
        """
        json_list = [cls_obj.to_dict() for cls_obj in self.classes.values()]
        with open(self.meta_path, 'w', encoding='utf-8') as f:
            json.dump(json_list, f, indent=4)
