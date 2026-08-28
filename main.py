from fastapi import FastAPI
import google.generativeai as genai
import os
import random

app = FastAPI()

# Configure Gemini API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def get_active_model_name():
    """Finds the first available text-generation model from Google API."""
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Return the full model name string
                return m.name
    except Exception:
        pass
    # Fallback default
    return "models/gemini-2.5-flash"

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
        
        # Dynamically fetch an active model
        active_model = get_active_model_name()
        model = genai.GenerativeModel(active_model)
        
        full_prompt = f"{system_instruction}\nUser prompt: {prompt}"
        response = model.generate_content(full_prompt)
        
        raw_text = response.text.strip().replace("\n", " ")
        
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
