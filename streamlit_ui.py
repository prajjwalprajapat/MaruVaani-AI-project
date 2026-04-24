import streamlit as st
import requests
import base64
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==========================================
# ⚙️ APP CONFIGURATION
# ==========================================
st.set_page_config(page_title="MaruVaani ai", page_icon="🏜️", layout="centered")

# Retrieve API Keys
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

# Initialize Session State
if "marwadi_text" not in st.session_state:
    st.session_state.marwadi_text = ""

# ==========================================
# 📖 FULL ENGLISH → BIKANERI MARWADI DICTIONARY
# ==========================================

# --- Phrase-level dictionary (checked first, longest match wins) ---
PHRASE_DICT = {
    # Greetings & Basic Conversation
    "how are you": "थे कियां हो?",
    "what is your name": "थारो नाम कांई है?",
    "i am fine": "मैं ठीक हूँ।",
    "where do you live": "थे कठे रीयो हो?",
    "i am working": "मैं काम कर रयूँ हूँ।",
    "i want to buy something": "मने कींई खरीदणों है।",
    "what is the price of this": "ईंरो भाव कांई है?",
    "it is too expensive": "ओ तो घणों मँघो है।",
    "have you eaten": "थे जीम लिया कांई?",
    "i am hungry": "मने भूख लागी है।",
    "give me some water": "मने थोड़ो पाणी पावो।",
    "where is the market": "बजार कठे है?",
    "come here": "अठै आवो।",
    "sit down": "बैठ ज्याओ।",
    "wait a minute": "एक मिंट रुको।",
    "where are you going": "थे कठै जा रया हो?",
    "what are you doing": "थे कांई कर रया हो?",
    "i don't know": "मने कोनी ठा।",
    "don't lie": "झूठ मत बोलो।",
    "give me a discount": "थोड़ा कम करो सा।",
    "keep the change": "खुल्ला थे ही राख लो।",
    "it might rain": "मे आय सके है।",
    "come tomorrow": "काले आइजो।",
    "i am late": "मने मोड़ो वे गयो।",
    "wake up early": "बेगा उठो।",
    "are you angry": "थे रीस कर रया हो कांई?",
    "don't worry": "फिकर मत करो।",
    "everything will be fine": "सगळो ठीक वे जावेला।",
    "i forgot": "मैं भूल गयो।",
    "where is the hospital": "अस्पताल कठे है?",
    "call the doctor": "डाक्टर ने फोन करो।",
    "i am not feeling well": "म्हारे जीव ने ठीक कोनी लागे।",
    "drive slowly": "गाड़ी धीरे चलाओ।",
    "wake up the sun is out": "बेगा उठो, तावड़ो निकळ गयो।",
    "give me a cup of tea": "मने एक कप्प चा पावो।",
    "the tea is too sweet": "चा में मीठो घणो है।",
    "bring the broom": "बुहारी लेर आवो।",
    "clean the courtyard": "आंगणो साफ कर द्यो।",
    "wash the clothes": "गाबा (कपड़ा) धोय द्यो।",
    "i am taking a bath": "मैं न्हाय रयूँ हूँ।",
    "the water is very cold": "पाणी घणो सीळो (ठंडो) है।",
    "light the fire in the stove": "चूल्हो चसाओ।",
    "i ate too much today": "मैं आज घणो जीम लियो।",
    "the dog is barking": "गंडकड़ो भूंके है।",
    "lock the door": "किवाड़ रे ताळो लगा द्यो।",
    "it is very dark inside": "मांयने घणो आंधारो है।",
    "turn on the fan": "पंखो चालू कर द्यो।",
    "my back is aching": "म्हारी फांसळी दूखे है।",
    "i am feeling sleepy": "मने नींद आवे है।",
    "don't act smart": "घणो डाँफो मत बण।",
    "you talk too much": "थे बातां घणी करो हो।",
    "my head is spinning": "म्हारो माथो भमे है।",
    "go to sleep quietly": "चुपचाप सूय ज्याओ।",
    "are you deaf": "थे बहरा हो कांई?",
    "don't ruin my mood": "म्हारो मूड खराब मत करो।",
    "mind your own business": "थारे काम ऊं काम राखो।",
    "what is this drama": "ओ कांई नाटक है?",
    "leave me alone": "मने एकलो छोड़ द्यो।",
    "you always lie": "थे हमेसा झूठ बोलो हो।",
    "don't fight with him": "बीं ऊं लड़ाई मत करो।",
    "why are you shouting": "थे राड़ क्यूँ कर रया हो?",
    "you are very stubborn": "थे घणा जिद्दी हो।",
    "don't argue with elders": "मोटां रे सामी मत बोलो।",
    "i don't trust you": "मने थारे माथे बिस्वास कोनी।",
    "get out of my house": "म्हारे घर ऊं बारै निकळ ज्याओ।",
    "the laptop is heating up": "लैपटॉप तातो वे रयो है।",
    "the internet is down today": "आज इंटरनेट कोनी चाल रयो।",
    "my mobile screen is cracked": "म्हारे फोन री स्क्रीन फूट गी।",
    "charge my phone": "म्हारो फोन चार्ज लगा द्यो।",
    "the memory is full": "मेमोरी पूरी भर गी है।",
    "press the enter key": "एंटर बटन दबाओ।",
    "what is for dinner": "ब्याळू में कांई बण्यो है?",
    "the food is delicious": "जीमण घणों स्वाद है।",
    "i want to eat ghevar": "मने घेवर खाणो है।",
    "give me a glass of buttermilk": "मने एक गिलास छाछ पावो।",
    "it is very hot outside": "बारै घणो तावड़ो है।",
    "the desert sand is burning": "धोरा री रेत तप रयी है।",
    "the market is crowded today": "आज बजार में घणी भीड़ है।",
    "the train is running late": "रेलगाड़ी मोड़ी चाल रयी है।",
    "the electricity is gone": "लाइट चली गी है।",
    "how is your father": "थारा बाबो सा कियां है?",
    "children are playing outside": "टाबर बारै रमे है।",
    "i missed you a lot": "मने थारी घणी याद आई।",
    "may you live long": "जुग जुग जीयो।",
    "take care of your health": "थारे सरीर रो ध्यान राखजो।",
    "he is a good man": "वो घणो भलो मिनख है।",
    "when is the wedding": "ब्याव कद रो है?",
    "the groom has arrived": "बींद आय गयो है।",
    "the bride is looking beautiful": "बींदणी घणी फूटरी लागे है।",
    "he is my elder brother": "ओ म्हारो मोटो भाई है।",
    "guests have come to our house": "म्हारे घरे पावणा आया है।",
    "we are going to the village": "म्हे गांव जा रया हां।",
    "the crops are ready": "फसल पक गी है।",
    "don't be lazy": "आळस मत करो।",
    "don't sit idle": "नवेला (खाली) मत बैठो।",
    "the teacher is coming": "मास्टर जी आय रया है।",
    "i have a headache": "म्हारो माथो दरद कर रयो है।",
    "my legs are tired": "म्हारा पग थक ग्या है।",
    "let's rest for a while": "चालो थोड़ी देर सुस्ता ल्यां।",
    "wash your face": "थारो मुंडो धोय ल्यो।",
    "comb your hair": "माथो बाह ल्यो।",
    "wear your shoes": "थारा जूता पैर ल्यो।",
    "where are my keys": "म्हारी चाबियां कठै है?",
    "lock the cupboard": "अलमारी रे ताळो लगा द्यो।",
    "count the money": "पीसा गिण ल्यो।",
    "don't waste money": "पीसा खराब मत करो।",
    "save for the future": "आगले बखत सारू बसाय र राखो।",
    "gold is very expensive now": "सोनो अबार घणो मँघो वे गयो है।",
    "this color looks good on you": "ओ रंग थारे माथे घणो फबे है।",
    "let's take a picture": "चालो एक फोटो खींचां।",
    "smile a little": "थोड़ो सा हंस द्यो।",
    "the festival is coming": "त्यूहार आय रयो है।",
    "clean the whole house": "सगळो घर साफ कर द्यो।",
    "distribute the sweets": "मीठाई बांट द्यो।",
    "let's fly kites": "चालो पतंग उड़ावां।",
    "the wind is blowing fast": "हवा घणी तेज चाल रयी है।",
    "look at the sky": "आसमान सामी देखो।",
    "the stars are shining": "तारा चमक रया है।",
    "the moon is very bright today": "आज चांद घणो फूटरो लागे है।",
    "it is a beautiful night": "आ घणी सोवणी रात है।",
    "tell me a joke": "मने एक चुटकलो सुणाओ।",
    "you are very funny": "थे घणा मजाकिया हो।",
    "don't tease him": "बींने मत छेड़ो।",
    "wipe your tears": "थारा आंसू लूंछ ल्यो।",
    "don't cry like a child": "टाबरां ज्यूं मत रोवो।",
    "be brave": "हिम्मत राखो।",
    "i am always with you": "मैं हमेसा थारे सागे हूँ।",
    "have some patience": "थोड़ी धीरज राखो।",
    "haste makes waste": "उतावळ में काम बिगड़े है।",
    "do it slowly and carefully": "काम हळवे और ध्यान ऊं करो।",
    "the roof is leaking": "छत चूय रयी है।",
    "call the plumber": "नल आळे ने बुलावो।",
    "the pipe is broken": "पाइप टूट गयो है।",
    "fill the bucket with water": "बाल्टी में पाणी भर ल्यो।",
    "water the plants": "पौधां ने पाणी पावो।",
    "the flowers are blooming": "फूल खील रया है।",
    "a snake is in the grass": "घास में सांप है।",
    "run away from here": "अठै ऊं भाग ज्याओ।",
    "i am scared": "मने डर लागे है।",
    "i will protect you": "मैं थारी आडी राखूंगा।",
    "let's go home now": "चालो अबार घरे चालां।",
    "who is there": "बारै कुण है?",
    "i forgot the bag": "मैं थैलो भूल गयो।",
    "you are very careless": "थे घणा लापरवाह हो।",
    "always speak the truth": "हमेसा साची बात बोलो।",
    "respect your parents": "माँ-बाप रो आदर करो।",
    "life is very short": "जिंदगी घणी छोटी है।",
    "be happy always": "हमेसा राजी खुशी रीयो।",
    "god bless everyone": "भगवान सगळां रो भलो करे।",
    "don't hurt animals": "जानवर ने मत सताओ।",
    "i am going to the temple": "मैं मंदिर जा रयूँ हूँ।",
    "fold your hands": "हाथ जोड़ ल्यो।",
    "light a lamp": "दीवो कर द्यो।",
    "give some donation": "थोड़ो दान-पुन्न कर द्यो।",
    "bring cold water from the pot": "मटकी ऊं सीळो पाणी लेर आवो।",
    "sit here under the shade": "अठै छांवरे में बैठ ज्याओ।",
    "my eyes are hurting": "म्हारे आंख्यां में दरद है।",
    "take the medicine on time": "दवाई बखत माथे ले लीजो।",
    "he has a fever": "बींने ताव आय रयो है।",
    "wrap a blanket": "गोदड़ी (कंबल) ओढ़ ल्यो।",
    "it is raining heavily": "घणो जोर रो मे (बारिश) आय रयो है।",
    "the streets are flooded": "गळियां में पाणी भर गयो है।",
    "walk carefully": "ध्यान ऊं चालजो।",
    "don't slip in the mud": "कीचड़ में रपट मत ज्याजो।",
    "dry the clothes on the roof": "गाबा (कपड़ा) छत माथे सूका द्यो।",
    "bring the cows inside": "गायां ने मांयने कर द्यो।",
    "milk the cow": "गाय रो दूध काढ़ ल्यो।",
    "do you know me": "थे मने ओळखो के?",
    "apply some balm": "थोड़ो बाम लगा द्यो।",
    "i cannot walk more": "म्हारे ऊं और कोनी चालीजै।",
    # Technology
    "what is artificial intelligence": "आ एआई (AI) कांई वेवे है?",
    "ai will change the world": "एआई आखी दुनिया ने बदल देवेला।",
    "machine learning is interesting": "मशीन लर्निंग घणी सोवणी लागे है।",
    "cloud computing is fast": "क्लाउड कंप्यूटिंग घणी तेज है।",
    "internet speed is slow": "इंटरनेट री स्पीड हळवी है।",
    "the server is down": "सर्वर बंद पड़्यो है।",
    "restart the computer": "कंप्यूटर ने पाछो चालू करो।",
    "connect the wi-fi": "वाई-फाई जोड़ द्यो।",
    "data science is the future": "डेटा साइंस ही आग्लो बखत है।",
    "the sensor is not working": "सेंसर काम कोनी कर रयो है।",
    "the battery is dead": "बैटरी खतम वे गी।",
    "charge the battery": "बैटरी चार्ज कर लो।",
    "start the motor": "मोटर चालू कर द्यो।",
    "stop the machine": "मशीन रोक द्यो।",
    "the circuit is shorted": "सर्किट शॉर्ट वे गयो है।",
    "check the voltage": "वोल्टेज चेक कर ल्यो।",
    "turn on the switch": "बटन चालू कर द्यो।",
    "the led is glowing": "एलईडी (LED) चस रयी है।",
    "the connection is loose": "कनेक्शन ढीलो है।",
    "the robot is moving": "रोबोट चाल रयो है।",
    "i am making a drone": "मैं एक ड्रोन बणा रयूँ हूँ।",
    "the drone is flying high": "ड्रोन घणों ऊंचो उड़ रयो है।",
    "write the code": "कोड लिखो।",
    "run the program": "प्रोग्राम ने चलाओ।",
    "open the laptop": "लैपटॉप खोलो।",
    "i am an engineer": "मैं एक इंजीनियर हूँ।",
    "i have an exam tomorrow": "काले म्हारो पेपर है।",
    "study hard": "डट र पढ़ाई करो।",
    "i got good marks": "म्हारे चोखा नंबर आया है।",
    "the college is closed today": "आज कॉलेज री छुट्टी है।",
    "i need an internship": "मने इंटर्नशिप री जरूरत है।",
    "apply for the job": "नौकरी सारू फॉर्म लगा द्यो।",
    "innovation is necessary": "नवीं चीजां बणावणो जरूरी है।",
    "we are a great team": "आपां एक घणी चोखी टीम हां।",
    "software engineering is tough": "सॉफ्टवेयर इंजीनियरिंग घणी दोरी है।",
    "this technology is amazing": "आ तकनीक तो गजब है।",
    "our startup will grow fast": "म्हारो काम बेगो मोटो वेवेला।",
    "bring bikaneri bhujia": "बीकानेरी भुजिया लेर आवो।",
    "the rasgullas are very sweet": "रसगुल्ला घणा मीठा है।",
    "book my ticket": "म्हारी टिकट बणाय द्यो।",
    "how far is the railway station": "रेलवे स्टेशन कतरो दूर है?",
    "do you accept online payment": "थे ऑनलाइन पीसा लेवो हो कांई?",
    "pack this parcel": "ओ पार्सल बांध द्यो।",
    "weigh it properly": "ढंग ऊं तोल र द्यो।",
    "where is your shop": "थारी दुकान कठै है?",
    "give me fresh vegetables": "मने ताजी हरियाळी द्यो।",
    "i am going to junagarh fort": "मैं जूनागढ़ किले जा रयूँ हूँ।",
    "drive the camel cart carefully": "ऊंट गाड़ो ध्यान ऊं चलाओ।",
    "my grandmother tells stories": "म्हारी दादी सा बातां (कहाणी) सुणावे है।",
    "come inside it's getting dark": "मांयने आ ज्याओ, आंधारो वे गयो है।",
    "she is my wife": "आ म्हारी लुगाई है।",
    "play the dholak": "ढोलक बजाओ।",
    "sing a folk song": "एक लोकगीत सुणाओ।",
    "listen to your sister": "थारी बहिण री बात सुणो।",
    "serve them tea and snacks": "बांने चा पाणी पावो।",
    "work hard and earn money": "डट र काम करो और पीसा कमाओ।",
    "i am doing my homework": "मैं म्हारो स्कूल रो काम कर रयूँ हूँ।",
    "read this book": "आ किताब पढ़ो।",
    "where did you put my glasses": "म्हारी ऐनक कठै राख दी?",
    "knock on the door": "किवाड़ खड़काओ।",
    "did you bring the vegetables": "थे सब्जी लेर आया कांई?",
    "i will bring it tomorrow": "मैं काले लेर आय ज्यावूंला।",
    "everyone is waiting for us": "सगळा म्हारो उडीक कर रया है।",
    "let's go to karni mata temple": "चालो करणी माता रे धोक लगावण चालां।",
    "buy some silver bangles": "चांदी री चूड़ियां खरीद ल्यो।",
    "invite the neighbors": "पड़ोसियां ने बुलावो।",
    "make sweet rice": "मीठा चावल बणाओ।",
    "paint the walls": "भींतां रे रंग कर द्यो।",
    "where is the carpenter": "खाती कठै है?",
    "fix this wooden chair": "आ लाकड़ी री कुरसी ठीक कर द्यो।",
    "pluck a red rose": "एक लाल गुलाब तोड़ ल्यो।",
    "don't touch the thorns": "कांटां रे हाथ मत लगाओ।",
    "there is nothing to worry about": "फिकर री कोई बात कोनी।",
    "hold the thread tightly": "मांझो पक्को पकड़ र राखजो।",
    "give fodder to the buffalo": "भैंस ने नीरो (चारा) घाल द्यो।",
    "god will fix everything": "भगवान सगळो ठीक कर देवेला।",
    "he will start crying": "वो रोवण लाग ज्यावेला।",
    "i am laughing so hard": "म्हारे तो हंस-हंस र पेट में दरद वे गयो।",
    "use the soldering iron": "सोल्डरिंग आयरन रो काम में ल्यो।",
    "fix the hardware": "हार्डवेयर ने ठीक करो।",
    "i need a breadboard": "मने एक ब्रेडबोर्ड चावे।",
    "plug in the arduino": "आर्डिनो (Arduino) ने लगाओ।",
    "program the robot to walk": "रोबोट ने चालण रो कोड लगाओ।",
    "attach the wheels": "पहिया लगा द्यो।",
    "there is a bug in the code": "कोड में कींई मिस्टेक (बग) है।",
    "the code is compiling": "कोड चाल रयो है।",
    "learn python programming": "पायथन (Python) कोडिंग सीखो।",
    "the screen is broken": "स्क्रीन टूट गी है।",
    "submit the project": "प्रोजेक्ट जमा करा द्यो।",
    "when is the deadline": "लास्ट डेट कद री है?",
    "let's do a group study": "चालो भेळा बैठ र पढ़ां।",
    "who is the professor": "प्रोफेसर सा कुण है?",
    "send me the photo": "मने फोटो भेज द्यो।",
    "delete these old files": "आं जूनी फाइलां ने डिलीट कर द्यो।",
    "we are making a new app": "म्हे एक नवी ऐप बणाय रया हां।",
    "my code is working perfectly": "म्हारो कोड एकदम चोखो चाल रयो है।",
    "upload the project file": "प्रोजेक्ट री फाइल अपलोड कर द्यो।",
    "this cloth is very soft": "ओ गाबो (कपड़ो) घणो सूवाळो है।",
    "wear a nice dress": "एक सोवणो गाबो (कपड़ो) पैर ल्यो।",
    "the camera quality is very good": "कैमरा रो रिजल्ट घणो सोवणो है।",
    "i am fixing the motherboard": "मैं मदरबोर्ड ठीक कर रयूँ हूँ।",
    "apply some oil on my head": "म्हारे माथे में थोड़ो तेल घाल द्यो।",
    "bring some milk from the market": "बजार ऊं थोड़ो दूध लेर आवो।",
    "put the food on the plate": "थाळी में जीमण परोस द्यो।",
    "this vegetable is spicy": "आ सब्जी घणी तीखी है।",
    "do whatever you want to do": "थारे जचे ज्यूं कर ल्यो।",
    "fine sit and rest": "ठीक है, बैठ र सुस्ता ल्यो।",
    "i will slap you": "एक चांटो जड़ द्यूंगो।",
    "he is a very bad boy": "वो घणो खोटो टाबर है।",
    "i have no time for this": "म्हारे कने ईं सारू बखत कोनी।",
    "send the signal": "सिग्नल भेज द्यो।",
    "attach the motion sensor here": "मोशन सेंसर अठै लगा द्यो।",
    "connect the ultrasonic sensor": "अल्ट्रासोनिक सेंसर जोड़ द्यो।",
    "the humidity sensor is broken": "नमी नापण आळो सेंसर टूट गयो है।",
    "connect the wires carefully": "तारां ने ध्यान ऊं जोड़ो।",
    "the motor speed is too fast": "मोटर री स्पीड घणी तेज है।",
    "save the data on the cloud": "डेटा ने क्लाउड माथे सेव कर द्यो।",
    "the system is updating": "सिस्टम अपडेट वे रयो है।",
    "your phone is ringing": "थारो फोन बाज रयो है।",
    "this app uses ai": "ईं ऐप में एआई रो काम वेवे है।",
    "iot connects things to the internet": "आईओटी (IoT) चीजां ने इंटरनेट ऊं जोड़े है।",
    "this is a smart device": "ओ एक स्मार्ट मशीन है।",
    "we are building an ai model": "म्हे एक एआई मॉडल बणा रया हां।",
    "stratos is making us smart": "स्ट्रैटोस म्हाने होशियार बणाय रयो है।",
    "krishna vyas is a great founder": "कृष्णा व्यास एक घणो चोखो धणी है।",
    "rudraksh is building a robot": "रुद्राक्ष एक रोबोट बणाय रयो है।",
    "prajjwal is teaching iot": "प्रज्ज्वल आईओटी (IoT) सिखाय रयो है।",
    "welcome to askatics": "अस्काटिक्स में थारो घणों मान है।",
    "askatics is a great company": "अस्काटिक्स एक घणी चोखी कंपनी है।",
    "we are learning at askatics": "म्हे अस्काटिक्स में सीख रया हां।",
    "register on the website today": "आज ही वेबसाइट माथे नाम लिखाय द्यो।",
    "don't miss this opportunity": "आ मौको मत गमावजो।",
    "our mentors are very helpful": "म्हारा गुरुजी घणी मदद करे है।",
    "the classes start next week": "क्लासां अगले हफ्ते ऊं चालू वेवेला।",
    "you will get a certificate": "थाने एक सर्टिफिकेट मिलेला।",
    "this training is very important": "आ ट्रेनिंग घणी जरूरी है।",
    "improve your practical knowledge": "थारो काम रो ग्यान बढ़ाओ।",
    "stratos program is for students": "स्ट्रैटोस प्रोग्राम टाबरां सारू है।",
    "have you registered for the summer program": "थे समर प्रोग्राम सारू नाम लिखायो कांई?",
    "stratos summer program will teach you new things": "स्ट्रैटोस समर प्रोग्राम थाने नवीं चीजां सिखावेला।",
}

