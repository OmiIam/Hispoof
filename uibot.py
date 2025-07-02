from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
import subprocess

# Load environment variables from .env file
load_dotenv()

# Retrieve secure values
TOKEN = os.getenv("TELEGRAM_TOKEN")
SIP_USER = os.getenv("SIP_USER")
SIP_PASS = os.getenv("SIP_PASS")
PJSUA_PATH = os.getenv("PJSUA_PATH")
DYLD_LIB_PATH = os.getenv("DYLD_LIB_PATH")

user_state = {}  # Store user session info

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📞 Place Call", callback_data="place_call")],
        [InlineKeyboardButton("👤 Set Caller ID", callback_data="set_caller_id")],
        [InlineKeyboardButton("ℹ️ Status", callback_data="status")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to SpoofBot!", reply_markup=reply_markup)

# Handle button presses
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    state = user_state.setdefault(user_id, {"caller_id": "+12065550123"})

    if query.data == "place_call":
        await query.edit_message_text("📲 Enter the number you want to call (e.g. +14155550100):")
        state["awaiting"] = "target_number"

    elif query.data == "set_caller_id":
        await query.edit_message_text("📝 Enter new spoofed caller ID (e.g. +12065550123):")
        state["awaiting"] = "caller_id"

    elif query.data == "status":
        await query.edit_message_text(f"📞 Caller ID: {state['caller_id']}")

# Handle user inputs
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = user_state.setdefault(user_id, {"caller_id": "+12065550123"})

    awaiting = state.get("awaiting")

    if awaiting == "target_number":
        target = update.message.text.strip()
        caller_id = state["caller_id"]

        await update.message.reply_text(f"📞 Calling {target} from {caller_id}...")

        command = [
            PJSUA_PATH,
            "--id", f"sip:{caller_id}@didlogic.net",
            "--registrar", "sip:didlogic.net",
            "--realm", "*",
            "--username", SIP_USER,
            "--password", SIP_PASS,
            "--null-audio",
            f"sip:{target}@didlogic.net"
        ]

        env = {
            "DYLD_LIBRARY_PATH": DYLD_LIB_PATH
        }

        subprocess.Popen(command, env={**env, **os.environ})

        state["awaiting"] = None

    elif awaiting == "caller_id":
        state["caller_id"] = update.message.text.strip()
        await update.message.reply_text(f"✅ Caller ID updated to {state['caller_id']}")
        state["awaiting"] = None

    else:
        await update.message.reply_text("❓ Use /start to begin.")

# Run bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()