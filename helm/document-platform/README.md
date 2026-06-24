# Document Platform Helm Chart

Helm chart for deploying the Document Platform on Kubernetes.

## Installation

```bash
helm install document-platform .
```

## Upgrade

```bash
helm upgrade document-platform .
```

## Uninstall

```bash
helm uninstall document-platform
```

## Configuration

Important values:

```yaml
replicaCount: 2

image:
  repository: swayanshuswain/document-platform-backend
  tag: latest
```

### AWS Configuration

```yaml
aws:
  region: ap-south-1
  bucket: document-platform-dev-006870473063
```

### DynamoDB Configuration

```yaml
dynamodb:
  usersTable: users-dev
  filesTable: files-dev
  auditTable: audit_logs-dev
```

## Features

* ConfigMap support
* Secret management
* Resource limits
* Readiness probes
* Liveness probes
* Horizontal scalability through replica configuration

## Verify Deployment

```bash
kubectl get pods
kubectl get deployments
kubectl get services
```
