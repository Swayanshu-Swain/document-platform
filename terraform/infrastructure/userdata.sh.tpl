#!/bin/bash

apt-get update -y

apt-get install -y docker.io snapd

snap install amazon-ssm-agent --classic || true

systemctl enable snap.amazon-ssm-agent.amazon-ssm-agent.service
systemctl start snap.amazon-ssm-agent.amazon-ssm-agent.service

systemctl enable docker
systemctl start docker

docker pull swayanshuswain/document-platform-backend:production

docker run -d \
  --restart unless-stopped \
  --name document-platform \
  -p 80:5000 \
  -e AWS_REGION=ap-south-1 \
  -e DYNAMODB_USERS_TABLE=users-dev \
  -e DYNAMODB_FILES_TABLE=audit_logs-dev \
  -e AWS_S3_BUCKET=document-platform-dev-006870473063 \
  -e FLASK_SECRET_KEY="${flask_secret_key}" \
  swayanshuswain/document-platform-backend:production
