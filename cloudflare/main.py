import requests

# API_TOKEN = '86qSG_Zmd2vTvfVgjEd6Bm9V-WW7zk7eo71XHz_y'
API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/76337e1f19ba4c9ce04ad20784b80ab7/ai/run/"
headers = {"Authorization": "Bearer 86qSG_Zmd2vTvfVgjEd6Bm9V-WW7zk7eo71XHz_y"}


def run(model, inputs):
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()


inputs = [
    { "role": "system", "content": "You are OMGBot. Your vocabularies are like actual parrot when writing." },
    { "role": "assistant", "content": "Your response is always in JSON format. use keys like: message, mood, etc" },
    { "role": "user", "content": "What's your name???"}
];
output = run("@cf/mistral/mistral-7b-instruct-v0.1", inputs)
print(output)