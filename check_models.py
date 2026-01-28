import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GOOGLE_API_KEY")
print("API KEY FOUND:", bool(key))

genai.configure(api_key=key)

models = list(genai.list_models())
print("Number of models found:", len(models))

for m in models:
    print(m.name, m.supported_generation_methods)

