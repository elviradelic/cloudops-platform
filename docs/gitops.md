# GitOps Deployment with Argo CD

## Overview

CloudOps Platform uses Argo CD to manage Kubernetes application deployments through GitOps principles.

The GitHub repository serves as the source of truth for Kubernetes manifests, while Argo CD monitors the repository and synchronizes the desired configuration with the cluster.

## Architecture

The GitOps workflow consists of:

1. **GitHub** - Stores version-controlled Kubernetes manifests.
2. **Kustomize** - Organizes and builds Kubernetes configurations.
3. **Argo CD** - Detects configuration changes and synchronizes cluster resources.
4. **Sealed Secrets** - Enables encrypted Kubernetes Secrets to be stored in Git.
5. **Kubernetes** - Runs the FastAPI backend and PostgreSQL database.

## Repository Structure

```text
cloudops-platform/
├── gitops/
│   └── cloudops-application.yaml
├── k8s/
│   ├── kustomization.yaml
│   ├── sealed-secret.yaml
│   ├── backend-deployment.yaml
│   ├── postgres-deployment.yaml
│   └── ...
└── docs/
    └── gitops.md
```

## Deployment Workflow

1. Kubernetes configuration changes are committed and pushed to the `main` branch.
2. Argo CD detects differences between Git and the running cluster.
3. The application enters the `OutOfSync` state.
4. An operator reviews the differences and initiates synchronization.
5. Argo CD applies the desired Kubernetes configuration.
6. The application returns to `Synced` when the cluster matches Git.

Automatic synchronization is currently disabled to allow manual review before deployment.

## Secrets Management

Sensitive application credentials are managed using Bitnami Sealed Secrets.

The original Kubernetes Secret is excluded from Git using `.gitignore`.

The encrypted `k8s/sealed-secret.yaml` manifest contains the encrypted `DB_PASSWORD` and `POSTGRES_PASSWORD` fields.

The Sealed Secrets controller decrypts these values inside the Kubernetes cluster and manages the corresponding `cloudops-secret`.

The controller's private key must be securely backed up to support disaster recovery. The encrypted manifest alone cannot restore the original credentials if the required private key is lost.

## Validation

The GitOps integration has been tested through:

- Detecting a GitHub configuration change.
- Observing Argo CD transition to `OutOfSync`.
- Performing successful manual synchronization.
- Validating SealedSecret decryption.
- Confirming Kubernetes Secret ownership.
- Verifying backend and PostgreSQL availability.

## Current Environment

The application is deployed and tested on a local Kubernetes cluster using Docker Desktop.

Terraform definitions for AWS infrastructure are maintained separately. AWS resources have not been provisioned as part of this GitOps implementation.