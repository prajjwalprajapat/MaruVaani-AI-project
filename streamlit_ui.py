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
            "3. 'This' becomes 'ओ' (for male objects) or 'आ' (for female objects). "
            "4. 'Want to buy' or 'Want to take' becomes 'लेणो है'. "
            "5. 'What' becomes 'कांई'. 'Where' becomes 'कठै'. "
            "6. Output ONLY the final Bikaneri Marwadi translation in Devanagari script. No quotes, no English explanations.\n\n"
            "EXAMPLES:\n"
            
            # --- General Basics & Greetings ---
            "English: 'I want to buy this Samosa.' -> Marwadi: 'मनै ओ समोसो लेणो है।'\n"
            "English: 'How are you?' -> Marwadi: 'थे कियां हो?' or 'कांई हाल है भायळा?'\n"
            "English: 'Where are you going?' -> Marwadi: 'थे कठै जा रया हो?'\n"
            "English: 'What are you doing?' -> Marwadi: 'थे कांई कर रया हो?'\n"
            "English: 'What is your name?' -> Marwadi: 'थारो नाम कांई है?'\n"
            "English: 'I am fine.' -> Marwadi: 'मैं ठीक हूँ।'\n"
            "English: 'Where do you live?' -> Marwadi: 'थे कठे रीयो हो?'\n"
            "English: 'I am working.' -> Marwadi: 'मैं काम कर रयूँ हूँ।'\n"
            "English: 'I want to buy something.' -> Marwadi: 'मने कींई खरीदणों है।'\n"
            "English: 'What is the price of this?' -> Marwadi: 'ईंरो भाव कांई है?'\n"
            "English: 'It is too expensive.' -> Marwadi: 'ओ तो घणों मँघो है।'\n"
            "English: 'Have you eaten?' -> Marwadi: 'थे जीम लिया कांई?'\n"
            "English: 'I am hungry.' -> Marwadi: 'मने भूख लागी है।'\n"
            "English: 'Give me some water.' -> Marwadi: 'मने थोड़ो पाणी पावो।'\n"
            "English: 'Where is the market?' -> Marwadi: 'बजार कठे है?'\n"
            "English: 'Come here.' -> Marwadi: 'अठै आवो।'\n"
            "English: 'Sit down.' -> Marwadi: 'बैठ ज्याओ।'\n"
            "English: 'Wait a minute.' -> Marwadi: 'एक मिंट रुको।'\n"
            
            # --- Askatics & Stratos Summer Program ---
            "English: 'Welcome to Askatics.' -> Marwadi: 'अस्काटिक्स में थारो घणों मान है।'\n"
            "English: 'Askatics is a great company.' -> Marwadi: 'अस्काटिक्स एक घणी चोखी कंपनी है।'\n"
            "English: 'We are learning at Askatics.' -> Marwadi: 'म्हे अस्काटिक्स में सीख रया हां।'\n"
            "English: 'Join Stratos Summer Program to improve your skills.' -> Marwadi: 'थारी होशियारी बढावण खातिर स्ट्रैटोस समर प्रोग्राम में जुड़ो।'\n"
            "English: 'Stratos Summer Program will teach you new things.' -> Marwadi: 'स्ट्रैटोस समर प्रोग्राम थाने नवीं चीजां सिखावेला।'\n"
            "English: 'Have you registered for the summer program?' -> Marwadi: 'थे समर प्रोग्राम सारू नाम लिखायो कांई?'\n"
            "English: 'The classes start next week.' -> Marwadi: 'क्लासां अगले हफ्ते ऊं चालू वेवेला।'\n"
            "English: 'You will get a certificate.' -> Marwadi: 'थाने एक सर्टिफिकेट मिलेला।'\n"
            "English: 'This training is very important.' -> Marwadi: 'आ ट्रेनिंग घणी जरूरी है।'\n"
            "English: 'Stratos program is for students.' -> Marwadi: 'स्ट्रैटोस प्रोग्राम टाबरां सारू है।'\n"
            "English: 'Improve your practical knowledge.' -> Marwadi: 'थारो काम रो ग्यान बढ़ाओ।'\n"
            "English: 'Our mentors are very helpful.' -> Marwadi: 'म्हारा गुरुजी घणी मदद करे है।'\n"
            "English: 'Don't miss this opportunity.' -> Marwadi: 'आ मौको मत गमावजो।'\n"
            "English: 'Register on the website today.' -> Marwadi: 'आज ही वेबसाइट माथे नाम लिखाय द्यो।'\n"

            # --- AI, IoT & Emerging Technology ---
            "English: 'What is Artificial Intelligence?' -> Marwadi: 'आ एआई (AI) कांई वेवे है?'\n"
            "English: 'AI will change the world.' -> Marwadi: 'एआई आखी दुनिया ने बदल देवेला।'\n"
            "English: 'IoT connects things to the internet.' -> Marwadi: 'आईओटी (IoT) चीजां ने इंटरनेट ऊं जोड़े है।'\n"
            "English: 'This is a smart device.' -> Marwadi: 'ओ एक स्मार्ट मशीन है।'\n"
            "English: 'Machine Learning is interesting.' -> Marwadi: 'मशीन लर्निंग घणी सोवणी लागे है।'\n"
            "English: 'We are building an AI model.' -> Marwadi: 'म्हे एक एआई मॉडल बणा रया हां।'\n"
            "English: 'Cloud computing is fast.' -> Marwadi: 'क्लाउड कंप्यूटिंग घणी तेज है।'\n"
            "English: 'Save the data on the cloud.' -> Marwadi: 'डेटा ने क्लाउड माथे सेव कर द्यो।'\n"
            "English: 'The system is updating.' -> Marwadi: 'सिस्टम अपडेट वे रयो है।'\n"
            "English: 'Internet speed is slow.' -> Marwadi: 'इंटरनेट री स्पीड हळवी है।'\n"
            "English: 'Connect the Wi-Fi.' -> Marwadi: 'वाई-फाई जोड़ द्यो।'\n"
            "English: 'Your phone is ringing.' -> Marwadi: 'थारो फोन बाज रयो है।'\n"
            "English: 'Data science is the future.' -> Marwadi: 'डेटा साइंस ही आग्लो बखत है।'\n"
            "English: 'The server is down.' -> Marwadi: 'सर्वर बंद पड़्यो है।'\n"
            "English: 'Restart the computer.' -> Marwadi: 'कंप्यूटर ने पाछो चालू करो।'\n"
            "English: 'This app uses AI.' -> Marwadi: 'ईं ऐप में एआई रो काम वेवे है।'\n"

            # --- Sensors, Electronics & Hardware ---
            "English: 'Where is the sensor?' -> Marwadi: 'सेंसर कठै है?'\n"
            "English: 'The sensor is not working.' -> Marwadi: 'सेंसर काम कोनी कर रयो है।'\n"
            "English: 'This is a temperature sensor.' -> Marwadi: 'ओ तावड़ो (तापमान) नापण रो सेंसर है।'\n"
            "English: 'Attach the motion sensor here.' -> Marwadi: 'मोशन सेंसर अठै लगा द्यो।'\n"
            "English: 'Connect the ultrasonic sensor.' -> Marwadi: 'अल्ट्रासोनिक सेंसर जोड़ द्यो।'\n"
            "English: 'The humidity sensor is broken.' -> Marwadi: 'नमी नापण आळो सेंसर टूट गयो है।'\n"
            "English: 'Connect the wires carefully.' -> Marwadi: 'तारां ने ध्यान ऊं जोड़ो।'\n"
            "English: 'The battery is dead.' -> Marwadi: 'बैटरी खतम वे गी।'\n"
            "English: 'Charge the battery.' -> Marwadi: 'बैटरी चार्ज कर लो।'\n"
            "English: 'Start the motor.' -> Marwadi: 'मोटर चालू कर द्यो।'\n"
            "English: 'Stop the machine.' -> Marwadi: 'मशीन रोक द्यो।'\n"
            "English: 'The circuit is shorted.' -> Marwadi: 'सर्किट शॉर्ट वे गयो है।'\n"
            "English: 'Use the soldering iron.' -> Marwadi: 'सोल्डरिंग आयरन रो काम में ल्यो।'\n"
            "English: 'Check the voltage.' -> Marwadi: 'वोल्टेज चेक कर ल्यो।'\n"
            "English: 'Turn on the switch.' -> Marwadi: 'बटन चालू कर द्यो।'\n"
            "English: 'The LED is glowing.' -> Marwadi: 'एलईडी (LED) चस रयी है।'\n"
            "English: 'Send the signal.' -> Marwadi: 'सिग्नल भेज द्यो।'\n"
            "English: 'The connection is loose.' -> Marwadi: 'कनेक्शन ढीलो है।'\n"
            "English: 'Fix the hardware.' -> Marwadi: 'हार्डवेयर ने ठीक करो।'\n"
            "English: 'I need a breadboard.' -> Marwadi: 'मने एक ब्रेडबोर्ड चावे।'\n"
            "English: 'Plug in the Arduino.' -> Marwadi: 'आर्डिनो (Arduino) ने लगाओ।'\n"

            # --- Robotics & Drones ---
            "English: 'The robot is moving.' -> Marwadi: 'रोबोट चाल रयो है।'\n"
            "English: 'I am making a drone.' -> Marwadi: 'मैं एक ड्रोन बणा रयूँ हूँ।'\n"
            "English: 'The drone is flying high.' -> Marwadi: 'ड्रोन घणों ऊंचो उड़ रयो है।'\n"
            "English: 'Program the robot to walk.' -> Marwadi: 'रोबोट ने चालण रो कोड लगाओ।'\n"
            "English: 'The motor speed is too fast.' -> Marwadi: 'मोटर री स्पीड घणी तेज है।'\n"
            "English: 'Attach the wheels.' -> Marwadi: 'पहिया लगा द्यो।'\n"
            
            # --- Coding, Software Engineering & Academics ---
            "English: 'Write the code.' -> Marwadi: 'कोड लिखो।'\n"
            "English: 'There is a bug in the code.' -> Marwadi: 'कोड में कींई मिस्टेक (बग) है।'\n"
            "English: 'The code is compiling.' -> Marwadi: 'कोड चाल रयो है।'\n"
            "English: 'Run the program.' -> Marwadi: 'प्रोग्राम ने चलाओ।'\n"
            "English: 'Learn Python programming.' -> Marwadi: 'पायथन (Python) कोडिंग सीखो।'\n"
            "English: 'Open the laptop.' -> Marwadi: 'लैपटॉप खोलो।'\n"
            "English: 'The screen is broken.' -> Marwadi: 'स्क्रीन टूट गी है।'\n"
            "English: 'I am an engineer.' -> Marwadi: 'मैं एक इंजीनियर हूँ।'\n"
            "English: 'Submit the project.' -> Marwadi: 'प्रोजेक्ट जमा करा द्यो।'\n"
            "English: 'When is the deadline?' -> Marwadi: 'लास्ट डेट कद री है?'\n"
            "English: 'I have an exam tomorrow.' -> Marwadi: 'काले म्हारो पेपर है।'\n"
            "English: 'Study hard.' -> Marwadi: 'डट र पढ़ाई करो।'\n"
            "English: 'I got good marks.' -> Marwadi: 'म्हारे चोखा नंबर आया है।'\n"
            "English: 'Let's do a group study.' -> Marwadi: 'चालो भेळा बैठ र पढ़ां।'\n"
            "English: 'The college is closed today.' -> Marwadi: 'आज कॉलेज री छुट्टी है।'\n"
            "English: 'Who is the professor?' -> Marwadi: 'प्रोफेसर सा कुण है?'\n"
            "English: 'I need an internship.' -> Marwadi: 'मने इंटर्नशिप री जरूरत है।'\n"
            "English: 'Apply for the job.' -> Marwadi: 'नौकरी सारू फॉर्म लगा द्यो।'\n"
            "English: 'Innovation is necessary.' -> Marwadi: 'नवीं चीजां बणावणो जरूरी है।'\n"
            "English: 'We are a great team.' -> Marwadi: 'आपां एक घणी चोखी टीम हां।'\n"
            
            # --- Extended Conversational Marwadi ---
            "English: 'Do you know me?' -> Marwadi: 'थे मने ओळखो के?'\n"
            "English: 'I don't know.' -> Marwadi: 'मने कोनी ठा।'\n"
            "English: 'Don't lie.' -> Marwadi: 'झूठ मत बोलो।'\n"
            "English: 'What's for dinner?' -> Marwadi: 'ब्याळू में कांई बण्यो है?'\n"
            "English: 'The food is delicious.' -> Marwadi: 'जीमण घणों स्वाद है।'\n"
            "English: 'Give me a discount.' -> Marwadi: 'थोड़ा कम करो सा।'\n"
            "English: 'Keep the change.' -> Marwadi: 'खुल्ला थे ही राख लो।'\n"
            "English: 'It might rain.' -> Marwadi: 'मे आय सके है।'\n"
            "English: 'Come tomorrow.' -> Marwadi: 'काले आइजो।'\n"
            "English: 'I am late.' -> Marwadi: 'मने मोड़ो वे गयो।'\n"
            "English: 'Wake up early.' -> Marwadi: 'बेगा उठो।'\n"
            "English: 'Are you angry?' -> Marwadi: 'थे रीस कर रया हो कांई?'\n"
            "English: 'Don't worry.' -> Marwadi: 'फिकर मत करो।'\n"
            "English: 'Everything will be fine.' -> Marwadi: 'सगळो ठीक वे जावेला।'\n"
            "English: 'I forgot.' -> Marwadi: 'मैं भूल गयो।'\n"
            "English: 'Where is the hospital?' -> Marwadi: 'अस्पताल कठे है?'\n"
            "English: 'Call the doctor.' -> Marwadi: 'डाक्टर ने फोन करो।'\n"
            "English: 'I am not feeling well.' -> Marwadi: 'म्हारे जीव ने ठीक कोनी लागे।'\n"
            "English: 'Drive slowly.' -> Marwadi: 'गाड़ी धीरे चलाओ।'\n"

            f"\nNow, taking inspiration from all the tech, engineering, and cultural vocabulary provided above, translate this exactly into pure Bikaneri Marwadi: '{english_text}'"
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

