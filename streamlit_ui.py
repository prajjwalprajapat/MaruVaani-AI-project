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
            "English: 'What is your name?' -> Marwadi: 'थारो नाम कांई है?'"
            "English: 'How are you?' -> Marwadi: 'थे क्यां हो?'"
            "English: 'I am fine.' -> Marwadi: 'मैं ठीक हूँ।'"
            "English: 'Where do you live?' -> Marwadi: 'थे कठे रीयो हो?'"
            "English: 'What are you doing?' -> Marwadi: 'थे कांई कर रया हो?'"
            "English: 'I am working.' -> Marwadi: 'मैं काम कर रयूँ हूँ।'"
            "English: 'Where are you going?' -> Marwadi: 'थे कठे जा रया हो?'"
            "English: 'I want to buy something.' -> Marwadi: 'मने कींई खरीदणों है।'"
            "English: 'What is the price of this?' -> Marwadi: 'ईंरो भाव कांई है?'"
            "English: 'It is too expensive.' -> Marwadi: 'ओ तो घणों मँघो है।'"
            "English: 'Have you eaten?' -> Marwadi: 'थे जीम लिया कांई?'"
            "English: 'I am hungry.' -> Marwadi: 'मने भूख लागी है।'"
            "English: 'Give me some water.' -> Marwadi: 'मने थोड़ो पाणी पावो।'"
            "English: 'Where is the market?' -> Marwadi: 'बजार कठे है?'"
            "English: 'Come here.' -> Marwadi: 'अठै आवो।'"
            "English: 'Sit down.' -> Marwadi: 'बैठ ज्याओ।'"
            "English: 'Wait a minute.' -> Marwadi: 'एक मिंट रुको।'"
            "English: 'Do you know me?' -> Marwadi: 'थे मने ओळखो के?'"
            "English: 'I don't know.' -> Marwadi: 'मने कोनी ठा।'"
            "English: 'Talk to me.' -> Marwadi: 'म्हारे ऊं बात करो।'"
            "English: 'Don't lie.' -> Marwadi: 'झूठ मत बोलो।'"
            "English: 'What's for dinner?' -> Marwadi: 'ब्याळू में कांई बण्यो है?'"
            "English: 'The food is delicious.' -> Marwadi: 'जीमण घणों स्वाद है।'"
            "English: 'Do you want more?' -> Marwadi: 'थाने और चावे कांई?'"
            "English: 'Give me some salt.' -> Marwadi: 'मने थोड़ो लूण दीजो।'"
            "English: 'I don't like this.' -> Marwadi: 'मने ओ कोनी सावे।'"
            "English: 'Let's go eat.' -> Marwadi: 'चालो जीमण चालां।'"
            "English: 'The tea is hot.' -> Marwadi: 'चा ताती है।'"
            "English: 'Give me a discount.' -> Marwadi: 'थोड़ा कम करो सा।'"
            "English: 'Do you have a bag?' -> Marwadi: 'थारे कने थैलो है कांई?'"
            "English: 'I don't have money.' -> Marwadi: 'म्हारे कने पीसा कोनी।'"
            "English: 'Show me another one.' -> Marwadi: 'मने दूजो दिखाओ।'"
            "English: 'This is very good.' -> Marwadi: 'ओ घणों सोवणों है।'"
            "English: 'Keep the change.' -> Marwadi: 'खुल्ला थे ही राख लो।'"
            "English: 'What time is it?' -> Marwadi: 'कतरा बज्या है?'"
            "English: 'It is very hot today.' -> Marwadi: 'आज घणी तावड़ो है।'"
            "English: 'It might rain.' -> Marwadi: 'मे आय सके है।'"
            "English: 'Come tomorrow.' -> Marwadi: 'काले आइजो।'"
            "English: 'I am late.' -> Marwadi: 'मने मोड़ो वे गयो।'"
            "English: 'Wake up early.' -> Marwadi: 'बेगा उठो।'"
            "English: 'When will you come?' -> Marwadi: 'थे कद आवोला?'"
            "English: 'It's night time.' -> Marwadi: 'रात वे गयी है।'"
            "English: 'Who is at home?' -> Marwadi: 'घरे कुण है?'"
            "English: 'My mother is calling.' -> Marwadi: 'म्हारी मा सा बुलावे है।'"
            "English: 'Where is your father?' -> Marwadi: 'थारा बाबो सा कठे है?'"
            "English: 'He is my brother.' -> Marwadi: 'ओ म्हारो भाई है।'"
            "English: 'Clean the room.' -> Marwadi: 'कमरो साफ कर द्यो।'"
            "English: 'Switch off the light.' -> Marwadi: 'लाइट बंद कर द्यो।'"
            "English: 'Open the door.' -> Marwadi: 'किवाड़ खोलो।'"
            "English: 'I am very happy.' -> Marwadi: 'मैं घणों राजी हूँ।'"
            "English: 'Are you angry?' -> Marwadi: 'थे रीस कर रया हो कांई?'"
            "English: 'Don't worry.' -> Marwadi: 'फिकर मत करो।'"
            "English: 'Help me.' -> Marwadi: 'म्हारी मदद करो।'"
            "English: 'I am tired.' -> Marwadi: 'मैं थक गयो हूँ।'"
            "English: 'Everything will be fine.' -> Marwadi: 'सगळो ठीक वे जावेला।'"
            "English: 'I forgot.' -> Marwadi: 'मैं भूल गयो।'"
            "English: 'Listen to me.' -> Marwadi: 'म्हारी बात सुणो।'"
            "English: 'Look at me.' -> Marwadi: 'म्हारो सामी देखो।'"
            "English: 'Speak loudly.' -> Marwadi: 'जोर ऊं बोलो।'"
            "English: 'Yes' -> Marwadi: 'हां।'"
            "English: 'No' -> Marwadi: 'कोनी।'"
            "English: 'Thank you' -> Marwadi: 'थारो घणों मान।'"
            "English: 'Sorry' -> Marwadi: 'मने माफ करजो।'"
            "English: 'Please' -> Marwadi: 'सा / विनती है।'"
            "English: 'Go away' -> Marwadi: 'अठै ऊं जाओ।'"
            "English: 'Stop it' -> Marwadi: 'बस करो।'"
            "English: 'Why?' -> Marwadi: 'क्यूँ?'"
            "English: 'How?' -> Marwadi: 'कींया?'"
            "English: 'Who?' -> Marwadi: 'कुण?'"
            "English: 'Where is the hospital?' -> Marwadi: 'अस्पताल कठे है?'"
            "English: 'Call the doctor.' -> Marwadi: 'डाक्टर ने फोन करो।'"
            "English: 'I am not feeling well.' -> Marwadi: 'म्हारे जीव ने ठीक कोनी लागे।'"
            "English: 'Where can I find a taxi?' -> Marwadi: 'टैक्सी कठे मिलेला?'"
            "English: 'Drive slowly.' -> Marwadi: 'गाड़ी धीरे चलाओ।'"
            "English: 'Why?' -> Marwadi: 'क्यूँ?'"
            "English: 'How?' -> Marwadi: 'कांई रीती?'"
            "English: 'Who?' -> Marwadi: 'कुण?'"
            "English: 'What?' -> Marwadi: 'कांई?'"
