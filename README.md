# CloudOps Platform

CloudOps Platform is a hands-on DevOps project focused on containerization, Kubernetes orchestration, CI/CD automation, infrastructure management, monitoring, and GitOps.

The application consists of a FastAPI backend and PostgreSQL database, deployed using Docker and Kubernetes.

The project integrates GitHub Actions, GitHub Container Registry (GHCR), Trivy, Prometheus, Grafana, Argo CD, and Bitnami Sealed Secrets.

Development, deployment, and infrastructure testing are performed primarily in a local Kubernetes environment. AWS infrastructure is defined using Terraform but has not been provisioned.

## Architecture

### Local Kubernetes Environment

```text
                  GitHub Repository
                         |
                   GitHub Actions
                         |
                  Tests + Docker Build
                         |
                    Trivy Scan
                         |
                GitHub Container Registry
                         |
                 Versioned Docker Image
                         |
              Kubernetes Image Reference
                         |
                       Argo CD
                  (Manual GitOps Sync)
                         |
                  Local Kubernetes
                    /          \
             FastAPI Backend   PostgreSQL
               (2 replicas)       |
                    |        Persistent Volume
               API Metrics
                    |
                Prometheus
                    |
                  Grafana

GitHub -> Argo CD -> Sealed Secrets -> Kubernetes Secret
```

GitHub Actions handles application testing, container image builds, vulnerability scanning, and publishing to GHCR.

Argo CD monitors Kubernetes configuration stored in GitHub, detects differences between the desired and actual cluster state, and manages application synchronization.

Bitnami Sealed Secrets enables encrypted application credentials to be stored in Git and decrypted within the Kubernetes cluster.

The GitOps workflow currently uses manual synchronization, allowing deployment changes to be reviewed before they are applied.

### AWS Infrastructure

Terraform configurations define a proposed AWS deployment environment, including:

- Virtual Private Cloud (VPC)
- Public subnets and networking resources
- Amazon Elastic Container Registry (ECR)
- Amazon Elastic Kubernetes Service (EKS)
- IAM roles and permissions
- EKS managed node group

The Terraform configuration has been formatted and validated locally. No AWS resources have been provisioned.

## Tech Stack

**Application**
- Python
- FastAPI
- PostgreSQL

**Containers & Orchestration**
- Docker
- Docker Compose
- Kubernetes
- Kustomize
- Horizontal Pod Autoscaler
- Ingress

**CI/CD & Security**
- GitHub Actions
- GitHub Container Registry (GHCR)
- Pytest
- Trivy
- Bitnami Sealed Secrets

**GitOps**
- Argo CD

**Monitoring**
- Prometheus
- Grafana
- Prometheus FastAPI Instrumentator

**Infrastructure as Code**
- Terraform
- AWS infrastructure definitions (ECR, EKS, VPC, IAM)

## Implemented Features

### Application and Containerization

The FastAPI backend provides REST API endpoints, application health checks, database connectivity checks, and Prometheus-compatible metrics.

Docker is used to package the backend application, while Docker Compose provides a local development environment.

### Kubernetes Deployment

The local Kubernetes deployment includes:

- FastAPI backend with two replicas
- PostgreSQL database deployment
- Kubernetes Services
- ConfigMaps and Secrets
- PersistentVolumeClaim for PostgreSQL
- Readiness and liveness probes
- Horizontal Pod Autoscaler
- Ingress configuration
- Versioned container images from GHCR

Kustomize organizes the Kubernetes manifests consumed by Argo CD.

The deployment has been tested successfully with two running backend replicas and a healthy application status.

### Continuous Integration and Container Registry

GitHub Actions runs automated CI workflows when changes are pushed to or proposed for the `main` branch.

The CI workflow includes:

1. Python environment setup
2. Dependency installation
3. Automated tests with Pytest
4. Application import verification
5. Docker image build
6. Container vulnerability scanning with Trivy

Trivy scans for HIGH and CRITICAL vulnerabilities. The scan is currently informational and does not block the pipeline.

Backend container images are also published to GitHub Container Registry (GHCR) through the project's container publishing workflow.

Container images are versioned using Git commit identifiers, enabling specific application builds to be referenced by Kubernetes manifests.

**Container registry:**

```text
ghcr.io/elviradelic/cloudops-platform/cloudops-backend
```

The local Kubernetes deployment has been successfully updated to use a commit-specific image published to GHCR.

### Monitoring

