from models import Object, Attribute
import xml.etree.ElementTree as ET


def parse_input_xml(path: str) -> tuple:
    """Чтение исходного xml файла

    Args:
        path (str): путь к файлу

    Returns:
        tuple: словарь(ключ - название объекта, значение - Object), корневой объект(Object)
    """

    root_cls_obj = None
    classes = {}

    config = ET.parse(path)
    root = config.getroot()

    for cls_conf in root.findall('Class'): # обработать все теги Class

        attrs_list = []
        for attr in cls_conf:
            attrs_list.append(Attribute(**attr.attrib))

        cls_obj = Object(
            name=cls_conf.attrib['name'],
            isRoot=(cls_conf.attrib['isRoot']=='true'),
            documentation=cls_conf.attrib['documentation'],
            attrs=attrs_list
        )
        

        if cls_obj.isRoot: root_cls_obj = cls_obj
        classes[cls_obj.name] = cls_obj

    for aggregation in root.findall('Aggregation'): # обработать все теги Aggreagation
        source_obj = classes[aggregation.attrib['source']]
        sourceMultiplicity = aggregation.attrib['sourceMultiplicity'].split('.')

        if len(sourceMultiplicity) == 1:    
            source_obj.max = source_obj.min = int(sourceMultiplicity[0])
        else:
            source_obj.min = int(sourceMultiplicity[0])
            source_obj.max = int(sourceMultiplicity[-1])

        classes[aggregation.attrib['target']].children.append(source_obj)
    return classes, root_cls_obj