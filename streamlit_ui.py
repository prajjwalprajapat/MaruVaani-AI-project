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
def translate_to_marwadi(english_text):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        prompt = (
            "You are an elder from Bikaner, Rajasthan. You speak the pure, authentic Bikaneri Marwadi dialect. "
            "Your task is to translate the following English text into 100% pure Bikaneri Marwadi. "
            "CRITICAL RULES: "
            "1. DO NOT use standard Hindi words. If you use standard Hindi, you fail. "
            "2. 'I'/'Me' becomes 'मैं' or 'मनै'. "
            "3. 'This' becomes 'ओ' (for male objects like Samosa) or 'आ'. "
            "4. 'Want to buy' or 'Want to take' becomes 'लेणो है'. "
            "5. 'What' becomes 'कांई'. 'Where' becomes 'कठै'. "
            "6. Output ONLY the final Bikaneri Marwadi translation in Devanagari script. No quotes, no English explanations.\n\n"
            "EXAMPLES:\n"
            "English: 'I want to buy this Samosa.' -> Marwadi: 'मनै ओ समोसो लेणो है।'\n"
            "English: 'How are you?' -> Marwadi: 'थे कियां हो?' or 'कांई हाल है भायळा?'\n"
            "English: 'Where are you going?' -> Marwadi: 'थे कठै जा रया हो?'\n"
            "English: 'What are you doing?' -> Marwadi: 'थे कांई कर रया हो?'\n\n"
           {
  "Inside": "थू ओ सामान घर में राख दे।",
  "Window": "खड़की बंद कर दे, गर्मी आवे है।",
  "Praise": "वो छोरो थारी घणी तारीफ कर रयो है।",
  "Wait": "म्हारो इंतजार करजो, मैं दस मिनट में आऊँ।",
  "Idea": "मने एक बढ़िया आइडिया आयो है।",
  "To Inform": "थू आ बात घरवालां ने बता दे।",
  "Handicapped": "विकलांग लोगां री मदद करनी चाहिए।",
  "Electricity": "कल बिजली तीन बजे आई थी।",
  "Evening meal": "आज शाम को काई बन्यो है?",
  "To Search": "म्हारो फोन ढूंढ के देख।",
  "Opposite": "वो हमेशा उल्टा ही करे है।",
  "Ginger": "चाय में थोड़ा अदरक डाल दे।",
  "Half": "मने आधा किलो चीनी चाहिए।",
  "West": "सूरज पश्चिम में ढल जावे है।",
  "Tears": "ओ बात सुनके मने रोना आ गयो।",
  "Daily": "मैं रोज सुबह जल्दी उठूँ।",
  "To extinguish": "चूल्हो बंद कर दे।",
  "Bangle": "थारी चूड़ी घणी सुंदर लागे है।",
  "Mother": "मारी माँ मने घणो प्यार करे है।",
  "Cheat": "वो आदमी धोखेबाज है।",
  "Garbage": "कचरो बाहर फेंक दे।",
  "Beside": "म्हारे पास आके बैठ।",
  "Difference": "इन दोनों में घणो फर्क है।",
  "Between": "तुम बीच में मत बोलो।",
  "Button": "म्हारी कमीज रो बटन टूट गयो।",
  "Mind": "आ बात ध्यान में रख।",
  "Excellent": "यो काम घणो बढ़िया है।",
  "To make": "आज रोटी बना ले।",
  "Congratulations": "थाने बधाई हो।",
  "To change": "अपनी आदत बदल ले।",
  "Almond": "रोज बादाम खाया कर।",
  "Wednesday": "मैं बुधवार ने जाऊँगा।",
  "Service": "बड़ों की सेवा करो।",
  "Friend": "वो थारी दोस्त किथे गई?",
  "To use": "म्हारो पेन इस्तेमाल कर ले।",
  "Evening": "शाम हो गई, घर चलो।"
}
"I don't know.": "मने कोनी ठा।"
{
  "What is your name?": "थारो नाम काई है?",
  "How are you?": "थू काई हाल में है?",
  "I am fine.": "मैं ठीक हूँ।",
  "Where do you live?": "थू किथे रहवे है?",
  "What are you doing?": "थू काई कर रियो है?",
  "I am working.": "मैं काम कर रियो हूँ।",
  "Where are you going?": "थू किथे जा रियो है?",
  "I want to buy something.": "मने काई खरीदनो है।",
  "What is the price of this?": "इको भाव काई है?",
  "It is too expensive.": "यो घणो महंगो है।",
  "Have you eaten?": "थू खायो के?",
  "I am hungry.": "मने भूख लागी है।",
  "Give me some water.": "मने पानी देवो।",
  "Where is the market?": "बाजार किथे है?",
  "Come here.": "इधर आवो।",
  "Sit down.": "बैठ जावो।",
  "Wait a minute.": "थोड़ी देर रुक।",
  "Do you know me?": "थू मने जाणे है के?",
  "I don't know.": "मने नीं पता।",
  "Talk to me.": "मने बात करो।",
  "Don't lie.": "झूठ मत बोल।",
  "What's for dinner?": "रात ने काई बन्यो है?",
  "The food is delicious.": "खाणो घणो बढ़िया है।",
  "Do you want more?": "थाने और चाहिए के?",
  "Give me some salt.": "मने थोड़ो नमक देवो।",
  "I don't like this.": "मने यो पसंद नीं।",
  "Let's go eat.": "चालो खावां।",
  "The tea is hot.": "चाय गरम है।",
  "Give me a discount.": "थोड़ा कम करो।",
  "Do you have a bag?": "थारे पास थैलो है के?",
  "I don't have money.": "म्हारे पास पैसा नीं।",
  "Show me another one.": "मने एक और दिखाओ।",
  "This is very good.": "यो घणो बढ़िया है।",
  "Keep the change.": "बाकी थू रख ले।",
  "What time is it?": "कितना बजे है?",
  "It is very hot today.": "आज घणो गरम है।",
  "It might rain.": "बारिश आ सके है।",
  "Come tomorrow.": "कल आवो।",
  "I am late.": "मैं लेट हो गयो।",
  "Wake up early.": "जल्दी उठो।",
  "When will you come?": "थू कद आवेगो?",
  "It's night time.": "रात हो गी है।",
  "Who is at home?": "घर में कूं है?",
  "My mother is calling.": "म्हारी मां बुला री है।",
  "Where is your father?": "थारो बाप किथे है?",
  "He is my brother.": "यो म्हारो भाई है।",
  "Clean the room.": "कमरो साफ करो।",
  "Switch off the light.": "लाइट बंद करो।",
  "Open the door.": "दरवाजो खोलो।",
  "I am very happy.": "मैं घणो खुश हूँ।",
  "Are you angry?": "थू गुस्से में है के?",
  "Don't worry.": "फिकर मत करो।",
  "Help me.": "मने मदद करो।",
  "I am tired.": "मैं थक गयो हूँ।",
  "Everything will be fine.": "सब ठीक हो जावेगो।",
  "I forgot.": "मैं भूल गयो।",
  "Listen to me.": "मने सुनो।",
  "Look at me.": "मने देखो।",
  "Speak loudly.": "जोर से बोलो।",
  "Yes": "हाँ।",
  "No": "ना।",
  "Thank you": "धन्यवाद / थैंक्यू।",
  "Sorry": "माफ करो।",
  "Please": "कृपा करके / प्लीज।",
  "Go away": "इधर सूं जाओ।",
  "Stop it": "बस करो।",
  "Why?": "क्यूं?",
  "How?": "कैसे?",
  "Who?": "कूं?",
  "Where is the hospital?": "हॉस्पिटल किथे है?",
  "Call the doctor.": "डॉक्टर ने फोन करो।",
  "I am not feeling well.": "मने ठीक नीं लागे।",
  "Where can I find a taxi?": "टैक्सी किथे मिलेगी?",
  "Drive slowly.": "धीरे चलाओ।"
}

            f"Now, translate this exactly into Bikaneri Marwadi: '{english_text}'"
        )
        
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
