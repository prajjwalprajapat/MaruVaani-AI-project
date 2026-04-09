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
st.set_page_config(page_title="MaruVaani ai", page_icon="🏜️", layout="wide")

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

        st.error(f"Sarvam API Error: {response.text}")
        return None

    except Exception as e:
        st.error(f"Audio Generation Error: {str(e)}")
        return None

# ==========================================
# 🖥️ STREAMLIT UI
# ==========================================
st.title("MaruVaani ai 🏜️")
st.markdown("Your Ultimate Rajasthan Companion: Translate English to pure Bikaneri Marwadi and explore the state!")

with st.sidebar:
    st.header("⚙️ App Navigation")

    feature = st.selectbox(
        "🔧 Select Feature",
        ["Translator", "District Places Recommendation"]
    )

    st.markdown("---")
    st.header("⚙️ Voice Settings (Translator)")

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

# ==========================================
# 🚀 FEATURE 1: TRANSLATOR
# ==========================================
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

# ==========================================
# 🗺️ FEATURE 2: DISTRICT PLACES RECOMMENDATION
# ==========================================
elif feature == "District Places Recommendation":

    # District Selection on top
    st.subheader("📍 Select a District to Explore")
    district = st.selectbox(
        "Choose District",
        ["Bikaner"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.header(f"🌟 Must Visit Places in {district}")

    # Database of places
    places_data = {
        "Bikaner": [
            {
                "name": "Laxmi Nath Ji Temple",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Laxmi+Nath+Ji+Temple",
                "desc": "One of the oldest temples in Bikaner, built in 1488 by Rao Bika. Dedicated to Lord Vishnu and Goddess Laxmi, it boasts intricate silver artwork and serves as the spiritual center of the city."
            },
            {
                "name": "Junagarh Fort",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Junagarh+Fort",
                "desc": "Built in 1589 by Raja Rai Singh, this impressive fort is one of the few in Rajasthan not built on a hilltop. It features a beautiful amalgamation of Rajput, Mughal, and Gujarati architectural styles."
            },
            {
                "name": "Kodemdesar Bheruji Temple",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Kodemdesar+Temple",
                "desc": "Located slightly outside the city, this unique temple is dedicated to Lord Bhairav. Notably, the temple has no roof, and the sacred idol is placed open to the sky, highly revered by the locals."
            },
            {
                "name": "Devi Kund Sagar",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Devi+Kund+Sagar",
                "desc": "This site houses the royal cenotaphs (chhatris) of the Bikaji dynasty rulers. Each pavilion is beautifully crafted from red sandstone and white marble, displaying exquisite historical Rajput architecture."
            },
            {
                "name": "Bhandasar Jain Temple",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Bhandasar+Jain+Temple",
                "desc": "A spectacular 15th-century temple famous for its vibrant frescoes and leaf paintings. Legend says the foundation was built using 40,000 kilograms of pure ghee instead of water!"
            },
            {
                "name": "Gajner Palace",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Gajner+Palace",
                "desc": "Described as an 'incomparable jewel in the Thar desert', this grand lakeside palace was built by Maharaja Ganga Singh. It served as a hunting resort and is now a beautiful heritage hotel."
            }
        ]
    }

    # Displaying the places in a 2-column layout for a cleaner look
    cols = st.columns(2)

    for idx, place in enumerate(places_data[district]):
        with cols[idx % 2]:
            st.image(place["image"], use_container_width=True)
            st.subheader(place["name"])
            st.write(place["desc"])
            st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 🌟 FOOTER SECTION
# ==========================================
st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:20px;">
        Made with ❤️ by <br>
        Bhupesh Danewa • Prajjwal Prajapat • Aniket Prajapat • Kunal Gahlot
    </div>
    """,
    unsafe_allow_html=True
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

# ==========================================
# 🚀 FEATURE 1: TRANSLATOR
# ==========================================
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

# ==========================================
# 🗺️ FEATURE 2: DISTRICT PLACES RECOMMENDATION
# ==========================================
elif feature == "District Places Recommendation":

    # District Selection on top
    st.subheader("📍 Select a District to Explore")
    district = st.selectbox(
        "Choose District",
        ["Bikaner"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.header(f"🌟 Must Visit Places in {district}")

    # Database of places
    places_data = {
        "Bikaner": [
            {
                "name": "Laxmi Nath Ji Temple",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Laxmi+Nath+Ji+Temple",
                "desc": "One of the oldest temples in Bikaner, built in 1488 by Rao Bika. Dedicated to Lord Vishnu and Goddess Laxmi, it boasts intricate silver artwork and serves as the spiritual center of the city."
            },
            {
                "name": "Junagarh Fort",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Junagarh+Fort",
                "desc": "Built in 1589 by Raja Rai Singh, this impressive fort is one of the few in Rajasthan not built on a hilltop. It features a beautiful amalgamation of Rajput, Mughal, and Gujarati architectural styles."
            },
            {
                "name": "Kodemdesar Bheruji Temple",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Kodemdesar+Temple",
                "desc": "Located slightly outside the city, this unique temple is dedicated to Lord Bhairav. Notably, the temple has no roof, and the sacred idol is placed open to the sky, highly revered by the locals."
            },
            {
                "name": "Devi Kund Sagar",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Devi+Kund+Sagar",
                "desc": "This site houses the royal cenotaphs (chhatris) of the Bikaji dynasty rulers. Each pavilion is beautifully crafted from red sandstone and white marble, displaying exquisite historical Rajput architecture."
            },
            {
                "name": "Bhandasar Jain Temple",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Bhandasar+Jain+Temple",
                "desc": "A spectacular 15th-century temple famous for its vibrant frescoes and leaf paintings. Legend says the foundation was built using 40,000 kilograms of pure ghee instead of water!"
            },
            {
                "name": "Gajner Palace",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Gajner+Palace",
                "desc": "Described as an 'incomparable jewel in the Thar desert', this grand lakeside palace was built by Maharaja Ganga Singh. It served as a hunting resort and is now a beautiful heritage hotel."
            }
        ]
    }

    # Displaying the places in a 2-column layout for a cleaner look
    cols = st.columns(2)

    for idx, place in enumerate(places_data[district]):
        with cols[idx % 2]:
            st.image(place["image"], use_container_width=True)
            st.subheader(place["name"])
            st.write(place["desc"])
            st.markdown("<br>", unsafe_allow_html=True) # Adds a little spacing between rows

# ==========================================
# 🌟 FOOTER SECTION
# ==========================================
st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:20px;">
        Made with ❤️ by <br>
        Bhupesh Danewa • Prajjwal Prajapat • Aniket Prajapat • Kunal Gahlot
    </div>
    """,
    unsafe_allow_html=True
)
        if st.button("Translate"):
        do_something()
    else:  # <-- Aligns perfectly with 'if'
        do_something_else()

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

    for feature_text in upcoming_features:
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
                "desc": "Junagarh Fort is one of the few forts in Rajasthan not built on a hill."
            },
            {
                "name": "Karni Mata Temple",
                "image": "images/karni_mata.jpg",
                "desc": "Also known as the Rat Temple, famous for thousands of rats."
            },
            {
                "name": "Lalgarh Palace",
                "image": "images/lalgarh.jpg",
                "desc": "A grand palace reflecting royal heritage of Bikaner."
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
    <div style="text-align:center; padding:20px;">
        Made with ❤️ by <br>
        Bhupesh Danewa • Prajjwal Prajapat • Aniket Prajapat • Kunal Gahlot
    </div>
    """,
    unsafe_allow_html=True
)
