from fastapi import FastAPI
from google import genai
from google.genai import types
import os
import random

app = FastAPI()

# Initialize official GenAI client with environment key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.get("/")
def home():
    return {"status": "Rudy's brain is online!"}

@app.get("/chat")
def chat(prompt: str):
    try:
        sys_instruct = (
            "You are Rudy, a helpful animatronic pet dog. Keep responses UNDER 30 characters total. "
            "Separate line 1 and line 2 with a '|' symbol. Example: Hello!|I am Rudy!"
        )
        
        # Use gemini-2.5-flash with official types configuration
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"User prompt: {prompt}",
            config=types.GenerateContentConfig(
                system_instruction=sys_instruct,
                max_output_tokens=60,
                temperature=0.7,
            )
        )
        
        raw_text = response.text.strip().replace("\n", " ")
        
        # Split text into Line 1 and Line 2 for 16x2 LCD
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
