FROM python:3.14-slim

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-client \
    sshpass \
    curl \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Ansible + коллекции
RUN pip install --no-cache-dir \ 
    ansible \
    docker \
    requests

RUN ansible-galaxy collection install \
    community.docker \
    community.general

# Настройки для удобной работы
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh

WORKDIR /workspace