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
from prometheus_client import Counter, Histogram, start_http_server

resource = Resource.create({"service.name": "chatbot"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(
    endpoint="http://opentelemetry-collector.monitoring.svc.cluster.local:4318",
    insecure=True,
)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


chat_sessions_total = Counter("chat_sessions_total", "Total number of chat sessions")
response_time_seconds = Histogram(
    "response_time_seconds", "Response time for sending prompt", ["method"]
)
openai_requests_total = Counter(
    "openai_requests_total", "Total requests to OpenAI", ["status"]
)
openai_request_errors_total = Counter(
    "openai_request_errors_total", "Total errors from OpenAI requests", ["error_type"]
)
messages_sent_total = Counter(
    "messages_sent_total", "Total messages sent in chats", ["role"]
)

start_http_server(8099, addr="0.0.0.0")


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
        chat_sessions_total.inc()
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
            messages_sent_total.inc(labels={"role": "user"})
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
                    openai_requests_total.inc(labels={"status": "success"})
                except Exception as e:
                    openai_requests_total.inc(labels={"status": "error"})
                    openai_request_errors_total.inc(labels={"error_type": str(e)})

                response_time = time.time() - start_time
                response_time_seconds.observe(response_time)

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
