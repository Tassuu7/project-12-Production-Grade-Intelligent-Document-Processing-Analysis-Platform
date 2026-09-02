# Platform Security Architecture & Compliance

## Security Architecture Highlights
1. **Zero External Data Transmission**: All NLP and ML processing runs strictly locally.
2. **Cryptographic Integrity**: SHA-256 checksums on all uploaded and generated assets.
3. **Strict RBAC**:
   - `User`: Isolated document uploads, search, analysis viewing, and report downloads.
   - `Admin`: Global user directory, document explorer, job monitor, audit logs, and telemetry.
4. **Immutable Audit Trail**: Every authentication event, upload, download, and reprocess operation is recorded in `audit_logs` table.
5. **No Prohibited Open-Source Licenses**: Pure proprietary enterprise software.
6. **No API Keys or Secrets in Codebase**: Zero hardcoded secrets, API tokens, or external credentials.
