# Bhasha2Code — Development Environment Setup

## Phase 10 — Setup

**Project:** Bhasha2Code  
**Phase:** 10 — Setup  
**Version:** 1.0  
**Status:** COMPLETE  
**Primary Development Tool:** Antigravity  
**Primary Runtime:** Localhost  
**Core AI Runtime:** Ollama + Local Coding LLM

---

# 1. Purpose

This document defines how to prepare a fresh development machine for Bhasha2Code.

The setup must provide:

```text
Operating System
↓
Development Tools
↓
Python Environment
↓
Backend
↓
Frontend
↓
Database
↓
NLP Libraries
↓
Ollama
↓
Local Coding Model
↓
Docker Sandbox
↓
Git
↓
Antigravity
↓
First Working Local AI Response
```

---

# 2. Setup Philosophy

Bhasha2Code is designed as a local-first application.

The development environment should therefore prioritize:

```text
Local Execution
Privacy
Reproducibility
Low Resource Usage
Simple Recovery
Offline Operation
```

Internet is required initially for installing packages and downloading the local model.

After installation, the core application should operate without internet.

---

# 3. Target Development Environment

## 3.1 Operating System

Primary development target:

```text
Ubuntu Linux 64-bit
```

The exact Ubuntu release should be recorded on the developer machine.

Check:

```bash
lsb_release -a
```

or:

```bash
cat /etc/os-release
```

---

# 4. Hardware Requirements

## Minimum Practical Development Environment

```text
CPU:
4+ cores

RAM:
16 GB

Storage:
At least 30 GB free

Architecture:
x86_64 / amd64
```

## Recommended

```text
CPU:
6+ cores

RAM:
16–32 GB

Storage:
50+ GB free

GPU:
Optional NVIDIA GPU
```

GPU acceleration is optional.

The application must remain functional using CPU execution when GPU acceleration is unavailable.

---

# 5. Software Components

| Component | Target |
|---|---|
| Python | 3.11 |
| Node.js | 24 LTS |
| npm | Bundled with Node.js |
| FastAPI | Current project-compatible version |
| React | Current project-compatible version |
| Vite | Current project-compatible version |
| SQLite | Local |
| Ollama | Current stable |
| Coding Model | `qwen2.5-coder:3b-instruct` |
| Docker | Current stable |
| Git | Current stable |
| Antigravity | Development tool |
| VS Code | Recommended editor |

Node.js currently lists v24 as an LTS release.

---

# 6. System Update

Run:

```bash
sudo apt update
sudo apt upgrade -y
```

Install common development tools:

```bash
sudo apt install -y \
    git \
    curl \
    wget \
    build-essential \
    ca-certificates \
    python3-pip \
    python3-venv \
    python3-dev
```

Verify:

```bash
git --version
python3 --version
pip3 --version
gcc --version
```

---

# 7. Python Setup

Bhasha2Code uses a dedicated virtual environment.

Python virtual environments keep project dependencies isolated from the system installation.

---

## 7.1 Check Python

```bash
python3 --version
```

Required development target:

```text
Python 3.11.x
```

If Python 3.11 is installed:

```bash
python3.11 --version
```

---

## 7.2 Create Project Directory

```bash
mkdir -p ~/projects
cd ~/projects
```

Create the repository:

```bash
mkdir Bhasha2Code
cd Bhasha2Code
```

---

# 8. Create Python Virtual Environment

Create:

```bash
python3.11 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

Verify:

```bash
which python
python --version
```

Expected:

```text
Python 3.11.x
```

---

# 9. Upgrade Python Packaging Tools

```bash
python -m pip install --upgrade pip setuptools wheel
```

Verify:

```bash
pip --version
```

---

# 10. Backend Environment

Create backend directory:

```bash
mkdir -p backend
```

Initial backend structure:

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   ├── services/
│   ├── nlp/
│   ├── context/
│   ├── llm/
│   ├── code_engine/
│   ├── database/
│   ├── sandbox/
│   ├── study/
│   └── export/
└── requirements.txt
```

---

# 11. Initial Python Dependencies

The exact package versions should be finalized after compatibility testing.

Initial dependency categories:

```text
FastAPI
Uvicorn
Pydantic
SQLAlchemy
SQLite support
spaCy
NLTK
Language Detection
scikit-learn
NumPy
Pandas
python-multipart
HTTP client
PDF generation
pytest
```

Install only dependencies that are actually required.

Do not install the entire ecosystem before implementation.

---

# 12. Create Requirements File

Initial `requirements.txt`:

```text
fastapi
uvicorn[standard]
pydantic
sqlalchemy
spacy
nltk
lingua-language-detector
scikit-learn
numpy
pandas
httpx
python-multipart
reportlab
pytest
pytest-asyncio
```

