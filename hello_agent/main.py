import os
import asyncio
import httpx
import requests

# For Streamlit secrets fallback
try:
    import streamlit as st
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL = "google/gemini-flash-1.5"
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "https://yourdomain.com",  # Optional
    "X-Title": "agentic-ai-test"
}

# 🔹 SYNC MODE
def run_sync(question):
    print("\n🔵 SYNC RESPONSE:\n")
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": question}]
    }
    response = requests.post(BASE_URL, headers=HEADERS, json=payload)
    try:
        print(response.json()["choices"][0]["message"]["content"])
    except Exception:
        print("❌ No response:", response.json())

# 🔹 ASYNC MODE
async def run_async(question):
    print("\n🟣 ASYNC RESPONSE:\n")
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": question}]
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(BASE_URL, headers=HEADERS, json=payload)
            print(response.json()["choices"][0]["message"]["content"])
        except Exception as e:
            print("❌ Async error:", e)

# 🔹 STREAM MODE
def run_stream(question):
    print("\n🟢 STREAM RESPONSE:\n")
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": question}],
        "stream": True
    }
    try:
        with requests.post(BASE_URL, headers={**HEADERS, "Accept": "text/event-stream"}, json=payload, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        data = line.removeprefix("data: ").strip()
                        if data == "[DONE]":
                            break
                        if data.startswith("{"):
                            import json
                            delta = json.loads(data)["choices"][0]["delta"]
                            if "content" in delta:
                                print(delta["content"], end="", flush=True)
        print()
    except Exception as e:
        print("❌ Streaming error:", e)

# 🔸 Main controller
def main():
    question = input("💬 Ask your question: ")
    mode = input("⚙️ Choose mode (sync / async / stream): ").strip().lower()

    if mode == "sync":
        run_sync(question)
    elif mode == "async":
        asyncio.run(run_async(question))
    elif mode == "stream":
        run_stream(question)
    else:
        print("❌ Invalid mode selected.")

if __name__ == "__main__":
    main()
