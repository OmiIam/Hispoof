from datetime import datetime

def log_call(from_number, to_number):
    with open("logs/calls.log", "a") as f:
        f.write(f"[{datetime.now()}] {from_number} → {to_number}\n")