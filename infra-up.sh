#!/bin/bash

set -e

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

