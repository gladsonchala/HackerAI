import re
import logging
from datetime import datetime, timedelta
from cachetools import TTLCache

#---------------------------
# !    Logging Setup
#---------------------------
# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an in-memory cache with a time-to-live (TTL) of 1 day
cache = TTLCache(maxsize=1000, ttl=86400)  # 86400 seconds in a day

#-------------------------------
# !    Method to get user info
#-------------------------------
def get_user_info(update):
    user = update.message.from_user
    user_id = user.id
    user_name = user.first_name
    username = user.username if user.username else user_name

    return user_id, user_name, username

# Function to get search state
def get_search_state(user_id):
    try:
        search_state = cache.get(f"search_enabled_{user_id}")
        return search_state if search_state is not None else False
    except Exception as e:
        logger.error(e)
        return False

# Function to set search state
def set_search_state(user_id, search_state):
    try:
        # Ensure search_state is a valid integer
        search_state = int(search_state)

        # Now set the search state in the cache
        cache[f"search_enabled_{user_id}"] = search_state
    except ValueError as ve:
        logger.error(
            f"Invalid search state value: {search_state}. It should be an integer."
        )
    except Exception as e:
        logger.error(e)

# Function to store user messages and AI responses in the cache with logging
def store_message(user_id, user_message, ai_response):
    try:
        key = f"{user_id}_{latest_key() + 1}"
        cache[key] = f"User: {user_message}\nYou: {ai_response}"

        # Log the stored message
        logger.info(
            f"Stored message for user {user_id}: {user_message} -> {ai_response}")
    except Exception as e:
        # Log any errors that occur during storage
        logger.error(f"Error storing message for user {user_id}: {e}")


# Function to get the user's previous messages from the cache
def get_user_previous_messages(user_id):
    user_key = str(user_id)
    messages = [cache[key] for key in cache.keys() if key.startswith(user_key)]
    return "\n".join(messages)

# Function to get the latest key from the cache
def latest_key():
    try:
        keys = cache.keys()
        return int(keys[-1].split('_')[1]) if keys else 0
    except Exception as e:
        logger.error(e)
        return 0


#*********************************
def link_from_text(text):
    # Regular expression to match URLs
    url_pattern = re.compile(r'\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b')
    
    # Find the first match in the text
    match = re.search(url_pattern, text)
    
    # Return the matched link if found, otherwise return None
    return match.group() if match else None

#*********************************