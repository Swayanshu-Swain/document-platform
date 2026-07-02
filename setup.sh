#!/bin/bash

set -e

echo
echo "=================================================="
echo "🚀 Document Platform Local Environment Setup"
echo "=================================================="
echo
echo "Prerequisite: Run ./infra-up.sh before ./setup.sh"
echo

###################################################
# Dependency Check
###################################################

for cmd in docker kubectl minikube git sudo; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "❌ Missing dependency: $cmd"
        exit 1
    fi
done

echo "✅ Dependencies verified"
echo

###################################################
# Load .env
###################################################

if [ -f ".env" ]; then
    echo "📄 Loading .env ..."
    set -a
    source .env
    set +a
    echo "✅ .env loaded"
    echo
fi

###################################################
# Start Minikube
###################################################

echo "[1/7] Starting Minikube..."

DRIVER=${MINIKUBE_DRIVER:-docker}

minikube start \
    --driver="$DRIVER" \
    --cpus=2 \
    --memory=2500

echo
echo "✅ Minikube running"
echo

###################################################
# Enable Ingress
###################################################

echo "[2/7] Enabling ingress..."

minikube addons enable ingress

echo
echo "⏳ Waiting for ingress controller..."

kubectl wait \
    --namespace ingress-nginx \
    --for=condition=ready pod \
    --selector=app.kubernetes.io/component=controller \
    --timeout=300s

MINIKUBE_IP=$(minikube ip)

echo
echo "Updating /etc/hosts..."

sudo sed -i '/document.local/d' /etc/hosts

echo "$MINIKUBE_IP dev.document.local prod.document.local" \
| sudo tee -a /etc/hosts >/dev/null

echo "✅ dev.document.local -> $MINIKUBE_IP"
echo "✅ prod.document.local -> $MINIKUBE_IP"

echo
echo "✅ Ingress enabled"
echo

###################################################
# Install ArgoCD
###################################################

echo "[3/7] Installing ArgoCD..."

kubectl create namespace argocd \
    --dry-run=client \
    -o yaml \
| kubectl apply -f -

kubectl apply \
    --server-side \
    -n argocd \
    -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo
echo "⏳ Waiting for ArgoCD..."

kubectl wait \
    --for=condition=available \
    deployment/argocd-server \
    -n argocd \
    --timeout=300s

echo
echo "✅ ArgoCD ready"
echo

###################################################
# Create Namespaces
###################################################

echo "[4/7] Creating namespaces..."

kubectl apply -f argocd/namespaces/

echo "✅ Namespaces ready"
echo

###################################################
# Create Secrets
###################################################

echo "[5/7] Creating application secrets..."

[ -z "$AWS_ACCESS_KEY_ID" ] \
    && read -p "AWS_ACCESS_KEY_ID: " AWS_ACCESS_KEY_ID

[ -z "$AWS_SECRET_ACCESS_KEY" ] \
    && read -s -p "AWS_SECRET_ACCESS_KEY: " AWS_SECRET_ACCESS_KEY \
    && echo

[ -z "$FLASK_SECRET_KEY" ] \
    && read -s -p "FLASK_SECRET_KEY: " FLASK_SECRET_KEY \
    && echo

for ns in dev prod
do
    echo "🔐 Configuring secrets for namespace: $ns"

    kubectl create secret generic aws-credentials \
        -n "$ns" \
        --from-literal=AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
        --from-literal=AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
        --dry-run=client -o yaml \
    | kubectl apply -f -

    kubectl create secret generic document-platform-secret \
        -n "$ns" \
        --from-literal=FLASK_SECRET_KEY="$FLASK_SECRET_KEY" \
        --dry-run=client -o yaml \
    | kubectl apply -f -
done

echo
echo "✅ Secrets configured"
echo

###################################################
# Deploy ApplicationSet
###################################################

echo "[6/7] Deploying ApplicationSet..."

kubectl apply -f argocd/applicationset.yaml

echo
echo "⏳ Waiting for ArgoCD applications..."

until kubectl get application document-platform-dev -n argocd >/dev/null 2>&1
do
    sleep 2
done

until kubectl get application document-platform-prod -n argocd >/dev/null 2>&1
do
    sleep 2
done

echo
echo "⏳ Waiting for deployments..."

kubectl rollout status \
    deployment/document-platform \
    -n dev \
    --timeout=300s

kubectl rollout status \
    deployment/document-platform \
    -n prod \
    --timeout=300s

echo
echo "✅ Applications deployed"
echo

###################################################
# ArgoCD Port Forward
###################################################

echo "[7/7] Starting ArgoCD UI..."

pkill -f "argocd-server.*8080:443" \
>/dev/null 2>&1 || true

nohup kubectl port-forward \
    svc/argocd-server \
    -n argocd \
    8080:443 \
    >/tmp/argocd.log 2>&1 &

sleep 5

ARGO_PASSWORD=$(
kubectl \
    -n argocd \
    get secret argocd-initial-admin-secret \
    -o jsonpath="{.data.password}" \
| base64 -d
)

echo
echo "=================================================="
echo "🎉 DOCUMENT PLATFORM IS READY"
echo "=================================================="
echo

echo "Dev Environment:"
echo "http://dev.document.local"
echo

echo "Production Environment:"
echo "http://prod.document.local"
echo

echo "ArgoCD:"
echo "https://localhost:8080"
echo

echo "Username: admin"
echo "Password: $ARGO_PASSWORD"
echo

echo "=================================================="
