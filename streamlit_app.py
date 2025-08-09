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
favicon = Image.open("assets/favicon.png")
st.set_page_config(page_title="GirlzApp+ Chatbot", page_icon=favicon, layout="centered")

# App title & intro
st.title(st.secrets["openai"]["APP_TITLE"])
st.write("""
### Welcome to your safe space, Girl!

I'm here just for you. Ask me anything about your body, your period, your emotions, or your rights.
Want to track your cycle? Learn about birth control? Understand changes in your body?
You’re in the right place. It’s private. It’s judgment-free. It’s made for you. 
""")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "active_topic" not in st.session_state:
    st.session_state.active_topic = None
if "last_topic_rendered" not in st.session_state:
    st.session_state.last_topic_rendered = None

# Educational Topics
topics = {
    "Menstrual Health": "Your period is a natural part of growing up. It may start between ages 10 and 16. If you ever feel worried about it, I'm here to answer your questions!",
    "Contraception": "Contraceptives help prevent pregnancy. There are many safe and effective options like pills, implants, and condoms. Let’s talk about what’s best for you.",
    "Mental Health": "It’s okay not to be okay. Whether it’s stress, sadness, or anxiety, talking to someone is a powerful step. I’m here to listen and support.",
    "STIs": "Sexually transmitted infections can be prevented and treated. It’s important to get tested and talk openly about protection and symptoms.",
    "SRHR Counseling": "Sexual and Reproductive Health and Rights (SRHR) help you understand your body, make informed choices, and know your rights. If you ever feel unsure, confused, or need someone to talk to, I'm here to help you through it."
}

# Help Categories with Contacts
help_categories = {
    "🏥 Health Clinics": {
        "description": "Visit a nearby clinic for personal and private care.",
        "options": {
            "Hope For Women": {
                "Location": "Paynesvillie",
                "Services": "SRH Counseling, Contraceptives, Mental Health",
                "Contact": "Nurse Martha – 0778 123 456"
            }
            ,
            "ELWA Hospital": {
                "Location": "Paynesvillie",
                "Services": "STI Testing, Pregnancy Support, Peer Counseling",
                "Contact": "Dr. Massa – 0886 555 789"
            }
            ,
            "JFK": {
                "Location": "Sinkor",
                "Services": "STI Testing, Pregnancy Support, Peer Counseling",
                "Contact": "Mr. Gbessay – 0886 555 789"
            }
            ,
            "Catholic Hospital": {
                "Location": "Congo Town",
                "Services": "STI Testing, Pregnancy Support, Peer Counseling",
                "Contact": "St. Theresa – 0886 555 789"
            }
            ,
            "SOS Hospital": {
                "Location": "Congo Town",
                "Services": "STI Testing, Pregnancy Support, Peer Counseling",
                "Contact": "Mrs. Jallah – 0886 555 789"
            }
        }
    },
    "🏫 School Support": {
        "description": "Talk to a school nurse.",
        "options": {
            "J.J Robert": {
                "Location": "Sinkor",
                "Contact": "Madam Teta – School Counselor – 0777 002 334"
            },
            "Tubman High": {
                "Location": "Sinkor",
                "Contact": "Mrs. Kpaye – Health Club Focal – 0888 998 123"
            },
            "Voka Mission": {
                "Location": "Paynesvillie",
                "Contact": "Mrs. Leo – Health Club Focal – 0888 998 123"
            },
            "Best Brain": {
                "Location": "Rehab",
                "Contact": "Mrs. Jerome – Health Club Focal – 0888 998 123"
            },
        }
    },
    "🤝 NGOs": {
        "description": "NGOs provide youth-friendly, sometimes free services.",
        "options": {
            "Restore Hope Liberia": {
                "Location": "Voinjama",
                "Contact": "Joyce Bayo – SRHR Officer – 0777 456 789"
            },
            "Liberia Youth Network": {
                "Location": "Monrovia (online too)",
                "Contact": "WhatsApp +231 777 111 222"
            },
            "Plan Liberia": {
                "Location": "Monrovia (online too)",
                "Contact": "WhatsApp +231 777 111 222"
            },
            "CSI": {
                "Location": "Monrovia (online too)",
                "Contact": "WhatsApp +231 777 111 222"
            }
        }
    },
    "🌐 Online Platforms": {
        "description": "Chat or email health workers online.",
        "options": {
            "Ask-A-Nurse Liberia": {
                "Platform": "WhatsApp Chat",
                "Contact": "+231 770 000 111"
            },
            "Email": {
                "Platform": "Gmail",
                "Contact": "sos@girlzapp1.com"
            },
            "GirlTalk": {
                "Platform": "Web Chat",
                "Contact": "https://girlzapp1.streamlit.app/"
            }
        }
    },
    "📱 Telemedicine": {
        "description": "Call or video-chat a provider if you can’t visit. Consultations are private and confidential.",
        "options": {
            "DKT Healthline": {
                "Service": "Phone & WhatsApp consultation",
                "Contact": "+231 777 300 444"
            },
            "Video Chat": {
                "Service": "WhatsApp",
                "Contact": "+231 777 300 444"
            },
            "Call": {
                "Service": "Phone",
                "Contact": "+231 777 300 444"
            }
        }
    },
    "☎️ Hotlines": {
        "description": "Emergency Lines",
        "options": {
            "SRHR Emergency Line": {
                "Service": "24/7 hotline",
                "Contact": "0777 911 911"
            },
            "Confidential Line": {
                "Service": "24/7 hotline",
                "Contact": "0777 911 911"
            },
            "Rescue Line": {
                "Service": "24/7 hotline",
                "Contact": "0777 911 911"
            },
            "Ambulance Line": {
                "Service": "24/7 hotline",
                "Contact": "0777 911 911"
            }
        }
    }
}

