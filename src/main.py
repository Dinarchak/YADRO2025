import xml.etree.ElementTree as ET
import xml.dom.minidom
import json

class Object:
    def __init__(self, name, isRoot, documentation, attrs):
        self.name = name
        self.isRoot = isRoot
        self.documentation = documentation

        self.attrs = attrs
        self.children = []
        self.max = None
        self.min = None

    def create_xml_element(self, parent):
        if self.isRoot:
            elem = ET.Element(self.name)
        else:
            elem = ET.SubElement(parent, self.name)

        for attr in self.attrs:
            attr.create_xml_element(elem)

        return elem
    
    def to_dict(self):
        return {
            'class': self.name,
            'documentation': self.documentation,
            'isRoot': self.isRoot,
            'max': self.max,
            'min': self.min,
            'parameters': [attr.to_dict() for attr in self.attrs]
        }

class Attribute:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def create_xml_element(self, parent):
        ET.SubElement(parent, self.name).text = self.type

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type
        }
    

def create_xml_tree(root_xml, children):
    for child in children:
        child_xml = child.create_xml_element(root_xml)
        create_xml_tree(child_xml, child.children)

def run():
#===========================================Чтение и обработка данных==========================================
    root_cls_obj = None
    classes = {}

    config = ET.parse('./input/test_input.xml')
    root = config.getroot()

    for cls_conf in root.findall('Class'):

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

    for aggregation in root.findall('Aggregation'):
        source_obj = classes[aggregation.attrib['source']]
        sourceMultiplicity = aggregation.attrib['sourceMultiplicity'].split('.')

        if len(sourceMultiplicity) == 1:    
            source_obj.max = source_obj.min = int(sourceMultiplicity[0])
        else:
            source_obj.min = int(sourceMultiplicity[0])
            source_obj.max = int(sourceMultiplicity[-1])

        classes[aggregation.attrib['target']].children.append(source_obj)
#=================================================================Создание meta.json и config.xml============================================================

    root_xml = root_cls_obj.create_xml_element(None)
    create_xml_tree(root_xml, root_cls_obj.children)
    tree = ET.ElementTree(root_xml)

    rough_string = ET.tostring(root_xml, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open("./out/config.xml", "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    json_list = [cls_obj.to_dict() for cls_obj in classes.values() if not cls_conf.isRoot]
    with open('./out/meta.json', 'w', encoding='utf-8') as f:
        json.dump(json_list, f, indent=4)

if __name__ == '__main__':
    run()