import logging
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from hackerAI import HackerAI

class TelegramBot:
    def __init__(self, token):
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher
        self.hacker_ai = HackerAI()

    def start(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(
            "Welcome to HackerAI Chatbot! Send me your question and I'll generate a response for you."
        )

    def generate_text(self, update: Update, context: CallbackContext) -> None:
        prompt = update.message.text
        response_text = self.hacker_ai.generate_text(self.hacker_ai.ChatMLFormatter(prompt))
        if response_text is not None:
            update.message.reply_text(response_text, parse_mode=ParseMode.MARKDOWN)
        else:
            update.message.reply_text("Something went wrong. Please try again later.")

    def run(self):
        start_handler = CommandHandler("start", self.start)
        text_handler = MessageHandler(Filters.text & ~Filters.command, self.generate_text)

        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(text_handler)

        self.updater.start_polling()
        self.updater.idle()

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    # Initialize the Telegram bot with your token
    token = "YOUR_TELEGRAM_BOT_TOKEN"
    telegram_bot = TelegramBot(token)
    
    # Start the bot
    telegram_bot.run()
