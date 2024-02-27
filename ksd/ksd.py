
from typing import Dict, Optional, Callable
import base64
import sys
from copy import deepcopy
import argparse
import textwrap
import abc
import json
import yaml


class BaseFormatter(abc.ABC):
    
    @abc.abstractmethod
    def dump(self, data) -> str:
        ...


class YamlFormatter(BaseFormatter):
    def dump(self, data) -> str:
        return yaml.dump_all(data, default_flow_style=False)


class JsonFormatter(BaseFormatter):
    def dump(self, data) -> str:
        return json.dumps(data, indent=2)


def evaluate_secret(k8s_resource: Dict, verbose: bool = False) -> Dict:
    """Given a kubernetes resource dictionary, base64 decode any secrets in it

    :param k8s_resource: the k8s resource to operate on
    :param verbose: if True, print more output
    :return: Return a dictionary that has the secrets decoded (if input resource was 
     as secret)
    """
    resource_type = k8s_resource['kind']
    if not resource_type == "Secret":
        if verbose:
            print(
                f"Resource must be a secret type. Found {resource_type}",
                file=sys.stderr)
        return k8s_resource

    if 'data' not in k8s_resource:
        if verbose:
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


def evaluate_document(k8s_resource_document: Dict, verbose: bool = False) -> Dict:
    """Given a single k8s resource determine if it is a List of Secrets or Secret
       and decode the secret if so.
    
    :param k8s_resource_document: a kubernetes resource document dict
    :param verbose: if True, print more output
    """
    if 'kind' not in k8s_resource_document:
        print(f"Yaml needs a 'kind' key.", file=sys.stderr)
        exit(1)

    if k8s_resource_document['kind'] == "List" and k8s_resource_document.get('items', []):
        new_items = []
        for resource in k8s_resource_document['items']:
            resource_cp = deepcopy(resource)
            new_items.append(evaluate_secret(resource_cp, verbose=verbose))
        k8s_resource_document['items'] = new_items
    elif k8s_resource_document['kind'] == 'Secret':
        resource_cp = deepcopy(k8s_resource_document)
        k8s_resource_document = evaluate_secret(resource_cp, verbose=verbose)

    return k8s_resource_document


def decoder(
        input_str: str, 
        verbose: bool = False, 
        formatter: Optional[Callable] = None) -> str:
    """Given a raw JSON or YAML string, decode any base64 encoded k8s Secrets in it

    :param input_str: A raw JSON or YAML string that represents one or more k8s 
        resources, and hopefully containing Secrets
    :param verbose: if True, print more output
    :return: a string just like the input, but with decoded secrets
    """
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
        new_k8s_docs.append(evaluate_document(yaml_doc, verbose=verbose))

    if not formatter:
        formatter = YamlFormatter()

    return formatter.dump(new_k8s_docs)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog='ksd',
        description=textwrap.dedent("""\
            Given YAML or JSON output from kubectl decode any base64 encoded secrets.
                                    
            Usage: 
                # Simple usage to get all secrets
                kubectl get secret -o yaml | ksd
                
                # Simple usage to get a single secret
                kubectl get secret my_secret -o yaml | ksd
                
        """),
    )
    parser.add_argument(
        'infile', nargs='?', type=argparse.FileType('r'),
        default=sys.stdin)
    parser.add_argument(
        '-v', '--verbose', action='store_true', 
        dest="verbose", default=False)
    parser.add_argument(
        '-f', '--format', action='store',
        help="Output format: yaml or json",
        choices=["json", "yaml"],
        dest="format", default="yaml") 
    inargs = parser.parse_args()
    input_str = inargs.infile.read()

    if inargs.format == 'yaml':
        formatter = YamlFormatter()
    elif inargs.format == 'json':
        formatter = JsonFormatter()
    else:
        raise Exception("Invalid formatter")
    output_str = decoder(
        input_str, verbose=inargs.verbose,
        formatter=formatter)
    print(output_str)


if __name__ == "__main__":
    main()
