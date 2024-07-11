# Author: DPEJOVIC

import streamlit as st
from openai import OpenAI


st.set_page_config(
    page_title="Chat",
    page_icon="👋",
)


st.title("Chat")


# Set up default system prompt
with open("defaultprompt.txt", "r") as file:
    defaultprompt = file.read()

if "default_prompt" not in st.session_state:
    st.session_state["default_prompt"] = defaultprompt

if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = defaultprompt


# Set up OpenAI API client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# Select GPT model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"


# Add reload counter
if "counter" not in st.session_state:
    st.session_state.counter = 0
st.session_state.counter += 1


# Initialise chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Initialise response counter
if "response_counter" not in st.session_state:
    st.session_state.response_counter = 0


# Write chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# if st.session_state.response_counter <= 5:

# Chat logic
if prompt := st.chat_input("Write something here"):
    
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        messages_with_system_prompt = [{"role": "system", "content": st.session_state["system_prompt"]}] + [
            {"role": m["role"], "content": m["content"]}
        for m in st.session_state.chat_history
        ]

        stream = client.chat.completions.create(
            model = st.session_state["openai_model"],
            messages = messages_with_system_prompt,
            stream = True,
        )
        response = st.write_stream(stream)

    st.session_state.response_counter += 1
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
# else:
#     st.write("Chat finished!")
