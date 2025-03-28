import os
import logging
import requests
import json
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Set your API keys and tokens
TELEGRAM_BOT_TOKEN = "7939098557:AAHSPvlUxQmeqWbjffZNKJwqLeNbOxTMkcw"
ZYLA_API_KEY = "7441|RafuP1rECMR2oAeC1lrNPH1blLe6qkwZ2qNW6SkP"

def generate_fake_id():
    """Generate a fake identity using the Synthetic Profile Builder API"""
    url = "https://zylalabs.com/api/5492/synthetic+profile+builder+api/7125/generate+identity"
    headers = {"Authorization": f"Bearer {ZYLA_API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error generating fake ID: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response: {e.response.text}")
        return None

def format_fake_id(fake_id):
    """Format the fake ID data as a readable message"""
    if not fake_id:
        return "Error generating fake ID. Please try again later."
    
    address = fake_id['address']
    credit_card = fake_id['creditCard']
    
    return (
        f"🪪 *FAKE IDENTITY GENERATED* 🪪\n\n"
        f"*Personal Information:*\n"
        f"• Name: {fake_id['firstName']} {fake_id['lastName']}\n"
        f"• Email: {fake_id['emailAddress']}\n"
        f"• Phone: {fake_id['phoneNumber']}\n"
        f"• DOB: {fake_id['dateOfBirth']}\n"
        f"• Gender: {fake_id['sex']}\n\n"
        
        f"*Employment:*\n"
        f"• Company: {fake_id['company']}\n"
        f"• Department: {fake_id['department']}\n\n"
        
        f"*Address:*\n"
        f"• Street: {address['street']}\n"
        f"• City: {address['city']}\n"
        f"• State: {address['state']}\n"
        f"• ZIP: {address['zipCode']}\n"
        f"• Country: {address['country']}\n\n"
        
        f"*Credit Card:*\n"
        f"• Card Number: {credit_card['cardNumber']}\n"
        f"• Expiration: {credit_card['expirationDate']}\n"
        f"• CVV: {credit_card['cvv']}\n\n"
        
        f"_This is a synthetic identity for educational purposes only._"
    )

async def fakeid_command(update: Update, context) -> None:
    """Handle the /fakeid command"""
    await update.message.reply_text("Generating fake ID... Please wait.")
    
    fake_id = generate_fake_id()
    formatted_message = format_fake_id(fake_id)
    
    await update.message.reply_text(formatted_message, parse_mode=ParseMode.MARKDOWN)

async def start_command(update: Update, context) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message .reply_text(f"Hello, {user.first_name}! Use the /fakeid command to generate a fake identity.")

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("fakeid", fakeid_command))

    # Start the Bot
    application.run_polling()

if __name__ == "__main__":
    main() 

# Ensure you have the latest version of the required libraries
# pip install python-telegram-bot --upgrade requests

# The bot will respond to the /fakeid command by generating a fake identity
# and sending the formatted information back to the user in the chat.