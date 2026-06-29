#!/bin/bash

apt-get update -y

apt-get install -y docker.io

systemctl enable docker
systemctl start docker

docker pull swayanshuswain/document-platform-backend:8d6259b

docker run -d \
  --restart unless-stopped \
  --name document-platform \
  -p 80:5000 \
  -e AWS_REGION=ap-south-1 \
  -e DYNAMODB_USERS_TABLE=users-dev \
  -e DYNAMODB_FILES_TABLE=files-dev \
  -e DYNAMODB_AUDIT_TABLE=audit_logs-dev \
  -e AWS_S3_BUCKET=document-platform-dev-006870473063 \
  swayanshuswain/document-platform-backend:8d6259b