The final file must be generated from the tested project environment.

---

# 13. Install Backend Dependencies

With `.venv` active:

```bash
pip install -r backend/requirements.txt
```

Verify:

```bash
pip list
```

---

# 14. FastAPI Verification

Create a basic backend health endpoint.

Run:

```bash
uvicorn backend.app.main:app --reload
```

Expected local address:

```text
http://127.0.0.1:8000
```

Health endpoint:

```text
GET /health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

# 15. Node.js Setup

Node.js is required for the React + Vite frontend.

Use an LTS release rather than the Current release.

Node.js currently lists v24.21.0 as LTS.

Recommended installation method:

```text
Node Version Manager (nvm)
```

Verify:

```bash
node --version
npm --version
```

Target:

```text
Node 24.x LTS
```

---

# 16. Frontend Setup

Create React + Vite application inside the project.

Initial structure:

```text
frontend/
├── src/
├── public/
├── package.json
└── vite.config.*
```

The final implementation must follow `DESIGN.md`.

---

# 17. Frontend Dependencies

Initial categories:

```text
React
React DOM
Vite
Monaco Editor
HTTP client
Routing
Icon library
```

Do not introduce UI libraries unless they provide clear value.

The design must remain:

```text
Minimalist
White-first
Professional
Coding-focused
Study-friendly
```

---

# 18. Frontend Verification

Start:

```bash
npm run dev
```

Verify that the frontend loads locally.

Expected:

```text
Frontend
↓
Browser
↓
localhost
```

---

# 19. SQLite Setup

SQLite is the primary local database.

No separate database server is required for the initial local deployment.

Expected location:

```text
data/
└── bhasha2code.db
```

The database path must be configurable.

---

# 20. Database Initialization Test

The application should be able to:

```text
Create Database
↓
Create Tables
↓
Insert Test Session
↓
Read Session
↓
Delete Test Data
```

A failed database initialization must produce a clear error.

---

# 21. NLP Setup

Install required NLP packages inside `.venv`.

Initial NLP stack:

```text
spaCy
NLTK
Lingua
scikit-learn
regex / standard Python regex
```

---

# 22. NLP Resource Rule

NLP resources that are downloaded separately must be installed during setup.

The application must document all local NLP resources required for offline operation.

Example:

```text
NLTK data
spaCy model
Classifier models
```

---

# 23. Intent and Tone Models

Initial approach:

```text
TF-IDF
+
Logistic Regression
```

Separate locally stored models:

```text
models/
├── intent_classifier/
└── tone_classifier/
```

The training scripts and model version should be documented.

---

# 24. Programming Language Detection

Programming language detection should initially use a combination of:

```text
Explicit User Request
+
Code Syntax
+
Keywords
+
File/Editor Language
```

No external online API should be required.

---

# 25. Ollama Installation

Ollama provides the local model runtime.

Official installation instructions currently provide the Linux installer:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```



After installation:

```bash
ollama --version
```

---

# 26. Start Ollama

Run:

```bash
ollama serve
```

If Ollama is already running as a service, this may not be necessary.

Verify the local endpoint through the Ollama CLI or the application health check.

---

# 27. Download the Bhasha2Code Model

The V1 default coding model is:

```text
qwen2.5-coder:3b-instruct
```

Run:

```bash
ollama pull qwen2.5-coder:3b-instruct
```

Then:

```bash
ollama run qwen2.5-coder:3b-instruct
```

The Ollama registry lists this model at approximately 1.9 GB with 32K context.

---

# 28. Important Model Naming Rule

Do not use this as the production configuration:

```text
qwen2.5-coder:latest
```

without verifying the actual model size.

Ollama currently maps the `latest` Qwen2.5-Coder tag to a larger 7B model, around 4.7 GB.

Use the explicit V1 tag:

```text
qwen2.5-coder:3b-instruct
```

---

# 29. Verify Model

Run:

```bash
ollama list
```

Expected model:

```text
qwen2.5-coder:3b-instruct
```

---

# 30. First Local LLM Test

Run:

```bash
ollama run qwen2.5-coder:3b-instruct
```

Test:

```text
Write a Python program to calculate the factorial of a number.
```

The response must be generated locally.

---

# 31. Backend → Ollama Test

Bhasha2Code backend must communicate with Ollama through a dedicated service.

Architecture:

```text
FastAPI
↓
LLMService
↓
Ollama
↓
qwen2.5-coder:3b-instruct
```

The backend should never embed model-specific code inside unrelated services.

---

# 32. GPU Verification

GPU acceleration is optional.

If an NVIDIA GPU is installed:

```bash
nvidia-smi
```

If this works, record:

