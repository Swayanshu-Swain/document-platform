# Kubernetes Deployment

This directory contains the raw Kubernetes manifests used to deploy the Document Platform.

## Components

### Deployment

Creates application pods and manages replica lifecycle.

### Service

Exposes the Flask application through a NodePort service.

### ConfigMap

Stores non-sensitive application configuration.

### Secret

Stores sensitive application configuration.

## Deploy

```bash
kubectl apply -f .
```

## Verify

```bash
kubectl get all
kubectl get pods
kubectl logs <pod-name>
```

## Remove

```bash
kubectl delete -f .
```

These manifests were later converted into a Helm chart for reusable deployments.
