# 📊 WhatsApp Chat Analyzer

A powerful, interactive web application that lets you upload and analyze your personal or group WhatsApp chats. Built with **Streamlit**, it offers insights, visualizations, and even **PDF report generation**—all in one click!

🔗 **Live Demo:** [chat-analyzer-whatsapp](https://chat-analyzer-whatsapp.onrender.com)  
📁 **Repo:** [chat-analyzer-whatsapp](https://github.com/HarshalAl02/chat-analyzer-whatsapp)

---

## 🚀 Features

- ✅ Upload `.txt` WhatsApp chats in either **24-hour** or **AM/PM** format (auto-conversion supported)
- 📈 Timeline graphs: **monthly**, **daily**, and **activity maps**
- 📊 Top statistics: message counts, words, media, and links
- 🧑‍🤝‍🧑 Most engaged users in group chats
- ☁️ Auto-generated **word cloud** and **most common words**
- 😂 Emoji usage breakdown with **pie chart**
- 🧊 Weekly activity heatmap
- 🧠 **Chat Tone Classification** (Romantic, Sarcastic, Argumentative, Informational, Casual, etc.)
- 📌 Filter all graphs and insights **per user** or **overall**
- 📊 Interactive charts for timelines and activity
- 🍩 Donut chart for chat tone distribution
- 📦 Categorized bar charts for each tone over time
- 📄 One-click **PDF Report** generation with embedded visualizations

---

## 📂 Project Structure

```
📁 WhatsApp-Chat-Analyzer/
├── .gitignore
├── app.py
├── favicon.jpg
├── helper.py
├── logo.png
├── preprocessor.py
├── Procfile
├── requirements.txt
├── sample_chat.txt
├── stop_hinglish.txt
├── model.py
├── chat_classifier_model.pkl
└── tfidf_vectorizer.pkl

```

---

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/HarshalAl02/chat-analyzer-whatsapp.git
   cd chat-analyzer-whatsapp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

---

## 🧪 Sample Chat

A sample chat (`sample_chat.txt`) is included for testing. Toggle the “Use Sample Chat” checkbox in the sidebar to try the app without uploading anything.

---

## 📄 PDF Report

The app generates a complete PDF summary of your chat analysis, including:
- Timeline charts
- Word cloud
- Emoji chart
- Key statistics
- 🎨 Includes tone-based visualizations like donut chart, and individual tone trends

Just click the **“📄 Download PDF Report”** button after analyzing.

---

## 🧠 Tech Stack

- **Frontend/UI**: Streamlit
- **Data Analysis**: Pandas, Matplotlib, Seaborn
- **PDF Generation**: fpdf
- **NLP & Preprocessing**: Custom cleaning and stopword filtering

---

## 📝 How to Use

### 📤 Step 1: Export WhatsApp Chat as `.txt` File

To analyze your own WhatsApp chats, first export the conversation from your mobile device:

#### ✅ For Android:
1. Open the chat (individual or group) in **WhatsApp**
2. Tap the **three-dot menu** (⋮) → **More** → **Export chat**
3. Select **“Without media”** when prompted
4. Choose where to save/share the file (e.g., Google Drive, Email, Files)
5. You’ll get a `.txt` file — or sometimes a `.zip` file if sent via email or cloud

#### ✅ For iPhone (iOS):
1. Open the desired chat in **WhatsApp**
2. Tap the **chat name** at the top → Scroll down → **Export Chat**
3. Choose **“Without Media”**
4. Save the file using Mail, Files, or another method
5. You may receive a `.zip` file — download and extract it to get the `.txt` file inside

> ⚠️ *Always choose "Without media" to keep the file small and clean.*  
> 📦 *If you receive a `.zip` file, **extract it first** and use the `.txt` file inside.*

---

### 📥 Step 2: Upload and Analyze

1. Open the app (locally or via [Live Demo](https://chat-analyzer-whatsapp.onrender.com))
2. In the **sidebar**, click **“Browse files”** to upload your `.txt` chat file
3. Or check **“Use Sample Chat”** to test the app without uploading
4. Wait for the progress bar to finish – the app auto-detects and processes your chat format

---

## ✨ Author

**Harshal Alaspure**  
📫 [GitHub](https://github.com/HarshalAl02)
<br>
🔗 [LinkedIn](https://linkedin.com/in/harshal-alaspure-36b057291?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
