from telegram.ext import ApplicationBuilder
from .config import TELEGRAM_TOKEN
from .dispatcher import setup_handlers
print("🚀 Booting bot...")
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    setup_handlers(app)
    app.run_polling()

if __name__ == "__main__":
    main()