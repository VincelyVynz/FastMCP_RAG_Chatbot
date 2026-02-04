import chainlit as cl
import google.generativeai as genai
from fastmcp import FastMCP
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key = os.getenv("GENAI_API_KEY"))

from server import read_employees, update_employee_record

model = genai.GenerativeModel(
    model_name = "gemini-1.5-flash",
    tools = [read_employees, update_employee_record]
)

@cl.on_chat_start
async def start():
    cl.user_session.set("chat_session", model.start_chat(history=[]))
    await cl.Message(content = "Hi! I'm your AI assistant. How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    chat_session = cl.user_session.get("chat_session")

    response = chat_session.send_message(message.content)
    await cl.Message(content = response.text).send()