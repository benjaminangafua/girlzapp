import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import datetime
import os



# Show title and description.
st.set_page_config(page_title="Nurse Assistant", page_icon="💊")
st.title(st.secrets["openai"]["APP_TITLE"])

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management

load_dotenv()
OPENAI_API_KEY = st.secrets["openai"]["OPENAI_API_KEY"] if "openai" else os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})


# Convert messages to a clean string
def format_conversation(messages):
    lines = []
    for msg in messages:
        role = "Nurse" if msg["role"] == "user" else "Assistant"
        lines.append(f"{role}: {msg['content']}\n")
    return "\n".join(lines)

# Create download button
if st.session_state.messages:
    conversation_text = format_conversation(st.session_state.messages)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"nurse_conversation_{timestamp}.txt"
    

    if st.button("🔁 End Conversation"):
        st.download_button(
            label="📥 Download Conversation",
            data=conversation_text,
            file_name=filename,
            mime="text/plain"
        )

if st.button("🔁 Reset Conversation"):
    st.session_state.messages = []
    st.experimental_rerun()
