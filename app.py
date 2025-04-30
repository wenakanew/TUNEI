import os
import asyncio
import streamlit as st
import requests, feedparser, tweepy
from dotenv import load_dotenv
from serpapi import GoogleSearch
from telethon import TelegramClient
from textblob import TextBlob

# Load environment variables
load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_VERSION = "2024-12-01-preview"
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID"))
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_CHANNELS = [c.strip() for c in os.getenv("TELEGRAM_CHANNELS", "").split(",")]
RSS_FEEDS = os.getenv("RSS_FEEDS", "").split(",")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

st.set_page_config(page_title="Tunei", page_icon="🧠", layout="centered")

# 🎨 Custom CSS Styling
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
body {
    font-family: 'Inter', sans-serif;
    background-color: #1e1e22;
    color: #fff;
}
section[data-testid="stSidebar"] {
    background-color: #1e1e22;
    padding: 1.5rem;
    color: white;
    border-right: 1px solid rgba(255,255,255,0.1);
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #fff;
    font-size: 1.3rem;
    font-weight: 700;
    background: linear-gradient(to right, #7f5af0, #2cb67d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}
.stRadio > label {
    font-size: 0.95rem;
    color: #ccc;
    margin-bottom: 0.5rem;
    display: block;
    cursor: pointer;
}
.stRadio > div > div {
    background-color: #2a2a2f !important;
    border-radius: 10px;
    padding: 0.6rem;
    margin-bottom: 0.4rem;
    border: 1px solid transparent;
    transition: all 0.3s ease;
}
.stRadio > div > div:hover {
    border: 1px solid #2cb67d;
    background-color: #313137 !important;
}
.top-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 65px;
  background: rgba(30, 30, 34, 0.92);
  backdrop-filter: blur(8px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.8rem;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 2px 8px rgba(0,0,0,0.4);
}
.top-bar .left {
  font-size: 1.4rem;
  font-weight: 800;
  color: white;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.top-bar .left span {
  background: linear-gradient(to right, #8e44ad, #2cb67d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}
.top-bar .right {
  display: flex;
  align-items: center;
  gap: 1.3rem;
  font-size: 1.2rem;
  color: #aaa;
  transition: color 0.2s ease;
}
.top-bar .right:hover {
  color: #fff;
}
.main-content {
  margin-top: 80px;
}

.hero {
    text-align: center;
    margin: 2rem 0 1.5rem;
}
.hero h1 {
    font-size: 2.3rem;
    font-weight: 700;
    background: linear-gradient(to right, #8e44ad, #2cb67d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.news-block {
    margin: 1.5rem 0;
    padding: 1rem;
    border-radius: 16px;
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}
.stGenerateBtn button {
    position: fixed;
    top: 50px;
    right: 20px;
    width: 2.5rem;
    height: 1rem;
    border-radius: 50%;
    font-size: 1.2rem;
    line-height: 2.5rem;
    background: #2cb67d;
    color: white;
    border: none;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    transition: transform 0.2s ease;
}
.stGenerateBtn button:hover {
    background-color: #3b82f6;
    box-shadow: 0 0 0 5px #3b83f65f;
    color: #fff;
} 
.loader {
  background-color: black;
  position: relative;
  width: 0.8em;
  height: 0.8em;
  transform-origin: center;
  transition: 1s;
  border-radius: 50px;
  box-shadow: inset 0px 0px 10px purple,
  inset 5px 5px 12px rgba(44, 0, 114, 0.8),
  inset 8px 8px 1px rgba(160, 120, 255, 0.7),
  0px 0px 1px rgba(160, 120, 255, 0.6);
  animation: 1.2s linear infinite 0s running first682;
}
.loader div {
  width: inherit;
  height: inherit;
  position: absolute;
}
#first {
  transform: rotate(90deg)
}
#first::before {
  --width: 0.8em;
  --height: 0.8em;
  content: "";
  position: absolute;
  top: 100%;
  left: calc(50% - var(--width)/2);
  width: 0.8em;
  height: 0.8em;
  background-color: rgb(44, 0, 114);
  box-shadow: inset 5px 5px 10px rgb(160, 120, 255),
  0px 0px 2px white;
  border-radius: 50px;
  animation: 0.8s ease-in 0s infinite running jump2;
}
#second {
  transform: rotate(90deg);
}
#second::before {
  --width: 0.8em;
  --height: 0.8em;
  content: "";
  position: absolute;
  top: 100%;
  left: calc(50% - var(--width)/2);
  width: 0.8em;
  height: 0.8em;
  background-color: rgb(44, 0, 114);
  box-shadow: inset 5px 5px 10px rgb(160, 120, 255),
  0px 0px 2px white;
  border-radius: 50px;
  animation: 1.5s ease-in 0s infinite running jump2;
}
#third {
  transform: rotate(90deg)
}
#third::before {
  --width: 0.8em;
  --height: 0.8em;
  content: "";
  position: absolute;
  top: 100%;
  left: calc(50% - var(--width)/2);
  width: 0.8em;
  height: 0.8em;
  background-color: rgb(44, 0, 114);
  box-shadow: inset 5px 5px 10px rgb(160, 120, 255),
  0px 0px 2px white;
  border-radius: 50px;
  animation: 1.6s ease-in 0s infinite running jump2;
}
.loader::after {
  --width: 0.8em;
  --height: 0.8em;
  content: "";
  position: absolute;
  top: 100%;
  left: calc(50% - var(--width)/2);
  width: 0.8em;
  height: 0.8em;
  background-color: rgb(44, 0, 114);
  box-shadow: inset 5px 5px 10px rgb(160, 120, 255),
  0px 0px 2px white;
  border-radius: 50px;
  animation: 1.2s ease-in 1s alternate infinite running jump2;
}
@keyframes first682 {
  0% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(0deg);
    transform: rotate(90deg)
  }
  50% {
    transform: rotate(90deg);
    transform: rotate(180deg);
  }
  75% {
    transform: rotate(180deg);
    transform: rotate(270deg)
  }
  100% {
    transform: rotate(270deg);
    transform: rotate(360deg);
  }
}
@keyframes jump2 {
  0% {
    top: 100%;
  }
  25% {
    top: 230%
  }
  50% {
    top: 100%;
  }
  75% {
    height: 0.6em
  }
  100% {
    height: 1em
  }
}
.spinner {
  background-image: linear-gradient(rgb(186, 66, 255) 35%,rgb(0, 225, 255));
  width: 100px;
  height: 100px;
  animation: spinning82341 1.7s linear infinite;
  text-align: center;
  border-radius: 50px;
  filter: blur(1px);
  box-shadow: 0px -5px 20px 0px rgb(186, 66, 255), 0px 5px 20px 0px rgb(0, 225, 255);
}
.spinner1 {
  background-color: rgb(36, 36, 36);
  width: 100px;
  height: 100px;
  border-radius: 50px;
  filter: blur(10px);
}
@keyframes spinning82341 {
  to {
    transform: rotate(360deg);
  }
}
</style>
""", unsafe_allow_html=True)

# --- Streamlit App Layout ---
st.markdown("""
<div class="top-bar">
    <div class="left">🧠 <span>Tunei</span></div>
    <div class="right">⚙️ 🔔 👤</div>