with st.sidebar:
    st.header("⚙️ App Navigation")

    feature = st.selectbox(
        "🔧 Select Feature",
        ["Translator", "District Places Recommendation"]
    )
    
    st.markdown("---")
    
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

    st.markdown("---")

# Main UI Routing
if feature == "Translator":
    st.markdown("Translate English to pure Bikaneri Marwadi and generate lifelike AI speech.")

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

elif feature == "District Places Recommendation":
    st.markdown("Discover the rich history and beautiful places across Rajasthan.")
    
    st.subheader("📍 Select a District to Explore")
    district = st.selectbox(
        "Choose District",
        ["Bikaner"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.header(f"🌟 Must Visit Places in {district}")

    places_data = {
        "Bikaner": [
            {
                "name": "Laxmi Nath Ji Temple",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Laxminath-Temple_in_Bikaner.jpg?width=600",
                "desc": "One of the oldest temples in Bikaner, built in 1488 by Rao Bika. Dedicated to Lord Vishnu and Goddess Laxmi, it is the spiritual center of the city."
            },
            {
                "name": "Junagarh Fort",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Junagarh_fort_,_bikaner.jpg?width=600",
                "desc": "Built in 1589 by Raja Rai Singh, this impressive fort is one of the few in Rajasthan not built on a hilltop. It features a beautiful amalgamation of architectural styles."
            },
            {
                "name": "Kodemdesar Bheruji Temple",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Junagarh_Fort,Bikaner_01.jpg?width=600",
                "desc": "This unique temple is dedicated to Lord Bhairav. Notably, the temple has no roof, and the sacred idol is placed open to the sky, highly revered by locals."
            },
            {
                "name": "Devi Kund Sagar",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Devi_Kund_Sagar_and_Cenotaphs,_Bikaner.jpg?width=600",
                "desc": "This site houses the royal cenotaphs (chhatris) of the Bikaji dynasty rulers. Each pavilion is beautifully crafted, displaying exquisite historical Rajput architecture."
            },
            {
                "name": "Bhandasar Jain Temple",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Bhandasar_Jain_Temple_Bikaner_Rajasthan_DSC_9641.jpg?width=600",
                "desc": "A spectacular 15th-century temple famous for its vibrant frescoes. Legend says the foundation was built using 40,000 kilograms of pure ghee instead of water!"
            },
            {
                "name": "Gajner Palace",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Gajner_Palace_-_panoramio.jpg?width=600",
                "desc": "Described as an 'incomparable jewel in the Thar desert', this grand lakeside palace was built by Maharaja Ganga Singh and served as a hunting resort."
            }
        ]
    }

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
        <p            "English: 'Thank you' -> Marwadi: 'थारो घणों मान।'\n"
            "English: 'Sorry' -> Marwadi: 'मने माफ करजो।'\n"
            "English: 'Please' -> Marwadi: 'सा / विनती है।'\n"
            "English: 'Go away' -> Marwadi: 'अठै ऊं जाओ।'\n"
            "English: 'Stop it' -> Marwadi: 'बस करो।'\n"
            "English: 'Where is the hospital?' -> Marwadi: 'अस्पताल कठे है?'\n"
            "English: 'Call the doctor.' -> Marwadi: 'डाक्टर ने फोन करो।'\n"
            "English: 'I am not feeling well.' -> Marwadi: 'म्हारे जीव ने ठीक कोनी लागे।'\n"
            "English: 'Where can I find a taxi?' -> Marwadi: 'टैक्सी कठे मिलेला?'\n"
            "English: 'Drive slowly.' -> Marwadi: 'गाड़ी धीरे चलाओ।'\n"
            # --- AskAtics & Stratos Summer Program ---
            "English: 'Welcome to Askatics.' -> Marwadi: 'अस्काटिक्स में थारो घणों मान है।'\n"
            "English: 'Askatics is a great company.' -> Marwadi: 'अस्काटिक्स एक घणी चोखी कंपनी है।'\n"
            "English: 'Join Stratos Summer Program to improve your skills.' -> Marwadi: 'थारी होशियारी बढावण खातिर स्ट्रैटोस समर प्रोग्राम में जुड़ो।'\n"
            "English: 'Stratos Summer Program will teach you new things.' -> Marwadi: 'स्ट्रैटोस समर प्रोग्राम थाने नवीं चीजां सिखावेला।'\n"
            "English: 'Have you registered for the summer program?' -> Marwadi: 'थे समर प्रोग्राम सारू नाम लिखायो कांई?'\n"
            "English: 'The classes start next week.' -> Marwadi: 'क्लासां अगले हफ्ते ऊं चालू वेवेला।'\n"
            "English: 'You will get a certificate.' -> Marwadi: 'थाने एक सर्टिफिकेट मिलेला।'\n"
            "English: 'This training is very important.' -> Marwadi: 'आ ट्रेनिंग घणी जरूरी है।'\n"
            "English: 'We are learning at Askatics.' -> Marwadi: 'म्हे अस्काटिक्स में सीख रया हां।'\n"
            "English: 'Stratos program is for students.' -> Marwadi: 'स्ट्रैटोस प्रोग्राम टाबरां (विद्यार्थियों) सारू है।'\n"
            "English: 'Improve your practical knowledge.' -> Marwadi: 'थारो काम रो ग्यान बढ़ाओ।'\n"
            # --- AI, IoT & Technology ---
            "English: 'What is Artificial Intelligence?' -> Marwadi: 'आ एआई (AI) कांई वेवे है?'\n"
            "English: 'AI will change the world.' -> Marwadi: 'एआई आखी दुनिया ने बदल देवेला।'\n"
            "English: 'IoT connects things to the internet.' -> Marwadi: 'आईओटी (IoT) चीजां ने इंटरनेट ऊं जोड़े है।'\n"
            "English: 'This is a smart device.' -> Marwadi: 'ओ एक स्मार्ट मशीन है।'\n"
            "English: 'Machine Learning is interesting.' -> Marwadi: 'मशीन लर्निंग घणी सोवणी लागे है।'\n"
            "English: 'We are building an AI model.' -> Marwadi: 'म्हे एक एआई मॉडल बणा रया हां।'\n"
            "English: 'Cloud computing is fast.' -> Marwadi: 'क्लाउड कंप्यूटिंग घणी तेज है।'\n"
            "English: 'Save the data on the cloud.' -> Marwadi: 'डेटा ने क्लाउड माथे सेव कर द्यो।'\n"
            "English: 'The system is updating.' -> Marwadi: 'सिस्टम अपडेट वे रयो है।'\n"
            "English: 'Internet speed is slow.' -> Marwadi: 'इंटरनेट री स्पीड हळवी है।'\n"
            "English: 'Connect the Wi-Fi.' -> Marwadi: 'वाई-फाई जोड़ द्यो।'\n"
            "English: 'Enter the password.' -> Marwadi: 'पासवर्ड लगाओ।'\n"
            "English: 'Your phone is ringing.' -> Marwadi: 'थारो फोन बाज रयो है।'\n"
            # --- Sensors, Electronics & Robotics ---
            "English: 'Where is the sensor?' -> Marwadi: 'सेंसर कठै है?'\n"
            "English: 'The sensor is not working.' -> Marwadi: 'सेंसर काम कोनी कर रयो है।'\n"
            "English: 'This is a temperature sensor.' -> Marwadi: 'ओ तावड़ो (तापमान) नापण रो सेंसर है।'\n"
            "English: 'Attach the motion sensor here.' -> Marwadi: 'मोशन सेंसर अठै लगा द्यो।'\n"
            "English: 'The robot is moving.' -> Marwadi: 'रोबोट चाल रयो है।'\n"
            "English: 'I am making a drone.' -> Marwadi: 'मैं एक ड्रोन बणा रयूँ हूँ।'\n"
            "English: 'Connect the wires.' -> Marwadi: 'तार जोड़ द्यो।'\n"
            "English: 'The battery is dead.' -> Marwadi: 'बैटरी खतम वे गी।'\n"
            "English: 'Charge the battery.' -> Marwadi: 'बैटरी चार्ज कर लो।'\n"
            "English: 'Start the motor.' -> Marwadi: 'मोटर चालू कर द्यो।'\n"
            "English: 'Stop the machine.' -> Marwadi: 'मशीन रोक द्यो।'\n"
            "English: 'The circuit is shorted.' -> Marwadi: 'सर्किट शॉर्ट वे गयो है।'\n"
            "English: 'Use the soldering iron.' -> Marwadi: 'सोल्डरिंग आयरन रो काम में ल्यो।'\n"
            "English: 'Check the voltage.' -> Marwadi: 'वोल्टेज चेक कर ल्यो।'\n"
            "English: 'Turn on the switch.' -> Marwadi: 'बटन चालू कर द्यो।'\n"
            "English: 'The LED is glowing.' -> Marwadi: 'एलईडी (LED) चस रयी है।'\n"
            "English: 'Send the signal.' -> Marwadi: 'सिग्नल भेज द्यो।'\n"
            "English: 'The connection is loose.' -> Marwadi: 'कनेक्शन ढीलो है।'\n"
            "English: 'Fix the hardware.' -> Marwadi: 'हार्डवेयर ने ठीक करो।'\n"
            # --- Coding, Engineering & Student Life ---
            "English: 'Write the code.' -> Marwadi: 'कोड लिखो।'\n"
            "English: 'There is a bug in the code.' -> Marwadi: 'कोड में कींई मिस्टेक (बग) है।'\n"
            "English: 'The code is compiling.' -> Marwadi: 'कोड चाल रयो है।'\n"
            "English: 'Run the program.' -> Marwadi: 'प्रोग्राम ने चलाओ।'\n"
            "English: 'Learn Python programming.' -> Marwadi: 'पायथन (Python) कोडिंग सीखो।'\n"
            "English: 'Open the laptop.' -> Marwadi: 'लैपटॉप खोलो।'\n"
            "English: 'The screen is broken.' -> Marwadi: 'स्क्रीन टूट गी है।'\n"
            "English: 'I am an engineer.' -> Marwadi: 'मैं एक इंजीनियर हूँ।'\n"
            "English: 'Submit the project.' -> Marwadi: 'प्रोजेक्ट जमा करा द्यो।'\n"
            "English: 'When is the deadline?' -> Marwadi: 'लास्ट डेट कद री है?'\n"
            "English: 'I have an exam tomorrow.' -> Marwadi: 'काले म्हारो पेपर है।'\n"
            "English: 'Study hard.' -> Marwadi: 'डट र पढ़ाई करो।'\n"
            "English: 'I got good marks.' -> Marwadi: 'म्हारे चोखा नंबर आया है।'\n"
            "English: 'Let's do a group study.' -> Marwadi: 'चालो भेळा बैठ र पढ़ां।'\n"
            "English: 'The college is closed today.' -> Marwadi: 'आज कॉलेज री छुट्टी है।'\n"
            "English: 'Who is the professor?' -> Marwadi: 'प्रोफेसर सा कुण है?'\n"
            "English: 'Bring your ID card.' -> Marwadi: 'थारो आईडी कार्ड लेर आवजो।'\n"
            "English: 'I need an internship.' -> Marwadi: 'मने इंटर्नशिप री जरूरत है।'\n"
            "English: 'Apply for the job.' -> Marwadi: 'नौकरी सारू फॉर्म लगा द्यो।'\n"
            "English: 'Innovation is necessary.' -> Marwadi: 'नवीं चीजां बणावणो जरूरी है।'\n"
            "English: 'We are a great team.' -> Marwadi: 'आपां एक घणी चोखी टीम हां।'\n"
            f"\nNow, carefully applying these grammar rules, style, and tech-vocabulary integration, translate this exactly into pure Bikaneri Marwadi: '{english_text}'"
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

with st.sidebar:
    st.header("⚙️ App Navigation")

    feature = st.selectbox(
        "🔧 Select Feature",
        ["Translator", "District Places Recommendation"]
    )
    
    st.markdown("---")
    
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

    st.markdown("---")

# Main UI Routing
if feature == "Translator":
    st.markdown("Translate English to pure Bikaneri Marwadi and generate lifelike AI speech.")

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

elif feature == "District Places Recommendation":
    st.markdown("Discover the rich history and beautiful places across Rajasthan.")
    
    st.subheader("📍 Select a District to Explore")
    district = st.selectbox(
        "Choose District",
        ["Bikaner"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.header(f"🌟 Must Visit Places in {district}")

    places_data = {
        "Bikaner": [
            {
                "name": "Laxmi Nath Ji Temple",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Laxminath-Temple_in_Bikaner.jpg?width=600",
                "desc": "One of the oldest temples in Bikaner, built in 1488 by Rao Bika. Dedicated to Lord Vishnu and Goddess Laxmi, it is the spiritual center of the city."
            },
            {
                "name": "Junagarh Fort",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Junagarh_fort_,_bikaner.jpg?width=600",
                "desc": "Built in 1589 by Raja Rai Singh, this impressive fort is one of the few in Rajasthan not built on a hilltop. It features a beautiful amalgamation of architectural styles."
            },
            {
                "name": "Kodemdesar Bheruji Temple",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Junagarh_Fort,Bikaner_01.jpg?width=600",
                "desc": "This unique temple is dedicated to Lord Bhairav. Notably, the temple has no roof, and the sacred idol is placed open to the sky, highly revered by locals."
            },
            {
                "name": "Devi Kund Sagar",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Devi_Kund_Sagar_and_Cenotaphs,_Bikaner.jpg?width=600",
                "desc": "This site houses the royal cenotaphs (chhatris) of the Bikaji dynasty rulers. Each pavilion is beautifully crafted, displaying exquisite historical Rajput architecture."
            },
            {
                "name": "Bhandasar Jain Temple",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Bhandasar_Jain_Temple_Bikaner_Rajasthan_DSC_9641.jpg?width=600",
                "desc": "A spectacular 15th-century temple famous for its vibrant frescoes. Legend says the foundation was built using 40,000 kilograms of pure ghee instead of water!"
            },
            {
                "name": "Gajner Palace",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Gajner_Palace_-_panoramio.jpg?width=600",
                "desc": "Described as an 'incomparable jewel in the Thar desert', this grand lakeside palace was bu            "English: 'Call the doctor.' -> Marwadi: 'डाक्टर ने फोन करो।'"
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

@@ -46,7 +178,6 @@
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
@@ -57,12 +188,10 @@
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
@@ -78,19 +207,19 @@
        if response.status_code == 200:
            audio_base64 = response.json()["audios"][0]
            return base64.b64decode(audio_base64)
        st.error(f"Sarvam API Error: {response.text}")
        return None
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
st.markdown("Your Ultimate Rajasthan Companion: Translate English to pure Bikaneri Marwadi and explore the state!")

with st.sidebar:
    st.header("⚙️ App Navigation")
@@ -99,9 +228,10 @@
        "🔧 Select Feature",
        ["Translator", "District Places Recommendation"]
    )
    
    st.markdown("---")
    st.header("⚙️ Voice Settings (Translator)")
    
    st.header("⚙️ Voice Settings")

    if not GROQ_API_KEY or not SARVAM_API_KEY:
        st.error("⚠️ API Keys missing! Please check your .env file.")
@@ -119,10 +249,11 @@
    selected_voice_label = st.selectbox("🗣️ Select Voice Model", list(voice_options.keys()))
    selected_voice_code = voice_options[selected_voice_label]

# ==========================================
# 🚀 FEATURE 1: TRANSLATOR
# ==========================================
    st.markdown("---")
# Main UI Routing
if feature == "Translator":
    st.markdown("Translate English to pure Bikaneri Marwadi and generate lifelike AI speech.")

    st.subheader("1. Enter English Text")

@@ -144,6 +275,7 @@
    st.divider()

    st.subheader("2. Bikaneri Marwadi Translation")
    st.markdown("*(Review & Edit the translation below before generating audio)*")

    edited_marwadi = st.text_area(
        "Edit Marwadi Text:",
@@ -170,12 +302,9 @@
        else:
            st.warning("Please ensure there is Marwadi text to speak.")

# ==========================================
# 🗺️ FEATURE 2: DISTRICT PLACES RECOMMENDATION
# ==========================================
elif feature == "District Places Recommendation":
    # District Selection on top
    st.markdown("Discover the rich history and beautiful places across Rajasthan.")
    
    st.subheader("📍 Select a District to Explore")
    district = st.selectbox(
        "Choose District",
@@ -186,43 +315,41 @@
    st.markdown("---")
    st.header(f"🌟 Must Visit Places in {district}")

    # Database of places
    places_data = {
        "Bikaner": [
            {
                "name": "Laxmi Nath Ji Temple",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Laxmi+Nath+Ji+Temple",
                "desc": "One of the oldest temples in Bikaner, built in 1488 by Rao Bika. Dedicated to Lord Vishnu and Goddess Laxmi, it boasts intricate silver artwork and serves as the spiritual center of the city."
                "desc": "One of the oldest temples in Bikaner, built in 1488 by Rao Bika. Dedicated to Lord Vishnu and Goddess Laxmi, it is the spiritual center of the city."
            },
            {
                "name": "Junagarh Fort",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Junagarh+Fort",
                "desc": "Built in 1589 by Raja Rai Singh, this impressive fort is one of the few in Rajasthan not built on a hilltop. It features a beautiful amalgamation of Rajput, Mughal, and Gujarati architectural styles."
                "desc": "Built in 1589 by Raja Rai Singh, this impressive fort is one of the few in Rajasthan not built on a hilltop. It features a beautiful amalgamation of architectural styles."
            },
            {
                "name": "Kodemdesar Bheruji Temple",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Kodemdesar+Temple",
                "desc": "Located slightly outside the city, this unique temple is dedicated to Lord Bhairav. Notably, the temple has no roof, and the sacred idol is placed open to the sky, highly revered by the locals."
                "desc": "This unique temple is dedicated to Lord Bhairav. Notably, the temple has no roof, and the sacred idol is placed open to the sky, highly revered by locals."
            },
            {
                "name": "Devi Kund Sagar",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Devi+Kund+Sagar",
                "desc": "This site houses the royal cenotaphs (chhatris) of the Bikaji dynasty rulers. Each pavilion is beautifully crafted from red sandstone and white marble, displaying exquisite historical Rajput architecture."
                "desc": "This site houses the royal cenotaphs (chhatris) of the Bikaji dynasty rulers. Each pavilion is beautifully crafted, displaying exquisite historical Rajput architecture."
            },
            {
                "name": "Bhandasar Jain Temple",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Bhandasar+Jain+Temple",
                "desc": "A spectacular 15th-century temple famous for its vibrant frescoes and leaf paintings. Legend says the foundation was built using 40,000 kilograms of pure ghee instead of water!"
                "desc": "A spectacular 15th-century temple famous for its vibrant frescoes. Legend says the foundation was built using 40,000 kilograms of pure ghee instead of water!"
            },
            {
                "name": "Gajner Palace",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Gajner+Palace",
                "desc": "Described as an 'incomparable jewel in the Thar desert', this grand lakeside palace was built by Maharaja Ganga Singh. It served as a hunting resort and is now a beautiful heritage hotel."
                "desc": "Described as an 'incomparable jewel in the Thar desert', this grand lakeside palace was built by Maharaja Ganga Singh and served as a hunting resort."
            }
        ]
    }

    # Displaying the places in a 2-column layout for a cleaner look
    cols = st.columns(2)

    for idx, place in enumerate(places_data[district]):
@@ -232,295 +359,44 @@
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
    <style>
    .footer-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px 0px 10px 0px;
        text-align: center;
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
    district = st.selectbox            "English: 'Where is the sensor?' -> Marwadi: 'सेंसर कठै है?'\n"
            "English: 'The sensor is not working.' -> Marwadi: 'सेंसर काम कोनी कर रयो है।'\n"
            "English: 'This is a temperature sensor.' -> Marwadi: 'ओ तावड़ो (तापमान) नापण रो सेंसर है।'\n"
            "English: 'Attach the motion sensor here.' -> Marwadi: 'मोशन सेंसर अठै लगा द्यो।'\n"
            "English: 'Connect the ultrasonic sensor.' -> Marwadi: 'अल्ट्रासोनिक सेंसर जोड़ द्यो।'\n"
            "English: 'The humidity sensor is broken.' -> Marwadi: 'नमी नापण आळो सेंसर टूट गयो है।'\n"
            "English: 'Connect the wires carefully.' -> Marwadi: 'तारां ने ध्यान ऊं जोड़ो।'\n"
            "English: 'The battery is dead.' -> Marwadi: 'बैटरी खतम वे गी।'\n"
            "English: 'Charge the battery.' -> Marwadi: 'बैटरी चार्ज कर लो।'\n"
            "English: 'Start the motor.' -> Marwadi: 'मोटर चालू कर द्यो।'\n"
            "English: 'Stop the machine.' -> Marwadi: 'मशीन रोक द्यो।'\n"
            "English: 'The circuit is shorted.' -> Marwadi: 'सर्किट शॉर्ट वे गयो है।'\n"
            "English: 'Use the soldering iron.' -> Marwadi: 'सोल्डरिंग आयरन रो काम में ल्यो।'\n"
            "English: 'Check the voltage.' -> Marwadi: 'वोल्टेज चेक कर ल्यो।'\n"
            "English: 'Turn on the switch.' -> Marwadi: 'बटन चालू कर द्यो।'\n"
            "English: 'The LED is glowing.' -> Marwadi: 'एलईडी (LED) चस रयी है।'\n"
            "English: 'Send the signal.' -> Marwadi: 'सिग्नल भेज द्यो।'\n"
            "English: 'The connection is loose.' -> Marwadi: 'कनेक्शन ढीलो है।'\n"
            "English: 'Fix the hardware.' -> Marwadi: 'हार्डवेयर ने ठीक करो।'\n"
            "English: 'I need a breadboard.' -> Marwadi: 'मने एक ब्रेडबोर्ड चावे।'\n"
            "English: 'Plug in the Arduino.' -> Marwadi: 'आर्डिनो (Arduino) ने लगाओ।'\n"

            # --- Robotics & Drones ---
            "English: 'The robot is moving.' -> Marwadi: 'रोबोट चाल रयो है।'\n"
            "English: 'I am making a drone.' -> Marwadi: 'मैं एक ड्रोन बणा रयूँ हूँ।'\n"
            "English: 'The drone is flying high.' -> Marwadi: 'ड्रोन घणों ऊंचो उड़ रयो है।'\n"
            "English: 'Program the robot to walk.' -> Marwadi: 'रोबोट ने चालण रो कोड लगाओ।'\n"
            "English: 'The motor speed is too fast.' -> Marwadi: 'मोटर री स्पीड घणी तेज है।'\n"
            "English: 'Attach the wheels.' -> Marwadi: 'पहिया लगा द्यो।'\n"
            
            # --- Coding, Software Engineering & Academics ---
            "English: 'Write the code.' -> Marwadi: 'कोड लिखो।'\n"
            "English: 'There is a bug in the code.' -> Marwadi: 'कोड में कींई मिस्टेक (बग) है।'\n"
            "English: 'The code is compiling.' -> Marwadi: 'कोड चाल रयो है।'\n"
            "English: 'Run the program.' -> Marwadi: 'प्रोग्राम ने चलाओ।'\n"
            "English: 'Learn Python programming.' -> Marwadi: 'पायथन (Python) कोडिंग सीखो।'\n"
            "English: 'Open the laptop.' -> Marwadi: 'लैपटॉप खोलो।'\n"
            "English: 'The screen is broken.' -> Marwadi: 'स्क्रीन टूट गी है।'\n"
            "English: 'I am an engineer.' -> Marwadi: 'मैं एक इंजीनियर हूँ।'\n"
            "English: 'Submit the project.' -> Marwadi: 'प्रोजेक्ट जमा करा द्यो।'\n"
            "English: 'When is the deadline?' -> Marwadi: 'लास्ट डेट कद री है?'\n"
            "English: 'I have an exam tomorrow.' -> Marwadi: 'काले म्हारो पेपर है।'\n"

            # --- Extended Conversational Marwadi ---
            "English: 'Do you know me?' -> Marwadi: 'थे मने ओळखो के?'\n"
            "English: 'I don't know.' -> Marwadi: 'मने कोनी ठा।'\n"
            "English: 'Don't lie.' -> Marwadi: 'झूठ मत बोलो।'\n"
            "English: 'What's for dinner?' -> Marwadi: 'ब्याळू में कांई बण्यो है?'\n"
            "English: 'The food is delicious.' -> Marwadi: 'जीमण घणों स्वाद है।'\n"
            "English: 'Give me a discount.' -> Marwadi: 'थोड़ा कम करो सा।'\n"
            "English: 'Keep the change.' -> Marwadi: 'खुल्ला थे ही राख लो।'\n"
            "English: 'It might rain.' -> Marwadi: 'मे आय सके है।'\n"
            "English: 'Come tomorrow.' -> Marwadi: 'काले आइजो।'\n"
            "English: 'I am late.' -> Marwadi: 'मने मोड़ो वे गयो।'\n"
            "English: 'Wake up early.' -> Marwadi: 'बेगा उठो।'\n"
            "English: 'Are you angry?' -> Marwadi: 'थे रीस कर रया हो कांई?'\n"
            "English: 'Don't worry.' -> Marwadi: 'फिकर मत करो।'\n"
            "English: 'Everything will be fine.' -> Marwadi: 'सगळो ठीक वे जावेला।'\n"
            "English: 'I forgot.' -> Marwadi: 'मैं भूल गयो।'\n"
            "English: 'Where is the hospital?' -> Marwadi: 'अस्पताल कठे है?'\n"
            "English: 'Call the doctor.' -> Marwadi: 'डाक्टर ने फोन करो।'\n"
            "English: 'I am not feeling well.' -> Marwadi: 'म्हारे जीव ने ठीक कोनी लागे।'\n"
            "English: 'Drive slowly.' -> Marwadi: 'गाड़ी धीरे चलाओ।'\n"

            f"\nNow, taking inspiration from all the tech, engineering, and cultural vocabulary provided above, translate this exactly into pure Bikaneri Marwadi: '{english_text}'"
        )

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
            "English: 'Who is at home?' -> Madef translate_to_marwadi(english_text):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        prompt = (
            "You are an elder from Bikaner, Rajasthan. You speak the pure, authentic Bikaneri Marwadi dialect. "
            "Your task is to translate the following English text into 100% pure Bikaneri Marwadi. "
            "CRITICAL RULES: "
            "1. DO NOT use standard Hindi words. If you use standard Hindi, you fail. "
            "2. 'I'/'Me' becomes 'मैं' or 'मनै'. "
            "3. 'This' becomes 'ओ' (for male objects) or 'आ' (for female objects). "
            "4. 'Want to buy' or 'Want to take' becomes 'लेणो है'. "
            "5. 'What' becomes 'कांई'. 'Where' becomes 'कठै'. "
            "6. Output ONLY the final Bikaneri Marwadi translation in Devanagari script. No quotes, no English explanations.\n\n"
            "EXAMPLES:\n"
            
            # --- General Basics & Greetings ---
            "English: 'I want to buy this Samosa.' -> Marwadi: 'मनै ओ समोसो लेणो है।'\n"
            "English: 'How are you?' -> Marwadi: 'थे कियां हो?' or 'कांई हाल है भायळा?'\n"
            "English: 'Where are you going?' -> Marwadi: 'थे कठै जा रया हो?'\n"
            "English: 'What are you doing?' -> Marwadi: 'थे कांई कर रया हो?'\n"
            "English: 'What is your name?' -> Marwadi: 'थारो नाम कांई है?'\n"
            "English: 'I am fine.' -> Marwadi: 'मैं ठीक हूँ।'\n"
            "English: 'Where do you live?' -> Marwadi: 'थे कठे रीयो हो?'\n"
            "English: 'I am working.' -> Marwadi: 'मैं काम कर रयूँ हूँ।'\n"
            "English: 'I want to buy something.' -> Marwadi: 'मने कींई खरीदणों है।'\n"
            "English: 'What is the price of this?' -> Marwadi: 'ईंरो भाव कांई है?'\n"
            "English: 'It is too expensive.' -> Marwadi: 'ओ तो घणों मँघो है।'\n"
            "English: 'Have you eaten?' -> Marwadi: 'थे जीम लिया कांई?'\n"
            "English: 'I am hungry.' -> Marwadi: 'मने भूख लागी है।'\n"
            "English: 'Give me some water.' -> Marwadi: 'मने थोड़ो पाणी पावो।'\n"
            "English: 'Where is the market?' -> Marwadi: 'बजार कठे है?'\n"
            "English: 'Come here.' -> Marwadi: 'अठै आवो।'\n"
            "English: 'Sit down.' -> Marwadi: 'बैठ ज्याओ।'\n"
            "English: 'Wait a minute.' -> Marwadi: 'एक मिंट रुको।'\n"
            
            # --- Askatics & Stratos Summer Program ---
            "English: 'Welcome to Askatics.' -> Marwadi: 'अस्काटिक्स में थारो घणों मान है।'\n"
            "English: 'Askatics is a great company.' -> Marwadi: 'अस्काटिक्स एक घणी चोखी कंपनी है।'\n"
            "English: 'We are learning at Askatics.' -> Marwadi: 'म्हे अस्काटिक्स में सीख रया हां।'\n"
            "English: 'Join Stratos Summer Program to improve your skills.' -> Marwadi: 'थारी होशियारी बढावण खातिर स्ट्रैटोस समर प्रोग्राम में जुड़ो।'\n"
            "English: 'Stratos Summer Program will teach you new things.' -> Marwadi: 'स्ट्रैटोस समर प्रोग्राम थाने नवीं चीजां सिखावेला।'\n"
            "English: 'Have you registered for the summer program?' -> Marwadi: 'थे समर प्रोग्राम सारू नाम लिखायो कांई?'\n"
            "English: 'The classes start next week.' -> Marwadi: 'क्लासां अगले हफ्ते ऊं चालू वेवेला।'\n"
            "English: 'You will get a certificate.' -> Marwadi: 'थाने एक सर्टिफिकेट मिलेला।'\n"
            "English: 'This training is very important.' -> Marwadi: 'आ ट्रेनिंग घणी जरूरी है।'\n"
            "English: 'Stratos program is for students.' -> Marwadi: 'स्ट्रैटोस प्रोग्राम टाबरां सारू है।'\n"
            "English: 'Improve your practical knowledge.' -> Marwadi: 'थारो काम रो ग्यान बढ़ाओ।'\n"
            "English: 'Our mentors are very helpful.' -> Marwadi: 'म्हारा गुरुजी घणी मदद करे है।'\n"
            "English: 'Don't miss this opportunity.' -> Marwadi: 'आ मौको मत गमावजो।'\n"
            "English: 'Register on the website today.' -> Marwadi: 'आज ही वेबसाइट माथे नाम लिखाय द्यो।'\n"

            # --- AI, IoT & Emerging Technology ---
            "English: 'What is Artificial Intelligence?' -> Marwadi: 'आ एआई (AI) कांई वेवे है?'\n"
            "English: 'AI will change the world.' -> Marwadi: 'एआई आखी दुनिया ने बदल देवेला।'\n"
            "English: 'IoT connects things to the internet.' -> Marwadi: 'आईओटी (IoT) चीजां ने इंटरनेट ऊं जोड़े है।'\n"
            "English: 'This is a smart device.' -> Marwadi: 'ओ एक स्मार्ट मशीन है।'\n"
            "English: 'Machine Learning is interesting.' -> Marwadi: 'मशीन लर्निंग घणी सोवणी लागे है।'\n"
            "English: 'We are building an AI model.' -> Marwadi: 'म्हे एक एआई मॉडल बणा रया हां।'\n"
            "English: 'Cloud computing is fast.' -> Marwadi: 'क्लाउड कंप्यूटिंग घणी तेज है।'\n"
            "English: 'Save the data on the cloud.' -> Marwadi: 'डेटा ने क्लाउड माथे सेव कर द्यो।'\n"
            "English: 'The system is updating.' -> Marwadi: 'सिस्टम अपडेट वे रयो है।'\n"
            "English: 'Internet speed is slow.' -> Marwadi: 'इंटरनेट री स्पीड हळवी है।'\n"
            "English: 'Connect the Wi-Fi.' -> Marwadi: 'वाई-फाई जोड़ द्यो।'\n"
            "English: 'Your phone is ringing.' -> Marwadi: 'थारो फोन बाज रयो है।'\n"
            "English: 'Data science is the future.' -> Marwadi: 'डेटा साइंस ही आग्लो बखत है।'\n"
            "English: 'The server is down.' -> Marwadi: 'सर्वर बंद पड़्यो है।'\n"
            "English: 'Restart the computer.' -> Marwadi: 'कंप्यूटर ने पाछो चालू करो।'\n"
            "English: 'This app uses AI.' -> Marwadi: 'ईं ऐप में एआई रो काम वेवे है।'\n"

            # --- Sensors, Electronics & Hardware ---
            "English: 'Where is the sensor?' -> Marwadi: 'सेंसर कठै है?'\n"
            "English: 'The sensor is not working.' -> Marwadi: 'सेंसर काम कोनी कर रयो है।'\n"
            "English: 'This is a temperature sensor.' -> Marwadi: 'ओ तावड़ो (तापमान) नापण रो सेंसर है।'\n"
            "English: 'Attach the motion sensor here.' -> Marwadi: 'मोशन सेंसर अठै लगा द्यो।'\n"
            "English: 'Connect the ultrasonic sensor.' -> Marwadi: 'अल्ट्रासोनिक सेंसर जोड़ द्यो।'\n"
            "English: 'The humidity sensor is broken.' -> Marwadi: 'नमी नापण आळो सेंसर टूट गयो है।'\n"
            "English: 'Connect the wires carefully.' -> Marwadi: 'तारां ने ध्यान ऊं जोड़ो।'\n"
            "English: 'The battery is dead.' -> Marwadi: 'बैटरी खतम वे गी।'\n"
            "English: 'Charge the battery.' -> Marwadi: 'बैटरी चार्ज कर लो।'\n"
            "English: 'Start the motor.' -> Marwadi: 'मोटर चालू कर द्यो।'\n"
            "English: 'Stop the machine.' -> Marwadi: 'मशीन रोक द्यो।'\n"
            "English: 'The circuit is shorted.' -> Marwadi: 'सर्किट शॉर्ट वे गयो है।'\n"
            "English: 'Use the soldering iron.' -> Marwadi: 'सोल्डरिंग आयरन रो काम में ल्यो।'\n"
            "English: 'Check the voltage.' -> Marwadi: 'वोल्टेज चेक कर ल्यो।'\n"
            "English: 'Turn on the switch.' -> Marwadi: 'बटन चालू कर द्यो।'\n"
            "English: 'The LED is glowing.' -> Marwadi: 'एलईडी (LED) चस रयी है।'\n"
            "English: 'Send the signal.' -> Marwadi: 'सिग्नल भेज द्यो।'\n"
            "English: 'The connection is loose.' -> Marwadi: 'कनेक्शन ढीलो है।'\n"
            "English: 'Fix the hardware.' -> Marwadi: 'हार्डवेयर ने ठीक करो।'\n"
            "English: 'I need a breadboard.' -> Marwadi: 'मने एक ब्रेडबोर्ड चावे।'\n"
            "English: 'Plug in the Arduino.' -> Marwadi: 'आर्डिनो (Arduino) ने लगाओ।'\n"

            # --- Robotics & Drones ---
            "English: 'The robot is moving.' -> Marwadi: 'रोबोट चाल रयो है।'\n"
            "English: 'I am making a drone.' -> Marwadi: 'मैं एक ड्रोन बणा रयूँ हूँ।'\n"
            "English: 'The drone is flying high.' -> Marwadi: 'ड्रोन घणों ऊंचो उड़ रयो है।'\n"
            "English: 'Program the robot to walk.' -> Marwadi: 'रोबोट ने चालण रो कोड लगाओ।'\n"
            "English: 'The motor speed is too fast.' -> Marwadi: 'मोटर री स्पीड घणी तेज है।'\n"
            "English: 'Attach the wheels.' -> Marwadi: 'पहिया लगा द्यो।'\n"
            
            # --- Coding, Software Engineering & Academics ---
            "English: 'Write the code.' -> Marwadi: 'कोड लिखो।'\n"
            "English: 'There is a bug in the code.' -> Marwadi: 'कोड में कींई मिस्टेक (बग) है।'\n"
            "English: 'The code is compiling.' -> Marwadi: 'कोड चाल रयो है।'\n"
            "English: 'Run the program.' -> Marwadi: 'प्रोग्राम ने चलाओ।'\n"
            "English: 'Learn Python programming.' -> Marwadi: 'पायथन (Python) कोडिंग सीखो।'\n"
            "English: 'Open the laptop.' -> Marwadi: 'लैपटॉप खोलो।'\n"
            "English: 'The screen is broken.' -> Marwadi: 'स्क्रीन टूट गी है।'\n"
            "English: 'I am an engineer.' -> Marwadi: 'मैं एक इंजीनियर हूँ।'\n"
            "English: 'Submit the project.' -> Marwadi: 'प्रोजेक्ट जमा करा द्यो।'\n"
            "English: 'When is the deadline?' -> Marwadi: 'लास्ट डेट कद री है?'\n"
            "English: 'I have an exam tomorrow.' -> Marwadi: 'काले म्हारो पेपर है।'\n"
            "English: 'Study hard.' -> Marwadi: 'डट र पढ़ाई करो।'\n"
            "English: 'I got good marks.' -> Marwadi: 'म्हारे चोखा नंबर आया है।'\n"
            "English: 'Let's do a group study.' -> Marwadi: 'चालो भेळा बैठ र पढ़ां।'\n"
            "English: 'The college is closed today.' -> Marwadi: 'आज कॉलेज री छुट्टी है।'\n"
            "English: 'Who is the professor?' -> Marwadi: 'प्रोफेसर सा कुण है?'\n"
            "English: 'I need an internship.' -> Marwadi: 'मने इंटर्नशिप री जरूरत है।'\n"
            "English: 'Apply for the job.' -> Marwadi: 'नौकरी सारू फॉर्म लगा द्यो।'\n"
            "English: 'Innovation is necessary.' -> Marwadi: 'नवीं चीजां बणावणो जरूरी है।'\n"
            "English: 'We are a great team.' -> Marwadi: 'आपां एक घणी चोखी टीम हां।'\n"
            
            # --- Extended Conversational Marwadi ---
            "English: 'Do you know me?' -> Marwadi: 'थे मने ओळखो के?'\n"
            "English: 'I don't know.' -> Marwadi: 'मने कोनी ठा।'\n"
            "English: 'Don't lie.' -> Marwadi: 'झूठ मत बोलो।'\n"
            "English: 'What's for dinner?' -> Marwadi: 'ब्याळू में कांई बण्यो है?'\n"
            "English: 'The food is delicious.' -> Marwadi: 'जीमण घणों स्वाद है।'\n"
            "English: 'Give me a discount.' -> Marwadi: 'थोड़ा कम करो सा।'\n"
            "English: 'Keep the change.' -> Marwadi: 'खुल्ला थे ही राख लो।'\n"
            "English: 'It might rain.' -> Marwadi: 'मे आय सके है।'\n"
            "English: 'Come tomorrow.' -> Marwadi: 'काले आइजो।'\n"
            "English: 'I am late.' -> Marwadi: 'मने मोड़ो वे गयो।'\n"
            "English: 'Wake up early.' -> Marwadi: 'बेगा उठो।'\n"
            "English: 'Are you angry?' -> Marwadi: 'थे रीस कर रया हो कांई?'\n"
            "English: 'Don't worry.' -> Marwadi: 'फिकर मत करो।'\n"
            "English: 'Everything will be fine.' -> Marwadi: 'सगळो ठीक वे जावेला।'\n"
            "English: 'I forgot.' -> Marwadi: 'मैं भूल गयो।'\n"
            "English: 'Where is the hospital?' -> Marwadi: 'अस्पताल कठे है?'\n"
            "English: 'Call the doctor.' -> Marwadi: 'डाक्टर ने फोन करो।'\n"
            "English: 'I am not feeling well.' -> Marwadi: 'म्हारे जीव ने ठीक कोनी लागे।'\n"
            "English: 'Drive slowly.' -> Marwadi: 'गाड़ी धीरे चलाओ।'\n"

            f"\nNow, taking inspiration from all the tech, engineering, and cultural vocabulary provided above, translate this exactly into pure Bikaneri Marwadi: '{english_text}'"
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
rwadi: 'घरे कुण है?'"
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

with st.sidebar:
    st.header("⚙️ App Navigation")

    feature = st.selectbox(
        "🔧 Select Feature",
        ["Translator", "District Places Recommendation"]
    )
    
    st.markdown("---")
    
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

    st.markdown("---")

# Main UI Routing
if feature == "Translator":
    st.markdown("Translate English to pure Bikaneri Marwadi and generate lifelike AI speech.")

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

elif feature == "District Places Recommendation":
    st.markdown("Discover the rich history and beautiful places across Rajasthan.")
    
    st.subheader("📍 Select a District to Explore")
    district = st.selectbox(
        "Choose District",
        ["Bikaner"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.header(f"🌟 Must Visit Places in {district}")

    places_data = {
        "Bikaner": [
            {
                "name": "Laxmi Nath Ji Temple",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Laxmi+Nath+Ji+Temple",
                "desc": "One of the oldest temples in Bikaner, built in 1488 by Rao Bika. Dedicated to Lord Vishnu and Goddess Laxmi, it is the spiritual center of the city."
            },
            {
                "name": "Junagarh Fort",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Junagarh+Fort",
                "desc": "Built in 1589 by Raja Rai Singh, this impressive fort is one of the few in Rajasthan not built on a hilltop. It features a beautiful amalgamation of architectural styles."
            },
            {
                "name": "Kodemdesar Bheruji Temple",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Kodemdesar+Temple",
                "desc": "This unique temple is dedicated to Lord Bhairav. Notably, the temple has no roof, and the sacred idol is placed open to the sky, highly revered by locals."
            },
            {
                "name": "Devi Kund Sagar",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Devi+Kund+Sagar",
                "desc": "This site houses the royal cenotaphs (chhatris) of the Bikaji dynasty rulers. Each pavilion is beautifully crafted, displaying exquisite historical Rajput architecture."
            },
            {
                "name": "Bhandasar Jain Temple",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Bhandasar+Jain+Temple",
                "desc": "A spectacular 15th-century temple famous for its vibrant frescoes. Legend says the foundation was built using 40,000 kilograms of pure ghee instead of water!"
            },
            {
                "name": "Gajner Palace",
                "image": "https://placehold.co/600x400/FF9933/FFFFFF?text=Gajner+Palace",
                "desc": "Described as an 'incomparable jewel in the Thar desert', this grand lakeside palace was built by Maharaja Ganga Singh and served as a hunting resort."
            }
        ]
    }

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
