#!/bin/bash

apt-get update -y

apt-get install -y docker.io

systemctl enable docker
systemctl start docker

docker pull swayanshuswain/document-platform-backend:v1

docker run -d \
  --name document-platform \
  -p 80:5000 \
  -e AWS_REGION=ap-south-1 \
  -e DYNAMODB_USERS_TABLE=users-dev \
  -e AWS_S3_BUCKET=document-platform-dev-006870473063 \
  swayanshuswain/document-platform-backend:v3
