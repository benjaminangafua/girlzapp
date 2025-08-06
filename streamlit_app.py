import streamlit as st
import openai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Load OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment")
client = openai.OpenAI(api_key=api_key)

# Load favicon image
favicon = Image.open("assets/favicon.png")  # or replace with your correct path/image name

# Set page configuration
st.set_page_config(
    page_title="GirlzApp+ Chatbot",
    page_icon=favicon,
    layout="centered"
)

# Title
st.title(st.secrets["openai"]["APP_TITLE"])
st.write("""
### Welcome to your safe space, Girl!

I'm here just for you. Ask me anything about your body, your period, your emotions, or your rights.
Want to track your cycle? Learn about birth control? Understand changes in your body?
You’re in the right place. It’s private. It’s judgment-free. It’s made for you. 
""")



# Initialize session states
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "active_topic" not in st.session_state:
    st.session_state.active_topic = None
if "last_topic_rendered" not in st.session_state:
    st.session_state.last_topic_rendered = None

# Educational topics
# Educational topics
topics = {
    "Menstrual Health": "Your period is a natural part of growing up. It may start between ages 10 and 16. If you ever feel worried about it, I'm here to answer your questions!",
    "Contraception": "Contraceptives help prevent pregnancy. There are many safe and effective options like pills, implants, and condoms. Let’s talk about what’s best for you.",
    "Mental Health": "It’s okay not to be okay. Whether it’s stress, sadness, or anxiety, talking to someone is a powerful step. I’m here to listen and support.",
    "STIs": "Sexually transmitted infections can be prevented and treated. It’s important to get tested and talk openly about protection and symptoms.",
    "SRHR Counseling": "Sexual and Reproductive Health and Rights (SRHR) help you understand your body, make informed choices, and know your rights. If you ever feel unsure, confused, or need someone to talk to, I'm here to help you through it."
}


# Sidebar for educational menu
with st.sidebar:
    st.header("📚 SRH Education Modules")
    for title in topics:
        if st.button(title):
            st.session_state.active_topic = title

# Inject selected topic into chat (toggle behavior)
if st.session_state.active_topic and st.session_state.active_topic != st.session_state.last_topic_rendered:
    topic = st.session_state.active_topic
    # Remove old topic messages
    st.session_state.chat_history = [
        (sender, msg) for sender, msg in st.session_state.chat_history
        if not (sender == "Bot" and msg.startswith("📘"))
    ]
    # Add new topic
    st.session_state.chat_history.append((
        "Bot",
        f"📘 **{topic}**\n\n{topics[topic]}\n\n✅ If you have any questions about **{topic}**, just ask below!"
    ))
    # Update render tracker
    st.session_state.last_topic_rendered = topic

# Referral services
referral_services = {
    "Kolahun Health Center": {
        "Location": "Kolahun, Lofa County",
        "Services": "SRH Counseling, Contraceptives, Mental Health Support",
        "Hours": "Mon–Fri, 8am–4pm"
    },
    "Zorzor Youth Clinic": {
        "Location": "Zorzor, Lofa County",
        "Services": "Pregnancy Testing, STI Treatment, Peer Counseling",
        "Hours": "Mon–Sat, 9am–3pm"
    }
}

# User input
user_input = st.chat_input("Start the conversation...")

if user_input:
    st.session_state.chat_history.append(("You", user_input))

    if "referral" in user_input.lower():
        location = user_input.lower().split("referral")[-1].strip().capitalize()
        found = False
        for name, info in referral_services.items():
            if location in name:
                response = f"🏥 **{name}**\n📍 {info['Location']}\n🩺 Services: {info['Services']}\n🕒 Hours: {info['Hours']}"
                st.session_state.chat_history.append(("Bot", response))
                found = True
                break
        if not found:
            st.session_state.chat_history.append(("Bot", "Sorry, I couldn't find any referral info for that location."))
    else:
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You're a friendly, respectful chatbot helping Liberian adolescents with health and SRH-related questions."}
                ] + [
                    {"role": "user" if sender == "You" else "assistant", "content": msg}
                    for sender, msg in st.session_state.chat_history
                ]
            )
            answer = response.choices[0].message.content
            st.session_state.chat_history.append(("Bot", answer))

# Scrollable chat rendering
with st.container():
    for sender, msg in st.session_state.chat_history:
        with st.chat_message("user" if sender == "You" else "assistant"):
            st.markdown(msg)
