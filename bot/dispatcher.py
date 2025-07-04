from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    Application
)

from bot.handlers import (
    start,
    button,
    handle_text,
    list_users,
    help_command,
)

def setup_handlers(app: Application) -> None:
    # /start command
    app.add_handler(CommandHandler("start", start))
    
    # /help command
    app.add_handler(CommandHandler("help", help_command))

    # /users (admin only)
    app.add_handler(CommandHandler("users", list_users))

    # Inline button callbacks
    app.add_handler(CallbackQueryHandler(button))

    # Generic message handler (non-command text)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))