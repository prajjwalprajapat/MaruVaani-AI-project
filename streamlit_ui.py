import streamlit as st
import requests
import base64
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==========================================
# ⚙️ APP CONFIGURATION
# ==========================================
st.set_page_config(page_title="MaruVaani ai", page_icon="🏜️", layout="centered")

# Retrieve API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

# Initialize Session State for the translated text
if "marwadi_text" not in st.session_state:
    st.session_state.marwadi_text = ""

# ==========================================
# 🧠 HELPER FUNCTIONS
# ==========================================
from groq import Groq

client = Groq(api_key=GROQ_API_KEY)
# ✅ Local Dictionary (keep OUTSIDE prompt)
LOCAL_DICT = {
    "Inside": "थू ओ सामान घर में राख दे।",
    "Window": "खड़की बंद कर दे, गर्मी आवे है।",
    "Praise": "वो छोरो थारी घणी तारीफ कर रयो है।",
    "Wait": "म्हारो इंतजार करजो, मैं दस मिनट में आऊँ।",
    "Idea": "मने एक बढ़िया आइडिया आयो है।",
    "To Inform": "थू आ बात घरवालां ने बता दे।",
    "Electricity": "कल बिजली तीन बजे आई थी।",
    "Evening meal": "आज शाम को काई बन्यो है?",
    "To Search": "म्हारो फोन ढूंढ के देख।",
    "Opposite": "वो हमेशा उल्टा ही करे है।",
    "Ginger": "चाय में थोड़ा अदरक डाल दे।",
    "Half": "मने आधा किलो चीनी चाहिए।",
    "West": "सूरज पश्चिम में ढल जावे है।",
    "Daily": "मैं रोज सुबह जल्दी उठूँ।",
    "Bangle": "थारी चूड़ी घणी सुंदर लागे है।",
    "Mother": "मारी माँ मने घणो प्यार करे है।",
    "Garbage": "कचरो बाहर फेंक दे।",
    "Friend": "वो थारी दोस्त किथे गई?",
    "Evening": "शाम हो गई, घर चलो।",

    # Extra phrases
    "What is your name?": "थारो नाम काई है?",
    "How are you?": "थू काई हाल में है?",
    "Where are you going?": "थू किथे जा रियो है?",
    "What are you doing?": "थू काई कर रियो है?",
    "I don't know": "मने कोनी ठा।"
}

# 🔥 FINAL FUNCTION
def translate_to_marwadi(english_text):
    try:
        # ✅ Step 1: Local dictionary check
        if english_text in LOCAL_DICT:
            return LOCAL_DICT[english_text]

        # ✅ Step 2: AI fallback
        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""
You are an elder from Bikaner, Rajasthan.
You speak pure, simple Bikaneri Marwadi.

TASK:
Translate English to natural Marwadi.

RULES:
- Use simple बोलचाल Marwadi
- Avoid heavy Hindi
- Keep it short and natural
- Output ONLY Marwadi text

EXAMPLES:
I want to buy this → मनै ओ लेणो है।
How are you? → थे कियां हो?
Where are you going? → थे कठै जा रया हो?
What are you doing? → थे कांई कर रया हो?

