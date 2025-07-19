FROM python:3.10-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/llm-grader
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000
USER llm-grader
