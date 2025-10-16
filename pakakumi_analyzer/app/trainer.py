# pakakumi_analyzer/app/trainer.py

from pakakumi_analyzer.app.db import init_db
init_db()
from pakakumi_analyzer.app.models import train_model
from pakakumi_analyzer.app.db import get_all_rounds

def run_training():
    rounds = get_all_rounds()
    model = train_model(rounds)
    print("✅ Model trained successfully:", model)
