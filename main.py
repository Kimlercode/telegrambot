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
        f'Hi {user.mention_markdown_v2()}! Please register your account.',
        reply_markup={
            'keyboard': [
                ['/register'],
            ],
            'resize_keyboard': True
        }
    )

def register(update: Update, context: CallbackContext) -> None:
    """Asks the user to provide their username and password."""
    update.message.reply_text("Please enter your Telegram username:")
    return "USERNAME"

def register_username(update: Update, context: CallbackContext) -> None:
    """Stores the username and asks for the password."""
    username = update.message.text
    context.user_data["username"] = username 
    update.message.reply_text("Please enter a password (4-8 characters):")
    return "PASSWORD"

def register_password(update: Update, context: CallbackContext) -> None:
    """Stores the password and registers the user."""
    password = update.message.text
    if 4 <= len(password) <= 8:
        # Store username and password in the database
        # Replace with your actual database connection logic
        # Example using psycopg2:
        import psycopg2
        conn = psycopg2.connect(
            host=HOST,
            database=POSTGRESQL_DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (context.user_data["username"], password)
        )
        conn.commit()
        conn.close()
        
        update.message.reply_text("Registration successful!")
    else:
        update.message.reply_text("Password must be between 4 and 8 characters.")
    return ConversationHandler.END

# --- Main Function ---

def main() -> None:
    """Starts the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN) 
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Define the conversation flow for registration
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("register", register)],
        states={
            "USERNAME": [MessageHandler(Filters.text, register_username)],
            "PASSWORD": [MessageHandler(Filters.text, register_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add handlers for different commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("CONFIG", CONFIG))
    dispatcher.add_handler(CommandHandler("ACCOUNT", ACCOUNT))
    dispatcher.add_handler(conversation_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until interrupted
    updater.idle()

if __name__ == '__main__':
    main()
