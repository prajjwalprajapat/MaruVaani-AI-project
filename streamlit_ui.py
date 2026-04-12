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
            "English: 'Wake up, the sun is out.' -> Marwadi: 'बेगा उठो, तावड़ो निकळ गयो।'\n"
"English: 'Give me a cup of tea.' -> Marwadi: 'मने एक कप्प चा पावो।'\n"
"English: 'The tea is too sweet.' -> Marwadi: 'चा में मीठो घणो है।'\n"
"English: 'Bring the broom.' -> Marwadi: 'बुहारी लेर आवो।'\n"
"English: 'Clean the courtyard.' -> Marwadi: 'आंगणो साफ कर द्यो।'\n"
"English: 'Wash the clothes.' -> Marwadi: 'गाबा (कपड़ा) धोय द्यो।'\n"
"English: 'I am taking a bath.' -> Marwadi: 'मैं न्हाय रयूँ हूँ।'\n"
"English: 'The water is very cold.' -> Marwadi: 'पाणी घणो सीळो (ठंडो) है।'\n"
"English: 'Light the fire in the stove.' -> Marwadi: 'चूल्हो चसाओ।'\n"
"English: 'Put the food on the plate.' -> Marwadi: 'थाळी में जीमण परोस द्यो।'\n"
"English: 'I ate too much today.' -> Marwadi: 'मैं आज घणो जीम लियो।'\n"
"English: 'This vegetable is spicy.' -> Marwadi: 'आ सब्जी घणी तीखी है।'\n"
"English: 'Bring some milk from the market.' -> Marwadi: 'बजार ऊं थोड़ो दूध लेर आवो।'\n"
"English: 'The dog is barking.' -> Marwadi: 'गंडकड़ो भूंके है।'\n"
"English: 'Lock the door.' -> Marwadi: 'किवाड़ रे ताळो लगा द्यो।'\n"
"English: 'It is very dark inside.' -> Marwadi: 'मांयने घणो आंधारो है।'\n"
"English: 'Turn on the fan.' -> Marwadi: 'पंखो चालू कर द्यो।'\n"
"English: 'My back is aching.' -> Marwadi: 'म्हारी फांसळी दूखे है।'\n"
"English: 'Apply some oil on my head.' -> Marwadi: 'म्हारे माथे में थोड़ो तेल घाल द्यो।'\n"
"English: 'I am feeling sleepy.' -> Marwadi: 'मने नींद आवे है।'\n"
"English: 'Don't act smart.' -> Marwadi: 'घणो डाँफो मत बण।'\n"
"English: 'You talk too much.' -> Marwadi: 'थे बातां घणी करो हो।'\n"
"English: 'My head is spinning.' -> Marwadi: 'म्हारो माथो भमे है।'\n"
"English: 'Go to sleep quietly.' -> Marwadi: 'चुपचाप सूय ज्याओ।'\n"
"English: 'Are you deaf?' -> Marwadi: 'थे बहरा हो कांई?'\n"
"English: 'Don't ruin my mood.' -> Marwadi: 'म्हारो मूड खराब मत करो।'\n"
"English: 'Mind your own business.' -> Marwadi: 'थारे काम ऊं काम राखो।'\n"
"English: 'What is this drama?' -> Marwadi: 'ओ कांई नाटक है?'\n"
"English: 'I will slap you.' -> Marwadi: 'एक चांटो जड़ द्यूंगो।'\n"
"English: 'Leave me alone.' -> Marwadi: 'मने एकलो छोड़ द्यो।'\n"
"English: 'You always lie.' -> Marwadi: 'थे हमेसा झूठ बोलो हो।'\n"
"English: 'Don't fight with him.' -> Marwadi: 'बीं ऊं लड़ाई मत करो।'\n"
"English: 'He is a very bad boy.' -> Marwadi: 'वो घणो खोटो टाबर है।'\n"
"English: 'Why are you shouting?' -> Marwadi: 'थे राड़ क्यूँ कर रया हो?'\n"
"English: 'I have no time for this.' -> Marwadi: 'म्हारे कने ईं सारू बखत कोनी।'\n"
"English: 'You are very stubborn.' -> Marwadi: 'थे घणा जिद्दी हो।'\n"
"English: 'Don't argue with elders.' -> Marwadi: 'मोटां रे सामी मत बोलो।'\n"
"English: 'I don't trust you.' -> Marwadi: 'मने थारे माथे बिस्वास कोनी।'\n"
"English: 'Get out of my house.' -> Marwadi: 'म्हारे घर ऊं बारै निकळ ज्याओ।'\n"
"English: 'Do whatever you want to do.' -> Marwadi: 'थारे जचे ज्यूं कर ल्यो।'\n"
"English: 'The laptop is heating up.' -> Marwadi: 'लैपटॉप तातो वे रयो है।'\n"
"English: 'My code is working perfectly.' -> Marwadi: 'म्हारो कोड एकदम चोखो चाल रयो है।'\n"
"English: 'Stratos is making us smart.' -> Marwadi: 'स्ट्रैटोस म्हाने होशियार बणाय रयो है।'\n"
"English: 'Prajjwal is teaching IoT.' -> Marwadi: 'प्रज्ज्वल आईओटी (IoT) सिखाय रयो है।'\n"
"English: 'Rudraksh is building a robot.' -> Marwadi: 'रुद्राक्ष एक रोबोट बणाय रयो है।'\n"
"English: 'Krishna Vyas is a great founder.' -> Marwadi: 'कृष्णा व्यास एक घणो चोखो धणी है।'\n"
"English: 'Upload the project file.' -> Marwadi: 'प्रोजेक्ट री फाइल अपलोड कर द्यो।'\n"
"English: 'The internet is down today.' -> Marwadi: 'आज इंटरनेट कोनी चाल रयो।'\n"
"English: 'My mobile screen is cracked.' -> Marwadi: 'म्हारे फोन री स्क्रीन फूट गी।'\n"
"English: 'Charge my phone.' -> Marwadi: 'म्हारो फोन चार्ज लगा द्यो।'\n"
"English: 'I am fixing the motherboard.' -> Marwadi: 'मैं मदरबोर्ड ठीक कर रयूँ हूँ।'\n"
"English: 'The camera quality is very good.' -> Marwadi: 'कैमरा रो रिजल्ट घणो सोवणो है।'\n"
"English: 'Send me the photo.' -> Marwadi: 'मने फोटो भेज द्यो।'\n"
"English: 'The memory is full.' -> Marwadi: 'मेमोरी पूरी भर गी है।'\n"
"English: 'Delete these old files.' -> Marwadi: 'आं जूनी फाइलां ने डिलीट कर द्यो।'\n"
"English: 'Press the enter key.' -> Marwadi: 'एंटर बटन दबाओ।'\n"
"English: 'Software engineering is tough.' -> Marwadi: 'सॉफ्टवेयर इंजीनियरिंग घणी दोरी है।'\n"
"English: 'We are making a new app.' -> Marwadi: 'म्हे एक नवी ऐप बणाय रया हां।'\n"
"English: 'This technology is amazing.' -> Marwadi: 'आ तकनीक तो गजब है।'\n"
"English: 'Our startup will grow fast.' -> Marwadi: 'म्हारो काम बेगो मोटो वेवेला।'\n"
"English: 'Bring Bikaneri Bhujia.' -> Marwadi: 'बीकानेरी भुजिया लेर आवो।'\n"
"English: 'The Rasgullas are very sweet.' -> Marwadi: 'रसगुल्ला घणा मीठा है।'\n"
"English: 'It is very hot outside.' -> Marwadi: 'बारै घणो तावड़ो है।'\n"
"English: 'Let's go to Karni Mata temple.' -> Marwadi: 'चालो करणी माता रे धोक लगावण चालां।'\n"
"English: 'Weigh it properly.' -> Marwadi: 'ढंग ऊं तोल र द्यो।'\n"
"English: 'This cloth is very soft.' -> Marwadi: 'ओ गाबो (कपड़ो) घणो सूवाळो है।'\n"
"English: 'Give me fresh vegetables.' -> Marwadi: 'मने ताजी हरियाळी द्यो।'\n"
"English: 'Where is your shop?' -> Marwadi: 'थारी दुकान कठै है?'\n"
"English: 'The market is crowded today.' -> Marwadi: 'आज बजार में घणी भीड़ है।'\n"
"English: 'I am going to Junagarh Fort.' -> Marwadi: 'मैं जूनागढ़ किले जा रयूँ हूँ।'\n"
"English: 'The desert sand is burning.' -> Marwadi: 'धोरा री रेत तप रयी है।'\n"
"English: 'Give me a glass of buttermilk.' -> Marwadi: 'मने एक गिलास छाछ पावो।'\n"
"English: 'I want to eat Ghevar.' -> Marwadi: 'मने घेवर खाणो है।'\n"
"English: 'Pack this parcel.' -> Marwadi: 'ओ पार्सल बांध द्यो।'\n"
"English: 'Do you accept online payment?' -> Marwadi: 'थे ऑनलाइन पीसा लेवो हो कांई?'\n"
"English: 'How far is the railway station?' -> Marwadi: 'रेलवे स्टेशन कतरो दूर है?'\n"
"English: 'The train is running late.' -> Marwadi: 'रेलगाड़ी मोड़ी चाल रयी है।'\n"
"English: 'Book my ticket.' -> Marwadi: 'म्हारी टिकट बणाय द्यो।'\n"
"English: 'Drive the camel cart carefully.' -> Marwadi: 'ऊंट गाड़ो ध्यान ऊं चलाओ।'\n"
"English: 'The electricity is gone.' -> Marwadi: 'लाइट चली गी है।'\n"
"English: 'How is your father?' -> Marwadi: 'थारा बाबो सा कियां है?'\n"
"English: 'My grandmother tells stories.' -> Marwadi: 'म्हारी दादी सा बातां (कहाणी) सुणावे है।'\n"
"English: 'Children are playing outside.' -> Marwadi: 'टाबर बारै रमे है।'\n"
"English: 'Come inside, it's getting dark.' -> Marwadi: 'मांयने आ ज्याओ, आंधारो वे गयो है।'\n"
"English: 'I missed you a lot.' -> Marwadi: 'मने थारी घणी याद आई।'\n"
"English: 'May you live long.' -> Marwadi: 'जुग जुग जीयो।'\n"
"English: 'Take care of your health.' -> Marwadi: 'थारे सरीर रो ध्यान राखजो।'\n"
"English: 'He is a good man.' -> Marwadi: 'वो घणो भलो मिनख है।'\n"
"English: 'She is my wife.' -> Marwadi: 'आ म्हारी लुगाई है।'\n"
"English: 'When is the wedding?' -> Marwadi: 'ब्याव कद रो है?'\n"
"English: 'The groom has arrived.' -> Marwadi: 'बींद आय गयो है।'\n"
"English: 'The bride is looking beautiful.' -> Marwadi: 'बींदणी घणी फूटरी लागे है।'\n"
"English: 'Play the dholak.' -> Marwadi: 'ढोलक बजाओ।'\n"
"English: 'Sing a folk song.' -> Marwadi: 'एक लोकगीत सुणाओ।'\n"
"English: 'He is my elder brother.' -> Marwadi: 'ओ म्हारो मोटो भाई है।'\n"
"English: 'Listen to your sister.' -> Marwadi: 'थारी बहिण री बात सुणो।'\n"
"English: 'Guests have come to our house.' -> Marwadi: 'म्हारे घरे पावणा आया है।'\n"
"English: 'Serve them tea and snacks.' -> Marwadi: 'बांने चा पाणी पावो।'\n"
"English: 'We are going to the village.' -> Marwadi: 'म्हे गांव जा रया हां।'\n"
"English: 'The crops are ready.' -> Marwadi: 'फसल पक गी है।'\n"
"English: 'Don't be lazy.' -> Marwadi: 'आळस मत करो।'\n"
"English: 'Work hard and earn money.' -> Marwadi: 'डट र काम करो और पीसा कमाओ।'\n"
"English: 'Don't sit idle.' -> Marwadi: 'नवेला (खाली) मत बैठो।'\n"
"English: 'I am doing my homework.' -> Marwadi: 'मैं म्हारो स्कूल रो काम कर रयूँ हूँ।'\n"
"English: 'The teacher is coming.' -> Marwadi: 'मास्टर जी आय रया है।'\n"
"English: 'Read this book.' -> Marwadi: 'आ किताब पढ़ो।'\n"
"English: 'Write a letter to him.' -> Marwadi: 'बींने एक कागत (चिट्ठी) लिखो।'\n"
"English: 'Where did you put my glasses?' -> Marwadi: 'म्हारी ऐनक कठै राख दी?'\n"
"English: 'My eyes are hurting.' -> Marwadi: 'म्हारे आंख्यां में दरद है।'\n"
"English: 'Take the medicine on time.' -> Marwadi: 'दवाई बखत माथे ले लीजो।'\n"
"English: 'He has a fever.' -> Marwadi: 'बींने ताव आय रयो है।'\n"
"English: 'Wrap a blanket.' -> Marwadi: 'गोदड़ी (कंबल) ओढ़ ल्यो।'\n"
"English: 'It is raining heavily.' -> Marwadi: 'घणो जोर रो मे (बारिश) आय रयो है।'\n"
"English: 'The streets are flooded.' -> Marwadi: 'गळियां में पाणी भर गयो है।'\n"
"English: 'Walk carefully.' -> Marwadi: 'ध्यान ऊं चालजो।'\n"
"English: 'Don't slip in the mud.' -> Marwadi: 'कीचड़ में रपट मत ज्याजो।'\n"
"English: 'Dry the clothes on the roof.' -> Marwadi: 'गाबा (कपड़ा) छत माथे सूका द्यो।'\n"
"English: 'Bring the cows inside.' -> Marwadi: 'गायां ने मांयने कर द्यो।'\n"
"English: 'Give fodder to the buffalo.' -> Marwadi: 'भैंस ने नीरो (चारा) घाल द्यो।'\n"
"English: 'Milk the cow.' -> Marwadi: 'गाय रो दूध काढ़ ल्यो।'\n"
"English: 'I am going to the temple.' -> Marwadi: 'मैं मंदिर जा रयूँ हूँ।'\n"
"English: 'Fold your hands.' -> Marwadi: 'हाथ जोड़ ल्यो।'\n"
"English: 'God bless everyone.' -> Marwadi: 'भगवान सगळां रो भलो करे।'\n"
"English: 'Light a lamp.' -> Marwadi: 'दीवो कर द्यो।'\n"
"English: 'Give some donation.' -> Marwadi: 'थोड़ो दान-पुन्न कर द्यो।'\n"
"English: 'Don't hurt animals.' -> Marwadi: 'जानवर ने मत सताओ।'\n"
"English: 'Always speak the truth.' -> Marwadi: 'हमेसा साची बात बोलो।'\n"
"English: 'Respect your parents.' -> Marwadi: 'माँ-बाप रो आदर करो।'\n"
"English: 'Life is very short.' -> Marwadi: 'जिंदगी घणी छोटी है।'\n"
"English: 'Be happy always.' -> Marwadi: 'हमेसा राजी खुशी रीयो।'\n"
"English: 'I have a headache.' -> Marwadi: 'म्हारो माथो दरद कर रयो है।'\n"
"English: 'Apply some balm.' -> Marwadi: 'थोड़ो बाम लगा द्यो।'\n"
"English: 'I cannot walk more.' -> Marwadi: 'म्हारे ऊं और कोनी चालीजै।'\n"
"English: 'My legs are tired.' -> Marwadi: 'म्हारा पग थक ग्या है।'\n"
"English: 'Sit here under the shade.' -> Marwadi: 'अठै छांवरे में बैठ ज्याओ।'\n"
"English: 'Let's rest for a while.' -> Marwadi: 'चालो थोड़ी देर सुस्ता ल्यां।'\n"
"English: 'Bring cold water from the pot.' -> Marwadi: 'मटकी ऊं सीळो पाणी लेर आवो।'\n"
"English: 'Wash your face.' -> Marwadi: 'थारो मुंडो धोय ल्यो।'\n"
"English: 'Comb your hair.' -> Marwadi: 'माथो बाह ल्यो।'\n"
"English: 'Wear your shoes.' -> Marwadi: 'थारा जूता पैर ल्यो।'\n"
"English: 'Where are my keys?' -> Marwadi: 'म्हारी चाबियां कठै है?'\n"
"English: 'Lock the cupboard.' -> Marwadi: 'अलमारी रे ताळो लगा द्यो।'\n"
"English: 'Count the money.' -> Marwadi: 'पीसा गिण ल्यो।'\n"
"English: 'Don't waste money.' -> Marwadi: 'पीसा खराब मत करो।'\n"
"English: 'Save for the future.' -> Marwadi: 'आगले बखत सारू बसाय र राखो।'\n"
"English: 'Gold is very expensive now.' -> Marwadi: 'सोनो अबार घणो मँघो वे गयो है।'\n"
"English: 'Buy some silver bangles.' -> Marwadi: 'चांदी री चूड़ियां खरीद ल्यो।'\n"
"English: 'Wear a nice dress.' -> Marwadi: 'एक सोवणो गाबो (कपड़ो) पैर ल्यो।'\n"
"English: 'This color looks good on you.' -> Marwadi: 'ओ रंग थारे माथे घणो फबे है।'\n"
"English: 'Let's take a picture.' -> Marwadi: 'चालो एक फोटो खींचां।'\n"
"English: 'Smile a little.' -> Marwadi: 'थोड़ो सा हंस द्यो।'\n"
"English: 'The festival is coming.' -> Marwadi: 'त्यूहार आय रयो है।'\n"
"English: 'Clean the whole house.' -> Marwadi: 'सगळो घर साफ कर द्यो।'\n"
"English: 'Make sweet rice.' -> Marwadi: 'मीठा चावल बणाओ।'\n"
"English: 'Invite the neighbors.' -> Marwadi: 'पड़ोसियां ने बुलावो।'\n"
"English: 'Distribute the sweets.' -> Marwadi: 'मीठाई बांट द्यो।'\n"
"English: 'Let's fly kites.' -> Marwadi: 'चालो पतंग उड़ावां।'\n"
"English: 'The wind is blowing fast.' -> Marwadi: 'हवा घणी तेज चाल रयी है।'\n"
"English: 'Hold the thread tightly.' -> Marwadi: 'मांझो पक्को पकड़ र राखजो।'\n"
"English: 'Look at the sky.' -> Marwadi: 'आसमान सामी देखो।'\n"
"English: 'The stars are shining.' -> Marwadi: 'तारा चमक रया है।'\n"
"English: 'The moon is very bright today.' -> Marwadi: 'आज चांद घणो फूटरो लागे है।'\n"
"English: 'It is a beautiful night.' -> Marwadi: 'आ घणी सोवणी रात है।'\n"
"English: 'Tell me a joke.' -> Marwadi: 'मने एक चुटकलो सुणाओ।'\n"
"English: 'You are very funny.' -> Marwadi: 'थे घणा मजाकिया हो।'\n"
"English: 'I am laughing so hard.' -> Marwadi: 'म्हारे तो हंस-हंस र पेट में दरद वे गयो।'\n"
"English: 'Don't tease him.' -> Marwadi: 'बींने मत छेड़ो।'\n"
"English: 'He will start crying.' -> Marwadi: 'वो रोवण लाग ज्यावेला।'\n"
"English: 'Wipe your tears.' -> Marwadi: 'थारा आंसू लूंछ ल्यो।'\n"
"English: 'Don't cry like a child.' -> Marwadi: 'टाबरां ज्यूं मत रोवो।'\n"
"English: 'Be brave.' -> Marwadi: 'हिम्मत राखो।'\n"
"English: 'I am always with you.' -> Marwadi: 'मैं हमेसा थारे सागे हूँ।'\n"
"English: 'God will fix everything.' -> Marwadi: 'भगवान सगळो ठीक कर देवेला।'\n"
"English: 'Have some patience.' -> Marwadi: 'थोड़ी धीरज राखो।'\n"
"English: 'Haste makes waste.' -> Marwadi: 'उतावळ में काम बिगड़े है।'\n"
"English: 'Do it slowly and carefully.' -> Marwadi: 'काम हळवे और ध्यान ऊं करो।'\n"
"English: 'Where is the carpenter?' -> Marwadi: 'खाती कठै है?'\n"
"English: 'Fix this wooden chair.' -> Marwadi: 'आ लाकड़ी री कुरसी ठीक कर द्यो।'\n"
"English: 'Paint the walls.' -> Marwadi: 'भींतां रे रंग कर द्यो।'\n"
"English: 'The roof is leaking.' -> Marwadi: 'छत चूय रयी है।'\n"
"English: 'Call the plumber.' -> Marwadi: 'नल आळे ने बुलावो।'\n"
"English: 'The pipe is broken.' -> Marwadi: 'पाइप टूट गयो है।'\n"
"English: 'Fill the bucket with water.' -> Marwadi: 'बाल्टी में पाणी भर ल्यो।'\n"
"English: 'Water the plants.' -> Marwadi: 'पौधां ने पाणी पावो।'\n"
"English: 'The flowers are blooming.' -> Marwadi: 'फूल खील रया है।'\n"
"English: 'Pluck a red rose.' -> Marwadi: 'एक लाल गुलाब तोड़ ल्यो।'\n"
"English: 'Don't touch the thorns.' -> Marwadi: 'कांटां रे हाथ मत लगाओ।'\n"
"English: 'A snake is in the grass.' -> Marwadi: 'घास में सांप है।'\n"
"English: 'Run away from here.' -> Marwadi: 'अठै ऊं भाग ज्याओ।'\n"
"English: 'I am scared.' -> Marwadi: 'मने डर लागे है।'\n"
"English: 'There is nothing to worry about.' -> Marwadi: 'फिकर री कोई बात कोनी।'\n"
"English: 'I will protect you.' -> Marwadi: 'मैं थारी आडी राखूंगा।'\n"
"English: 'Let's go home now.' -> Marwadi: 'चालो अबार घरे चालां।'\n"
"English: 'Everyone is waiting for us.' -> Marwadi: 'सगळा म्हारो उडीक कर रया है।'\n"
"English: 'Knock on the door.' -> Marwadi: 'किवाड़ खड़काओ।'\n"
"English: 'Who is there?' -> Marwadi: 'बारै कुण है?'\n"
"English: 'It's me, open the door.' -> Marwadi: 'मैं हूँ, किवाड़ खोलो।'\n"
"English: 'Did you bring the vegetables?' -> Marwadi: 'थे सब्जी लेर आया कांई?'\n"
"English: 'I forgot the bag.' -> Marwadi: 'मैं थैलो भूल गयो।'\n"
"English: 'You are very careless.' -> Marwadi: 'थे घणा लापरवाह हो।'\n"
"English: 'I will bring it tomorrow.' -> Marwadi: 'मैं काले लेर आय ज्यावूंला।'\n"
"English: 'Fine, sit and rest.' -> Marwadi: 'ठीक है, बैठ र सुस्ता ल्यो।'\n"
        

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


## ==========================================
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
            Made with <span class="heart">&#10084;</span> by <br>
            <span class="team-names">Bhupesh Danewa • Prajjwal Prajapat • Aniket Prajapat • Kunal Gahlot</span>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