</div>
""", unsafe_allow_html=True)

# Add a spacer below the top bar
st.markdown('<div class="main-content"></div>', unsafe_allow_html=True)


# 🧠 Sidebar Category Selector
with st.sidebar:
    st.markdown("## 💬 Explore by Category", unsafe_allow_html=True)
    st.write("Choose a news topic:")
    category = st.radio("", [
        " ", "Sports", "Entertainment", "Politics", 
        "Music", "Tech", "Business", "Science"
    ])

# spinner
st.markdown("""<div class="spinner">
    <div class="spinner1"></div>
        </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
   <h></h1>
    <p> </p>
</div>
""", unsafe_allow_html=True)

topic = st.text_input(
        "",  # no label
        key="topic",
        placeholder="Type your topic…",
        label_visibility="collapsed"
    )

# 🧠 If a category is selected, use it instead of manual input
final_topic = topic.strip() if topic.strip() else (category if category != "None" else "")  # Simulate clicking generate button

#Generate Button
st.markdown('<div class="stGenerateBtn">', unsafe_allow_html=True)
generate = st.button("➤", key="generate", help="Generate summary")

# --- Core Fetch Functions ---
async def fetch_telegram_posts(query, max_results=5):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient("media_web_session", TELEGRAM_API_ID, TELEGRAM_API_HASH, loop=loop)
    await client.start()
    posts = []
    for channel in TELEGRAM_CHANNELS:
        try:
            msgs = await client.get_messages(channel, search=query, limit=100)
            for msg in msgs[:max_results]:
                if msg.message:
                    posts.append(f"[t/{channel}] {msg.message.replace('\n', ' ')}")
        except:
            continue
    return posts

twitter_client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

def fetch_tweets(query, max_results=10):
    try:
        tweets = twitter_client.search_recent_tweets(query=query, max_results=max_results)
        return [tweet.text for tweet in tweets.data] if tweets.data else []
    except:
        return []

def fetch_reddit_posts(query, max_results=5):
    try:
        url = f"https://api.pushshift.io/reddit/search/submission/?q={query}&size={max_results}"
        data = requests.get(url).json().get("data", [])
        return [f"[r/{p['subreddit']}] {p['title']}" for p in data]
    except:
        return []

def fetch_rss_posts(max_results=5):
    posts = []
    for url in RSS_FEEDS:
        d = feedparser.parse(url)
        for entry in d.entries[:max_results]:
            posts.append(f"[rss] {entry.get('title', '')} ({entry.get('link', '')})")
    return posts

def fetch_serpapi_image_urls(query, count=5):
    try:
        params = {"q": query, "tbm": "isch", "num": count, "api_key": SERPAPI_KEY}
        search = GoogleSearch(params)
        return [img["original"] for img in search.get_dict().get("images_results", [])[:count]]
    except:
        return []

def summarize_with_gpt4(contents, topic):
    joined = "\n".join(contents)
    prompt = f"""You're a professional journalist. Write a concise, real-time news article on "{topic}".
