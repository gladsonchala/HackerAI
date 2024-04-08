from telegram import ChatAction, Update
from telegram.ext import CallbackContext

from WebScrape import WebScraper
from app.utils import link_from_text
from hackerAI import HackerAI


def link_handler(update: Update, context: CallbackContext):
  # Extract user information
  user_id = update.effective_chat.id  # Get chat_id directly from the update

  # Extract the link from the user's message
  user_message = update.message.text
  url = link_from_text(user_message)
  if url:
    # Perform link scraping using WebScraper
    context.bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
    link_scraper = WebScraper(url)
    scraped_text = link_scraper.scrape_visible_text()
    urlScrapedData = "user_message: " + user_message + "Link: " + url + "\nThe Webpage Data" + scraped_text

    # Send the scraped text to the AI request
    hacker_ai = HackerAI() 
    ai_response = hacker_ai.generate_text(urlScrapedData) 

    # Reply to the user with AI response
    if ai_response: 
      try:
        update.message.reply_text(f"{ai_response}", parse_mode='Markdown')
      except Exception:
        update.message.reply_text(ai_response)
    else:
      update.message.reply_text("AI response is empty.")
  else:
    update.message.reply_text(
      "Invalid command format. Please use '/link <url>'.")