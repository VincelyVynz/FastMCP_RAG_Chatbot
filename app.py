import streamlit as st
from fastmcp import Client
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(
    page_title="RAG chatbot with MCP",
    page_icon= "🤖"
)
st.title("RAG chatbot with MCP")

# MCP Client

MCP_SERVER_URL = "http://localhost:8000"
mcp_client = Client(MCP_SERVER_URL)

# Streamlit async
def run_async(coro):
    return asyncio.run(coro)

# LLM

def ask_genai(context: str, question: str) -> str:
    prompt = f"""
You are a helpful assistant.
If the question is casual or conversational, answer normally.
If the question requires factual information, use the context below.
If the answer is not in the context, say you don't know.

Context: {context}
Question: {question}

"""

    response = client.models.generate_content(
        model= "models/gemini-2.5-flash",
        contents = prompt,
        config = types.GenerateContentConfig(
            temperature=0.3
        )
    )
    return response.text

# Chat

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

query = st.chat_input("Ask anything about employees")

if query:
    st.chat_message("user").markdown(query)
    st.session_state.messages.append(
        {"role": "user", "content": query}
    )

    with st.spinner("Retrieving documents..."):
        # Call MCP tool
        retrieved_chunks = run_async(
            mcp_client.call_tool(
                "retrieve_doc",
                arguments= {
                    "query": query,
                }
            )
        )

        st.write("Retrieved chunks:", retrieved_chunks) # FOR DEBUGGING

        context = "\n\n".join(retrieved_chunks)

    with st.spinner("Thinking..."):
        answer = ask_genai(context, query)

    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )








