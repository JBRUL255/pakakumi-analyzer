FROM python:3.11-slim

# System dependencies for LightGBM, NumPy, and Pandas
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 build-essential git curl \
    && rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure Python sees your module
ENV PYTHONPATH="/app"

# Run entrypoint
CMD ["bash", "entrypoint.sh"]
