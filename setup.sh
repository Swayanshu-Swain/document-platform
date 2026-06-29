#!/bin/bash

set -e

echo
echo "=================================================="
echo "🚀 Document Platform Local Environment Setup"
echo "=================================================="
echo
echo
echo "Prerequisite:"
echo "Run ./infra-up.sh before ./setup.sh"

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

echo "$MINIKUBE_IP document.local" \
| sudo tee -a /etc/hosts >/dev/null

echo "✅ document.local -> $MINIKUBE_IP"

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
# AWS Secret
###################################################

echo "[4/7] Checking aws-credentials..."

if kubectl get secret aws-credentials >/dev/null 2>&1; then

    echo "✅ Existing secret reused."

else

    echo "⚠️ Secret not found."

    [ -z "$AWS_ACCESS_KEY_ID" ] \
        && read -p "AWS_ACCESS_KEY_ID: " AWS_ACCESS_KEY_ID

    [ -z "$AWS_SECRET_ACCESS_KEY" ] \
        && read -s -p "AWS_SECRET_ACCESS_KEY: " AWS_SECRET_ACCESS_KEY \
        && echo

    kubectl create secret generic aws-credentials \
        --from-literal=AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
        --from-literal=AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY"

    echo "✅ Secret created."

fi

echo

###################################################
# Flask Secret
###################################################

echo "[5/7] Checking document-platform-secret..."

if kubectl get secret document-platform-secret >/dev/null 2>&1; then

    echo "✅ Existing secret reused."

else

    echo "⚠️ Secret not found."

    [ -z "$FLASK_SECRET_KEY" ] \
        && read -s -p "FLASK_SECRET_KEY: " FLASK_SECRET_KEY \
        && echo

    kubectl create secret generic document-platform-secret \
        --from-literal=FLASK_SECRET_KEY="$FLASK_SECRET_KEY"

    echo "✅ Secret created."

fi

echo

###################################################
# Deploy Application
###################################################

echo "[6/7] Deploying Document Platform..."

kubectl apply \
    -f gitops/document-platform-app.yaml

echo
echo "⏳ Waiting for ArgoCD to create deployment..."

until kubectl get deployment document-platform \
>/dev/null 2>&1
do
    sleep 5
done

echo
echo "⏳ Deployment found. Waiting for rollout..."

kubectl rollout status \
    deployment/document-platform \
    --timeout=300s
echo
echo "✅ Application deployed"
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

echo "Application (Portable Access):"
echo "The link to local deployment is given bellow"
echo

echo "Ingress Endpoint:"
echo "http://document.local"
echo
echo "Note:"
echo "Native Linux/macOS: works immediately."
echo "WSL2 + Docker driver users may need:"
echo "  minikube tunnel"
echo

echo "ArgoCD:"
echo "https://localhost:8080"
echo

echo "ArgoCD Username: admin"
echo "ArgoCD Password: $ARGO_PASSWORD"
echo
echo "=================================================="

minikube service document-platform-service --url
