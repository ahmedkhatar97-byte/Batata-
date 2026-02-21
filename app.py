import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_mic_recorder import mic_recorder
import time
import os

# --- 🛠️ إعدادات المحرك (السر في السطرين دول) ---
# حط المفتاح بتاعك هنا
MY_API_KEY = "AIzaSyCOdFVcx0W2pdlfh5uDTq-v5DN2zD2ZfWU" 

# إجبار المكتبة على تخطي النسخ القديمة المسببة للـ 404
os.environ["GOOGLE_API_USE_MTLS"] = "never" 
genai.configure(api_key=MY_API_KEY)

# استخدام أحدث موديل فلاش (سريع ومستقر)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 🎨 الستايل والدخول الشيك ---
st.set_page_config(page_title="X ASSISTANT v2", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    .stApp { background-color: #050505; color: #ffffff; }
    .neon-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 55px;
        color: #00f2fe;
        text-align: center;
        text-shadow: 0 0 20px #0fbcf9;
        margin-top: 50px;
    }
    .stChatMessage { border-radius: 20px; border: 1px solid #1e272e; }
    </style>
    """, unsafe_allow_html=True)

# --- 🎬 انيميشن الدخول ---
if 'startup' not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown('<h1 class="neon-title">X ASSISTANT v2</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; color:#4facfe;">System Loading... 🚀</p>', unsafe_allow_html=True)
        time.sleep(2.5)
    st.session_state.startup = True
    placeholder.empty()

# --- 🧠 الذاكرة وحفظ البيانات ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_name" not in st.session_state:
    st.session_state.user_name = "Harreef"

# --- 📂 القائمة الجانبية (الأدوات) ---
with st.sidebar:
    st.markdown(f"### أهلاً يا **{st.session_state.user_name}** 😎")
    st.divider()
    
    # رفع الصور
    img_up = st.file_uploader("📸 ابعت صورة للمساعد", type=["jpg", "png", "jpeg"])
    if img_up:
        st.image(img_up, caption="الصورة جاهزة", use_container_width=True)
    
    st.divider()
    # تسجيل الصوت
    st.write("🎤 سجل رسالة صوتية:")
    audio_data = mic_recorder(start_prompt="إبدأ الكلام", stop_prompt="إرسال", key='mic_recorder')
    
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.chat_history = []
        st.rerun()

# --- 💬 عرض المحادثة ---
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# --- ⌨️ منطقة الإدخال والذكاء الاصطناعي ---
prompt = st.chat_input("تؤمرني بإيه يا حريف؟")

# لو فيه صوت بس مفيش نص، بنفهمه إن فيه تسجيل
if audio_data and not prompt:
    prompt = "لقد أرسلت لك تسجيلاً صوتياً (جاري تطوير معالج الصوت، اسألني حالياً بالكتابة أو الصور)"

if prompt:
    # حفظ الاسم لو المستخدم عرف نفسه
    if "اسمي" in prompt:
        st.session_state.user_name = prompt.split("اسمي")[-1].strip()

    # عرض رسالة المستخدم
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد المساعد
    with st.chat_message("assistant"):
        with st.spinner("جاري جلب المعلومات من النت..."):
            try:
                if img_up:
                    img = Image.open(img_up)
                    response = model.generate_content([prompt, img])
                else:
                    response = model.generate_content(prompt)
                
                final_text = response.text
                st.markdown(final_text)
                st.session_state.chat_history.append({"role": "assistant", "content": final_text})
            except Exception as e:
                st.error(f"عذراً يا حريف، السيرفر لسه مأكسد. الخطأ: {e}")
                st.info("نصيحة: تأكد من تحديث الـ requirements وعمل Reboot App")
  
