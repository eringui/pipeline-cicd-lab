# Pipeline CI/CD Lab

[![CI/CD Pipeline](https://github.com/eringui/pipeline-cicd-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/eringui/pipeline-cicd-lab/actions/workflows/ci.yml)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=github-actions&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![LocalStack](https://img.shields.io/badge/LocalStack-3.4.0-000000?style=flat&logo=amazon-aws&logoColor=white)

---

## About the project

A complete CI/CD pipeline built as the first project in a DevOps portfolio. The application is a containerized Flask API with three automated delivery stages triggered on every `git push` to the main branch.

The goal was to simulate the real continuous delivery flow used at tech companies: no deployment happens manually. Every code change goes through automated tests, a Docker image build, and an environment check before reaching the deploy stage.

Since there's no access to a cloud provider requiring a credit card, the AWS infrastructure is simulated locally via LocalStack — demonstrating the same cloud service integration concept regardless of the environment used. Migrating to real AWS would only require swapping the endpoint and credentials.

---

## Architecture

<p align="center">
  <img width="540" height="675" alt="workflow" src="https://github.com/user-attachments/assets/56b68f40-c7f0-4f8d-a30f-9a148ea018d5" />
</p>

---

## Stack

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.11 | Application language |
| Flask | 3.1.3 | REST API framework |
| Pytest | 9.1.1 | Automated testing |
| Docker | 24.x | Application containerization |
| Docker Compose | 2.x | Service orchestration |
| GitHub Actions | — | CI/CD pipeline |
| LocalStack | **3.4.0** | AWS service simulation (S3) |
| AWS CLI | **1.32.0** | CLI interaction with LocalStack |

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com)
- [Python 3.11+](https://www.python.org/downloads)
- A [GitHub](https://github.com) account

---

## Running locally

**Via Docker Compose (recommended):**

```bash
git clone https://github.com/eringui/pipeline-cicd-lab
cd pipeline-cicd-lab
docker compose up -d
```

Wait ~15 seconds for LocalStack to initialize, then access:

- API: [http://localhost:5000](http://localhost:5000)
- Health check: [http://localhost:5000/health](http://localhost:5000/health)
- LocalStack: [http://localhost:4566/_localstack/health](http://localhost:4566/_localstack/health)

**To stop:**

```bash
docker compose down
```

---

**For local development (without Docker):**

```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
# venv\Scripts\Activate.ps1   # Windows

pip install -r requirements.txt
flask run --host=0.0.0.0 --port=5000
```

---

## API Endpoints

| Method | Route | Description | Response |
|---|---|---|---|
| GET | `/` | Project information | `{"status": "ok", "project": "Pipeline CI/CD Lab", "author": "Erick Paiva Silva"}` |
| GET | `/health` | Application health check | `{"status": "healthy"}` |

---

## Running the tests

```bash
source venv/bin/activate
pytest -v
```

Expected result:

```
collected 3 items

test_app.py::test_index_retorna_200       PASSED
test_app.py::test_index_retorna_status_ok PASSED
test_app.py::test_health_retorna_healthy  PASSED

3 passed in 0.45s
```

---

## CI/CD Pipeline

The pipeline consists of three jobs run in sequence via `needs`. Any failure at any stage halts the flow — broken code never reaches deployment.

### Job 1 — test
Runs on `ubuntu-latest`. Installs dependencies from `requirements.txt` and runs pytest. If any test fails, subsequent jobs are automatically cancelled.

### Job 2 — build
Runs on `ubuntu-latest`, depends on `test`. Builds the `cicd-lab-app` image, starts a temporary container, waits 5 seconds, checks whether `/health` returns 200 via `curl -f`, then stops and removes the container. Ensures the image is valid before deployment.

### Job 3 — deploy
Runs on `ubuntu-latest`, depends on `build`. Installs AWS CLI v1 (1.32.0) and awscli-local. Spins up the full environment via Docker Compose — the Flask app and LocalStack 3.4.0. Creates the simulated S3 bucket, uploads the artifact via `s3api put-object`, and verifies the application responds correctly.

---

## Project structure

```
pipeline-cicd-lab/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions pipeline
├── .dockerignore           # Files ignored by Docker
├── .gitignore              # Files ignored by Git
├── app.py                  # Flask application
├── docker-compose.yml      # Orchestration (app + localstack)
├── Dockerfile               # Application containerization
├── README.md               # This file
├── requirements.txt        # Python dependencies
└── test_app.py             # Pytest tests
```

---

## Technical decisions

**Why Flask and not Django?**
Flask is a simpler application, more suitable for beginners, and sufficient to demonstrate containerization and CI/CD. Django offers more features but requires deeper knowledge.

**Why LocalStack and not a self-hosted runner?**
A self-hosted runner would require the agent folder (~150MB) to be tracked in the repository, conflicting with GitHub's storage limits. LocalStack runs on GitHub's servers and simulates the necessary AWS services without depending on local infrastructure or a cloud account requiring a credit card.

**What would migration to real AWS look like?**
Two changes: remove the `localstack` service from `docker-compose.yml` and replace `AWS_ENDPOINT_URL` with real credentials via GitHub Secrets. The application code, Dockerfile, and workflow don't change at all.

---

## Author

**Erick Paiva Silva** — IT student, 6th semester, building a DevOps portfolio focused on Cloud Computing and infrastructure automation.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/erickpaivasilva/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/eringui)
