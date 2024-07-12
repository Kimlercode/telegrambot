import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# --- Command Handlers ---

def start(update: Update, context: CallbackContext) -> None:
    """Sends a greeting message with a custom keyboard."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'Hi {user.mention_markdown_v2()}!',
        reply_markup={
            'keyboard': [
                ['/help', '/settings'],
                ['/about', '/cancel']
            ],
            'resize_keyboard': True
        }
    )

def CONFIG(update: Update, context: CallbackContext) -> None:
    """Sends a message listing available commands."""
    update.message.reply_text("Available commands: /start, /help, /settings, /about, /cancel")

def ACCOUNT(update: Update, context: CallbackContext) -> None:
    """Sends a message listing available settings."""
    update.message.reply_text("Available settings: Language, Notifications, Theme")

# --- Main Function ---

def main() -> None:
    """Starts the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN) 
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handlers for different commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("CONFIG", CONFIG))
    dispatcher.add_handler(CommandHandler("ACCOUNT", ACCOUNT))

    # Start the Bot
    updater.start_polling()

    # Run the bot until interrupted
    updater.idle()

if __name__ == '__main__':
    main()
