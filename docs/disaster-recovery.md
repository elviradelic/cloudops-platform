# Disaster Recovery - CloudOps Platform

## Overview

This document describes backup and recovery procedures for the CloudOps Platform GitOps environment.

The primary objective is to restore Kubernetes application configuration and encrypted secrets after cluster failure or recreation.

## Recovery Components

The recovery process depends on the following components:

- **GitHub:** Version-controlled Kubernetes manifests and Argo CD application configuration.
- **Argo CD:** Restores the desired Kubernetes application configuration.
- **Sealed Secrets:** Decrypts encrypted secrets using the controller's private key.
- **PostgreSQL:** Requires a separate database backup and restoration strategy.

## Sealed Secrets Key Backup

The Sealed Secrets controller maintains private encryption keys as Kubernetes Secrets in the controller namespace.

These keys must be backed up securely because the encrypted manifests in Git cannot be decrypted without the corresponding private keys.

Example backup command:

```powershell
kubectl get secret -n kube-system -l sealedsecrets.bitnami.com/sealed-secrets-key -o yaml > sealed-secrets-keys-backup.yaml
```

The resulting file contains sensitive private key material and must never be committed to Git.

Store the backup in a secure, encrypted location with restricted access.

## Recovery Procedure

1. Restore or recreate the Kubernetes cluster.
2. Install the Sealed Secrets controller.
3. Restore the backed-up Sealed Secrets encryption keys into the controller namespace.
4. Verify that the controller recognizes the restored keys.
5. Install and configure Argo CD.
6. Restore the CloudOps Platform Argo CD Application.
7. Synchronize Kubernetes manifests from GitHub.
8. Verify that the SealedSecret is decrypted successfully.
9. Restore PostgreSQL data from a separate database backup if required.
10. Validate application health and database connectivity.

## Security Considerations

- Never commit plaintext Kubernetes Secrets or private encryption keys.
- Protect backups using encryption and restricted access.
- Retain previous encryption keys when rotating keys.
- Test recovery procedures in an isolated environment.
- Keep database backups separate from GitOps configuration backups.

## Current Implementation Status

The GitOps deployment and Sealed Secrets integration have been validated on a local Kubernetes cluster.

The disaster recovery procedure is documented but has not yet been tested end-to-end.

PostgreSQL backup automation and full cluster recovery testing remain future improvements.