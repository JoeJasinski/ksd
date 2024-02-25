# Easily Read kubernetes Secrets

Read base64 encoded Kubernetes secrets without getting in your way.

## Features

- allows you to read one or more 
- works with individual secrets, lists of secrets, and multiple yaml docs
- simple auditable Python source code

### Install

TDB

## Quick Example

```bash
$ kubectl  get secret -n mynamespace -o yaml mysecret | ksd
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

Get single secret as YAML

```bash
kubectl get secret -o yaml mysecret | ksd 
```

Get multiple secrets as YAML

```bash
kubectl get secret -o yaml  | ksd
```

Get secrets as JSON

```bash
kubectl  get secret -o json | ksd
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

I really like this project below, as it does exaclty this. 
However, before I install this on my corporate laptop,
I wanted something that I could easily audit the source code for,
since I cannot really do that with a Go binary. Python makes that
easier to do.

https://github.com/gechr/ksd
