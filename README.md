# Easily Read kubernetes Secrets

Read base64 encoded Kubernetes secrets without getting in your way.

Kubernetes secrets resources base64 encode the secret values. It is often
useful to view the decoded values for those secrets in place. This tool
offers a useful means to do that. 

## Features

- allows you to read one or more Secrets
- works with individual secrets, lists of secrets, and multiple yaml docs
- simple auditable Python source code

### Install

Install with pip

```bash
pip install ksd
```

Install with pipx

```bash
pipx install ksd
```

## Quick Example

```bash
$ kubectl get secret -n mynamespace -o yaml mysecret | ksd
```
```yaml
apiVersion: v1
data:
  password: my-decoded-password-secret
  username: my-decoded-username-secret
kind: Secret
metadata:
  creationTimestamp: '2024-01-01T00:00:0Z'
  labels:
    name: mynamespace
  name: mysecret
  namespace: mynamespace
  resourceVersion: '1234'
  uid: c4f4c4db-bdba-47d0-9a17-1e307e1448c7
type: Opaque
```

## Detailed Usage

Get help

```bash
ksd --help
```

Get single secret as YAML and decode as YAML

```bash
kubectl get secret -o yaml mysecret | ksd 
```

Get single secret as YAML and decode as JSON

```bash
kubectl get secret -o yaml mysecret | ksd -f json
```

Get multiple secrets as YAML and decode as YAML

```bash
kubectl get secret -o yaml  | ksd
```

Get multiple secrets as YAML and decode as JSON

```bash
kubectl get secret -o yaml  | ksd -f json
```

Get secrets as JSON and decode as YAML

```bash
kubectl  get secret -o json | ksd
```

Get secrets as JSON and decode as JSON

```bash
kubectl  get secret -o json | ksd -f json
```


Use k8s flags as normal

```bash
kubectl  get secret -n my_namespace -l label_key=label_value -o json | ksd
```

I don't know why you would do this, but the output is idempotent

```bash
kubectl get secret -o yaml  | ksd | ksd
```

Read Secrets from a file 

```bash
cat secrets.yaml | ksd
```

Suppoert multi-document yaml input (separated with the yaml '---')

```bash
kubectl get secret -o yaml mysecret > secrets.yaml
echo "---" >> secrets.yaml
kubectl get secret -o yaml ohter_secret >> secrets.yaml
cat secrets.yaml | ksd
```


## Inspired by

There are several projects with a similar name and purpose. However, they
are written in Go and distribute compiled binaries. I prefer to use a version
of this tool written in Python, for which the source code is auditable. 


## Tests

```bash
pip install -e .[tests]
pytest -vvv tests/
```