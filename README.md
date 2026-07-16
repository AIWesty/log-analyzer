# 📊 Log Analyzer

[![CI Pipeline](https://github.com/AIWesty/log-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/AIWesty/log-analyzer/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/AIWesty/log-analyzer/branch/main/graph/badge.svg)](https://codecov.io/gh/AIWesty/log-analyzer)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Nginx log analyzer built as a DevOps portfolio project. Demonstrates modern CI/CD practices, containerization, and infrastructure as code.

## 🚀 Features

- **Fast Log Parsing**: Analyzes nginx access logs with regex patterns
- **Statistics Generation**: Top IPs, error counts, status code distribution
- **Containerized**: Docker-ready with multi-stage builds
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions
- **Infrastructure as Code**: Ansible playbooks for deployment

## 📦 Quick Start

### Prerequisites

- Python 3.12+
- Docker & Docker Compose

### Local Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with sample logs
LOG_FILE_PATH=tests/fixtures/sample.log python -m src.log_analyzer.main

🐳 Docker

# Build image
docker build -t log-analyzer:latest .

# Run with docker-compose
docker-compose up -d

# Generate traffic
./scripts/generate_traffic.sh 100

# Analyze logs
docker-compose run --rm log-analyzer

🧪 Testing

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux


🐳 Docker Image

# Pull latest image
docker pull ghcr.io/YOUR_USERNAME/log-analyzer:latest

# Run image
docker run --rm -v /path/to/logs:/var/log/nginx ghcr.io/YOUR_USERNAME/log-analyzer:latest
