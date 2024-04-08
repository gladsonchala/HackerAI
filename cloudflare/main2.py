from fastapi import FastAPI, HTTPException, Query
import requests

app = FastAPI()

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/76337e1f19ba4c9ce04ad20784b80ab7/ai/run/"
HEADERS = {"Authorization": "Bearer 86qSG_Zmd2vTvfVgjEd6Bm9V-WW7zk7eo71XHz_y"}



def run_ai(model, inputs):
    input_data = {"messages": inputs}
    response = requests.post(f"{API_BASE_URL}{model}", headers=HEADERS, json=input_data)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="AI request failed")


@app.get("/ai")
def get_ai_response(user_content: str = Query(..., description="Content from the user")):
    inputs = [
        {"role": "system", "content": "You are OMGBot. Your vocabularies are like an actual parrot when writing."},
        {"role": "assistant", "content": "Your response is always in JSON format. use keys like: message, mood, etc"},
        {"role": "user", "content": user_content}
    ]
    try:
        output = run_ai("@cf/mistral/mistral-7b-instruct-v0.1", inputs)
        return output
    except HTTPException as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
