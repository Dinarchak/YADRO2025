import xml.etree.ElementTree as ET


class Attribute:
    def __init__(self, name: str, type: str):
        """
        Args:
            name (str): имя атрибута
            type (str): тип атрибута
        """
        self.name: str = name
        self.type: str = type

    def create_xml_element(self, parent: ET.Element):
        """Создает xlm элемент соответсвутющий атрибуту
        и внедряет его в xml дерево

        Args:
            parent (ET.Element): родитель в xml-дереве
        """
        ET.SubElement(parent, self.name).text = self.type

    def to_dict(self) -> dict:
        """Конверитация в словарь для записи в meta.json

        Returns: dict
        """
        return {
            'name': self.name,
            'type': self.type
        }

class Object:
    def __init__(self, name: str, isRoot: bool, documentation: str, attrs: list[Attribute]):
        """
        Args:
            name (str): имя класса
            isRoot (bool): является ли корнем
            documentation (str): описание класса
            attrs (list[Attribute]): список атрибутов
        """

        self.attrs: list[Attribute] = attrs
        self.children: list[Object] = []

        # мета-информация
        self.name: str = name
        self.isRoot: bool = isRoot
        self.documentation: str = documentation
        self.max: int | None = None # максимально значение исходящей связи
        self.min: int | None = None # минимальное значение исходящей связи

    def create_xml_element(self, parent: ET.Element) -> ET.Element:
        """Создает xlm элемент соответсвутющий атрибуту
        и внедряет его в xml дерево

        Args:
            parent (ET.Element): родитель в xml дереве

        Returns:
            ET.Element: xml-представление класса
        """
        if self.isRoot:
            elem = ET.Element(self.name) # создать как корень дерева
        else:
            elem = ET.SubElement(parent, self.name) # создать как ребенок xml-элемента

        for attr in self.attrs:
            attr.create_xml_element(elem)

        return elem
    
    def to_dict(self) -> dict:
        """Конверитация в словарь для записи в meta.json

        Returns: dict
        """
        return {
            'class': self.name,
            'documentation': self.documentation,
            'isRoot': self.isRoot,
            'max': self.max,
            'min': self.min,
            'parameters': ([sub_class.to_dict_as_param() for sub_class in self.children]
            + [attr.to_dict() for attr in self.attrs])
        }

    def to_dict_as_param(self) -> dict:
        """Конвертация в словарь для записи в meta.json.
        Класс представляется как элемент списка parameters родителя

        Returns:
            dict: _description_
        """
        return {'name': self.name, 'type': 'class'}