# Sidebar with Topics
with st.sidebar:
    st.header("📚 SRH Education Modules")
    for title in topics:
        if st.button(title):
            st.session_state.active_topic = title

    # Help System Dropdowns
    st.markdown("---")
    st.subheader("📞 Where to Get Help")

    selected_help_category = st.selectbox(
        "Choose a support type:",
        [""] + list(help_categories.keys()),
        index=0,
        format_func=lambda x: "Select one..." if x == "" else x
    )

    if selected_help_category:
        cat = help_categories[selected_help_category]
        st.markdown(f"**{cat['description']}:**")

        selected_option = st.selectbox(
            f"Available in {selected_help_category}:",
            [""] + list(cat["options"].keys()),
            index=0,
            format_func=lambda x: "Select an option..." if x == "" else x
        )

        if selected_option:
            details = cat["options"][selected_option]
            msg_lines = [f"📍 **{selected_option}**"]
            for k, v in details.items():
                msg_lines.append(f"**{k}**: {v}")
            bot_message = "\n".join(msg_lines)

            # Avoid repeating if already in chat
            if not any(bot_message in msg for sender, msg in st.session_state.chat_history):
                st.session_state.chat_history.append(("Bot", bot_message))

            st.markdown("---")
    st.markdown("---")
    st.subheader("📄 Resources")
    with open("assets/Accelerated-Action-for-the-Health-of-Adolescents.pdf", "rb") as pdf_file:
        st.download_button(
            label="📥 Download WHO SRH Guide",
            data=pdf_file,
            file_name="Accelerated-Action-for-the-Health-of-Adolescents.pdf",
            mime="application/pdf",
            help="Click to download the WHO guide on SRH"
        )

# Show topic in chat if toggled
if st.session_state.active_topic and st.session_state.active_topic != st.session_state.last_topic_rendered:
    topic = st.session_state.active_topic
    st.session_state.chat_history = [
        (sender, msg) for sender, msg in st.session_state.chat_history
        if not (sender == "Bot" and msg.startswith("📘"))
    ]
    st.session_state.chat_history.append((
        "Bot",
        f"📘 **{topic}**\n\n{topics[topic]}\n\n✅ If you have any questions about **{topic}**, just ask below!"
    ))
    st.session_state.last_topic_rendered = topic

# Chat input logic
user_input = st.chat_input("Start the conversation...")

if user_input:
    st.session_state.chat_history.append(("You", user_input))

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

# Display chat history
with st.container():
    for sender, msg in st.session_state.chat_history:
        with st.chat_message("user" if sender == "You" else "assistant"):
            st.markdown(msg)
