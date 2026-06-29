#!/bin/bash

set -e

echo
echo "======================================="
echo "Destroying AWS Infrastructure"
echo "======================================="
echo

cd terraform/infrastructure

terraform destroy -auto-approve

echo
echo "✅ AWS resources removed."
echo