"English: 'Where?' -> Marwadi: 'कठै?'"
"English: 'When?' -> Marwadi: 'कद?'"
"English: 'Yes' -> Marwadi: 'हां।'"
"English: 'No' -> Marwadi: 'कोनी।'"
"English: 'Come' -> Marwadi: 'आवो।'"
"English: 'Go' -> Marwadi: 'जाओ।'"
"English: 'Sit' -> Marwadi: 'बैठो।'"
"English: 'Stand' -> Marwadi: 'उभो रहो।'"
"English: 'Eat' -> Marwadi: 'जीमो।'"
"English: 'Drink' -> Marwadi: 'पीओ।'"
"English: 'Open' -> Marwadi: 'खोलो।'"
"English: 'Close' -> Marwadi: 'बंद करो।'"
"English: 'Stop' -> Marwadi: 'बस करो।'"
"English: 'Wait' -> Marwadi: 'रुको।'"
"English: 'Give' -> Marwadi: 'देवो।'"
"English: 'Take' -> Marwadi: 'लेवो।'"
"English: 'Bring' -> Marwadi: 'ल्याओ।'"
"English: 'Water' -> Marwadi: 'पाणी।'"
"English: 'Food' -> Marwadi: 'जीमण।'"
"English: 'Tea' -> Marwadi: 'चा।'"
"English: 'Milk' -> Marwadi: 'दूध।'"
"English: 'House' -> Marwadi: 'घरो।'"
"English: 'Room' -> Marwadi: 'कमरो।'"
"English: 'Door' -> Marwadi: 'किवाड़।'"
"English: 'Window' -> Marwadi: 'खड़की।'"
"English: 'Mother' -> Marwadi: 'माँ / बाई।'"
"English: 'Father' -> Marwadi: 'बाबो।'"
"English: 'Brother' -> Marwadi: 'भाई।'"
"English: 'Sister' -> Marwadi: 'बहिण।'"
"English: 'Friend' -> Marwadi: 'मीत।'"
"English: 'People' -> Marwadi: 'मनखा।'"
"English: 'Good' -> Marwadi: 'बड़िया।'"
"English: 'Bad' -> Marwadi: 'खराब।'"
"English: 'Big' -> Marwadi: 'मोटो।'"
"English: 'Small' -> Marwadi: 'नानो।'"
"English: 'Hot' -> Marwadi: 'तातो।'"
"English: 'Cold' -> Marwadi: 'ठंडो।'"
"English: 'Today' -> Marwadi: 'आज।'"
"English: 'Tomorrow' -> Marwadi: 'काले।'"
"English: 'Yesterday' -> Marwadi: 'गैला दिन।'"
"English: 'Now' -> Marwadi: 'हाळे।'"
"English: 'Later' -> Marwadi: 'पाछो।'"
"English: 'Money' -> Marwadi: 'पीसा।'"
"English: 'Market' -> Marwadi: 'बजार।'"
"English: 'Help' -> Marwadi: 'मदद।'"
"English: 'Work' -> Marwadi: 'काम।'"
"English: 'Happy' -> Marwadi: 'राजी।'"
"English: 'Sad' -> Marwadi: 'उदास।'"
"English: 'Fast' -> Marwadi: 'तेज।'"
"English: 'Slow' -> Marwadi: 'धीरे।'"
            f"Now, translate this exactly into Bikaneri Marwadi: '{english_text}'"
        )
