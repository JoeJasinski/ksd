
from typing import Dict
import fileinput
import yaml
import base64
import sys
from copy import deepcopy


def evaluate_secret(k8s_resource: Dict) -> Dict:
    
    resource_type = k8s_resource['kind']
    if not resource_type == "Secret":
        print(
            f"Resource must be a secret type. Found {resource_type}",
            file=sys.stderr)
        return k8s_resource

    if 'data' not in k8s_resource:
        print(f"Yaml needs a 'data' key.", file=sys.stderr)
        return k8s_resource

    data = k8s_resource['data']
    decoded_data = {}
    for key, value in data.items():
        try:
            decoded_data[key] = base64.b64decode(value).decode()
        except Exception:
            decoded_data[key] = value
    k8s_resource['data'] = decoded_data
    return k8s_resource


def evaluate_document(k8s_yaml_document: Dict) -> Dict:

    if 'kind' not in k8s_yaml_document:
        print(f"Yaml needs a 'kind' key.", file=sys.stderr)
        exit(1)

    if k8s_yaml_document['kind'] == "List" and k8s_yaml_document.get('items', []):
        new_items = []
        for resource in k8s_yaml_document['items']:
            resource_cp = deepcopy(resource)
            new_items.append(evaluate_secret(resource_cp))
        k8s_yaml_document['items'] = new_items
    elif k8s_yaml_document['kind'] == 'Secret':
        resource_cp = deepcopy(k8s_yaml_document)
        k8s_yaml_document = evaluate_secret(resource_cp)
    return k8s_yaml_document


def main():
    input_str = ""
    for line in fileinput.input():
        input_str += line

    try:
        yaml_docs = yaml.safe_load_all(input_str)
    except ValueError as exc:
        print(f"Invalid Resource Yaml: {exc}", file=sys.stderr)
        exit(1)
    except Exception as exc:
        print(f"Unknown Exception: {exc}", file=sys.stderr)
        exit(1)

    new_k8s_docs = []
    for yaml_doc in yaml_docs:
        new_k8s_docs.append(evaluate_document(yaml_doc))

    out_str = yaml.dump_all(new_k8s_docs, default_flow_style=False)
    print(out_str)


if __name__ == "__main__":
    main()