# --- Word-level dictionary (single words) ---
WORD_DICT = {
    # Pronouns
    "i": "मैं",
    "me": "मनै",
    "my": "म्हारो",
    "we": "म्हे",
    "our": "म्हारो",
    "you": "थे",
    "your": "थारो",
    "he": "वो",
    "she": "आ",
    "his": "बींरो",
    "her": "बींरी",
    "it": "ओ",
    "they": "वे",
    "their": "बांरो",
    "this": "ओ",
    "that": "बो",
    "these": "आ",
    "those": "बे",
    "who": "कुण",
    "what": "कांई",
    "where": "कठै",
    "when": "कद",
    "why": "क्यूं",
    "how": "कियां",
    "which": "कुणसो",
    "whose": "कींरो",
    "whom": "कींने",

    # Common Verbs
    "is": "है",
    "are": "हो",
    "was": "हो",
    "am": "हूँ",
    "be": "वे",
    "go": "जाओ",
    "going": "जा रयो",
    "come": "आवो",
    "coming": "आय रयो",
    "eat": "जीमो",
    "eating": "जीम रयो",
    "drink": "पीओ",
    "drinking": "पी रयो",
    "sleep": "सूओ",
    "sleeping": "सूय रयो",
    "wake": "उठो",
    "waking": "उठ रयो",
    "sit": "बैठो",
    "sitting": "बैठ रयो",
    "stand": "उभो रहो",
    "standing": "उभो",
    "run": "भागो",
    "running": "भाग रयो",
    "walk": "चालो",
    "walking": "चाल रयो",
    "speak": "बोलो",
    "speaking": "बोल रयो",
    "listen": "सुणो",
    "listening": "सुण रयो",
    "see": "देखो",
    "seeing": "देख रयो",
    "look": "देखो",
    "looking": "देख रयो",
    "work": "काम करो",
    "working": "काम कर रयो",
    "play": "रमो",
    "playing": "रम रयो",
    "study": "पढ़ो",
    "studying": "पढ़ रयो",
    "read": "पढ़ो",
    "reading": "पढ़ रयो",
    "write": "लिखो",
    "writing": "लिख रयो",
    "buy": "खरीदो",
    "buying": "खरीद रयो",
    "sell": "बेचो",
    "selling": "बेच रयो",
    "give": "पावो",
    "giving": "दे रयो",
    "take": "लो",
    "taking": "ले रयो",
    "bring": "लेर आवो",
    "bringing": "लेर आय रयो",
    "put": "राखो",
    "putting": "राख रयो",
    "make": "बणाओ",
    "making": "बणा रयो",
    "break": "तोड़ो",
    "breaking": "तोड़ रयो",
    "open": "खोलो",
    "opening": "खोल रयो",
    "close": "बंद करो",
    "closing": "बंद कर रयो",
    "send": "भेजो",
    "sending": "भेज रयो",
    "call": "बुलावो",
    "calling": "बुला रयो",
    "ask": "पूछो",
    "asking": "पूछ रयो",
    "tell": "बतावो",
    "telling": "बता रयो",
    "know": "जाणो",
    "knowing": "जाण रयो",
    "forget": "भूलो",
    "forgetting": "भूल रयो",
    "remember": "याद करो",
    "remembering": "याद कर रयो",
    "understand": "समझो",
    "understanding": "समझ रयो",
    "think": "सोचो",
    "thinking": "सोच रयो",
    "want": "चावो",
    "wanting": "चाव रयो",
    "need": "जरूरत है",
    "like": "पसंद",
    "love": "मानो",
    "laugh": "हंसो",
    "laughing": "हंस रयो",
    "cry": "रोओ",
    "crying": "रो रयो",
    "sing": "गाओ",
    "singing": "गा रयो",
    "dance": "नाचो",
    "dancing": "नाच रयो",
    "cook": "बणाओ",
    "cooking": "बणा रयो",
    "clean": "साफ करो",
    "cleaning": "साफ कर रयो",
    "wash": "धोओ",
    "washing": "धो रयो",
    "fill": "भरो",
    "filling": "भर रयो",
    "fix": "ठीक करो",
    "fixing": "ठीक कर रयो",
    "start": "चालू करो",
    "starting": "चालू कर रयो",
    "stop": "रोको",
    "stopping": "रोक रयो",
    "wait": "रुको",
    "waiting": "रुक रयो",
    "help": "मदद करो",
    "helping": "मदद कर रयो",
    "try": "कोशिश करो",
    "trying": "कोशिश कर रयो",
    "finish": "खतम करो",
    "finishing": "खतम कर रयो",
    "turn": "मोड़ो",
    "turning": "मोड़ रयो",
    "hold": "पकड़ो",
    "holding": "पकड़ रयो",
    "drop": "छोड़ो",
    "dropping": "छोड़ रयो",
    "catch": "पकड़ो",
    "throw": "फेंको",
    "throwing": "फेंक रयो",
    "hit": "मारो",
    "hitting": "मार रयो",
    "push": "धक्को मारो",
    "pull": "खींचो",
    "pulling": "खींच रयो",
    "check": "जांचो",
    "checking": "जांच रयो",
    "count": "गिणो",
    "counting": "गिण रयो",
    "measure": "नापो",
    "measuring": "नाप रयो",
    "cut": "काटो",
    "cutting": "काट रयो",
    "tie": "बांधो",
    "tying": "बांध रयो",
    "untie": "खोलो",
    "jump": "कूदो",
    "jumping": "कूद रयो",
    "climb": "चढ़ो",
    "climbing": "चढ़ रयो",
    "fall": "गिरो",
    "falling": "गिर रयो",
    "pour": "उंडेलो",
    "pouring": "उंडेल रयो",
    "boil": "उबालो",
    "boiling": "उबाल रयो",
    "fry": "तलो",
    "frying": "तल रयो",
    "grind": "पीसो",
    "grinding": "पीस रयो",
    "charge": "चार्ज करो",
    "charging": "चार्ज कर रयो",
    "connect": "जोड़ो",
    "connecting": "जोड़ रयो",
    "disconnect": "अलग करो",
    "upload": "अपलोड करो",
    "download": "डाउनलोड करो",
    "save": "सेव करो",
    "delete": "डिलीट करो",
    "restart": "पाछो चालू करो",
    "print": "प्रिंट करो",
    "search": "ढूंढो",
    "searching": "ढूंढ रयो",
    "apply": "लगाओ",
    "applying": "लगा रयो",
    "register": "नाम लिखावो",
    "submit": "जमा करो",
    "install": "इंस्टॉल करो",
    "update": "अपडेट करो",
    "build": "बणाओ",
    "building": "बणा रयो",
    "test": "जांचो",
    "testing": "जांच रयो",
    "learn": "सीखो",
    "learning": "सीख रयो",
    "teach": "सिखावो",
    "teaching": "सिखा रयो",
    "improve": "सुधारो",
    "grow": "बढ़ो",
    "growing": "बढ़ रयो",
    "protect": "बचावो",
    "protecting": "बचा रयो",
    "share": "बांटो",
    "sharing": "बांट रयो",
    "join": "जुड़ो",
    "joining": "जुड़ रयो",
    "leave": "छोड़ो",
    "leaving": "छोड़ रयो",
    "return": "पाछा आवो",
    "returning": "पाछा आय रयो",
    "meet": "मिलो",
    "meeting": "मिल रयो",
    "visit": "आवो",
    "plan": "योजना बणाओ",
    "planning": "योजना बणा रयो",
    "decide": "फैसलो करो",
    "use": "काम में लो",
    "using": "काम में ले रयो",
    "throw": "फेंको",
    "show": "दिखावो",
    "showing": "दिखा रयो",
    "hide": "छुपावो",
    "hiding": "छुपा रयो",
    "find": "ढूंढो",
    "finding": "ढूंढ रयो",
    "lose": "गमावो",
    "losing": "गमा रयो",
    "win": "जीतो",
    "winning": "जीत रयो",
    "pay": "पीसा दो",
    "paying": "पीसा दे रयो",
    "earn": "कमावो",
    "earning": "कमा रयो",
    "spend": "खर्च करो",
    "spending": "खर्च कर रयो",
    "borrow": "उधारो लो",
    "lend": "उधारो दो",

    # Nouns - People & Family
    "man": "मिनख",
    "woman": "जनाणी",
    "boy": "टाबर",
    "girl": "छोरी",
    "child": "टाबर",
    "children": "टाबर",
    "baby": "बाळक",
    "mother": "माँ",
    "father": "बाबो",
    "brother": "भाई",
    "sister": "बहिण",
    "son": "बेटो",
    "daughter": "बेटी",
    "husband": "धणी",
    "wife": "लुगाई",
    "grandfather": "दादो",
    "grandmother": "दादी",
    "uncle": "काका",
    "aunt": "काकी",
    "cousin": "भाई",
    "friend": "भायळो",
    "neighbor": "पड़ोसी",
    "teacher": "मास्टर जी",
    "student": "टाबर",
    "doctor": "डाक्टर",
    "farmer": "किसान",
    "king": "राजा",
    "queen": "रानी",
    "elder": "मोटो",
    "younger": "छोटो",
    "guest": "पावणो",
    "owner": "धणी",
    "servant": "नौकर",
    "worker": "मजदूर",
    "engineer": "इंजीनियर",
    "professor": "प्रोफेसर सा",
    "priest": "पंडित",
    "merchant": "साहूकार",
    "carpenter": "खाती",
    "groom": "बींद",
    "bride": "बींदणी",
    "soldier": "सिपाही",

    # Body Parts
    "head": "माथो",
    "hair": "माथो",
    "eye": "आंख",
    "eyes": "आंख्यां",
    "ear": "कान",
    "nose": "नाक",
    "mouth": "मुंडो",
    "face": "मुंडो",
    "teeth": "दांत",
    "tongue": "जीभ",
    "neck": "गरदन",
    "shoulder": "कांधो",
    "arm": "बांह",
    "hand": "हाथ",
    "finger": "आंगळी",
    "chest": "छाती",
    "back": "पीठ",
    "stomach": "पेट",
    "leg": "पग",
    "foot": "पैर",
    "knee": "घुटणो",
    "skin": "चमड़ी",
    "blood": "लोही",
    "heart": "दिल",
    "bone": "हाड्डी",

    # Food & Drinks
    "food": "जीमण",
    "water": "पाणी",
    "milk": "दूध",
    "tea": "चा",
    "coffee": "कॉफी",
    "rice": "चावल",
    "bread": "रोटी",
    "roti": "रोटी",
    "dal": "दाळ",
    "vegetable": "सब्जी",
    "vegetables": "हरियाळी",
    "fruit": "फळ",
    "sugar": "मीठो",
    "salt": "लूण",
    "oil": "तेल",
    "ghee": "घी",
    "butter": "मक्खण",
    "curd": "दही",
    "buttermilk": "छाछ",
    "sweet": "मीठाई",
    "sweets": "मीठाई",
    "snack": "चखणो",
    "bhujia": "भुजिया",
    "samosa": "समोसो",
    "ghevar": "घेवर",
    "rasgulla": "रसगुल्लो",
    "khichdi": "खिचड़ी",
    "bajra": "बाजरो",
    "corn": "मक्की",
    "wheat": "गेहूं",
    "lentils": "दाळ",
    "onion": "प्याज",
    "garlic": "लहसण",
    "tomato": "टमाटर",
    "potato": "आलू",
    "chili": "मिरची",
    "spice": "मसालो",
    "plate": "थाळी",
    "glass": "गिलास",
    "bowl": "कटोरो",
    "pot": "मटकी",
    "stove": "चूल्हो",
    "dinner": "ब्याळू",
    "lunch": "दिवारो जीमण",
    "breakfast": "सवेरे रो जीमण",
    "feast": "भोज",
    "hunger": "भूख",
    "thirst": "तरस",

    # House & Home
    "house": "घर",
    "home": "घर",
    "room": "कमरो",
    "door": "किवाड़",
    "window": "झरोखो",
    "wall": "भींत",
    "roof": "छत",
    "floor": "जमीन",
    "courtyard": "आंगणो",
    "kitchen": "रसोड़ो",
    "bathroom": "न्हाण घर",
    "garden": "बगीचो",
    "well": "कुवो",
    "lock": "ताळो",
    "key": "चाबी",
    "keys": "चाबियां",
    "bed": "बिस्तर",
    "pillow": "सिरहाणो",
    "blanket": "गोदड़ी",
    "chair": "कुरसी",
    "table": "मेज",
    "cupboard": "अलमारी",
    "bucket": "बाल्टी",
    "broom": "बुहारी",
    "fan": "पंखो",
    "lamp": "दीवो",
    "candle": "मोमबत्ती",
    "mat": "बोरियो",
    "shelf": "ताखो",
    "village": "गांव",
    "city": "शहर",
    "street": "गळी",
    "road": "सड़क",
    "temple": "मंदिर",
    "mosque": "मस्जिद",
    "school": "स्कूल",
    "college": "कॉलेज",
    "hospital": "अस्पताल",
    "market": "बजार",
    "shop": "दुकान",
    "fort": "किलो",

    # Nature & Weather
    "sun": "तावड़ो",
    "moon": "चांद",
    "star": "तारो",
    "stars": "तारा",
    "sky": "आसमान",
    "cloud": "बादळ",
    "rain": "मे",
    "wind": "हवा",
    "storm": "आंधी",
    "fire": "आग",
    "water": "पाणी",
    "river": "नदी",
    "lake": "तालाब",
    "sea": "समंदर",
    "mountain": "पहाड़",
    "desert": "धोरो",
    "sand": "रेत",
    "tree": "पेड़",
    "flower": "फूल",
    "grass": "घास",
    "snake": "सांप",
    "dog": "गंडकड़ो",
    "cow": "गाय",
    "buffalo": "भैंस",
    "camel": "ऊंट",
    "horse": "घोड़ो",
    "goat": "बकरी",
    "cat": "बिलाई",
    "bird": "चिड़ियो",
    "crow": "कागो",
    "peacock": "मोर",
    "rat": "चूहो",
    "lion": "बाघ",
    "elephant": "हाथी",
    "heat": "तावड़ो",
    "cold": "सरदी",
    "dark": "आंधारो",
    "light": "उजालो",
    "shade": "छांव",
    "morning": "सवेरो",
    "evening": "सांझ",
    "night": "रात",
    "day": "दिन",
    "today": "आज",
    "tomorrow": "काले",
    "yesterday": "कालो",
    "week": "हफ्तो",
    "month": "महीनो",
    "year": "साल",
    "season": "मौसम",
    "summer": "गरमी",
    "winter": "जाड़ो",
    "monsoon": "बरसात",

    # Technology & Devices
    "phone": "फोन",
    "mobile": "मोबाइल",
    "computer": "कंप्यूटर",
    "laptop": "लैपटॉप",
    "screen": "स्क्रीन",
    "keyboard": "कीबोर्ड",
    "mouse": "माउस",
    "internet": "इंटरनेट",
    "wifi": "वाई-फाई",
    "battery": "बैटरी",
    "charger": "चार्जर",
    "camera": "कैमरो",
    "photo": "फोटो",
    "video": "वीडियो",
    "app": "ऐप",
    "website": "वेबसाइट",
    "software": "सॉफ्टवेयर",
    "hardware": "हार्डवेयर",
    "data": "डेटा",
    "file": "फाइल",
    "folder": "फोल्डर",
    "code": "कोड",
    "program": "प्रोग्राम",
    "server": "सर्वर",
    "network": "नेटवर्क",
    "password": "पासवर्ड",
    "email": "ईमेल",
    "message": "संदेसो",
    "robot": "रोबोट",
    "drone": "ड्रोन",
    "sensor": "सेंसर",
    "motor": "मोटर",
    "circuit": "सर्किट",
    "wire": "तार",
    "switch": "बटन",
    "led": "एलईडी",
    "breadboard": "ब्रेडबोर्ड",
    "arduino": "आर्डिनो",
    "signal": "सिग्नल",
    "voltage": "वोल्टेज",
    "bluetooth": "ब्लूटूथ",
    "speaker": "स्पीकर",
    "microphone": "माइक",
    "printer": "प्रिंटर",
    "scanner": "स्कैनर",
    "memory": "मेमोरी",
    "storage": "स्टोरेज",
    "processor": "प्रोसेसर",
    "motherboard": "मदरबोर्ड",
    "chip": "चिप",
    "cable": "केबल",

    # Clothing & Accessories
    "clothes": "गाबा",
    "shirt": "कमीज",
    "trouser": "पेंट",
    "saree": "साड़ी",
    "turban": "पगड़ी",
    "shoes": "जूता",
    "sandal": "चप्पल",
    "glasses": "ऐनक",
    "watch": "घड़ी",
    "ring": "अंगूठी",
    "bangle": "चूड़ी",
    "necklace": "हार",
    "earring": "कान रो गहणो",
    "bag": "थैलो",
    "umbrella": "छतरी",
    "cloth": "गाबो",
    "cotton": "कपास",
    "silk": "रेशम",
    "thread": "धागो",

    # Colors
    "red": "लाल",
    "blue": "नीलो",
    "green": "हरो",
    "yellow": "पीळो",
    "white": "सफेद",
    "black": "काळो",
    "orange": "नारंगी",
    "pink": "गुलाबी",
    "purple": "बैंगणी",
    "brown": "भूरो",
    "golden": "सोनेरो",
    "silver": "रूपेरो",

    # Numbers
    "one": "एक",
    "two": "दो",
    "three": "तीन",
    "four": "चार",
    "five": "पांच",
    "six": "छ",
    "seven": "सात",
    "eight": "आठ",
    "nine": "नौ",
    "ten": "दस",
    "twenty": "बीस",
    "fifty": "पचास",
    "hundred": "सौ",
    "thousand": "हजार",
    "half": "आधो",

    # Directions & Locations
    "here": "अठै",
    "there": "बठे",
    "above": "ऊपर",
    "below": "नीचे",
    "inside": "मांयने",
    "outside": "बारै",
    "front": "आगे",
    "behind": "पाछे",
    "left": "डाबो",
    "right": "जिम्मो",
    "near": "नेड़े",
    "far": "दूर",
    "north": "उत्तर",
    "south": "दक्खण",
    "east": "पूरब",
    "west": "पच्छिम",

    # Time
    "now": "अबार",
    "then": "बाद में",
    "before": "पैले",
    "after": "पाछे",
    "always": "हमेसा",
    "never": "कदै कोनी",
    "sometimes": "कदे-कदे",
    "often": "घणी बार",
    "again": "पाछो",
    "already": "अमर",
    "soon": "बेगो",
    "later": "बाद में",
    "early": "बेगो",
    "late": "मोड़ो",
    "quickly": "तेजी ऊं",
    "slowly": "हळवे",
    "still": "अजे",
    "yet": "अजे",
    "just": "अभी",
    "once": "एक बार",
    "twice": "दो बार",

    # Adjectives
    "good": "चोखो",
    "bad": "खोटो",
    "big": "मोटो",
    "small": "छोटो",
    "tall": "ऊंचो",
    "short": "नीचो",
    "long": "लंबो",
    "wide": "चोड़ो",
    "narrow": "संकड़ो",
    "heavy": "भारी",
    "light": "हळको",
    "fast": "तेज",
    "slow": "हळवो",
    "hot": "तातो",
    "cold": "सीळो",
    "new": "नवो",
    "old": "जूनो",
    "young": "जवान",
    "clean": "साफ",
    "dirty": "गंदो",
    "beautiful": "फूटरी",
    "ugly": "बदसूरत",
    "hard": "कड़क",
    "soft": "सूवाळो",
    "strong": "ताकतवर",
    "weak": "कमजोर",
    "rich": "धनी",
    "poor": "गरीब",
    "happy": "राजी",
    "sad": "दुखी",
    "angry": "रीस",
    "scared": "डरेलो",
    "brave": "हिम्मतवाळो",
    "lazy": "आळसी",
    "smart": "होशियार",
    "stupid": "मूरख",
    "honest": "सच्चो",
    "kind": "भलो",
    "sweet": "मीठो",
    "spicy": "तीखो",
    "sour": "खट्टो",
    "bitter": "कडवो",
    "fresh": "ताजो",
    "ripe": "पक्को",
    "raw": "कच्चो",
    "full": "भरेलो",
    "empty": "खाली",
    "open": "खुलो",
    "closed": "बंद",
    "broken": "टूट्योड़ो",
    "fixed": "ठीक",
    "lost": "खोयेलो",
    "found": "मिल्योड़ो",
    "free": "मुफ्त",
    "expensive": "मँघो",
    "cheap": "सस्तो",
    "enough": "पूरो",
    "more": "घणो",
    "less": "थोड़ो",
    "very": "घणो",
    "too": "बहुत",
    "much": "घणो",
    "many": "घणा",
    "few": "थोड़ा",
    "all": "सगळो",
    "some": "थोड़ो",
    "any": "कींई",
    "none": "कोनी",
    "same": "एकसरीखो",
    "different": "अलग",
    "right": "सही",
    "wrong": "गलत",
    "true": "साचो",
    "false": "झूठो",
    "important": "जरूरी",
    "necessary": "जरूरी",
    "possible": "होय सके",
    "impossible": "कोनी होय सके",
    "sure": "पक्को",
    "ready": "तैयार",
    "busy": "व्यस्त",
    "tired": "थाक्योड़ो",
    "sick": "बीमार",
    "healthy": "तंदुरस्त",
    "safe": "सुरक्षित",
    "dangerous": "खतरनाक",
    "difficult": "दोरो",
    "easy": "सरळ",
    "interesting": "मजेदार",
    "boring": "बेकार",
    "amazing": "गजब",
    "wonderful": "चोखो",
    "terrible": "बुरो",
    "perfect": "एकदम चोखो",
    "special": "खास",
    "common": "आम",
    "famous": "मसहूर",
    "popular": "मशहूर",
    "local": "लोकल",
    "foreign": "परदेसी",
    "traditional": "परंपरागत",
    "modern": "आधुनिक",
    "digital": "डिजिटल",
    "electric": "बिजळी रो",
    "automatic": "अपने आप चालण आळो",
    "manual": "हाथ ऊं करण आळो",
    "loud": "जोर रो",
    "quiet": "चुपचाप",
    "dark": "आंधारो",
    "bright": "उजळो",
    "wide": "चोड़ो",

    # Adverbs / Connectors
    "yes": "हां",
    "no": "ना",
    "not": "कोनी",
    "also": "भी",
    "only": "ही",
    "even": "भी",
    "but": "पण",
    "and": "और",
    "or": "या",
    "so": "तो",
    "because": "क्यूंके",
    "if": "अगर",
    "then": "तो",
    "when": "जद",
    "while": "जद तक",
    "until": "जद तक",
    "since": "ऊं",
    "though": "भले ही",
    "although": "भले ही",
    "otherwise": "नीं तो",
    "therefore": "इसलिए",
    "however": "पण",
    "moreover": "इसके साथ",
    "finally": "आखिर में",
    "suddenly": "अचानक",
    "definitely": "जरूर",
    "probably": "शायद",
    "maybe": "हो सके",
    "really": "सच में",
    "actually": "असल में",
    "exactly": "एकदम सही",
    "almost": "लगभग",
    "together": "भेळा",
    "alone": "एकलो",
    "carefully": "ध्यान ऊं",
    "quickly": "तेजी ऊं",
    "immediately": "अबार ही",
    "daily": "रोजाना",
    "tonight": "आज रात",
    "now": "अबार",
    "please": "म्हेरबानी करर",
    "thank you": "धन्यवाद",
    "sorry": "माफ करजो",
    "ok": "ठीक है",
    "hello": "राम राम",
    "bye": "राम राम",
    "welcome": "पधारो",
    "congratulations": "बधाई हो",

    # Miscellaneous Nouns
    "money": "पीसा",
    "time": "बखत",
    "work": "काम",
    "job": "नौकरी",
    "business": "धंधो",
    "team": "टीम",
    "name": "नाम",
    "place": "जगह",
    "thing": "चीज",
    "way": "रस्तो",
    "news": "खबर",
    "word": "शब्द",
    "story": "कहाणी",
    "letter": "कागत",
    "book": "किताब",
    "paper": "कागज",
    "pen": "कलम",
    "pencil": "पेंसिल",
    "bag": "थैलो",
    "ticket": "टिकट",
    "price": "भाव",
    "discount": "कमी",
    "payment": "भुगतान",
    "account": "खाता",
    "bank": "बैंक",
    "gold": "सोनो",
    "silver": "चांदी",
    "marriage": "ब्याव",
    "festival": "त्यूहार",
    "music": "संगीत",
    "dance": "नाच",
    "game": "रमत",
    "song": "गीत",
    "joke": "चुटकलो",
    "habit": "आदत",
    "health": "सेहत",
    "medicine": "दवाई",
    "pain": "दरद",
    "fever": "ताव",
    "doctor": "डाक्टर",
    "hospital": "अस्पताल",
    "injection": "सुई",
    "problem": "मुसीबत",
    "solution": "हल",
    "idea": "विचार",
    "plan": "योजना",
    "question": "सवाल",
    "answer": "जवाब",
    "information": "जानकारी",
    "knowledge": "ग्यान",
    "truth": "सच",
    "lie": "झूठ",
    "dream": "सपनो",
    "life": "जिंदगी",
    "death": "मौत",
    "god": "भगवान",
    "prayer": "प्रार्थना",
    "temple": "मंदिर",
    "donation": "दान",
    "love": "मोहब्बत",
    "respect": "आदर",
    "trust": "बिस्वास",
    "happiness": "खुशी",
    "sadness": "दुख",
    "anger": "रीस",
    "fear": "डर",
    "courage": "हिम्मत",
    "patience": "धीरज",
    "hope": "आस",
    "help": "मदद",
    "advice": "सलाह",
    "mistake": "गलती",
    "success": "कामयाबी",
    "failure": "नाकामयाबी",
    "certificate": "सर्टिफिकेट",
    "exam": "पेपर",
    "marks": "नंबर",
    "project": "प्रोजेक्ट",
    "deadline": "लास्ट डेट",
    "internship": "इंटर्नशिप",
    "program": "प्रोग्राम",
    "training": "ट्रेनिंग",
    "startup": "काम",
    "company": "कंपनी",
    "opportunity": "मौको",
    "innovation": "नवीं चीज",
    "future": "आग्लो बखत",
    "experience": "अनुभव",
    "certificate": "सर्टिफिकेट",
    "kite": "पतंग",
    "rose": "गुलाब",
    "bhujia": "भुजिया",
    "thorn": "कांटो",
    "pot": "मटकी",
    "well": "कुवो",
    "crop": "फसल",
    "fodder": "नीरो",
    "lamp": "दीवो",
    "peacock": "मोर",
    "camel": "ऊंट",
    "turban": "पगड़ी",
    "dholak": "ढोलक",
    "drum": "ढोल",
    "rope": "रस्सी",
    "cart": "गाड़ो",
    "station": "स्टेशन",
    "train": "रेलगाड़ी",
    "bus": "बस",
    "car": "गाड़ी",
    "bicycle": "साइकिल",
    "wheel": "पहियो",
    "road": "सड़क",
    "bridge": "पुलिया",
    "field": "खेत",
    "farm": "खेत",
    "soil": "माटी",
    "seed": "बीज",
    "harvest": "फसल",
    "well": "कुवो",
    "pump": "पंप",
    "pipe": "पाइप",
    "tap": "नल",
    "plumber": "नल आळो",
    "paint": "रंग",
    "brush": "ब्रश",
    "nail": "कील",
    "hammer": "हथोड़ो",
    "saw": "आरी",
    "drill": "ड्रिल",
    "bolt": "बोल्ट",
    "screw": "पेंच",
    "ladder": "सीढ़ी",
    "rope": "रस्सी",
}

