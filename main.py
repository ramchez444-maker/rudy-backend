from fastapi import FastAPI
from google import genai
import os
import random

app = FastAPI()

# Initialize Google GenAI client with environment key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.get("/")
def home():
    return {"status": "Rudy's brain is online!"}

@app.get("/chat")
def chat(prompt: str):
    try:
        system_instruction = (
            "You are Rudy, a helpful animatronic pet dog. Keep responses UNDER 30 characters total. "
            "Separate line 1 and line 2 with a '|' symbol. Example: Hello!|I am Rudy!"
        )
        
        # Uses the latest active Flash model alias automatically
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=f"{system_instruction}\nUser prompt: {prompt}"
        )
        
        raw_text = response.text.strip().replace("\n", " ")
        
        # Split text for 16x2 LCD
        if "|" in raw_text:
            parts = raw_text.split("|", 1)
            line1 = parts[0][:16]
            line2 = parts[1][:16]
        else:
            line1 = raw_text[:16]
            line2 = raw_text[16:32]

        eye_x = random.randint(40, 140)
        eye_y = random.randint(60, 120)

        return {
            "line1": line1.strip(),
            "line2": line2.strip(),
            "eye_x": eye_x,
            "eye_y": eye_y
        }
    except Exception as e:
        err_msg = str(e)
        return {
            "line1": "Error occurred",
            "line2": err_msg[:16],
            "eye_x": 90,
            "eye_y": 90
        }
