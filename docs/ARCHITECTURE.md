# Architecture Document

## Overview

Document Platform is a cloud-native document management system designed to demonstrate modern DevOps, Infrastructure-as-Code, and AWS deployment practices.

The platform enables users to securely upload, download, preview, and share documents while maintaining metadata and audit information within AWS-managed services.

---

# Architectural Goals

The system was designed with the following goals:

- Infrastructure as Code
- Immutable Deployments
- Cloud-Native Storage
- Automated CI/CD
- Secure Remote Administration
- Separation of Concerns
- Minimal Operational Overhead

---

# System Architecture

The architecture can be viewed from four perspectives:

1. Runtime Infrastructure
2. AWS Infrastructure
3. Application Architecture
4. CI/CD Deployment Pipeline

---

# Runtime Infrastructure

![Runtime Infrastructure](screenshots/runtime-infrastructure.png)

## Request Flow

User Browser
→ Amazon EC2
→ Docker Engine
→ Docker Container
→ Gunicorn
→ Flask Application

Flask Application
→ DynamoDB

Flask Application
→ Amazon S3

---

## Component Responsibilities

### Amazon EC2

Provides the compute environment that hosts the application.

### Docker Engine

Runs the application inside a containerized environment.

### Docker Container

Contains all application dependencies and runtime configuration.

### Gunicorn

Acts as the WSGI server responsible for serving Flask requests.

### Flask Application

Handles business logic, routing, authentication, authorization, and document management.

### DynamoDB

Stores:

- User Accounts
- File Metadata
- Audit Logs

### Amazon S3

Stores uploaded documents.

---

# AWS Infrastructure

![AWS Infrastructure](screenshots/aws-infrastructure.png)

## Provisioned Resources

Terraform provisions and manages:

### Compute

- Amazon EC2

### Storage

- Amazon S3

### Database

- DynamoDB Users Table
- DynamoDB Files Table
- DynamoDB Audit Logs Table

### Security

- IAM Roles
- Security Groups

### Operations

- AWS Systems Manager

---

# Security Architecture

## Security Group

Only HTTP traffic is exposed publicly.

SSH access is not required.

### Benefits

- Reduced attack surface
- Simplified administration
- SSM-based management

---

## IAM Roles

The EC2 instance receives permissions through IAM roles rather than embedded credentials.

This allows:

- Secure S3 access
- Secure DynamoDB access
- Secure SSM integration

without storing AWS access keys on the server.

---

# Application Architecture

![Application Architecture](screenshots/application-architecture.png)

The application follows a layered architecture.

---

## Entry Point

### app.py

Responsible for:

- Flask initialization
- Blueprint registration
- Configuration loading
- AWS client initialization

---

## Routes Layer

### auth_routes.py

Handles:

- Login
- Logout
- Authentication workflows

### dashboard_routes.py

Handles:

- Dashboard rendering
- Navigation

### file_routes.py

Handles:

- Upload
- Download
- Preview
- Share
- Delete operations

---

## Services Layer

Business logic is isolated from HTTP routes.

### auth_service.py

Responsible for:

- Credential validation
- Session management
- Role validation

### file_service.py

Responsible for:

- File operations
- Metadata coordination

### audit_service.py

Responsible for:

- Activity tracking
- Audit log creation

### dynamodb_service.py

Responsible for:

- DynamoDB interactions

### s3_service.py

Responsible for:

- S3 uploads
- Downloads
- Presigned URL generation

---

## Models Layer

### user.py

Represents:

- Username
- Role
- Department

### file.py

Represents:

- File ID
- Filename
- Department
- Owner
- Metadata

---

# CI/CD Architecture

![CI/CD Pipeline](screenshots/CICD-pipeline.png)

The deployment pipeline follows an automated push-based workflow.

---

## Deployment Flow

Developer
→ Git Push
→ GitHub Repository
→ GitHub Actions
→ Docker Build
→ Docker Hub
→ AWS Systems Manager
→ EC2
→ Container Restart

---

## GitHub Actions Responsibilities

### Build Stage

- Checkout repository
- Build Docker image

### Registry Stage

- Push image to Docker Hub

### Deployment Stage

- Discover EC2 instance by tag
- Execute deployment through AWS SSM

---

## Deployment Strategy

Current deployment strategy:

### Rolling Container Replacement

1. Pull latest image
2. Stop running container
3. Remove container
4. Start new container

Advantages:

- Simple
- Reproducible
- Minimal operational complexity

---

# Design Decisions

## Why Terraform?

Terraform provides:

- Repeatable infrastructure
- Version-controlled changes
- Automated provisioning

---

## Why Docker?

Docker provides:

- Environment consistency
- Portable deployments
- Dependency isolation

---

## Why DynamoDB?

DynamoDB was chosen because:

- Fully managed
- Highly scalable
- No server maintenance

---

## Why Amazon S3?

Amazon S3 provides:

- Durable object storage
- Cost efficiency
- Presigned URL support

---

## Why AWS Systems Manager?

SSM eliminates the need for:

- Public SSH ports
- PEM key distribution
- Manual server administration

---

## Why GitHub Actions?

GitHub Actions provides:

- Native Git integration
- Automated deployments
- CI/CD workflow automation

---

# Future Architecture Evolution

## Version 1.1

Planned improvements:

- HTTPS
- Custom Domain
- Nginx Reverse Proxy
- CloudWatch Monitoring

---

## Version 1.2

Planned improvements:

- Application Load Balancer
- Auto Scaling Group

---

## Version 2.0

Long-term roadmap:

- Kubernetes (EKS)
- Helm Charts
- ArgoCD
- GitOps Workflows
- Blue/Green Deployments

---

# Conclusion

This project demonstrates a complete cloud-native application lifecycle:

Infrastructure Provisioning
→ Containerization
→ CI/CD Automation
→ Cloud Deployment
→ Secure Operations

while maintaining a clean separation between infrastructure, application logic, and deployment workflows.
