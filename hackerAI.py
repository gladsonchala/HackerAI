import requests
import logging
from strings import API_URL, instruction

class HackerAI:
    def __init__(self):
        self.API_URL = API_URL
        
        logging.basicConfig(level=logging.INFO)

    def generate_text(self, prompt):
        """
        Generates text based on the given prompt using the specified parameters.

        Args:
            prompt (str): The prompt to generate text from.

        Returns:
            str: The generated text.
        """
        params = {
            "prompt": prompt,
            "temperature": 0.5,
            "top_p": 1,
            "top_k": 40,
            "n": 1,
            "n_predict": -1,
            "stop": ["<|im_end|>"]
        }
        response = requests.post(self.API_URL, json=params)
        if response.status_code == 200:
            log_message = f"Text generated successfully: {response.status_code}"
            logging.info(log_message)
            return response.json()['content']
        else:
            log_message = f"Failed to generate text. Status code: {response.status_code}: {response.text}"
            logging.error(log_message)
            return None

    def ChatMLFormatter(self, prompt):
        """
        Formats the prompt for ChatML.

        Args:
            prompt (str): The user's prompt.

        Returns:
            str: The formatted prompt.
        """
        return f"""<|im_start|>system:{instruction}<|im_end|><|im_start|>user:{prompt}<|im_end|><|im_start|>assistant:"""

