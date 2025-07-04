from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from call_service import place_call
from .config import AUTHORIZED_ADMINS
import json

user_state = {}

def is_authorized(user_id):
    return user_id in AUTHORIZED_ADMINS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[DEBUG] User ID: {update.effective_user.id}")
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized access.")
        return

    keyboard = [
        [InlineKeyboardButton("📞 Place Call", callback_data="place_call")],
        [InlineKeyboardButton("👤 Set Caller ID", callback_data="set_caller_id")],
        [InlineKeyboardButton("ℹ️ Status", callback_data="status")]
    ]
    await update.message.reply_text("Welcome to SpoofBot", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    state = user_state.setdefault(user_id, {"caller_id": "+12065550123"})

    if query.data == "place_call":
        await query.edit_message_text("📲 Enter the number to call:")
        state["awaiting"] = "target"

    elif query.data == "set_caller_id":
        await query.edit_message_text("📝 Enter new spoofed caller ID:")
        state["awaiting"] = "caller_id"

    elif query.data == "status":
        await query.edit_message_text(f"📞 Current Caller ID: {state['caller_id']}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = user_state.setdefault(user_id, {"caller_id": "+12065550123"})
    if not is_authorized(user_id):
        await update.message.reply_text("❌ Unauthorized access.")
        return

    if state.get("awaiting") == "target":
        target = update.message.text.strip()
        caller_id = state["caller_id"]
        await update.message.reply_text(f"📞 Calling {target} from {caller_id}...")
        success, error_message = place_call(target, caller_id)
        if success:
            await update.message.reply_text("✅ Call initiated successfully.")
        else:
            await update.message.reply_text(f"❌ Failed to initiate call. Reason: {error_message}")
        state["awaiting"] = None

    elif state.get("awaiting") == "caller_id":
        state["caller_id"] = update.message.text.strip()
        await update.message.reply_text(f"✅ Caller ID updated to {state['caller_id']}")
        state["awaiting"] = None

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized access.")
        return
    try:
        with open("db/users.json", "r") as f:
            data = f.read().strip()
            if not data:
                await update.message.reply_text("No users found.")
                return
            users = json.loads(data)
            if not users:
                await update.message.reply_text("No users found.")
                return
            msg = "\n".join(str(u) for u in users)
            await update.message.reply_text(f"Users:\n{msg}")
    except Exception as e:
        await update.message.reply_text(f"Error reading users: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/users - List users (admin only)\n"
        "Use the buttons to place a call or set caller ID."
    )
    await update.message.reply_text(help_text)