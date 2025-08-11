import streamlit as st
import openai
import os
from dotenv import load_dotenv
from PIL import Image
from datetime import date, datetime, timedelta
import pandas as pd
from io import StringIO

# -------------------------
# Environment / API
# -------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment")
client = openai.OpenAI(api_key=api_key)

# -------------------------
# App Config
# -------------------------
favicon = Image.open("assets/favicon.png")
st.set_page_config(page_title="GirlzApp+ Chatbot", page_icon=favicon, layout="centered")

# -------------------------
# Title & Intro
# -------------------------
st.title(st.secrets["openai"]["APP_TITLE"])
st.write("""
### Welcome to your safe space, Girl!

I'm here just for you. Ask me anything about your body, your period, your emotions, or your rights.
Want to track your cycle? Learn about birth control? Understand changes in your body?
You’re in the right place. It’s private. It’s judgment-free. It’s made for you. 
""")

# -------------------------
# Session State
# -------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "active_topic" not in st.session_state:
    st.session_state.active_topic = None
if "last_topic_rendered" not in st.session_state:
    st.session_state.last_topic_rendered = None

# Emoji prompt & cycle state
if "active_prompt" not in st.session_state:
    # {"key":"...", "emoji":"🩸", "type":"yesno", "question":"...", "show_ui": bool}
    st.session_state.active_prompt = None
if "period_log" not in st.session_state:
    st.session_state.period_log = []       # [{"start": date}]
if "flow_log" not in st.session_state:
    st.session_state.flow_log = []         # [{"date": date, "flow": "heavy|medium|light"}]
if "cycle_length_days" not in st.session_state:
    st.session_state.cycle_length_days = 28

# -------------------------
# Educational Topics
# -------------------------
topics = {
    "Menstrual Health": "Your period is a natural part of growing up. It may start between ages 10 and 16. If you ever feel worried about it, I'm here to answer your questions!",
    "Contraception": "Contraceptives help prevent pregnancy. There are many safe and effective options like pills, implants, and condoms. Let’s talk about what’s best for you.",
    "Mental Health": "It’s okay not to be okay. Whether it’s stress, sadness, or anxiety, talking to someone is a powerful step. I’m here to listen and support.",
    "STIs": "Sexually transmitted infections can be prevented and treated. It’s important to get tested and talk openly about protection and symptoms.",
    "SRHR Counseling": "Sexual and Reproductive Health and Rights (SRHR) help you understand your body, make informed choices, and know your rights. If you ever feel unsure, confused, or need someone to talk to, I'm here to help you through it."
}

# -------------------------
# Help Categories (push to chat)
# -------------------------
help_categories = {
    "🏥 Health Clinics": {
        "description": "Visit a nearby clinic for personal and private care.",
        "options": {
            "Hope For Women": {
                "Location": "Paynesvillie",
                "Services": "SRH Counseling, Contraceptives, Mental Health",
                "Contact": "Nurse Martha – 0778 123 456"
            },
            "ELWA Hospital": {
                "Location": "Paynesvillie",
                "Services": "STI Testing, Pregnancy Support, Peer Counseling",
                "Contact": "Dr. Massa – 0886 555 789"
            },
            "JFK": {
                "Location": "Sinkor",
                "Services": "STI Testing, Pregnancy Support, Peer Counseling",
                "Contact": "Mr. Gbessay – 0886 555 789"
            },
            "Catholic Hospital": {
                "Location": "Congo Town",
                "Services": "STI Testing, Pregnancy Support, Peer Counseling",
                "Contact": "St. Theresa – 0886 555 789"
            },
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
            }
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
            "SRHR Emergency Line": {"Service": "24/7 hotline", "Contact": "0777 911 911"},
            "Confidential Line": {"Service": "24/7 hotline", "Contact": "0777 911 911"},
            "Rescue Line": {"Service": "24/7 hotline", "Contact": "0777 911 911"},
            "Ambulance Line": {"Service": "24/7 hotline", "Contact": "0777 911 911"}
        }
    }
}

# -------------------------
# Emoji → Prompt dictionary
# -------------------------
emoji_prompts = {
    # Menstrual Cycle Tracking
    "🩸": {"key": "period_start", "type": "yesno", "question": "Is this the first day of your period?"},
    "📅": {"key": "check_cycle",  "type": "yesno", "question": "Do you want me to check your cycle and predict the next period?"},
    "🌸": {"key": "fertile_window","type": "yesno","question": "Are you checking for your fertile window?"},
    "🔴": {"key": "flow_heavy",   "type": "yesno", "question": "Log today as **heavy flow**?"},
    "🟠": {"key": "flow_medium",  "type": "yesno", "question": "Log today as **medium flow**?"},
    "🟢": {"key": "flow_light",   "type": "yesno", "question": "Log today as **light flow**?"},
    # Symptoms (examples)
    "🤕": {"key": "sym_headache", "type": "yesno", "question": "Headache today — want simple relief tips?"},
    "😣": {"key": "sym_cramps",   "type": "yesno", "question": "Cramps or body pain — want safe pain relief ideas?"},
    # SRHR Awareness (examples)
    "🛡": {"key": "safe_practice","type": "yesno", "question": "Want to learn about safe practices and protection?"},
    "💊": {"key": "contraceptive","type": "yesno", "question": "Want quick info on contraceptive options?"}
}