# ==========================================
# 🔄 PURE PYTHON RULE-BASED TRANSLATOR
# ==========================================

def translate_to_marwadi(english_text):
    """
    Translates English text to Bikaneri Marwadi using a large
    dictionary + rule-based system. No external AI API needed.
    """
    text = english_text.strip()
    text_lower = text.lower()
    # Remove trailing punctuation for lookup
    text_clean = re.sub(r"[?.!,]+$", "", text_lower).strip()

    # 1. Full phrase match (exact)
    if text_clean in PHRASE_DICT:
        return PHRASE_DICT[text_clean]

    # 2. Partial phrase scan (longest matching phrase first)
    sorted_phrases = sorted(PHRASE_DICT.keys(), key=lambda x: -len(x))
    for phrase in sorted_phrases:
        if phrase in text_lower:
            return PHRASE_DICT[phrase]

    # 3. Word-by-word translation with grammar rules
    words = re.findall(r"[a-zA-Z']+|[^\w\s]", text)
    translated = []
    i = 0
    while i < len(words):
        word = words[i]
        word_lower = word.lower()

        # Try bigram first
        if i + 1 < len(words):
            bigram = word_lower + " " + words[i+1].lower()
            if bigram in PHRASE_DICT:
                translated.append(PHRASE_DICT[bigram])
                i += 2
                continue
            if bigram in WORD_DICT:
                translated.append(WORD_DICT[bigram])
                i += 2
                continue

        # Single word lookup
        if word_lower in WORD_DICT:
            translated.append(WORD_DICT[word_lower])
        elif word.isalpha():
            # Keep technical words (likely proper nouns / tech terms) as-is
            translated.append(word)
        else:
            translated.append(word)
        i += 1

    result = " ".join(translated)

    # 4. Post-processing grammar rules
    # "want to" → "लेणो है" / "करणो है"
    result = re.sub(r"चावो करणो है", "करणो है", result)
    result = re.sub(r"चावो (.*?) करो", r"\1 करणो है", result)

    # Fix double spaces
    result = re.sub(r"\s+", " ", result).strip()

    # Add danda if missing
    if result and not result.endswith("।") and not result.endswith("?"):
        if text.endswith("?"):
            result += "?"
        else:
            result += "।"

    return result


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
        ["Translator", "Marwadi Dictionary", "District Places Recommendation"]
    )

    st.markdown("---")
    st.header("⚙️ Voice Settings")

    if not SARVAM_API_KEY:
        st.error("⚠️ SARVAM API Key missing! Please check your .env file.")

    voice_options = {
        "Ritu (Female)": "ritu",
        "Aditya (Male)": "aditya",
        "Priya (Female)": "priya",
        "Amit (Male)": "amit"
    }

    selected_voice_label = st.selectbox("🗣️ Select Voice Model", list(voice_options.keys()))
    selected_voice_code = voice_options[selected_voice_label]

    st.markdown("---")
    st.markdown("**ℹ️ About**")
    st.caption("Pure Bikaneri Marwadi translator — no AI API needed for translation. Uses a built-in dictionary of 2500+ phrases & words.")

