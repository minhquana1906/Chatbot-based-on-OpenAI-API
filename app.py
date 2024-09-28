import streamlit as st
import openai
import os
import joblib
from dotenv import load_dotenv
import time

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatApp:
    def __init__(self):
        self.previous_chats = self.load_chat_history()
        self.initialize_session_state()

    def initialize_session_state(self):
        if "chat_id" not in st.session_state:
            st.session_state.chat_id = None
        if "chat_title" not in st.session_state:
            st.session_state.chat_title = ""
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def load_chat_history(self):
        try:
            return joblib.load("data/chats_history")
        except:
            return {}

    def save_chat_history(self):
        joblib.dump(self.previous_chats, "data/chats_history")

    def clear_all_chats(self):
        self.previous_chats.clear()
        joblib.dump(self.previous_chats, "data/chats_history")
        for filename in os.listdir("data/"):
            file_path = os.path.join("data/", filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.initialize_session_state()

    def new_chat(self):
        # Create a new chat session
        st.session_state.chat_id = str(time.time())
        st.session_state.messages = []
        st.session_state.chat_title = f"ChatSession-{st.session_state.chat_id}"
        self.previous_chats[st.session_state.chat_id] = st.session_state.chat_title
        self.save_chat_history()
        self.save_current_session()

    def save_current_session(self):
        joblib.dump(
            st.session_state.messages, f"data/{st.session_state.chat_id}-st_messages"
        )

    def load_current_session(self):
        if st.session_state.chat_id and st.session_state.chat_id in self.previous_chats:
            try:
                st.session_state.messages = joblib.load(
                    f"data/{st.session_state.chat_id}-st_messages"
                )
            except:
                st.session_state.messages = []

    def display_sidebar(self):
        with st.sidebar:
            st.write("# Chat History")
            # Update the select box options
            unique_chat_ids = list(set(self.previous_chats.keys()))
            selected_chat_id = st.selectbox(
                label="Previous chats",
                options=unique_chat_ids,
                format_func=lambda x: self.previous_chats[x],
                index=(
                    unique_chat_ids.index(st.session_state.chat_id)
                    if st.session_state.chat_id in unique_chat_ids
                    else 0
                ),
                placeholder="Select a previous chat",
            )

            # Update session state with the selected chat id
            if selected_chat_id != st.session_state.chat_id:
                st.session_state.chat_id = selected_chat_id
                st.session_state.chat_title = self.previous_chats[selected_chat_id]
                self.load_current_session()

            if st.button("New Chat"):
                self.new_chat()
                # Reload the chat history to update the selectbox
                self.previous_chats = self.load_chat_history()

            if st.button("Clear All Chats"):
                self.clear_all_chats()

    def display_chat(self):
        st.write("# Chat with GPT-3.5-turbo")
        st.markdown(
            """
            **Welcome to GPT-3.5-turbo chatbot!** 🤖\n
            I'm here to help you with any questions you have. Feel free to ask me anything, and I'll do my best to assist you!
            """
        )
        for message in st.session_state.messages:
            with st.chat_message(name=message["role"], avatar=message.get("avatar")):
                st.markdown(message["content"])
        if prompt := st.chat_input("Your message here..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            with st.chat_message(name="assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for chunk in response:
                    chunk_message = chunk["choices"][0]["delta"].get("content", "")
                    full_response += chunk_message
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
            self.save_current_session()

    def run(self):
        self.display_sidebar()
        self.display_chat()


if __name__ == "__main__":
    app = ChatApp()
    app.run()
