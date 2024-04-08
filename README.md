# Streamlit App with Telegram Bot

This project demonstrates how to integrate a Telegram bot with a Streamlit web application using Python.

## Description

This application consists of a Streamlit web interface and a Telegram bot. The Streamlit app allows users to interact with the bot through a web interface, while the Telegram bot enables communication via the Telegram messaging platform.

## Features

- **Streamlit App:**
  - Provides a user-friendly interface for interacting with the bot.
  - Allows users to input questions or prompts for the bot.
  - Displays bot responses in real-time.

- **Telegram Bot:**
  - Responds to user messages sent via the Telegram messaging platform.
  - Utilizes the `python-telegram-bot` library for bot functionality.
  - Runs automatically alongside the Streamlit app.

## Setup

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/streamlit-telegram-bot.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Obtain a Telegram Bot Token from the BotFather on Telegram.

4. Set the Telegram Bot Token in the `bot.py` file.

5. Run the Streamlit app:

   ```bash
   streamlit run streamlit_app.py
   ```

6. Interact with the Streamlit app through your web browser and the Telegram bot through the Telegram messaging platform.

## Usage

- Access the Streamlit app by visiting the URL provided after running the application.
- Input your questions or prompts in the designated text area.
- Click the "Generate Text" button to receive responses from the bot.
- Alternatively, communicate with the Telegram bot directly by sending messages to its Telegram handle.

## Dependencies

- Streamlit: Web framework for building interactive web applications.
- python-telegram-bot: Library for creating Telegram bots in Python.
- requests: HTTP library for making API requests.

## Author

- [Gemechis Chala](https://github.com/gladsonchala)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---