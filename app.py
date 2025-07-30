import streamlit as st
import openai 
import os
from dotenv import load_dotenv

client = openai.OpenAI()
# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="GirlzApp+ Chatbot", page_icon="💬")

st.title("💬 GirlzApp+ – Adolescent Health Chatbot")
st.write("Welcome! Ask me anything about your health, body, or services near you.")

# Sidebar for static educational content
with st.sidebar:
    st.header("📚 SRH Education Modules")
    topics = {
        "Menstrual Health": "Your period is a natural part of growing up...",
        "Contraception": "Contraceptives help prevent pregnancy...",
        "Mental Health": "It’s okay not to be okay. Let’s talk about your emotions...",
        "STIs": "Sexually transmitted infections can be prevented and treated..."
    }
    for title, content in topics.items():
        if st.button(title):
            st.session_state["chat_history"] = st.session_state.get("chat_history", []) + [(f"📘 {title}", content)]

# Referral system: static examples
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

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("Type your anonymous question or 'referral <location>'...")

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
            messages=[{"role": "system", "content": "You're a friendly, respectful chatbot helping Liberian adolescents with health and SRH-related questions."}] +
                    [{"role": "user" if sender == "You" else "assistant", "content": msg} for sender, msg in st.session_state.chat_history]
        )
            answer = response.choices[0].message.content
            st.session_state.chat_history.append(("Bot", answer))

# Display chat history
for sender, msg in st.session_state.chat_history:
    with st.chat_message("user" if sender == "You" else "assistant"):
        st.markdown(msg)