Prometheus collects application metrics exposed by the FastAPI backend.

Grafana provides dashboards for monitoring application and Kubernetes performance.

The exported dashboard includes:

- Backend request rate
- HTTP requests by status
- Backend CPU and memory usage
- Backend replica count
- HPA current and desired replicas

Dashboard configuration:

```text
monitoring/grafana-dashboard.json
```

### GitOps with Argo CD

Argo CD manages the Kubernetes application configuration from the GitHub repository.

The GitOps workflow follows these steps:

1. Application changes are committed and pushed to GitHub.
2. GitHub Actions builds and tests the application.
3. A Docker image is published to GHCR.
4. The Kubernetes Deployment manifest is updated to reference the new image version.
5. Argo CD detects the configuration change and reports an OutOfSync state.
6. The configuration difference is reviewed before synchronization.
7. Argo CD applies the updated Kubernetes configuration.
8. Deployment health and application availability are verified.

This workflow has been tested successfully, including deployment of a GHCR-hosted backend image to the local Kubernetes cluster.

The resulting deployment was verified with:

- Successful Argo CD synchronization
- Healthy application status
- Two available backend replicas
- Both backend Pods running the expected GHCR image
- Successful API health check

Automatic synchronization is currently disabled.

Argo CD Application configuration:

```text
gitops/cloudops-application.yaml
```

### Secrets Management

Bitnami Sealed Secrets is used to manage encrypted application credentials.

The encrypted manifest is stored in:

```text
k8s/sealed-secret.yaml
```

The original plaintext Kubernetes Secret manifest is excluded from Git.

The Sealed Secrets controller has been tested successfully, including decryption, synchronization, and ownership of the generated Kubernetes Secret.

## Project Structure

```text
cloudops-platform/
├── backend/
├── frontend/
├── k8s/
│   ├── kustomization.yaml
│   └── sealed-secret.yaml
├── gitops/
│   └── cloudops-application.yaml
├── monitoring/
├── terraform/
├── docs/
│   ├── gitops.md
│   └── disaster-recovery.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── compose.yaml
├── .env.example
└── README.md
```

## Running Locally

Clone the repository:

```bash
git clone https://github.com/elviradelic/cloudops-platform.git
cd cloudops-platform
```

Create an environment configuration file using `.env.example` as a template.

Start the application:

```bash
docker compose up --build
```

The backend is accessible at:

```text
http://localhost:8000
```

FastAPI API documentation:

```text
http://localhost:8000/docs
```

## Kubernetes and GitOps

The Kubernetes manifests are stored in `k8s/`.

To inspect the generated Kustomize configuration:

```bash
kubectl kustomize ./k8s
```

To inspect the local deployment:

```bash
kubectl get pods -n cloudops
kubectl get deployments -n cloudops
kubectl get services -n cloudops
kubectl get hpa -n cloudops
```

To inspect the Argo CD application:

```bash
kubectl get application cloudops-platform -n argocd
```

To verify the backend container image:

```bash
kubectl get deployment backend -n cloudops -o jsonpath="{.spec.template.spec.containers[0].image}"
```

Argo CD manages synchronization between GitHub and the local Kubernetes cluster.

The Sealed Secrets controller must be installed and configured with the appropriate encryption keys before restoring encrypted application credentials.

## Documentation

Additional technical documentation is available in:

- [GitOps Deployment](docs/gitops.md)
- [Disaster Recovery](docs/disaster-recovery.md)

## Roadmap

The following improvements are planned:

- Automated GitOps synchronization with appropriate safety controls
- Automated container image updates in Kubernetes manifests
- Improved image versioning and release management
- Centralized logging with Loki
- Additional Kubernetes security controls
- PostgreSQL backup automation
- Disaster recovery testing
- Further CI/CD improvements

AWS deployment remains a future option. Terraform configurations are maintained and validated without provisioning paid cloud resources.

## Project Status

The following components have been implemented and tested:

- Containerized FastAPI and PostgreSQL application
- Local Kubernetes deployment
- Monitoring with Prometheus and Grafana
- Automated CI testing and Docker builds
- Container vulnerability scanning with Trivy
- Container image publishing to GHCR
- GitOps deployment management with Argo CD
- Deployment of versioned GHCR images to Kubernetes
- Encrypted secrets management with Bitnami Sealed Secrets

Terraform-based AWS infrastructure definitions have been validated locally but not deployed.

The project remains under active development.