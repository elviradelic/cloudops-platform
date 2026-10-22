# CloudOps Platform

CloudOps Platform is a hands-on DevOps project focused on building, deploying, monitoring, and managing a containerized application using modern infrastructure and automation tools.

The project uses a FastAPI backend and PostgreSQL database as the application layer, with Docker and Kubernetes handling containerization and orchestration.

The platform has been expanded with CI, container security scanning, monitoring, Infrastructure as Code, and GitOps deployment management.

Development and deployment testing are performed primarily in a local Kubernetes environment. AWS infrastructure is defined using Terraform but has not been provisioned.

## Architecture

### Local Kubernetes Environment

```text
                   GitHub Repository
                          |
                   GitHub Actions
                    CI + Testing
                    Docker Build
                    Trivy Scanning
                          |
                    Kubernetes
                    Manifests
                          |
                       Argo CD
                          |
                 Local Kubernetes
                  /             \
           FastAPI Backend    PostgreSQL
                  |             |
             API Metrics    Persistent Volume
                  |
              Prometheus
                  |
               Grafana

GitHub -> Argo CD -> Sealed Secrets -> Kubernetes Secret
```

Argo CD monitors Kubernetes configuration stored in GitHub and detects differences between the repository and the running cluster.

Sealed Secrets enables encrypted application credentials to be stored in Git and decrypted inside the Kubernetes cluster.

The current GitOps workflow uses manual synchronization to allow changes to be reviewed before deployment.

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

**CI & Security**
- GitHub Actions
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

The backend provides REST API endpoints, application health checks, database connectivity checks, and Prometheus-compatible metrics.

Docker is used to package the backend application, while Docker Compose provides a local development environment.

### Kubernetes Deployment

The local Kubernetes deployment includes:

- FastAPI backend with multiple replicas
- PostgreSQL database deployment
- Kubernetes Services
- ConfigMaps and Secrets
- PersistentVolumeClaim for PostgreSQL
- Readiness checks
- Horizontal Pod Autoscaler
- Ingress configuration

Kustomize is used to organize the Kubernetes manifests consumed by Argo CD.

### Continuous Integration

GitHub Actions runs a CI workflow when changes are pushed to or proposed for the `main` branch.

The workflow includes:

1. Python environment setup
2. Dependency installation
3. Automated tests with Pytest
4. Application import verification
5. Docker image build
6. Container vulnerability scanning with Trivy

Trivy reports HIGH and CRITICAL vulnerabilities. The current scan is informational and does not block the pipeline.

Container images are built during CI but are not currently published to a remote registry.

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

The GitOps workflow has been tested by:

1. Updating a Kubernetes manifest
2. Committing and pushing the change to GitHub
3. Detecting an OutOfSync state in Argo CD
4. Reviewing the configuration difference
5. Performing a manual synchronization
6. Verifying the updated Kubernetes resource

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
kubectl get services -n cloudops
kubectl get hpa -n cloudops
```

Argo CD is used to manage synchronization between GitHub and the local Kubernetes cluster.

The Sealed Secrets controller must be installed and configured with the appropriate encryption keys before restoring encrypted application credentials.

## Documentation

Additional technical documentation is available in:

- [GitOps Deployment](docs/gitops.md)
- [Disaster Recovery](docs/disaster-recovery.md)

## Roadmap

The following improvements are planned:

- Automated GitOps synchronization with appropriate safety controls
- Container image publishing to a registry
- Improved image versioning and deployment automation
- Centralized logging with Loki
- Additional Kubernetes security controls
- PostgreSQL backup automation
- Disaster recovery testing
- Further CI/CD improvements

AWS deployment remains a future option. Terraform configurations are maintained and validated without provisioning paid cloud resources.

## Project Status

The local Kubernetes deployment, monitoring stack, CI pipeline, GitOps workflow, and Sealed Secrets integration have been implemented and tested.

Terraform-based AWS infrastructure definitions have been validated locally but not deployed.

The project remains under active development.