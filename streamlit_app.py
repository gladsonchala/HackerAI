import telegram
from app.handlers import link_handler
import streamlit as st
import logging
# import threading
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from hack import HackAI

class StreamlitApp:
    def __init__(self, hacker_ai):
        self.hacker_ai = hacker_ai

    def run(self):
        st.title("HackerAI Chatbot")
        st.markdown("This chatbot can generate responses based on the provided prompt.")

        # Prompt input
        prompt = st.text_area("Enter your question:", """e.g. Code python script...""")

        # Generate text button
        if st.button("Generate Text"):
            with st.spinner("Generating..."):
                response_text = self.hacker_ai.generate_text(self.hacker_ai.ChatMLFormatter(prompt))
                if response_text is not None:
                    log_message = f"Response displayed successfully: {response_text}"
                    logging.info(log_message)
                    st.markdown(response_text)
                else:
                    st.error("Something is wrong. Please try again later.")
                    logging.error("Failed to generate text.")

class TelegramBot:
    def __init__(self, token, hacker_ai):
        self.token = token
        self.hacker_ai = hacker_ai
        self.lock_file = "telegram_bot.lock"

    def start(self, update, context):
        update.message.reply_text(
            "Welcome to HackerAI Chatbot! Send me your question and I'll generate a response for you."
        )

    def generate_text(self, update, context):
        prompt = update.message.text
        response_text = self.hacker_ai.generate_text(self.hacker_ai.ChatMLFormatter(prompt))
        if response_text is not None:
            try:
                update.message.reply_text(response_text, parse_mode="Markdown")
            except telegram.error.BadRequest:
                update.message.reply_text(response_text)
        else:
            update.message.reply_text("Something went wrong. Please try again later.")

    def run(self):
        if os.path.exists(self.lock_file):
            logging.info("Another instance of the bot is already running.")
            return

        with open(self.lock_file, "w") as f:
            f.write("")

        updater = Updater(self.token)
        dispatcher = updater.dispatcher

        start_handler = CommandHandler("start", self.start)
        text_handler = MessageHandler(Filters.text & ~Filters.command, self.generate_text)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(text_handler)
        dispatcher.add_handler(CommandHandler("link", link_handler))

        updater.start_polling()
        updater.idle()

        os.remove(self.lock_file)

def main():
    hacker_ai = HackAI()
    streamlit_app = StreamlitApp(hacker_ai)
    st.set_page_config(page_title="HackerAI Chatbot", page_icon=":robot:")
    
    # Run Streamlit app
    streamlit_app.run()

    # Initialize the Telegram bot with your token
    from strings import token
    token = token
    telegram_bot = TelegramBot(token, hacker_ai)
    
    # Run the Telegram bot
    telegram_bot.run()

if __name__ == "__main__":
    main()
