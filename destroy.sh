#!/bin/bash

set -e

echo
echo "======================================="
echo "Destroying Local Environment"
echo "======================================="
echo

###################################################
# Stop ArgoCD Port Forward
###################################################

pkill -f "argocd-server.*8080:443" \
>/dev/null 2>&1 || true

###################################################
# Delete Minikube Cluster
###################################################

echo "🗑️ Removing Minikube cluster..."

minikube delete

###################################################
# Cleanup Hosts File
###################################################

echo "🧹 Cleaning /etc/hosts..."

sudo sed -i '/document.local/d' /etc/hosts

echo
echo "✅ Local environment removed."
echo
echo "The following remain untouched:"
echo "  • AWS infrastructure"
echo "  • Docker Hub images"
echo "  • GitHub repositories"
echo
echo "Run ./infra-down.sh to destroy cloud resources."
echo
echo "======================================="
