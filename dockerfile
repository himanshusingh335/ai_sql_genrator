FROM python:3.13-slim

WORKDIR /app

# Copy dependency files first
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies globally in Docker
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

RUN crewai install
RUN .venv/bin/python -m ensurepip --upgrade
RUN .venv/bin/pip3 install flask

# Expose the port
EXPOSE 5001

# Run crewai from system Python (not .venv)
CMD ["crewai", "run"]

# docker build -t mariox1105/ai-sql-generator-for-budget .

#docker run -d \
#  --env-file .env \
#  --name ai-sql-generator \
#  -p 5001:5001 \
#  -v budget_data:/app/data \
#  mariox1105/ai-sql-generator-for-budget