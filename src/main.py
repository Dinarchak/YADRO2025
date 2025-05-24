from parser import parse_input_xml
from builder import build_xml_config, build_json_meta
    

def run():
    classes, root_cls_obj = parse_input_xml('./input/test_input.xml')
    build_xml_config("./out/config.xml", root_cls_obj)
    build_json_meta('./out/meta.json', classes)


if __name__ == '__main__':
    run()