```text
GPU Model
Driver Version
CUDA Information
Available VRAM
```

If it fails:

```text
Application must still run.
```

CPU fallback is mandatory.

---

# 33. Docker Setup

Docker is required for the safe code-execution sandbox.

Docker officially supports Ubuntu installations through its official package repository; supported Ubuntu releases currently include 22.04, 24.04 and 26.04 LTS.

Follow the official Docker Engine installation procedure for the specific Ubuntu release.

Install the required packages:

```text
docker-ce
docker-ce-cli
containerd.io
docker-buildx-plugin
docker-compose-plugin
```



---

# 34. Docker Verification

Check:

```bash
docker --version
docker compose version
```

Then test:

```bash
sudo docker run hello-world
```

Docker documents `hello-world` as a basic installation verification step.

---

# 35. Sandbox Development Rule

Do not implement unrestricted host execution.

Never use:

```python
os.system(...)
```

or equivalent host execution for user/generated code.

Required architecture:

```text
User Code
↓
Validation
↓
Sandbox Policy
↓
Docker Container
↓
Restricted Execution
↓
Output
```

---

# 36. Git Setup

Configure Git:

```bash
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_EMAIL"
```

Verify:

```bash
git config --global --list
```

Initialize:

```bash
git init
```

---

# 37. Initial `.gitignore`

The following must not be committed:

```text
.venv/
.env
__pycache__/
*.pyc
node_modules/
dist/
data/*.db
exports/
models/*.bin
models/*.joblib
models/*.pkl
.DS_Store
```

Generated model files should be added intentionally when they are required for reproducibility.

---

# 38. Environment Variables

Create:

```text
.env
```

Example configuration:

```text
APP_ENV=development

BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000

OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5-coder:3b-instruct

DATABASE_URL=sqlite:///./data/bhasha2code.db

MAX_REPAIR_ATTEMPTS=3
```

Never commit `.env`.

Create:

```text
.env.example
```

without sensitive values.

---

# 39. Project Configuration Rule

Configuration must be centralized.

Do not hard-code:

```text
Model name
Ports
Database path
Repair attempts
Sandbox limits
```

throughout the codebase.

---

# 40. Antigravity Setup

Open the project directory in Antigravity.

Before implementation, Antigravity must read:

```text
README.md
PROJECT_WORKFLOW.md
RULES.md
docs/04_prd/PRD.md
docs/05_tech_stack/TECH_STACK.md
docs/06_architecture/ARCHITECTURE.md
docs/07_design/DESIGN.md
docs/08_rules/RULES_REFERENCE.md
docs/09_task_breakdown/TASKS.md
```

Antigravity must then work task-by-task according to `TASKS.md`.

---

# 41. Antigravity First Instruction

The first development instruction should NOT be:

```text
Build Bhasha2Code.
```

Use:

```text
Inspect the repository and project documentation.

Do not modify code yet.

Report:
1. Current repository structure
2. Missing project components
3. Development dependencies
4. Relevant Phase 9 tasks
5. Recommended first implementation task

Wait for task-specific implementation instructions.
```

---

# 42. Environment Verification Script

Create a local setup verification script:

```text
scripts/
└── verify_setup.py
```

It should check:

```text
Python
pip
Node
npm
Git
SQLite
Ollama
Configured model
Docker
```

---

# 43. Verification Commands

Run:

```bash
python --version
pip --version
node --version
npm --version
git --version
sqlite3 --version
ollama --version
docker --version
docker compose version
```

---

# 44. Setup Health Check

Expected:

```text
Python             PASS
Virtual Environment PASS
Node.js             PASS
npm                 PASS
Git                 PASS
SQLite              PASS
Ollama              PASS
Coding Model        PASS
Docker              PASS
```

A missing optional GPU should not fail the complete setup.

---

# 45. Backend + Frontend Verification

Start backend:

```bash
source .venv/bin/activate
uvicorn backend.app.main:app --reload
```

Start frontend in another terminal:

```bash
cd frontend
npm run dev
```

Expected:

```text
Browser
↓
React UI
↓
FastAPI
↓
SQLite
```

---

# 46. First Full Local AI Test

Test the complete chain:

```text
Browser
↓
Frontend
↓
FastAPI
↓
NLP Pipeline
↓
Context Manager
↓
Prompt Builder
↓
Ollama
↓
qwen2.5-coder:3b-instruct
↓
Response
↓
Frontend
```

Example:

```text
python madhe calculator bana
```

Expected behavior:

```text
Language → Marathi / Mixed
Intent → GENERATE_CODE
Programming Language → Python
LLM → Local
Response → Python code
```

---

# 47. First Context Test

User:

```text
python madhe calculator bana
```

Then:

```text
yat division by zero error handling add kar
```

Expected:

```text
The second request modifies the existing calculator context.
```

The user should not need to paste the calculator again.

---

# 48. First Validation Test

Generate invalid Python:

```python
print("Hello"
```

Expected:

```text
Validation Failed
```

Then debugging:

```text
Debug this code.
```

Expected flow:

```text
Problem
↓
Cause
↓
Fix
↓
Corrected Code
↓
Validation
```

---

# 49. Offline Readiness Test

After all required packages, NLP resources and model files are present:

```text
Disable internet
↓
Start application
↓
Open localhost
↓
Create chat
↓
Send coding request
↓
Generate response
↓
Save session
↓
Reopen session
```

The core flow must continue working without external network access.

---

# 50. Offline Dependency Rule

Any feature requiring internet must be explicitly marked.

Example:

```text
Core Chat       → Offline
NLP             → Offline
LLM             → Offline
SQLite          → Offline
Sessions        → Offline
Study Mode      → Offline
PDF Export      → Offline
Code Validation → Offline
Sandbox         → Offline
```

---

# 51. Reproducibility

The following must be documented:

```text
Python Version
Node Version
Package Versions
Ollama Version
Model Name
Docker Version
OS Version
```

Use:

```text
requirements.txt
package-lock.json
.env.example
README.md
SETUP.md
```

---

# 52. Environment Snapshot

Create:

```text
docs/10_setup/ENVIRONMENT.md
```

Record:

```text
OS:
Python:
Node:
npm:
Git:
Ollama:
Model:
Docker:
CPU:
RAM:
GPU:
```

Actual values must be collected from the machine.

Do not invent them.

---

# 53. Troubleshooting Principles

## Backend does not start

Check:

```bash
source .venv/bin/activate
python --version
pip install -r backend/requirements.txt
```

---

## Ollama unavailable

Check:

```bash
ollama --version
ollama list
```

Then verify that Ollama is running.

---

## Model missing

Run:

```bash
ollama pull qwen2.5-coder:3b-instruct
```

---

## Frontend does not start

Check:

```bash
node --version
npm --version
npm install
npm run dev
```

---

## Docker unavailable

Check:

```bash
docker --version
docker compose version
sudo systemctl status docker
```

Docker's Ubuntu documentation provides service verification and startup guidance.

---

# 54. Setup Security Rules

Never:

```text
Commit .env
Expose Ollama unnecessarily
Expose Docker daemon to the internet
Run generated code directly on host
Store secrets in source code
Disable sandbox security for convenience
```

---

# 55. Setup Completion Gate

Phase 10 is complete only when:

```text
[ ] Project directory created
[ ] Git initialized
[ ] Python environment created
[ ] Backend dependencies installed
[ ] FastAPI starts
[ ] Frontend starts
[ ] SQLite initializes
[ ] NLP dependencies installed
[ ] Ollama installed
[ ] Coding model downloaded
[ ] Backend can reach Ollama
[ ] Docker installed
[ ] Sandbox prerequisites verified
[ ] .env configured
[ ] .gitignore configured
[ ] Antigravity can inspect repository
[ ] First local AI response works
[ ] Context follow-up test works
```

---

# 56. Expected End State

At the end of setup:

```text
Bhasha2Code
│
├── Frontend       → Running
├── Backend        → Running
├── SQLite         → Ready
├── NLP            → Ready
├── Ollama         → Ready
├── Coding Model   → Ready
├── Docker         → Ready
├── Git            → Ready
└── Antigravity    → Ready
```

---

# 57. Phase 10 Acceptance Criteria

- [x] Development OS defined
- [x] Hardware baseline defined
- [x] Python environment defined
- [x] Backend setup defined
- [x] Frontend setup defined
- [x] SQLite setup defined
- [x] NLP setup defined
- [x] Ollama setup defined
- [x] Explicit V1 coding model defined
- [x] Docker setup defined
- [x] Git setup defined
- [x] Environment configuration defined
- [x] Antigravity setup defined
- [x] Verification flow defined
- [x] Offline verification defined
- [x] Troubleshooting defined
- [x] Setup completion gate defined

---

# 58. Phase 10 Status

**STATUS: COMPLETE**

The Bhasha2Code development environment is now formally defined from fresh-machine setup to the first local AI response.

---

# 59. Next Phase

## Phase 11 — Development

Development will now start using the Phase 9 task backlog.

The implementation sequence begins with:

```text
Backend Skeleton
↓
Database
↓
NLP Pipeline
↓
Ollama Integration
↓
Prompt Builder
↓
Context Manager
↓
Code Generation
```

Each task must follow:

```text
Inspect
↓
Implement
↓
Test
↓
Review
↓
Mark Done
```