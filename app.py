import os
import chainlit as cl
from google import genai
from dotenv import  load_dotenv
from proto.marshal.compat import message

from server import read_employees, update_employee_record

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_ID = "gemini-1.5-flash"

@cl.on_chat_start
async def start():
    cl.user_session.set("chat_history", [])
    await cl.Message(content="System Ready. I can read and update employees.md!").send()

@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("chat_history")

    response = client.models.generate_content(
        model = MODEL_ID,
        content = message.content,
        config={
            "tools" : [read_employees, update_employee_record],
        }
    )

    history.append({"role": "user", "parts": [{"text": message.content}]})
    history.append({"role": "model", "parts": [{"text": response.text}]})
    await cl.Message(content=response.text).send()