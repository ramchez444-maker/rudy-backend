from fastapi import FastAPI
import google.generativeai as genai
import os
import random

app = FastAPI()

# Configure Gemini with the API Key from environment variables
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.get("/")
def home():
    return {"status": "Rudy's brain is online!"}

@app.get("/chat")
def chat(prompt: str):
    try:
        # Prompt engineering to force short, 16x2-friendly responses
        system_instruction = (
            "You are Rudy, a helpful animatronic pet dog. Keep all responses UNDER 30 characters total. "
            "Separate line 1 and line 2 with a '|' symbol. Example: Hello!|I am Rudy!"
        )
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"{system_instruction}\nUser: {prompt}")
        
        raw_text = response.text.strip().replace("\n", " ")
        
        # Split text into Line 1 and Line 2 for the 1602 LCD
        if "|" in raw_text:
            parts = raw_text.split("|", 1)
            line1 = parts[0][:16]
            line2 = parts[1][:16]
        else:
            line1 = raw_text[:16]
            line2 = raw_text[16:32]

        # Generate random eye movements (X: 30-150, Y: 60-120)
        eye_x = random.randint(30, 150)
        eye_y = random.randint(60, 120)

        return {
            "line1": line1.strip(),
            "line2": line2.strip(),
            "eye_x": eye_x,
            "eye_y": eye_y
        }
    except Exception as e:
        return {
            "line1": "Error occurred",
            "line2": str(e)[:16],
            "eye_x": 90,
            "eye_y": 90
        }
