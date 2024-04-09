import json
import requests
import logging
from strings import instruction, API_BASE_URL, headers, model

class HackAI:
    def __init__(self):
        self.API_BASE_URL = API_BASE_URL
        self.headers = headers
        self.model = model
        
        logging.basicConfig(level=logging.INFO)



    def run_ai(self, model, inputs): 
        input_data = {"messages": inputs}
        response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input_data)
        if response.status_code == 200:
            log_message = f"Text generated successfully: {response.status_code}"
            response_text = response.text
            parsed_response = json.loads(response_text)
            response_message = parsed_response['result']['response']
            return response_message
        else:
            log_message = f"Failed to generate text. Status code: {response.status_code}: {response.text}"
            logging.error(log_message)
            return None


    def generate_text(self, prompt):
        """
        Generates text based on the given prompt using the specified parameters.

        Args:
            prompt (str): The prompt to generate text from.

        Returns:
            str: The generated text.
        """
        inputs = [
            {"role": "system", "content": instruction},
            # {"role": "assistant", "content": instruction2},
            {"role": "user", "content": prompt}
        ]
        try:
            output = self.run_ai(model, inputs)
            return output
        except Exception as e:
            return {"error": str(e)}
