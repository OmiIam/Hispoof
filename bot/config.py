from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file from root directory

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SIP_USER = os.getenv("SIP_USER")
SIP_PASS = os.getenv("SIP_PASS")
PJSUA_PATH = os.getenv("PJSUA_PATH")
DYLD_LIB_PATH = os.getenv("DYLD_LIB_PATH")
AUTHORIZED_ADMINS = list(map(int, os.getenv("AUTHORIZED_ADMINS", "").split(",")))

# Debug
print(f"✅ TELEGRAM_TOKEN loaded: {TELEGRAM_TOKEN}")