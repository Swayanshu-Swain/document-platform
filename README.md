# Document Platform

A cloud-native document management platform built with AWS, Terraform, Docker, and GitHub Actions.

This project demonstrates the complete software delivery lifecycle, from infrastructure provisioning and containerized deployment to automated CI/CD and cloud-native document storage.

The platform provides secure document storage, retrieval, sharing, and metadata management while showcasing modern DevOps and Infrastructure-as-Code practices.

---

## Project Highlights

### Cloud Infrastructure
- Infrastructure provisioning using Terraform
- Amazon EC2 compute layer
- Amazon DynamoDB for metadata and authentication
- Amazon S3 for document storage
- IAM-based access management
- AWS Systems Manager (SSM) for remote administration

### Application Features
- User authentication
- Role-based authorization
- Document upload
- Document download
- File sharing
- File preview
- Audit logging

### DevOps & Automation
- Dockerized application deployment
- GitHub Actions CI/CD pipeline
- Docker Hub image registry
- Automated deployment via AWS SSM
- Infrastructure as Code (IaC)

---

# Architecture

The project architecture is documented using four different perspectives.

---

## 1. Runtime Infrastructure

This diagram shows how requests flow through the deployed runtime environment.

![Runtime Infrastructure](docs/screenshots/runtime-infrastructure.png)

### Request Flow

```text
Browser
    ↓
Amazon EC2
    ↓
Docker Engine
    ↓
Docker Container
    ↓
Gunicorn
    ↓
Flask Application
    ↓
DynamoDB / S3
```

Responsibilities:

| Component | Purpose |
|------------|----------|
| Browser | User interface |
| EC2 | Compute infrastructure |
| Docker Engine | Container runtime |
| Docker Container | Application environment |
| Gunicorn | WSGI application server |
| Flask | Backend application |
| DynamoDB | Metadata and authentication storage |
| S3 | Document storage |

---

## 2. AWS Infrastructure

This diagram illustrates the AWS resources provisioned and managed through Terraform.

![AWS Infrastructure](docs/screenshots/aws-infrastructure.png)

Provisioned Resources:

- Amazon EC2
- Amazon DynamoDB
- Amazon S3
- IAM Roles
- Security Groups
- AWS Systems Manager

Infrastructure provisioning is fully automated through Terraform.

---

## 3. Application Architecture

This diagram represents the internal structure of the Flask application.

![Application Architecture](docs/screenshots/application-infrastructure.png)

### Layered Design

```text
app.py
   │
Routes
   │
Services
   │
Models
   │
AWS Resources
```

### Route Layer

- auth_routes.py
- dashboard_routes.py
- file_routes.py

### Service Layer

- auth_service.py
- file_service.py
- audit_service.py
- dynamodb_service.py
- s3_service.py

### Model Layer

- user.py
- file.py

---

## 4. CI/CD Deployment Pipeline

This diagram demonstrates the automated deployment workflow.

![CI/CD Pipeline](docs/screenshots/CICD-pipeline.png)

### Deployment Flow

```text
Developer
    ↓
Git Push
    ↓
GitHub Repository
    ↓
GitHub Actions
    ↓
Docker Build
    ↓
Docker Hub
    ↓
AWS Systems Manager
    ↓
Amazon EC2
    ↓
Docker Container Restart
```

Deployment occurs automatically whenever changes are pushed to the main branch.

---

# Technology Stack

## Backend

- Python
- Flask
- Gunicorn

## Cloud Services

- Amazon EC2
- Amazon S3
- Amazon DynamoDB
- AWS IAM
- AWS Systems Manager

## DevOps

- Docker
- Docker Hub
- GitHub Actions
- Terraform

## Version Control

- Git
- GitHub

---

# Design Decisions

## Why Terraform?

Terraform enables reproducible infrastructure provisioning and eliminates manual resource configuration.

## Why Docker?

Docker ensures environment consistency between development and deployment environments.

## Why DynamoDB?

DynamoDB provides a managed, scalable NoSQL datastore ideal for metadata and user management.

## Why Amazon S3?

S3 offers highly durable and cost-effective object storage for documents.

## Why AWS Systems Manager Instead of SSH?

SSM allows secure remote administration without exposing SSH ports to the public internet.

## Why GitHub Actions?

GitHub Actions provides seamless CI/CD integration directly from the source repository.

---

# Project Structure

```text
document-platform/
│
├── backend/
│   ├── auth/
│   ├── config/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   ├── utils/
│   ├── app.py
│   └── Dockerfile
│
├── terraform/
│   ├── bootstrap/
│   └── infrastructure/
│
├── docs/
│   └── screenshots/
│
├── .github/
│   └── workflows/
│
├── README.md
└── .gitignore
```

---

# Screenshots

## Login Page

![Login](docs/screenshots/login-page.png)

---

## Application Dashboard

![Application Dashboard](docs/screenshots/application-home.png)

---

## GitHub Actions Deployment

![GitHub Actions](docs/screenshots/github-actions.png)

---

## Docker Runtime

![Docker Runtime](docs/screenshots/docker-container.png)

---

## Amazon DynamoDB

![DynamoDB](docs/screenshots/dynamodb-tables.png)

---

## Amazon S3

![Amazon S3](docs/screenshots/s3-buckets.png)

---

## Amazon EC2

![Amazon EC2](docs/screenshots/ec2-instance.png)

---

# Infrastructure Components

| Service | Responsibility |
|----------|---------------|
| EC2 | Hosts application runtime |
| Docker | Container execution |
| Gunicorn | Application server |
| Flask | Business logic |
| DynamoDB | Metadata storage |
| S3 | Document storage |
| IAM | Access management |
| SSM | Remote administration |
| GitHub Actions | CI/CD |
| Docker Hub | Image registry |
| Terraform | Infrastructure provisioning |

---

# Deployment

Infrastructure provisioning:

```bash
terraform init
terraform plan
terraform apply
```

Application deployment:

```text
Git Push
    ↓
GitHub Actions
    ↓
Docker Build
    ↓
Docker Hub
    ↓
AWS SSM
    ↓
EC2 Deployment
```

No manual server access is required during deployment.

---

# Future Enhancements

### Infrastructure

- Custom Domain
- HTTPS (TLS/SSL)
- Nginx Reverse Proxy
- CloudWatch Monitoring
- CloudWatch Alarms
- Application Load Balancer
- Auto Scaling

### Platform Features

- User Management Dashboard
- Audit Log Dashboard
- File Versioning
- Department-Based Access Controls
- Advanced Search

### Platform Engineering

- Kubernetes (EKS)
- Helm Charts
- ArgoCD GitOps
- Blue-Green Deployments

---

# Author

**Swayanshu Swain**

B.Tech Computer Science & Engineering  
Silicon University, Bhubaneswar

---

## License

This project is intended for educational, portfolio, and learning purposes.
