from parser import parse_input_xml
from builder import ConfigBuilder
    

def run():
    classes, root_cls_obj = parse_input_xml('./input/test_input.xml')
    builder = ConfigBuilder(
        root=root_cls_obj,
        classes=classes,
        config_path='./out/config.xml',
        meta_path='./out/meta.json'
    )
    builder.build_xml_config()
    builder.build_json_meta()


if __name__ == '__main__':
    run()