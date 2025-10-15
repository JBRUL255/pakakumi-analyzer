# pakakumi_analyzer/app/config.py
import os

# Use a writable directory on Render
DB_PATH = os.getenv("DB_PATH", "/data/pakakumi.db")

# Other config values
MODEL_PATH = os.getenv("MODEL_PATH", "/data/pakakumi_model.pkl")
API_BASE_URL = "https://api.pakakumi.com"
