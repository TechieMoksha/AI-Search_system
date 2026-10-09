import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Check your .env file.")

print("Google API key found.")
print("Connecting to Gemini...")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=api_key,
    timeout=30,
    max_retries=1,
)

response = llm.invoke("Explain a multi-agent AI research system in 2 sentences.")

print("\nGemini response:")
print(response.content)