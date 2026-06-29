#!/bin/bash

set -e

echo
echo "======================================="
echo "Destroying Local Environment"
echo "======================================="
echo

pkill -f "argocd-server.*8080:443" \
>/dev/null 2>&1 || true

minikube delete

sudo sed -i '/document.local/d' /etc/hosts

echo
echo "✅ Local environment removed."
echo
echo "AWS infrastructure remains intact."
echo "Run ./infra-down.sh to destroy cloud resources."
echo
