# Bhasha2Code — Production Deployment

## Phase 17 — Production

**Project:** Bhasha2Code  
**Phase:** 17 — Production  
**Version:** 1.0  
**Status:** COMPLETE  
**Primary Deployment Target:** Local Machine / Localhost  
**Deployment Model:** Local-first, Offline-capable  
**Primary AI Runtime:** Ollama + Local Coding Model  
**Execution Runtime:** Docker Sandbox

---

# 1. Purpose

This document defines how the validated Bhasha2Code application is packaged, configured, started, backed up, recovered, and maintained as a local production application.

The first production target is:

```text id="p7n2m5"
User Machine
    ↓
Localhost
    ↓
Bhasha2Code
```

Public/cloud deployment is not part of the initial production gate.

---

# 2. Production Philosophy

Production means:

```text id="x4m8q1"
Stable
+
Predictable
+
Recoverable
+
Secure
+
Configured
+
Tested
```

Production does NOT mean:

```text id="r2v7c5"
Perfect
```

Known non-critical limitations must be documented.

---

# 3. Production Architecture

```text id="m8c3q7"
                    USER
                      │
                      ▼
              ┌──────────────┐
              │    Browser   │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │ React / Vite │
              │  Frontend    │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │   FastAPI    │
              │   Backend    │
              └──────┬───────┘
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
      NLP         SQLite        Session
       │                           │
       └──────────┬────────────────┘
                  ▼
           Context Manager
                  │
                  ▼
           Prompt Builder
                  │
                  ▼
               Ollama
                  │
                  ▼
          Local Coding Model
                  │
                  ▼
            Output Parser
                  │
          ┌───────┴────────┐
          ▼                ▼
      Validator         Sandbox
                           │
                         Docker
```

---

# 4. Production Components

Production consists of:

```text id="q9m2x7"
Frontend
Backend
SQLite Database
NLP Models
Ollama
Local Coding Model
Docker
Sandbox Configuration
Configuration Files
Export Storage
Logs
Backup Storage
```

---

# 5. Production Environment Separation

Production must not accidentally use development resources.

Separate:

```text id="c7n4m1"
Development
Testing
Preview
Production
```

Examples:

```text id="w2x8q5"
Development DB → data/dev.db
Preview DB     → data/preview.db
Production DB  → data/production.db
```

Actual paths may differ, but the separation must be explicit.

---

# 6. Production Configuration

Create a production environment configuration.

Example:

```text id="m5q1v8"
APP_ENV=production

BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000

OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5-coder:3b-instruct

DATABASE_URL=sqlite:///./data/production.db

MAX_REPAIR_ATTEMPTS=3
```

Production-specific configuration must not be hard-coded inside application logic.

---

# 7. Configuration Rules

Configuration must control:

```text id="x8n3c6"
Model
Ports
Database
Logging
Sandbox
Timeouts
Resource Limits
Feature Flags
Environment
```

Do not scatter configuration across unrelated source files.

---

# 8. Production Secrets

If any future production feature requires credentials:

```text id="q1m7v4"
Secrets
↓
Environment / Secure Secret Store
```

Never:

```text id="n6c2x8"
Commit secrets
Embed secrets in frontend
Store secrets in prompts
Print secrets in logs
```

---

# 9. Production Build

The production process is:

```text id="r4m9c1"
Validated Source
↓
Dependency Installation
↓
Frontend Build
↓
Backend Configuration
↓
Database Initialization
↓
Service Startup
↓
Health Check
↓
Smoke Test
```

---

# 10. Frontend Production Build

Typical build flow:

```bash id="w7x3n5"
cd frontend
npm install
npm run build
```

Expected:

```text id="p2m8q4"
Production frontend artifacts generated.
```

The exact build command must follow the final frontend configuration.

---

# 11. Backend Production Preparation

Activate the project environment:

```bash id="n4c7v1"
source .venv/bin/activate
```

Install the tested dependency set:

```bash id="x8m2q6"
pip install -r backend/requirements.txt
```

Do not casually update packages during the production build.

---

# 12. Dependency Reproducibility

Production should use the dependency versions that were tested during QA.

Maintain:

```text id="c5q9n1"
requirements.txt
package-lock.json
```

where applicable.

Do not introduce a new dependency during final deployment without retesting affected functionality.

---

