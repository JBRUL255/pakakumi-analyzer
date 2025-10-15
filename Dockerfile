FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add this line 👇 to make the package visible
ENV PYTHONPATH="/app"

CMD ["bash", "entrypoint.sh"]