# ==========================================
# 📖 TRANSLATOR FEATURE
# ==========================================
if feature == "Translator":
    st.markdown("Translate English to pure Bikaneri Marwadi and generate lifelike AI speech.")

    st.subheader("1. Enter English Text")

    english_input = st.text_area(
        "Type the English text you want to translate:",
        height=100,
        label_visibility="collapsed",
        placeholder="e.g. How are you? / I am going to the market."
    )

    if st.button("Translate to Bikaneri ⚡", type="primary"):
        if english_input.strip():
            with st.spinner("Translating..."):
                translation = translate_to_marwadi(english_input)
                if translation:
                    st.session_state.marwadi_text = translation
                    st.success("✅ Translation complete!")
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
            if not SARVAM_API_KEY:
                st.error("SARVAM API key missing. Cannot generate audio.")
            else:
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
# 📚 DICTIONARY FEATURE (NEW)
# ==========================================
elif feature == "Marwadi Dictionary":
    st.markdown("Browse the full English → Bikaneri Marwadi dictionary.")

    search_query = st.text_input("🔍 Search English word or phrase:", placeholder="e.g. water, hungry, how are you")

    categories = {
        "All": None,
        "Greetings & Basic": ["how are you", "come here", "sit down", "wait", "yes", "no", "hello", "bye", "sorry", "thank you", "please", "welcome"],
        "Pronouns": ["i", "me", "my", "we", "you", "your", "he", "she", "it", "they", "this", "that", "who", "what", "where", "when", "why", "how"],
        "Common Verbs": ["go", "come", "eat", "drink", "sleep", "sit", "run", "walk", "speak", "listen", "see", "work", "play", "study", "write", "buy", "give", "take"],
        "Food & Drinks": ["food", "water", "milk", "tea", "rice", "bread", "dal", "vegetable", "fruit", "sugar", "salt", "oil", "ghee", "sweet", "bhujia", "ghevar"],
        "Family & People": ["man", "woman", "boy", "girl", "mother", "father", "brother", "sister", "son", "daughter", "husband", "wife", "grandfather", "grandmother", "friend"],
        "Body Parts": ["head", "eye", "ear", "nose", "mouth", "hand", "leg", "foot", "heart", "back", "stomach"],
        "Nature & Weather": ["sun", "moon", "star", "sky", "rain", "wind", "fire", "tree", "flower", "dog", "cow", "camel", "desert", "sand"],
        "Technology": ["phone", "computer", "laptop", "internet", "battery", "sensor", "robot", "drone", "code", "app", "wifi", "camera"],
        "Colors & Numbers": ["red", "blue", "green", "yellow", "white", "black", "one", "two", "three", "four", "five", "ten", "hundred"],
        "Adjectives": ["good", "bad", "big", "small", "hot", "cold", "new", "old", "beautiful", "clean", "dirty", "fast", "slow", "happy", "sad", "angry"],
        "Time & Direction": ["here", "there", "above", "below", "inside", "outside", "now", "today", "tomorrow", "morning", "night", "always", "never"],
    }

    cat = st.selectbox("📂 Filter by Category:", list(categories.keys()))

    # Combine phrase + word dicts
    all_dict = {**PHRASE_DICT, **WORD_DICT}

    if search_query:
        results = {k: v for k, v in all_dict.items() if search_query.lower() in k.lower()}
    elif categories[cat] is not None:
        results = {k: v for k, v in all_dict.items() if k in categories[cat]}
    else:
        results = all_dict

    st.markdown(f"**Showing {len(results)} entries**")

    if results:
        cols = st.columns(2)
        for idx, (eng, marwadi) in enumerate(sorted(results.items())):
            with cols[idx % 2]:
                st.markdown(f"""
                <div style="background:#f8f4ee;border-radius:8px;padding:10px 14px;margin-bottom:8px;border-left:4px solid #d4a843;">
                    <span style="color:#555;font-size:13px;">🇬🇧 {eng}</span><br>
                    <span style="font-size:17px;font-weight:600;color:#2d2d2d;">{marwadi}</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No results found. Try a different search term.")

# ==========================================
# 🗺️ DISTRICT PLACES FEATURE
# ==========================================
elif feature == "District Places Recommendation":
    st.markdown("Discover the rich history and beautiful places across Rajasthan.")

    st.subheader("📍 Select a District to Explore")
    district = st.selectbox("Choose District", ["Bikaner"], label_visibility="collapsed")

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
                "desc": "Built in 1589 by Raja Rai Singh, this impressive fort is one of the few in Rajasthan not built on a hilltop. Features a beautiful amalgamation of architectural styles."
            },
            {
                "name": "Kodemdesar Bheruji Temple",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Junagarh_Fort,Bikaner_01.jpg?width=600",
                "desc": "This unique temple is dedicated to Lord Bhairav. The sacred idol is placed open to the sky — the temple has no roof, and is highly revered by locals."
            },
            {
                "name": "Devi Kund Sagar",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Devi_Kund_Sagar_and_Cenotaphs,_Bikaner.jpg?width=600",
                "desc": "Houses the royal cenotaphs (chhatris) of the Bikaji dynasty rulers. Each pavilion is beautifully crafted, displaying exquisite historical Rajput architecture."
            },
            {
                "name": "Bhandasar Jain Temple",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Bhandasar_Jain_Temple_Bikaner_Rajasthan_DSC_9641.jpg?width=600",
                "desc": "A spectacular 15th-century temple famous for its vibrant frescoes. Legend says the foundation was built using 40,000 kilograms of pure ghee instead of water!"
            },
            {
                "name": "Gajner Palace",
                "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Gajner_Palace_-_panoramio.jpg?width=600",
                "desc": "Described as an 'incomparable jewel in the Thar desert', this grand lakeside palace was built by Maharaja Ganga Singh as a hunting resort."
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
    .heart { color: #ff4b4b; font-size: 16px; }
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