# 13. Database Production Setup

Production database:

```text id="v7m3q8"
SQLite
```

Initialization must:

```text id="m1x6c4"
Create Database
↓
Create Tables
↓
Apply Required Schema
↓
Verify Database
```

---

# 14. Production Database Safety

Never run destructive database initialization against an existing production database without a migration/recovery plan.

Do not use:

```text id="q8n2v5"
DROP DATABASE
```

or equivalent destructive operation as part of normal startup.

---

# 15. Database Backup

Before significant schema changes:

```text id="r3c7m1"
Production DB
↓
Backup
↓
Change
↓
Verify
```

---

# 16. Database Integrity Check

Periodically verify:

```text id="x5m8q2"
Database Exists
Tables Exist
Sessions Readable
Messages Readable
Notes Readable
Saved Messages Readable
```

---

# 17. Ollama Production Readiness

Production requires:

```text id="m6q1c8"
Ollama Available
+
Configured Model Installed
+
Backend Connection Working
```

The application must detect:

```text id="p9v3n5"
Ollama unavailable
```

without crashing.

---

# 18. Model Configuration

The production model must be explicitly configured.

Example:

```text id="4x7m2n"
OLLAMA_MODEL=qwen2.5-coder:3b-instruct
```

Changing the production model requires:

```text id="c8q1v5"
Compatibility Check
↓
Performance Test
↓
NLP / Context Test
↓
E2E Test
```

---

# 19. Model Startup Behavior

Production startup should avoid unnecessary repeated model operations.

Preferred:

```text id="n5m7c3"
Application Start
↓
Check Ollama
↓
Check Model
↓
Ready
```

Do not repeatedly reload the model for every user request.

---

# 20. Localhost Binding

Because the initial target is local production:

```text id="q2x8m4"
127.0.0.1
```

should be preferred where remote access is not required.

This minimizes unnecessary network exposure.

---

# 21. Remote Access

Remote access is not required for V1.

If enabled later, it must receive a separate:

```text id="m7c3n1"
Network Security Review
+
Authentication Review
+
Authorization Review
+
TLS Review
```

---

# 22. Production Sandbox

The production execution environment must use the reviewed Docker sandbox.

Required controls:

```text id="x4n8q2"
Non-root
No Network
Resource Limits
Timeout
Restricted Filesystem
Controlled Workspace
No Docker Socket
No Privileged Mode
```

---

# 23. Sandbox Failure Rule

If Docker is unavailable:

```text id="p5m1c8"
Code Execution
     ↓
DISABLED
```

Do NOT fallback to host execution.

---

# 24. Sandbox Startup

The application should not keep unnecessary containers running.

Preferred:

```text id="r8n3m6"
Request
↓
Create / Start Restricted Container
↓
Execute
↓
Capture Output
↓
Stop / Remove
```

The exact lifecycle may be optimized later.

---

# 25. Production Logging

Production logs should provide:

```text id="c2m7x5"
Errors
Warnings
Service Events
Sandbox Events
LLM Errors
Database Errors
Performance Information
```

Logs should not reveal:

```text id="n9q3v1"
Secrets
Passwords
Private Credentials
Unnecessary Sensitive Data
```

---

# 26. Log Levels

Recommended conceptual levels:

