import os
import chainlit as cl
from google import genai
from dotenv import  load_dotenv

from server import read_employees, update_employee_record

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_ID = "gemini-1.5-flash"

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message(content = "Employee System Connected. Ask me anything related to employees").send()

@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "parts": [{"text": message.content}]})

    try:
        response = client.models.generate_content(
            model = MODEL_ID,
            contents = history,
            config = {
                "tools": [read_employees, update_employee_record],
            }
        )


        response_text = response.text
        history.append({"role": "model", "parts": [{"text": response_text}]})
        cl.user_session.set("history", history)

        await cl.Message(content = response_text).send()

    except Exception as e:
        await cl.Message(content = f"Error: {str(e)}").send()