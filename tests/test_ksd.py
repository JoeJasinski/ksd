import textwrap
import json

import yaml
import pytest

from ksd.ksd import decoder

secret_single = textwrap.dedent("""\
    apiVersion: v1
    data:
      EMPTY_VALUE: ""
      lower_emtpy_value: ""
      mysecret: b3ZlcnJpZGUtdGhpcy1rZXktaGVyZQ==
      bool_secret: RmFsc2U=
    kind: Secret
    metadata:
      annotations:
        some.annotation: some-value
      creationTimestamp: "2024-02-24T23:08:53Z"
      labels:
        some.label/instance: my-release
      name: mysecret
      namespace: mynamespace
      resourceVersion: "1234"
      uid: 006bef6d-98ae-48e6-bfdb-9518a1b54ace
    type: Opaque
    """)


secret_single_expected_output = {'apiVersion': 'v1',
    'data': {'EMPTY_VALUE': '',
            'bool_secret': 'False',
            'lower_emtpy_value': '',
            'mysecret': 'override-this-key-here'},
    'kind': 'Secret',
    'metadata': {'annotations': {'some.annotation': 'some-value'},
                'creationTimestamp': '2024-02-24T23:08:53Z',
                'labels': {'some.label/instance': 'my-release'},
                'name': 'mysecret',
                'namespace': 'mynamespace',
                'resourceVersion': '1234',
                'uid': '006bef6d-98ae-48e6-bfdb-9518a1b54ace'},
    'type': 'Opaque'}


secret_list = textwrap.dedent("""\
    apiVersion: v1
    kind: List
    items:
    - apiVersion: v1
      data:
        EMPTY_VALUE: ""
        mysecret: b3ZlcnJpZGUtdGhpcy1rZXktaGVyZQ==
      kind: Secret
      metadata:
        labels:
          some.label/instance: my-release
        name: secret1
        namespace: mynamespace
        resourceVersion: "1234"
      type: Opaque
    - apiVersion: v1
      data:
        EMPTY_VALUE: ""
        mysecret: b3ZlcnJpZGUtdGhpcy1rZXktaGVyZQ==
      kind: Secret
      metadata:
        labels:
          some.label/instance: my-release
        name: secret2
        namespace: mynamespace
        resourceVersion: "1234"
      type: Opaque
    """)


secret_list_expected_output = {
    'apiVersion': 'v1',
    'items': [{'apiVersion': 'v1',
                'data': {'EMPTY_VALUE': '', 'mysecret': 'override-this-key-here'},
                'kind': 'Secret',
                'metadata': {'labels': {'some.label/instance': 'my-release'},
                            'name': 'secret1',
                            'namespace': 'mynamespace',
                            'resourceVersion': '1234'},
                'type': 'Opaque'},
                {'apiVersion': 'v1',
                'data': {'EMPTY_VALUE': '', 'mysecret': 'override-this-key-here'},
                'kind': 'Secret',
                'metadata': {'labels': {'some.label/instance': 'my-release'},
                            'name': 'secret2',
                            'namespace': 'mynamespace',
                            'resourceVersion': '1234'},
                'type': 'Opaque'}],
    'kind': 'List'}


secret_no_data = textwrap.dedent("""\
    apiVersion: v1
    kind: Secret
    metadata:
      annotations:
        some.annotation: some-value
      creationTimestamp: "2024-02-24T23:08:53Z"
      labels:
        some.label/instance: my-release
      name: mysecret
      namespace: mynamespace
      resourceVersion: "1234"
      uid: 006bef6d-98ae-48e6-bfdb-9518a1b54ace
    type: Opaque
    """)

secret_no_data_expected_output = {
    'apiVersion': 'v1',
    'kind': 'Secret',
    'metadata': {'annotations': {'some.annotation': 'some-value'},
                'creationTimestamp': '2024-02-24T23:08:53Z',
                'labels': {'some.label/instance': 'my-release'},
                'name': 'mysecret',
                'namespace': 'mynamespace',
                'resourceVersion': '1234',
                'uid': '006bef6d-98ae-48e6-bfdb-9518a1b54ace'},
    'type': 'Opaque'}


@pytest.mark.parametrize("transsform_input", [
    pytest.param(lambda x: x, id="from_yaml"),
    pytest.param(lambda x: json.dumps(yaml.safe_load(x)), id="from_json"),
])
@pytest.mark.parametrize("input, expected", [
    pytest.param(secret_single, secret_single_expected_output, id="secret_single"),
    pytest.param(secret_no_data, secret_no_data_expected_output, id="no_data"),
    pytest.param(secret_list, secret_list_expected_output, id="secret_list"),
])
def test__decoder(input, expected, transsform_input):
    output = decoder(transsform_input(input))
    yaml_output = yaml.safe_load(output)
    assert yaml_output == expected


secret_multi_doc = textwrap.dedent("""\
    apiVersion: v1
    data:
      EMPTY_VALUE_1: ""
      mysecret: b3ZlcnJpZGUtdGhpcy1rZXktaGVyZQ==
    kind: Secret
    metadata:
      name: secret1
      namespace: mynamespace
    type: Opaque
    ---
    apiVersion: v1
    data:
      EMPTY_VALUE: ""
      mysecret: b3ZlcnJpZGUtdGhpcy1rZXktaGVyZQ==
    kind: Secret
    metadata:
      name: secret2
      namespace: mynamespace
    type: Opaque
    """)


def test__decoder__multi_doc_secret():
    output = decoder(secret_multi_doc)
    yaml_output = list(yaml.safe_load_all(output))

    expected_output = [
        {'apiVersion': 'v1',
            'data': {'EMPTY_VALUE_1': '', 'mysecret': 'override-this-key-here'},
            'kind': 'Secret',
            'metadata': {'name': 'secret1', 'namespace': 'mynamespace'},
            'type': 'Opaque'},
        {'apiVersion': 'v1',
            'data': {'EMPTY_VALUE': '', 'mysecret': 'override-this-key-here'},
            'kind': 'Secret',
            'metadata': {'name': 'secret2', 'namespace': 'mynamespace'},
            'type': 'Opaque'}
    ]

    assert yaml_output == expected_output