def translate_to_marwadi(english_text):
    client = Groq(api_key=GROQ_API_KEY)

    try:
        prompt = f"Translate this into pure Bikaneri Marwadi: '{english_text}'"

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

with st.sidebar:
    st.header("⚙️ Voice Settings")

    # -------------------------------
    # FEATURE SWITCHER (NEW)
    # -------------------------------
    feature = st.selectbox(
        "🔧 Select Feature",
        ["Translator", "Visiting Places"]
    )

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

    st.markdown("---")

    st.header("🚀 Coming Soon")
    st.caption("We are working on making MaruVaani your ultimate Rajasthan companion!")

    upcoming_features = [
        "🗺️ **Personalized Tourist Guide**: AI-powered local insights.",
        "📍 **District Recommendations**: Best places to visit in your area.",
        "🍽️ **Local Food Finder**: Discover authentic Marwadi cuisine.",
        "📜 **History Mode**: Narrating the legends of Rajasthan's forts."
    ]

    for feature_text in upcoming_features:   # ✅ FIXED
        st.info(feature_text)

    st.markdown("---")


# Main UI
if feature == "Translator":

    st.subheader("1. Enter English Text")

    english_input = st.text_area(
        "Type the English text you want to translate:",
        height=100,
        label_visibility="collapsed"
    )

    if st.button("Translate to Bikaneri ⚡", type="primary"):
        if english_input.strip():
            with st.spinner("Translating at lightning speed..."):
                translation = translate_to_marwadi(english_input)
                if translation:
                    st.session_state.marwadi_text = translation
        else:
            st.warning("Please enter some text to translate.")

    st.divider()

    st.subheader("2. Bikaneri Marwadi Translation")
    st.markdown("*(Review & Edit the translation below before generating audio)*")

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
                    st.audio(audio_bytes, format="audio/wav")

                    st.download_button(
                        label="💾 Download .wav File",
                        data=audio_bytes,
                        file_name="maruvaani_audio.wav",
                        mime="audio/wav"
                    )
        else:
            st.warning("Please ensure there is Marwadi text to speak.")


elif feature == "Visiting Places":

    st.sidebar.title("📍 Select District")

    district = st.sidebar.selectbox(
        "Choose District",
        ["Bikaner"]
    )

    places_data = {
        "Bikaner": [
            {
                "name": "Junagarh Fort",
                "image": "images/junagarh.jpg",
                "desc": "Junagarh Fort is one of the few forts in Rajasthan not built on a hill. Built in 1589, it is known for its beautiful palaces, temples, and intricate architecture."
            },
            {
                "name": "Karni Mata Temple",
                "image": "images/karni_mata.jpg",
                "desc": "Also known as the Rat Temple, it is famous for thousands of rats living freely inside. It is a unique spiritual and cultural attraction."
            },
            {
                "name": "Lalgarh Palace",
                "image": "images/lalgarh.jpg",
                "desc": "A grand palace built in Indo-Saracenic style architecture. It reflects the royal heritage of Bikaner."
            }
        ]
    }

    st.title("🏜️ Visiting Places")
    st.write(f"Showing places in **{district}**")

    cols = st.columns(3)

    for idx, place in enumerate(places_data[district]):
        with cols[idx % 3]:
            st.image(place["image"], use_container_width=True)
            st.subheader(place["name"])
            st.write(place["desc"])
            st.markdown("---")


# ==========================================
# 🌟 FOOTER SECTION
# ==========================================
st.divider()

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
        color: #808495;
        font-family: 'Inter', sans-serif;
    }
    .heart {
        color: #ff4b4b;
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
