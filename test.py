import os
import sys
import logging
import javalang
import yaml  # pip install pyyaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def get_java_files(target_dir):
    logging.info(f"Scanning directory: {target_dir}")
    java_files = []
    for root, dirs, files in os.walk(target_dir):
        for f in files:
            if f.endswith('.java'):
                full_path = os.path.join(root, f)
                java_files.append(full_path)
    logging.info(f"Found {len(java_files)} Java files in {target_dir}")
    return java_files

def get_classes_and_relations(java_files):
    classes = {}
    
    for f in java_files:
        logging.debug(f"Parsing file: {f}")
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        try:
            tree = javalang.parse.parse(content)
        except javalang.parser.JavaSyntaxError as e:
            logging.warning(f"Syntax error in file {f}: {e}")
            continue
        
        package_name = tree.package.name if tree.package else ''
        
        for type_decl in tree.types:
            if isinstance(type_decl, (javalang.tree.ClassDeclaration, javalang.tree.InterfaceDeclaration)):
                class_name = package_name + '.' + type_decl.name if package_name else type_decl.name
                
                # extends 처리
                parent = None
                if isinstance(type_decl, javalang.tree.ClassDeclaration):
                    if type_decl.extends:
                        parent = type_decl.extends.name
                elif isinstance(type_decl, javalang.tree.InterfaceDeclaration):
                    if type_decl.extends and len(type_decl.extends) > 0:
                        parent = type_decl.extends[0].name
                
                # implements 처리
                if hasattr(type_decl, 'implements') and type_decl.implements is not None:
                    implements = [impl.name for impl in type_decl.implements]
                else:
                    implements = []
                
                # imports
                imports = [imp.path for imp in tree.imports if imp.path]
                
                classes[class_name] = {
                    'extends': parent,
                    'implements': implements,
                    'imports': imports
                }
                logging.debug(f"Discovered class: {class_name}, extends: {parent}, implements: {implements}, imports: {len(imports)}")
    
    logging.info(f"Total classes found: {len(classes)}")
    return classes

def print_as_yaml(classes):
    # classes 딕셔너리를 YAML 형태로 출력
    yaml_str = yaml.dump(classes, default_flow_style=False, sort_keys=True, allow_unicode=True)
    print(yaml_str)

def save_as_yaml(classes, filename):
    yaml_str = yaml.dump(classes, default_flow_style=False, sort_keys=True, allow_unicode=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(yaml_str)
    logging.info("Saved YAML output to %s", filename)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test.py [TARGET_DIR]")
        sys.exit(1)

    target_dir = '/Users/dvmoomoodv/Project/company/gsitm/framework/ustra-framework2.2-java/framework/' + sys.argv[1]
    if not os.path.isdir(target_dir):
        print("Invalid directory:", target_dir)
        sys.exit(1)
    
    java_files = get_java_files(target_dir)
    classes = get_classes_and_relations(java_files)
    
    print_as_yaml(classes)

    base_name = os.path.basename(target_dir.rstrip('/'))
    output_file = f"{base_name}_classes.yaml"
    save_as_yaml(classes, output_file)