- Use short impactful paragraphs (max 5–6).
- Capture the latest developments and public opinion.
- Include quotes (paraphrased or real) and real events.
\n\n{joined}"""
    
    url = "https://ai-kaniujeffray7064ai233651742665.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-12-01-preview"
    headers = {"Content-Type": "application/json", "api-key": AZURE_OPENAI_API_KEY}
    body = {
        "messages": [
            {"role": "system", "content": "You are a helpful journalist."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    res = requests.post(url, headers=headers, json=body)
    if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"]
    st.error("❌ GPT-4 summary failed")
    return None

spinner_placeholder = st.empty()
# --- Trigger on Button ---
if generate and final_topic:
      spinner_placeholder.markdown("""<div class="loader">
            <div id="first"></div>
            <div id="second"></div>
           </div>""", unsafe_allow_html=True)

with st.spinner("📡..."):
        tweets = fetch_tweets(topic)
        reddit = fetch_reddit_posts(topic)
        telegram = asyncio.run(fetch_telegram_posts(topic))
        rss = fetch_rss_posts()
        combined =  telegram + tweets + reddit + rss
 
        spinner_placeholder.empty()
        # 📰 If no content found, show warning 
        if not combined:
            st.warning("⚠️ No relevant content found.")
        else:
            summary = summarize_with_gpt4(combined, topic)
            paragraphs = summary.strip().split("\n\n")
            image_urls = fetch_serpapi_image_urls(topic, count=len(paragraphs))
            
            # 📰 Render the news summary
            for i, para in enumerate(paragraphs):
                st.markdown('<div class="news-block">', unsafe_allow_html=True)
                if i < len(image_urls):
                    col1, col2 = st.columns([3, 2]) if i % 2 == 0 else st.columns([2, 3])
                    with col1:
                        st.markdown(para)
                    with col2:
                        st.image(image_urls[i], use_container_width=True)
                else:
                    st.markdown(para)
                st.markdown('</div>', unsafe_allow_html=True)
        