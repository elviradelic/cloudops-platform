
# CI/CD Workflow

## Overview

CloudOps Platform uses GitHub Actions for continuous integration and GitHub Container Registry (GHCR) for container image distribution.

Kubernetes deployments are managed through Argo CD using a GitOps workflow.

## Continuous Integration

The CI pipeline runs on pushes and pull requests targeting the `main` branch.

The pipeline performs:

1. Python dependency installation
2. Automated backend tests using Pytest
3. FastAPI application import verification
4. Docker image build
5. Container vulnerability scanning using Trivy

Trivy reports HIGH and CRITICAL vulnerabilities. The scan is currently informational and does not block the pipeline.

## Container Registry

Successful pushes to `main` publish Docker images to GitHub Container Registry.

Images are tagged using the Git commit SHA and `latest`.

## Branch Protection

The `main` branch uses branch protection rules requiring pull requests and successful CI checks before merging.

Feature development takes place in separate branches.

## GitOps Deployment

Argo CD monitors Kubernetes manifests stored in the repository.

Deployment changes are reviewed before manual synchronization.

Automatic synchronization is currently disabled.

## Deployment Process

1. Create a feature branch.
2. Implement and commit changes.
3. Open a pull request targeting `main`.
4. Wait for CI checks to complete.
5. Merge the pull request when permitted.
6. Review any deployment configuration changes in Argo CD.
7. Manually synchronize the application when required.
8. Verify application health and Kubernetes resources.
