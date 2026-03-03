# DataOps CI/CD Pipeline

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

> GitHub Actions + Great Expectations + dbt — 90% fewer failures

## Architecture

![Architecture Diagram](./architecture.svg)

## Project Structure

```
dataops-ci-cd-pipeline/
    ├── .gitignore
    ├── Makefile
    ├── main.py
    ├── requirements.txt
    ├── .github/
        ├── workflows/
            ├── data_quality_check.yml
    ├── config/
    ├── dashboards/
    ├── docker/
    ├── src/
        ├── __init__.py
        ├── gates/
            ├── __init__.py
            ├── pipeline_gate.py
        ├── notifications/
            ├── __init__.py
            ├── slack_notifier.py
        ├── quality/
            ├── __init__.py
            ├── expectation_suite.py
        ├── utils/
            ├── __init__.py
    ├── tests/
        ├── __init__.py
```

## Quick Start

```bash
# 1. Clone
git clone https://github.com/itsnikhile/dataops-ci-cd-pipeline
cd dataops-ci-cd-pipeline

# 2. Install
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env with your credentials

# 4. Run demo (no external services needed)
python main.py demo
```

## Local Development with Docker

```bash
# Start all infrastructure (Kafka, Redis, etc.)
docker-compose up -d

# Run the full pipeline
make run

# Run tests
make test
```

## Running Tests

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

## Configuration

All config is in `config/config.yaml`. Override with environment variables.
Copy `.env.example` to `.env` and fill in your credentials.

## Key Features

- ✅ Production-grade error handling and retry logic
- ✅ Comprehensive test suite with mocks
- ✅ Docker Compose for local development
- ✅ Makefile for common commands
- ✅ Structured logging with metrics
- ✅ CI/CD ready (GitHub Actions workflow)

---

> Built by [Nikhil E](https://github.com/itsnikhile) — Senior Data Engineer
