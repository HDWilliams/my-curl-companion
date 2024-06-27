import os
import streamlit as st
from openai import OpenAI
from assistant_interface import  create_thread, create_assistant, add_message_to_thread, get_assitant_messages, attach_vector_store, retrieve_assistant
from retrieval_tool import ResearchTool


api_key = st.secrets["OPENAI_SECRET_KEY"]

client = OpenAI(api_key=api_key)


conversation_assistant = create_assistant(client, st.secrets["CONVERSATION_ASSISTANT_INSTRUCTIONS"])
conversation_thread = create_thread(client)  

get_research = ResearchTool(client,
    create_assistant(client, st.secrets["RESEARCH_ASSISTANT_INSTRUCTIONS"], model="gpt-3.5-turbo"),
    create_thread(client))


st.title("GAim Bot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! I'm here to answer all your Eldin Ring questions. I know item locations, questlines, weapon state and more. And I can also give spoiler free hints..."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    user_message = add_message_to_thread(conversation_thread, prompt, client)

    message = get_assitant_messages(client, conversation_thread, conversation_assistant)


    st.session_state.messages.append({"role": "assistant", "content": message})
    st.chat_message("assistant").write(message)
