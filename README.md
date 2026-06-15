# Document Platform

A cloud-native document management platform built using AWS, Docker, Terraform, and GitHub Actions.

## Features

* User authentication using DynamoDB
* Document upload and storage in Amazon S3
* Role-based access control
* Audit logging
* Infrastructure as Code using Terraform
* Containerized backend using Docker
* Automated CI/CD pipeline using GitHub Actions
* Zero-SSH deployments using AWS Systems Manager

## Architecture

User → EC2 → Docker Container → Flask Application

Flask Application interacts with:

* DynamoDB (Users, Files, Audit Logs)
* S3 (Document Storage)

GitHub Actions:

* Builds Docker image
* Pushes image to Docker Hub
* Triggers deployment through AWS SSM

## Technology Stack

### Backend

* Python
* Flask
* Gunicorn

### Cloud

* AWS EC2
* AWS S3
* AWS DynamoDB
* AWS IAM
* AWS Systems Manager

### DevOps

* Docker
* Terraform
* GitHub Actions
* Docker Hub

## Deployment Workflow

1. Developer pushes code to GitHub
2. GitHub Actions builds Docker image
3. Image pushed to Docker Hub
4. GitHub Actions finds EC2 instance by tag
5. AWS SSM sends deployment command
6. EC2 pulls latest image
7. Existing container replaced
8. New version becomes available automatically

## Public URL

http://3.108.219.132

## Future Improvements

* Custom Domain
* HTTPS using Let's Encrypt
* Nginx Reverse Proxy
* Application Load Balancer
* CloudWatch Monitoring
* Kubernetes (EKS)
* GitOps using ArgoCD
