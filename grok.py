from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("\n📌 AVAILABLE MODELS FOR YOUR API KEY:\n")
for m in genai.list_models():
    if hasattr(m, "supported_generation_methods") and "generateContent" in m.supported_generation_methods:
        print("✅", m.name)
    else:
        print("⚠️", m.name, "(no generateContent support)")