# -------------------------
# Prompt helpers (UI-only rendering)
# -------------------------
def begin_prompt_for_emoji(emoji: str, *, show_ui: bool):
    """Create an active prompt; for this UX we only render UI (no chat line)."""
    if emoji in emoji_prompts:
        cfg = emoji_prompts[emoji]
        st.session_state.active_prompt = {
            "key": cfg["key"],
            "emoji": emoji,
            "type": cfg["type"],
            "question": cfg["question"],
            "show_ui": show_ui,
        }

def _handle_prompt_yes(p):
    today = date.today()
    if p["key"] == "period_start":
        st.session_state.period_log.append({"start": today})
        next_period = today + timedelta(days=st.session_state.cycle_length_days)
        st.session_state.chat_history.append(("Bot",
            f"🩸 Logged **period start** for **{today.strftime('%b %d, %Y')}**.\n"
            f"📅 Estimated **next period**: **{next_period.strftime('%b %d, %Y')}** "
            f"(~{st.session_state.cycle_length_days}-day cycle)."
        ))
    elif p["key"] in {"flow_heavy","flow_medium","flow_light"}:
        flow_map = {"flow_heavy":"heavy","flow_medium":"medium","flow_light":"light"}
        st.session_state.flow_log.append({"date": today, "flow": flow_map[p["key"]]})
        st.session_state.chat_history.append(("Bot",
            f"🗓 Logged **{flow_map[p['key']]} flow** for **{today.strftime('%b %d, %Y')}**."
        ))
    elif p["key"] == "check_cycle":
        if st.session_state.period_log:
            last_start = st.session_state.period_log[-1]["start"]
            next_period = last_start + timedelta(days=st.session_state.cycle_length_days)
            st.session_state.chat_history.append(("Bot",
                f"Last start: **{last_start.strftime('%b %d, %Y')}**.\n"
                f"📅 Estimated **next period**: **{next_period.strftime('%b %d, %Y')}**."
            ))
        else:
            st.session_state.chat_history.append(("Bot", "I need a start date. Type **🩸** to log it."))
    elif p["key"] == "fertile_window":
        if st.session_state.period_log:
            last_start = st.session_state.period_log[-1]["start"]
            ovulation = last_start + timedelta(days=14)
            st.session_state.chat_history.append(("Bot",
                f"🌸 Estimated fertile window around **{ovulation.strftime('%b %d, %Y')}** (varies by person)."
            ))
        else:
            st.session_state.chat_history.append(("Bot", "Type **🩸** to log your last start first."))
    elif p["key"] in {"sym_headache","sym_cramps"}:
        tips = "• Rest and hydrate\n• Warm compress on lower belly or back\n• If pain is strong, consider safe pain relief and talk to a clinic"
        st.session_state.chat_history.append(("Bot", f"Here are simple tips:\n{tips}"))
    elif p["key"] == "safe_practice":
        st.session_state.chat_history.append(("Bot", "Use condoms correctly every time. If unsure, ask a clinic or trusted adult."))
    elif p["key"] == "contraceptive":
        st.session_state.chat_history.append(("Bot", "There are many safe options (pill, implant, injection, condoms). A clinic can help you choose."))
    st.session_state.active_prompt = None

def _handle_prompt_no(p):
    st.session_state.chat_history.append(("Bot", "Okay 👍. You can choose another emoji or ask a question."))
    st.session_state.active_prompt = None

