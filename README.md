```markdown
# GirlzApp+ – Adolescent-Friendly SRH Chatbot

**GirlzApp+** is an adolescent-friendly, privacy-conscious chatbot designed to provide accurate, respectful, and easy-to-understand information on **sexual and reproductive health (SRH)** for girls and young women in Liberia.

The app combines **AI-powered conversations** with **local health resources**, making it a safe, judgment-free space for both literate and semi-literate users to learn, ask questions, and get connected to care.

---

## ✨ Features

- **📚 Educational Modules**  
  Quick-access learning topics including:

  - 🩸 Menstrual Health
  - 🛡️ Contraception
  - ❤️ Mental Health
  - 🦠 STIs
  - 📢 SRHR Counseling

- **💬 AI Chat Support**  
  Friendly, adolescent-focused chatbot powered by OpenAI’s GPT model for personalized SRH questions.

- **🗂 “Where to Get Help” System**  
  Dropdown menus listing support categories:

  - 🏥 Health Clinics
  - 🏫 School Support
  - 🤝 NGOs
  - 🌐 Online Platforms
  - 📱 Telemedicine
  - ☎️ Hotlines  
    Includes **contact names, locations, and services** for each option.

- **📍 Local Referral Search**  
  Find nearby clinics or health providers by typing:
```

referral <location>

```markdown
in the chat.

- **📄 Resource Downloads**  
  Built-in access to the **WHO SRH Guide** in PDF format for offline learning.
```

---

## 📦 Installation & Setup

1. **Clone this repository**

```sh
git clone https://github.com/your-username/girlzapp.git
cd girlzapp
```

2. **Create a virtual environment**

```sh
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
```

3. **Install dependencies**

```sh
   pip install -r requirements.txt
```

4. **Set your OpenAI API key**
   Create a `.env` file in the project root and add:

```js
OPENAI_API_KEY = your_api_key_here;
```

5. **Run the app**

```sh
    streamlit run streamlit_app.py
```

```sh
xcode-select --install
pip install watchdog
pip install --upgrade openai
```

6. **Access in your browser**
   Streamlit will give you a local link, e.g.:

   ```sh
   Local URL: http://localhost:8501
   ```

---

## 🛠 Tech Stack

- **Frontend & UI**: [Streamlit](https://streamlit.io/)
- **AI Model**: OpenAI GPT-4
- **Environment Management**: python-dotenv
- **Image Handling**: Pillow
- **Data Handling**: Python dictionaries for help categories and referrals

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 📸 Usage

1. **Select a Topic** from the sidebar under **📚 SRH Education Modules** to learn about menstrual health, contraception, STIs, mental health, or SRHR counseling.
2. **Ask Questions** in the chat to get personalized, AI-powered answers.
3. **Use the “Where to Get Help” Menu** to find local health clinics, school support staff, NGOs, online platforms, telemedicine options, or hotlines.
4. **Download Resources** like the WHO SRH Guide for offline access.
5. **Search for Referrals** by typing:

   ```sh
   referral <location>
   ```

   in the chat to get clinic contact info.

---

## 📌 Project Goal

GirlzApp+ was created to break barriers to sexual and reproductive health information for adolescent girls and young women in Liberia. It provides private, judgment-free access to accurate resources and connects users to real-world health services.