```text id="m8x4c2"
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Production should avoid excessive DEBUG logging unless temporarily enabled for diagnosis.

---

# 27. Log Rotation

Logs must not grow indefinitely.

A production setup should define:

```text id="q6n1v7"
Maximum Log Size
Retention Period
Rotation Policy
```

Exact values should be selected based on actual local usage.

---

# 28. Health Checks

Production should provide at least:

```text id="x3c8m5"
/health
```

Where useful, separate internal service checks may verify:

```text id="p7n2q4"
Database
Ollama
Model
Sandbox
```

---

# 29. Startup Health Sequence

Recommended:

```text id="m4v9c1"
Application Start
↓
Configuration Check
↓
Database Check
↓
Ollama Check
↓
Model Check
↓
Sandbox Check
↓
Application Ready
```

A failed non-critical dependency should be reported accurately rather than hidden.

---

# 30. Readiness vs Availability

The application should distinguish:

```text id="n1x7c4"
Application Running
```

from:

```text id="m5q2v8"
All Features Available
```

Example:

```text id="r8c3n6"
Backend = Running
Ollama = Unavailable
Sandbox = Ready
```

This is better than incorrectly reporting the entire system as fully ready.

---

# 31. Production Startup Script

Create a controlled startup mechanism.

Example:

```text id="x7m2q9"
scripts/
└── start_production.sh
```

Responsibilities may include:

```text id="c4n8v1"
Environment Check
Database Check
Service Startup
Health Check
```

The script must not silently ignore failures.

---

# 32. Production Stop Script

Provide a controlled shutdown process.

Example:

```text id="p9m3x6"
scripts/
└── stop_production.sh
```

It should stop application processes cleanly.

---

# 33. Production Status Script

Recommended:

```text id="m6c1q8"
scripts/
└── production_status.sh
```

Display:

```text id="q2n7v4"
Backend
Frontend
SQLite
Ollama
Model
Docker
```

---

# 34. Production Startup Behavior

Preferred:

```text id="x8m4c2"
Start
↓
Check
↓
Fail Safely if Required Dependency Missing
↓
Report Status
```

Avoid:

```text id="n5q1v7"
Start
↓
Ignore Errors
↓
Pretend Ready
```

---

# 35. Database Backup Strategy

At minimum maintain:

```text id="m3c8x5"
Manual Backup
+
Pre-Change Backup
```

Recommended backup structure:

```text id="r7n2v6"
backups/
├── database/
├── exports/
└── configuration/
```

---

# 36. Backup Naming

Use meaningful names:

```text id="x1q7m4"
bhasha2code_2026-10-07.db
```

Avoid:

```text id="c8m2n5"
backup1.db
backup-final.db
backup-final2.db
```

---

# 37. Backup Validation

A backup is not considered successful merely because a file exists.

Verify:

```text id="m5v9q2"
Backup Created
↓
File Readable
↓
Database Can Be Restored
↓
Restored Data Verified
```

---

# 38. Recovery Procedure

Basic recovery:

```text id="n4c7x1"
Stop Application
↓
Preserve Failed State
↓
Restore Backup
↓
Verify Database
↓
Start Application
↓
Run Smoke Test
```

Do not overwrite the failed database before preserving evidence where practical.

---

# 39. Recovery Test

Perform at least one controlled recovery test before declaring production deployment complete.

Test:

```text id="q8m1v6"
Backup
↓
Simulated Failure
↓
Restore
↓
Application Start
↓
Session Verification
```

---

# 40. Recovery Verification

After restoration verify:

```text id="x3c9m7"
Sessions
Messages
Saved Messages
Notes
Generated Code
Study Content
```

are available as expected.

---

# 41. Rollback Strategy

If a release causes a major regression:

```text id="m6n2q8"
Stop
↓
Identify Last Known Good Version
↓
Preserve Current State
↓
Rollback
↓
Restore Compatible Database if Required
↓
Smoke Test
↓
Resume
```

---

# 42. Versioning

Every production build should have an identifiable version.

Example:

```text id="q4v8c1"
Bhasha2Code v1.0.0
```

Versioning should distinguish:

```text id="n7m2x5"
Major
Minor
Patch
```

---

# 43. Release Tagging

Stable production releases should be tagged in Git.

Example:

```bash id="m3c7q2"
git tag v1.0.0
```

Then:

```bash id="x8n4m1"
git push origin v1.0.0
```

only when the repository setup supports remote Git hosting.

---

# 44. Production Git Rule

Production should correspond to a known source revision.

Record:

```text id="q5m8c2"
Git Commit
Version
Build Date
Environment
Model Version
```

---

# 45. No Untracked Production Changes

Avoid manually editing production source files without recording the change.

Preferred:

```text id="n1x6v4"
Change Source
↓
Test
↓
Commit
↓
Build
↓
Deploy
```

---

# 46. Production File Structure

Recommended:

```text id="m7c2q9"
Bhasha2Code/
├── backend/
├── frontend/
├── data/
├── models/
├── exports/
├── backups/
├── logs/
├── docker/
├── scripts/
├── docs/
├── .env
├── .env.example
├── README.md
├── RULES.md
└── PROJECT_WORKFLOW.md
```

Sensitive/runtime directories should remain protected from accidental Git commits.

---

# 47. Production Permissions

Production files should use reasonable OS permissions.

Protect:

```text id="x4n8m2"
.env
Database
Backups
Logs
Model Files where appropriate
```

Do not make sensitive files world-writable.

---

# 48. Production Database Permissions

Only the application process and authorized local users should need write access to the production database.

Avoid unnecessarily broad permissions.

---

# 49. Export Storage

PDFs and generated exports should be stored in:

```text id="m8q3c1"
exports/
```

Use controlled filenames.

Avoid allowing arbitrary filesystem paths from user input.

---

# 50. Export Cleanup

Define a policy for old generated files.

Possible:

```text id="n5x7v2"
Manual Cleanup
or
Retention Policy
```

Do not delete user exports automatically without a documented policy.

---

# 51. Temporary Files

Temporary files must be stored in controlled temporary directories.

They should be cleaned after use where practical.

---

# 52. Production Error Handling

For every dependency:

```text id="q2m8c5"
Failure
↓
Detect
↓
Log
↓
User-Friendly Response
↓
Recovery Guidance
```

---

# 53. Ollama Failure

User should see something like:

```text id="x6n1m4"
The local AI model is currently unavailable.
Please check that Ollama is running.
```

Do not show raw internal connection traces.

---

# 54. Docker Failure

Expected:

```text id="m3c8q7"
Code execution is currently unavailable because the execution sandbox is not running.
```

Never:

```text id="n7q2v5"
Fallback to host execution.
```

---

# 55. Database Failure

Expected:

```text id="x1m6c4"
The local database could not be accessed.
Your existing data has not been intentionally deleted.
```

The exact message should reflect the actual recovery behavior.

---

# 56. Production Feature Availability Matrix

| Component | Required | Failure Impact |
|---|---|---|
| Frontend | Yes | Application unavailable |
| Backend | Yes | Application unavailable |
| SQLite | Yes | Persistence unavailable |
| NLP | Yes | Core AI flow degraded/broken |
| Ollama | Yes | AI generation unavailable |
| Local Model | Yes | AI generation unavailable |
| Docker | Yes for Run | Code execution disabled |
| PDF Engine | Yes | Export disabled |
| Search | Yes | Search feature disabled |
| Study Mode | Yes | Study feature unavailable |

---

# 57. Graceful Degradation

Only safe degradation is allowed.

Example:

```text id="q8c2m5"
Docker unavailable
↓
Run button disabled
+
Explanation remains available
```

Not:

```text id="n4m7x1"
Docker unavailable
↓
Execute code directly on host
```

---

# 58. Production Monitoring

Production should record useful local metrics:

```text id="m5q1c8"
Response Latency
First Token Latency
LLM Errors
API Errors
Database Errors
Validation Results
Sandbox Failures
CPU
RAM
GPU where available
Disk Usage
```

---

# 59. Resource Monitoring

Monitor periodically:

```text id="x7n3m6"
RAM
CPU
VRAM
Disk
Docker Containers
Database Size
Log Size
```

---

# 60. Resource Thresholds

Thresholds should be based on:

```text id="q2m8v5"
Actual Hardware
Observed Usage
Application Stability
```

Do not invent arbitrary thresholds and label them as validated requirements.

---

# 61. Disk Monitoring

The following can grow over time:

```text id="m1c7x9"
Database
Logs
PDF Exports
Backups
Docker Images
Model Files
```

Disk usage should be reviewed periodically.

---

# 62. Model Storage

Local LLM model files may consume significant disk space.

Production documentation must record:

```text id="n6q2v4"
Model Name
Model Size / Storage Usage
Location
Version
```

Use actual measured values.

---

# 63. Database Backup Frequency

For the first local deployment:

```text id="x8m3c5"
Manual Backup:
Before Important Changes
```

A scheduled automated backup can be added later if needed.

---

# 64. Recovery Documentation

The operator should be able to answer:

```text id="m4q9n1"
How do I start Bhasha2Code?
How do I stop it?
How do I check status?
Where is the database?
Where are backups?
How do I restore?
How do I rollback?
How do I restart Ollama?
What happens if Docker fails?
```

---

# 65. Production Runbook

Create:

```text id="q7c2m8"
docs/17_production/RUNBOOK.md
```

The runbook should contain the actual commands required for:

```text id="n5m1x6"
Start
Stop
Status
Restart
Backup
Restore
Logs
Rollback
Health Check
```

---

# 66. Production Startup Checklist

```text id="x3q8m2"
[ ] Correct Git version
[ ] Correct environment file
[ ] Database available
[ ] Database backup available
[ ] Ollama running
[ ] Correct model installed
[ ] Docker running
[ ] Sandbox configuration present
[ ] Backend starts
[ ] Frontend starts
[ ] Health check passes
```

---

# 67. Production Smoke Test

Immediately after deployment:

```text id="m7c4n1"
Open UI
↓
New Chat
↓
Simple Coding Request
↓
Generate Code
↓
Validate
↓
Save Session
↓
Reopen Session
```

Expected:

```text id="q2n8v5"
Core flow works.
```

---

# 68. Production Critical Journey

Run the complete validated workflow:

```text id="x5m1c8"
New Chat
↓
Marathi Coding Request
↓
Generate Python Code
↓
Follow-Up
↓
Add Error Handling
↓
Validate
↓
Explain in Marathi
↓
Optimize
↓
Save
↓
Close
↓
Reopen
↓
Continue
↓
Study Mode
↓
PDF Export
```

---

# 69. Production Offline Gate

After installation is complete:

```text id="n8q3m5"
Disable Internet
↓
Start Application
↓
Chat
↓
Generate
↓
Debug
↓
Validate
↓
Save
↓
Reopen
↓
Study
↓
PDF
```

Expected:

```text id="m4x7c2"
Core local functionality remains available.
```

---

# 70. Production Security Gate

Verify:

```text id="q1n6v8"
[ ] No host code execution
[ ] Sandbox enabled
[ ] Network restricted
[ ] Filesystem restricted
[ ] Non-root execution
[ ] No Docker socket
[ ] No privileged container
[ ] Secrets protected
[ ] Localhost binding where appropriate
[ ] Session isolation preserved
```

---

# 71. Production Data Safety Gate

Verify:

```text id="x7m2c4"
[ ] Database backup exists
[ ] Restore procedure tested
[ ] Production database separated
[ ] No destructive startup migration
[ ] Export directory controlled
[ ] Sensitive runtime files protected
```

---

# 72. Production Rollback Gate

Before final release:

```text id="n3q8v5"
Known Good Version Identified
+
Rollback Steps Documented
+
Backup Available
```

A rollback procedure that has never been tested should be treated as unverified.

---

# 73. Production Release Record

Create a release record containing:

```text id="m6c1x9"
Version
Git Commit
Date
Environment
OS
Python
Node
Ollama
Model
Docker
Database
QA Result
Security Result
Known Limitations
```

---

# 74. Production Known Limitations

Document actual limitations such as:

```text id="q5m2n8"
Limited Supported Languages
Local Hardware Constraints
LLM Response Variability
Certain Code Validators Unsupported
GPU Acceleration Optional
Advanced Features Deferred to V2
```

Only include limitations that are actually present.

---

# 75. V1 Production Scope

V1 production focuses on:

```text id="x8c3m1"
Multilingual Coding
+
Context
+
Offline LLM
+
Debugging
+
Explanation
+
Validation
+
Persistent Sessions
+
Study
+
PDF
+
Safe Sandbox
```

---

# 76. Public Deployment Rule

Public deployment is a separate future project.

Before public exposure, perform additional work for:

```text id="m1q7v4"
Authentication
Authorization
HTTPS
Rate Limiting
Remote Network Security
Secrets Management
Multi-User Isolation
Cloud Infrastructure
Monitoring
Abuse Prevention
```

Do not treat localhost production as equivalent to internet-facing production.

---

# 77. Production Deployment Procedure

The complete procedure is:

```text id="q4n8c2"
1. Freeze Release Candidate
2. Run Final Tests
3. Run Security Gate
4. Create Backup
5. Record Git Commit
6. Configure Environment
7. Build Frontend
8. Prepare Backend
9. Initialize / Verify Database
10. Verify Ollama
11. Verify Model
12. Verify Docker
13. Start Services
14. Run Health Check
15. Run Smoke Test
16. Run Critical User Journey
17. Run Offline Gate
18. Record Release
```

---

# 78. Production Change Procedure

For future updates:

```text id="x2m7c9"
Change Request
↓
Task
↓
Development
↓
Testing
↓
Security Review
↓
Code Review
↓
Preview
↓
QA
↓
Backup
↓
Production Update
↓
Smoke Test
```

Never bypass the quality pipeline for convenience.

---

# 79. Emergency Fix Procedure

For a critical production issue:

```text id="m5q8n2"
Identify
↓
Preserve Evidence
↓
Backup
↓
Fix
↓
Test
↓
Review
↓
Deploy
↓
Smoke Test
```

An emergency fix should still be documented after the immediate recovery.

---

# 80. Production Incident Categories

Use:

```text id="q7n3c1"
Application
LLM
Database
Sandbox
Security
Performance
Storage
Configuration
```

---

# 81. Incident Record

Record:

```text id="x8m1v5"
Incident ID
Time
Component
Impact
Observed Error
Root Cause
Fix
Recovery
Follow-Up
```

---

# 82. Production Support Rule

When investigating a failure:

```text id="m2c7q9"
Do not guess.
```

Use:

```text id="q4n8v1"
Logs
Health Checks
Test Output
Database State
Git Version
Environment Configuration
```

---

# 83. Production Verification After Update

After every significant update:

```text id="x7m3c5"
Application Starts
↓
Health Check
↓
Core Chat
↓
Code Generation
↓
Validation
↓
Session Persistence
```

Then run affected regression tests.

---

# 84. Production Quality Gates

## Gate P1 — Build

```text id="m6q2n8"
Build succeeds
```

## Gate P2 — Startup

```text id="x1c7v4"
Services start
```

## Gate P3 — Health

```text id="n8m3q5"
Health checks pass
```

## Gate P4 — Smoke

```text id="q2x7c1"
Core functionality works
```

## Gate P5 — Security

```text id="m4n8v6"
Security controls active
```

## Gate P6 — Data

```text id="x5c2q9"
Backup / recovery available
```

## Gate P7 — Offline

```text id="n7m1v3"
Core offline workflow passes
```

## Gate P8 — Release

```text id="q8c4m2"
Version recorded
+
Known limitations documented
```

---

# 85. Production Blockers

Do not release when there is an unresolved:

```text id="m3x7n8"
Host Code Execution
Sandbox Bypass
Critical Data Loss
Cross-Session Leakage
Broken MUST-HAVE Core Flow
Critical Security Vulnerability
Unrecoverable Database Failure
```

---

# 86. Production Acceptance Criteria

Production is accepted only when:

```text id="q1n6m4"
[ ] Validated release candidate exists
[ ] Production configuration recorded
[ ] Frontend build succeeds
[ ] Backend dependencies verified
[ ] Database verified
[ ] Ollama verified
[ ] Model verified
[ ] Docker verified
[ ] Sandbox verified
[ ] Startup process verified
[ ] Health checks verified
[ ] Backup created
[ ] Recovery procedure documented
[ ] Rollback procedure documented
[ ] Smoke test passed
[ ] Critical user journey passed
[ ] Offline gate passed
[ ] Security gate passed
[ ] Known limitations documented
[ ] Release version recorded
```

---

# 87. Production Definition of Done

```text id="x8m2c5"
Validated
+
Reviewed
+
Configured
+
Backed Up
+
Recoverable
+
Smoke Tested
+
Security Checked
+
Offline Verified
=
Production Candidate
```

---

# 88. Production Status

**STATUS: COMPLETE**

The Bhasha2Code local production process is now defined.

The product moves through:

```text id="m5q7n2"
Development
↓
Testing
↓
Security Review
↓
Code Review
↓
Preview
↓
QA
↓
Production
```

with explicit quality and recovery gates.

---

# 89. Important Production Principle

> **A successful startup is not the same as a successful production deployment.**

Production requires:

```text id="q3n8c1"
Startup
+
Health
+
Functionality
+
Persistence
+
Security
+
Recovery
+
Offline Operation
```

---

# 90. Next Phase

## Phase 18 — Monitoring

The final phase will define how Bhasha2Code is observed after production:

```text id="x7m2c4"
Application Health
↓
LLM Health
↓
Response Latency
↓
First Token Latency
↓
CPU / RAM / GPU
↓
Database
↓
Sandbox
↓
Errors
↓
Disk
↓
Logs
↓
Alerts / Local Notifications
↓
Maintenance
```

The final goal is to make Bhasha2Code not only deployable, but **observable and maintainable after deployment**.