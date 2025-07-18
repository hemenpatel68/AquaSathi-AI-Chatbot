# 💧 AquaSathi – AI Chatbot for Clean Water & Sanitation Awareness

AquaSathi is a lightweight AI chatbot designed to raise awareness about clean water, hygiene, and sanitation practices. Built with Streamlit and powered by Gemini 1.5 Flash (Google Generative AI), AquaSathi offers users short, conversational responses and optional detailed explanations on water-related topics.

🌍 This project aligns with the United Nations Sustainable Development Goal 6 (Clean Water & Sanitation).

---

## 🚀 Features

- ✨ Real-time AI chatbot interface
- ✏️ Short answers with an option for "More Details"
- 🧼 Focused on water hygiene, sanitation, and conservation
- 🧭 Clean and minimal UI with sidebar navigation
- 🔐 API key security using .env
- ☁️ Easily deployable on Streamlit Cloud

---

## 🛠️ Tech Stack

- Python 3.x
- Streamlit
- Google Generative AI (Gemini 1.5 Flash)
- dotenv (.env config)

---

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/AquaSathi-AI-Chatbot.git
cd AquaSathi-AI-Chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file and add your Gemini API key:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

4. Run the app:
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
AquaSathi-AI-Chatbot/
├── app.py                  # Main Streamlit app
├── .env                   # Gemini API key (not tracked in Git)
├── requirements.txt       # Dependencies
├── README.md              # This file
├── .gitignore             # Ignores .env and __pycache__