def render_active_prompt_ui():
    p = st.session_state.active_prompt
    if not p or not p.get("show_ui", False):
        return
    st.markdown(f"**{p['emoji']} {p['question']}**")
    c1, c2 = st.columns(2)
    if c1.button("✅ Yes", key="prompt_yes_icon"):
        _handle_prompt_yes(p)
    if c2.button("❌ No", key="prompt_no_icon"):
        _handle_prompt_no(p)

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    # Topics toggle
    st.header("📚 SRH Education Modules")
    for title in topics:
        if st.button(title):
            st.session_state.active_topic = title

    # Help menu
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
            if not any(bot_message in msg for sender, msg in st.session_state.chat_history):
                st.session_state.chat_history.append(("Bot", bot_message))
            st.markdown("---")

    # Emoji grid (click = UI prompt only, no chat question)
    st.subheader("🩺 Quick SRHR Actions")
    emoji_rows = [
        ["🩸", "📅", "🌸", "🔴", "🟠", "🟢"],
        ["🤕", "😣"],
        ["🛡", "💊"]
    ]
    for row_i, row in enumerate(emoji_rows):
        cols = st.columns(len(row))
        for i, emoji in enumerate(row):
            if cols[i].button(emoji, key=f"emoji-row{row_i}-{i}"):
                st.session_state.chat_history.append(("You", emoji))
                begin_prompt_for_emoji(emoji, show_ui=True)

    # Period Settings
    st.markdown("---")
    st.subheader("🩸 Period Settings")
    st.session_state.cycle_length_days = st.slider(
        "Typical cycle length (days)",
        min_value=21, max_value=35, value=st.session_state.get("cycle_length_days", 28),
        help="Most cycles are 21–35 days. Choose what fits you."
    )
    if st.session_state.get("period_log"):
        last_start = st.session_state.period_log[-1]["start"]
        next_period = last_start + timedelta(days=st.session_state.cycle_length_days)
        ovulation = last_start + timedelta(days=14)
        st.info(
            f"**Last start:** {last_start.strftime('%b %d, %Y')}\n\n"
            f"**Estimated next period:** {next_period.strftime('%b %d, %Y')}\n"
            f"**Fertile window (approx.):** {ovulation.strftime('%b %d, %Y')}"
        )
    if st.button("🧹 Clear period history"):
        st.session_state.period_log = []
        st.session_state.flow_log = []
        st.success("Cleared.")

    # Export CSV (includes estimated next period & fertile window for period starts)
    st.markdown("---")
    st.subheader("⬇️ Export")

    def build_history_df():
        rows = []
        cycle_len = st.session_state.cycle_length_days

        # Normalize to date objects and build rows
        for e in st.session_state.period_log:
            start_date = e["start"]
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            next_period = start_date + timedelta(days=cycle_len)
            fertile_window = start_date + timedelta(days=14)
            rows.append({
                "date": start_date,
                "type": "period_start",
                "detail": "",
                "estimated_next_period": next_period,
                "fertile_window_approx": fertile_window
            })

        for f in st.session_state.flow_log:
            log_date = f["date"]
            if isinstance(log_date, str):
                log_date = datetime.strptime(log_date, "%Y-%m-%d").date()
            rows.append({
                "date": log_date,
                "type": "flow",
                "detail": f["flow"],
                "estimated_next_period": None,
                "fertile_window_approx": None
            })

        # Sort safely by date (all are datetime.date)
        rows.sort(key=lambda r: r["date"])

        # Convert dates to strings for CSV
        for row in rows:
            row["date"] = row["date"].strftime("%Y-%m-%d") if row["date"] else ""
            row["estimated_next_period"] = (
                row["estimated_next_period"].strftime("%Y-%m-%d")
                if row["estimated_next_period"] else ""
            )
            row["fertile_window_approx"] = (
                row["fertile_window_approx"].strftime("%Y-%m-%d")
                if row["fertile_window_approx"] else ""
            )

        return pd.DataFrame(
            rows,
            columns=["date", "type", "detail", "estimated_next_period", "fertile_window_approx"]
        )

    df_hist = build_history_df()
    if not df_hist.empty:
        csv_buf = StringIO()
        df_hist.to_csv(csv_buf, index=False)
        st.download_button(
            "Download period history (CSV)",
            data=csv_buf.getvalue(),
            file_name="period_history.csv",
            mime="text/csv",
            help="Your logs include period starts, daily flow, and cycle predictions."
        )
    else:
        st.caption("No history yet to download.")

    # WHO PDF
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

# -------------------------
# Topic toggle into chat
# -------------------------
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

# -------------------------
# Chat input
# -------------------------
user_input = st.chat_input("Start the conversation...")

if user_input:
    st.session_state.chat_history.append(("You", user_input))

    # If the user typed a defined emoji, start the UI prompt (no extra chat question)
    typed_emoji = next((e for e in emoji_prompts.keys() if e in user_input), None)
    if typed_emoji:
        begin_prompt_for_emoji(typed_emoji, show_ui=True)
    else:
        # Normal GPT fallback
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

# -------------------------
# Chat history display + inline prompt UI
# -------------------------
with st.container():
    for sender, msg in st.session_state.chat_history:
        with st.chat_message("user" if sender == "You" else "assistant"):
            st.markdown(msg)

    # Render active prompt UI as the next assistant bubble so it appears right under the user's emoji
    if st.session_state.active_prompt and st.session_state.active_prompt.get("show_ui", False):
        with st.chat_message("assistant"):
            render_active_prompt_ui()
