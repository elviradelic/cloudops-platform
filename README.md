# CloudOps Platform

CloudOps Platform is a hands-on DevOps project built around deploying and operating a containerized application in a Kubernetes environment.

The project started with a simple FastAPI backend and PostgreSQL database and is being expanded step by step with the tools typically used in DevOps and cloud environments.

The current setup includes Docker, Kubernetes, autoscaling, Prometheus and Grafana. The next stages will introduce AWS infrastructure, Terraform, CI/CD, GitOps and additional security and observability tooling.

## Architecture

The project is being developed toward the following architecture:

```text
                         GitHub
                            |
                     GitHub Actions
                            |
                         Trivy
                            |
                           ECR
                            |
                         Argo CD
                            |
                           EKS
                    /       |       \
               Backend   Frontend   Monitoring
                  |                    |
                 RDS             Prometheus
                                      |
                                    Grafana
                                      |
                                     Loki

Infrastructure provisioning: Terraform
Cloud platform: AWS
```

## Tech Stack

**Application**
- FastAPI
- PostgreSQL
- Python

**Containers & Orchestration**
- Docker
- Docker Compose
- Kubernetes
- Horizontal Pod Autoscaler
- Ingress

**Monitoring**
- Prometheus
- Grafana

**Planned Cloud & DevOps Tooling**
- AWS
- Amazon EKS
- Amazon ECR
- Amazon RDS
- Terraform
- GitHub Actions
- Argo CD
- Loki
- Trivy

## Current Progress

The application can run locally with Docker Compose and has also been deployed to a local Kubernetes cluster.

The Kubernetes setup currently includes separate backend and PostgreSQL workloads, Services, ConfigMaps, Secrets, persistent storage, health checks and resource configuration.

The backend runs with multiple replicas and uses Horizontal Pod Autoscaling to adjust the number of pods based on resource usage.

Monitoring has also been added. The backend exposes application metrics that are collected by Prometheus through a ServiceMonitor.

Grafana is used to visualize the collected metrics.

The current dashboard tracks:

- backend request rate
- HTTP requests by status
- backend CPU usage
- backend memory usage
- backend replica count
- HPA current replicas
- HPA desired replicas

The exported Grafana dashboard is stored in:

```text
monitoring/grafana-dashboard.json
```

## Project Structure

```text
cloudops-platform/
├── backend/
├── frontend/
├── k8s/
├── monitoring/
├── docs/
├── compose.yaml
├── .env.example
└── README.md
```

`backend/` contains the FastAPI application.

`k8s/` contains Kubernetes manifests for the application, database, networking, autoscaling and monitoring integration.

`monitoring/` contains Prometheus configuration and the exported Grafana dashboard.

## Running Locally

Clone the repository:

```bash
git clone https://github.com/elviradelic/cloudops-platform.git
cd cloudops-platform
```

Create the environment file:

```bash
cp .env.example .env
```

Then start the application:

```bash
docker compose up --build
```

The backend API is available at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

## Kubernetes

Kubernetes manifests are located in the `k8s` directory.

Apply the configuration:

```bash
kubectl apply -f k8s/
```

Check the application pods:

```bash
kubectl get pods -n cloudops
```

Check services:

```bash
kubectl get services -n cloudops
```

Check the Horizontal Pod Autoscaler:

```bash
kubectl get hpa -n cloudops
```

## Monitoring

Prometheus and Grafana are used to monitor the application and Kubernetes resources.

Application metrics are exposed by the FastAPI backend and discovered by Prometheus using:

```text
k8s/service-monitor.yaml
```

The Grafana dashboard configuration is stored in:

```text
monitoring/grafana-dashboard.json
```

Prometheus configuration values are stored in:

```text
monitoring/values.yaml
```

## Roadmap

The project is still in development.

Next steps include:

- CI/CD pipeline with GitHub Actions
- AWS infrastructure
- Infrastructure as Code with Terraform
- Kubernetes deployment on Amazon EKS
- container images stored in Amazon ECR
- PostgreSQL migration to Amazon RDS
- GitOps deployment with Argo CD
- centralized logging with Loki
- container vulnerability scanning with Trivy
- additional Kubernetes security controls

The README will be updated as these parts are implemented.
