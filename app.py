import os
import time
import joblib
import openai
import streamlit as st
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_tracer():
    if isinstance(trace.get_tracer_provider(), TracerProvider):
        return trace.get_tracer(__name__)
    resource = Resource.create({"service.name": "chatbot"})
    provider = TracerProvider(resource=resource)
    otlp_exporter = OTLPSpanExporter(
        endpoint="opentelemetry-collector.monitoring:4317",
        insecure=True,
    )
    span_processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
    return trace.get_tracer(__name__)


tracer = setup_tracer()

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def ensure_data_directory():
    data_directory = "/app/data"
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)


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
            return joblib.load("/app/data/chats_history")
        except:
            return {}

    def save_chat_history(self):
        joblib.dump(self.previous_chats, "/app/data/chats_history")

    def clear_all_chats(self):
        self.previous_chats.clear()
        joblib.dump(self.previous_chats, "/app/data/chats_history")
        for filename in os.listdir("/app/data/"):
            file_path = os.path.join("/app/data/", filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.initialize_session_state()

    def new_chat(self):
        st.session_state.chat_id = str(time.time())
        st.session_state.messages = []
        st.session_state.chat_title = f"ChatSession-{st.session_state.chat_id}"
        self.previous_chats[st.session_state.chat_id] = st.session_state.chat_title
        self.save_chat_history()
        self.save_current_session()

    def save_current_session(self):
        joblib.dump(
            st.session_state.messages,
            f"/app/data/{st.session_state.chat_id}-st_messages",
        )

    def load_current_session(self):
        if st.session_state.chat_id and st.session_state.chat_id in self.previous_chats:
            try:
                st.session_state.messages = joblib.load(
                    f"/app/data/{st.session_state.chat_id}-st_messages"
                )
            except FileNotFoundError:
                st.session_state.messages = []
                self.new_chat()
            except Exception as e:
                st.session_state.messages = []
                st.error(f"An error occurred: {e}")
        else:
            self.new_chat()

    def display_sidebar(self):
        with st.sidebar:
            st.write("# Chat History")
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

            if selected_chat_id != st.session_state.chat_id:
                st.session_state.chat_id = selected_chat_id
                st.session_state.chat_title = self.previous_chats[selected_chat_id]
                self.load_current_session()

            if st.button("New Chat"):
                self.new_chat()
                self.previous_chats = self.load_chat_history()

            if st.button("Clear All Chats"):
                self.clear_all_chats()

    def display_chat(self):
        st.write("# Chat with Molly-Q1")
        st.markdown(
            """
            **Welcome to Molly-Q1!** 🤖\n
            I'm here to help you with any questions you have. Feel free to ask me anything, and I'll do my best to assist you!
            """
        )
        for message in st.session_state.messages:
            with st.chat_message(name=message["role"], avatar=message.get("avatar")):
                st.markdown(message["content"])
        if prompt := st.chat_input("Enter a prompt here..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            with tracer.start_as_current_span("send_prompt"):
                start_time = time.time()  # Thời gian bắt đầu
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )
                except Exception as e:
                    st.error(f"Error occurred while sending prompt: {e}")

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
    ensure_data_directory()
    app = ChatApp()
    app.run()