Now translate:
{english_text}
"""

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {str(e)}"
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Groq Translation Error: {str(e)}")
        return None

def generate_tts_audio(marwadi_text, voice_code):
    try:
        url = "https://api.sarvam.ai/text-to-speech"
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": [marwadi_text],
            "target_language_code": "hi-IN",
            "speaker": voice_code,
            "pace": 1.05, 
            "speech_sample_rate": 8000,
            "enable_preprocessing": True,
            "model": "bulbul:v3"
        }

        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            audio_base64 = response.json()["audios"][0]
            return base64.b64decode(audio_base64)
        else:
            st.error(f"Sarvam API Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Audio Generation Error: {str(e)}")
        return None

# ==========================================
# 🖥️ STREAMLIT UI
# ==========================================
st.title("MaruVaani ai 🏜️")
st.markdown("Translate English to pure Bikaneri Marwadi and generate lifelike AI speech.")

# Sidebar Settings
# ==========================================
# ⚙️ SIDEBAR (Settings & Roadmap)
# ==========================================
with st.sidebar:
    st.header("⚙️ Voice Settings")
    
    if not GROQ_API_KEY or not SARVAM_API_KEY:
        st.error("⚠️ API Keys missing! Please check your .env file.")
        st.stop()
    else:
        st.success("✅ API Keys loaded.")

    voice_options = {
        "Ritu (Female)": "ritu",
        "Aditya (Male)": "aditya",
        "Priya (Female)": "priya",
        "Amit (Male)": "amit"
    }
    selected_voice_label = st.selectbox("🗣️ Select Voice Model", list(voice_options.keys()))
    selected_voice_code = voice_options[selected_voice_label]

    st.markdown("---") # Visual separator

    # 🚀 UPCOMING FEATURES SECTION
    st.header("🚀 Coming Soon")
    st.caption("We are working on making MaruVaani your ultimate Rajasthan companion!")
    
    upcoming_features = [
        "🗺️ **Personalized Tourist Guide**: AI-powered local insights.",
        "📍 **District Recommendations**: Best places to visit in your area.",
        "🍽️ **Local Food Finder**: Discover authentic Marwadi cuisine.",
        "📜 **History Mode**: Narrating the legends of Rajasthan's forts."
    ]

    for feature in upcoming_features:
        st.info(feature)

    st.markdown("---")

# Main Area - Step 1
st.subheader("1. Enter English Text")
english_input = st.text_area("Type the English text you want to translate:", height=100, label_visibility="collapsed")

if st.button("Translate to Bikaneri ⚡", type="primary"):
    if english_input.strip():
        with st.spinner("Translating at lightning speed..."):
            translation = translate_to_marwadi(english_input)
            if translation:
                st.session_state.marwadi_text = translation
    else:
        st.warning("Please enter some text to translate.")

st.divider()

# Main Area - Step 2
st.subheader("2. Bikaneri Marwadi Translation")
st.markdown("*(Review & Edit the translation below before generating audio)*")

# Use session state to populate the text area, but allow the user to edit it
edited_marwadi = st.text_area(
    "Edit Marwadi Text:", 
    value=st.session_state.marwadi_text, 
    height=120, 
    label_visibility="collapsed"
)

if st.button("Generate & Speak 🔊", type="primary"):
    if edited_marwadi.strip():
        with st.spinner(f"Generating human-like audio using {selected_voice_label}..."):
            audio_bytes = generate_tts_audio(edited_marwadi, selected_voice_code)
            
            if audio_bytes:
                st.success("Audio generated successfully!")
                
                # Streamlit's native audio player
                st.audio(audio_bytes, format="audio/wav")
                
                # Native download button (replaces the "Save to Disk" checkbox logic)
                st.download_button(
                    label="💾 Download .wav File",
                    data=audio_bytes,
                    file_name="maruvaani_audio.wav",
                    mime="audio/wav"
                )
    else:
        st.warning("Please ensure there is Marwadi text to speak.")


# ==========================================
# 🌟 FOOTER SECTION
# ==========================================
st.divider() # Adds a clean thematic line

st.markdown(
    """
    <style>
    .footer-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px 0px 10px 0px;
        text-align: center;
    }
    .footer-text {
        font-size: 15px;
        color: #808495; /* Subtle gray that works in light/dark mode */
        font-family: 'Inter', sans-serif;
    }
    .heart {
        color: #ff4b4b; /* Streamlit's primary red/pink */
        font-size: 16px;
    }
    .team-names {
        font-weight: 600;
        background: -webkit-linear-gradient(45deg, #4b61ff, #ff4b4b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>

    <div class="footer-container">
        <p class="footer-text">
            Made with <span class="heart">❤️</span> by <br>
            <span class="team-names">Bhupesh Danewa • Prajjwal Prajapat • Aniket Prajapat • Kunal Gahlot</span>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
