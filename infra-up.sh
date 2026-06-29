#!/bin/bash

set -e

if [ -f ".env" ]; then
    set -a
    source .env
    set +a
fi

if [ -z "$FLASK_SECRET_KEY" ]; then
    read -s -p "FLASK_SECRET_KEY: " FLASK_SECRET_KEY
    echo
fi

export TF_VAR_flask_secret_key="$FLASK_SECRET_KEY"

echo
echo "======================================="
echo "Provisioning AWS Infrastructure"
echo "======================================="
echo

cd terraform/infrastructure

terraform init

terraform apply -auto-approve

echo
echo "✅ Infrastructure created."
echo

terraform output public_ip

echo
echo "Open in browser:"
echo "http://$(terraform output -raw public_ip)"
echo
echo "Use AWS SSM for shell access:"
echo
terraform output ssm_connect_command

echo

