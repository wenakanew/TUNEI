 Tunei — Your Real-Time Media Intelligence Companion

> **"Tunei into real-time truth — stay ahead of the world, one summary at a time."**

Tunei is a real-time, AI-powered media intelligence agent designed to **monitor**, **analyze**, and **summarize** content across **social media**, **RSS feeds**, **web search results**, and **Telegram channels** — all beautifully presented in a modern, immersive Streamlit UI. 

Tunei helps you stay informed about **any topic** by fetching the latest insights and transforming them into **readable, image-rich news-style summaries**, complete with **sentiment analysis**, **source breakdown**, and even **PDF export**.

---

## ✨ Features

### 🔎 Real-Time Multi-Source Monitoring
- **Twitter/X**: Uses Twitter API (v2 Bearer Token) to fetch recent tweets based on the query.
- **Telegram**: Monitors public channels for relevant posts using Telethon.
- **RSS Feeds**: Parses multiple RSS sources simultaneously.
- **Web Search**: Leverages SerpAPI to fetch contextual images for summaries.

### 🧠 AI-Powered Summarization
- Integrates with **Azure OpenAI** to generate accurate, concise, and fluent summaries with natural language understanding.

### 🖼️ Rich Visuals
- Automatically fetches **contextual images** from the web using SerpAPI and embeds them within summaries for a gazette-like layout.

### 📊 Analytics Dashboard *(Planned or In Progress)*
- Displays **word count**, **sentiment polarity**, and **source contribution breakdown** for every summary.

### 🧾 Styled PDF Export *(Planned)*
- Export summaries as sleek, media-style PDFs with text and images included.

---

## 🧪 Tech Stack

| Area | Tools |
|------|-------|
| **Frontend** | [Streamlit](https://streamlit.io), Custom CSS (Dark Mode + Glassmorphism) |
| **Backend** | Python, Asyncio |
| **AI/NLP** | Azure OpenAI, TextBlob |
| **Data Sources** | Twitter API v2, Telegram via Telethon, RSS via `feedparser`, Web via SerpAPI |
| **Environment** | `dotenv`, `os`, `requests` |

---

## 📷 Screenshots

<details>
<summary>🖼 Click to expand</summary>

- **Modern Dark UI with Top Bar and Loader**
- **Alternating Image/Text Summary Blocks**
- **Microphone-Enabled Input Bar**
- **Floating Settings & Spinner Animation**
- *(Add screenshots here for better visual impression)*

</details>

---

## ⚙️ Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/tunei.git
cd tunei
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up `.env`

Create a `.env` file in the root directory:

```env
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
DEPLOYMENT_NAME=your_deployment_name
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
TELEGRAM_CHANNELS=@channel1,@channel2
RSS_FEEDS=https://feed1.xml,https://feed2.xml
SERPAPI_KEY=your_serpapi_key
```

### 4. Run Tunei

```bash
streamlit run app.py
```

---

## 💡 Use Cases

- 📈 **Media Monitoring** for brands, influencers, and public figures.
- 🧑‍💼 **Corporate Intelligence** for trend and sentiment analysis.
- 🗞️ **AI-Generated Newsletters** or bulletins.
- 📚 **Research Summarization** on niche topics.

---

## 🚧 Roadmap

- [x] Real-time summarization from multiple platforms
- [x] Custom dark UI with glassmorphism
- [x] SerpAPI image preview support
- [ ] Live dashboard for sentiment & trends
- [ ] Plugin system for extensibility

---

## 🧠 Project Structure

```bash
tunei/
├── app.py               # Main Streamlit App
├── .env                 # Environment variables
├── README.md
└── requirements.txt
```

---

## 👨‍💻 Author

**Kanew** — [@wenakanew](https://github.com/wenakanew)  
Passionate about building smart, AI-powered experiences.

---

## 📄 License

This project is licensed under the **MIT License**. Feel free to use, adapt, or contribute!

