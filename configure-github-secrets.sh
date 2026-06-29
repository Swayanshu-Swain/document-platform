#!/bin/bash

set -e

echo
echo "=================================================="
echo " GitHub Actions Secret Configuration"
echo "=================================================="
echo

# ==================================================
# Dependency Checks
# ==================================================

if ! command -v gh >/dev/null 2>&1; then
    echo "❌ GitHub CLI is not installed."
    echo
    echo "Install:"
    echo "https://cli.github.com/"
    exit 1
fi

# ==================================================
# Authentication
# ==================================================

if ! gh auth status >/dev/null 2>&1; then

    echo "⚠️ GitHub CLI is not authenticated."
    echo "Launching login flow..."
    echo

    gh auth login

fi

echo
echo "Current repository:"
gh repo view --json nameWithOwner -q '.nameWithOwner'
echo

read -p "Continue and configure secrets for this repository? [Y/n]: " CONFIRM

CONFIRM=${CONFIRM:-Y}

if [[ "$CONFIRM" != "Y" && "$CONFIRM" != "y" ]]; then
    echo "Aborted."
    exit 0
fi

echo

# ==================================================
# DockerHub
# ==================================================

read -p "DOCKERHUB_USERNAME: " DOCKERHUB_USERNAME

read -s -p "DOCKERHUB_TOKEN: " DOCKERHUB_TOKEN
echo

# ==================================================
# AWS
# ==================================================

read -p "AWS_ACCESS_KEY_ID: " AWS_ACCESS_KEY_ID

read -s -p "AWS_SECRET_ACCESS_KEY: " AWS_SECRET_ACCESS_KEY
echo

read -p "AWS_REGION [ap-south-1]: " AWS_REGION
AWS_REGION=${AWS_REGION:-ap-south-1}

# ==================================================
# Flask
# ==================================================

read -s -p "FLASK_SECRET_KEY: " FLASK_SECRET_KEY
echo

# ==================================================
# Create Secrets
# ==================================================

echo
echo "Creating repository secrets..."
echo

echo "$DOCKERHUB_USERNAME" \
| gh secret set DOCKERHUB_USERNAME

echo "$DOCKERHUB_TOKEN" \
| gh secret set DOCKERHUB_TOKEN

echo "$AWS_ACCESS_KEY_ID" \
| gh secret set AWS_ACCESS_KEY_ID

echo "$AWS_SECRET_ACCESS_KEY" \
| gh secret set AWS_SECRET_ACCESS_KEY

echo "$AWS_REGION" \
| gh secret set AWS_REGION

echo "$FLASK_SECRET_KEY" \
| gh secret set FLASK_SECRET_KEY

echo
echo "=================================================="
echo "✅ Repository secrets configured successfully"
echo "=================================================="
echo
echo "Configured:"
echo
echo "• DOCKERHUB_USERNAME"
echo "• DOCKERHUB_TOKEN"
echo "• AWS_ACCESS_KEY_ID"
echo "• AWS_SECRET_ACCESS_KEY"
echo "• AWS_REGION"
echo "• FLASK_SECRET_KEY"
echo
echo "GitHub Actions pipelines are now ready."
echo
