import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# --- 1. إعدادات وتنسيق الصفحة ---
st.set_page_config(page_title="JAI - رعاية القلب الذكية", page_icon="❤️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    .stButton > button { border-radius: 12px; font-weight: bold; width: 100%; height: 3em; }
    .chat-box { background-color: #f1f3f4; padding: 15px; border-radius: 15px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة الحالة (Session State) ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'data_history' not in st.session_state:
    st.session_state.data_history = pd.DataFrame(columns=['الوقت', 'النبض', 'الضغط', 'الأكسجين', 'الحالة', 'اللون'])

# --- 3. وظائف المساعد الذكي JAI ---
def predict_health(hr, bp, ox):
    if hr > 110 or bp > 150 or ox < 90: return "خطير", "#ff4b4b"
    elif hr > 100 or bp > 140 or ox < 94: return "متوسط", "#ffaa00"
    return "طبيعي", "#28a745"

def jai_robot(query)
def jai_robot(query):
    query = query.lower()
    
    # 1. الرد على التحية
    if any(word in query for word in ["هلا", "مرحبا", "السلام", "hi", "hello"]):
        return f"أهلاً بكِ يا مبرمجة {st.session_state.user_name}! أنا JAI، مستشارك لسلامة القلب. كيف يمكنني مساعدتكِ اليوم؟"
    
    # 2. شرح فكرة المشروع (IoT)
    elif any(word in query for word in ["كيف يعمل", "طريقة", "IoT", "كيف"]:
        return "سؤال ذكي! النظام يستخدم مستشعرات (IoT) لجمع نبضات قلبكِ، ثم يرسلها للسحابة حيث أقوم أنا (الذكاء الاصطناعي) بتحليلها فوراً للتنبؤ بأي خطر."
    
    # 3. تحليل البيانات الحالية
    elif any(word in query for word in ["حالتي", "صحتي", "قلبي", "البيانات"]):
        last_status = st.session_state.data_history['الحالة'].iloc[-1] if not st.session_state.data_history.empty else "غير معروفة"
        if last_status == "طبيعي":
            return "بناءً على آخر القراءات، مؤشراتكِ الحيوية ممتازة ومستقرة. استمري في نمط حياتكِ الصحي!"
        else:
            return "ألاحظ بعض الاضطرابات في القراءات الأخيرة. أنصحكِ بالجلوس والراحة ومراقبة النبض مجدداً."
    
    # 4. تقديم نصائح طبية
    elif any(word in query for word in ["نصيحة", "بماذا تنصح", "نصيحه"]):
        return "إليكِ نصيحة JAI: احرصي على تقليل الملح في الطعام، ومارسي رياضة المشي لمدة 30 دقيقة، وتجنبي السهر، فهذا يقوي عضلة قلبكِ بشكل رائع."
    
    # 5. معلومات عن المبرمجة
    elif "مين صممك" in query or "من برمجك" in query:
        return f"لقد قامت المبرمجة المبدعة {st.session_state.user_name} بتصميمي وبرمجتي لأكون رفيقاً ذكياً لمرضى القلب."
    
    # الرد الافتراضي إذا لم يفهم السؤال
    else:
        return "عذراً، لم أفهم سؤالكِ تماماً. هل تريدين معرفة (كيف يعمل النظام)، (نصيحة صحية)، أو (تحليل لحالتكِ الحالية)؟"# --- 4. منطق الصفحات ---

# الصفحة الأولى: الترحيب والتسجيل
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center; color: #cc0000;'>❤️ مرحباً بك في منصة JAI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>نظام إنترنت الأشياء المتقدم لرعاية مرضى القلب</h3>", unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/iot-concept-illustration_114360-1234.jpg", width=400)
    
    with st.container():
        st.write("---")
        name_input = st.text_input("فضلاً، أدخلي اسمكِ الثلاثي للبدء:")
        if st.button("دخول للمنصة 🚀"):
            if name_input:
                st.session_state.user_name = name_input
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("عذراً، يجب كتابة الاسم أولاً للتمكن من متابعة حالتك الصحية.")

# الصفحة الثانية: لوحة التحكم والبيانات
elif st.session_state.page == "dashboard":
    st.title(f"🏥 لوحة التحكم - المريض: {st.session_state.user_name}")
    
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    with col_nav1:
        if st.button("📟 بدء المحاكاة المباشرة"): st.session_state.sub_page = "sim"
    with col_nav2:
        if st.button("📊 عرض بياناتي"): st.session_state.sub_page = "data"
    with col_nav3:
        if st.button("⚠️ التنبيهات"): st.session_state.sub_page = "alerts"

    # المحاكاة (توليد بيانات عشوائية)
    if 'sub_page' not in st.session_state or st.session_state.sub_page == "sim":
        hr, bp, ox = np.random.randint(60, 120), np.random.randint(100, 160), np.random.randint(88, 100)
        status, color = predict_health(hr, bp, ox)
        
        # حفظ البيانات
        new_row = pd.DataFrame({'الوقت': [time.strftime("%H:%M:%S")], 'النبض': [hr], 'الضغط': [bp], 'الأكسجين': [ox], 'الحالة': [status], 'اللون': [color]})
        st.session_state.data_history = pd.concat([st.session_state.data_history, new_row], ignore_index=True).tail(10)
        
        # العرض البصري
        c1, c2, c3 = st.columns(3)
        c1.metric("❤️ نبض القلب", f"{hr} BPM")
        c2.metric("🩸 ضغط الدم", f"{bp} mmHg")
        c3.metric("☁️ الأكسجين", f"{ox} %")
        
        st.markdown(f"<div style='background-color:{color}; padding:20px; border-radius:15px; text-align:center; color:white;'><h3>التنبؤ الذكي: الحالة {status}</h3></div>", unsafe_allow_html=True)
        
        fig = px.line(st.session_state.data_history, x='الوقت', y=['النبض', 'الضغط'], title="الرسوم البيانية للمؤشرات")
        st.plotly_chart(fig, use_container_width=True)
        
        time.sleep(4)
        st.rerun()

    # صفحة البيانات (الجدول)
    elif st.session_state.sub_page == "data":
        st.subheader("📋 سجل القراءات التاريخي")
        st.table(st.session_state.data_history[['الوقت', 'النبض', 'الضغط', 'الأكسجين', 'الحالة']])

    # صفحة التنبيهات
    elif st.session_state.sub_page == "alerts":
        st.subheader("⚠️ سجل التنبيهات العاجلة")
        alerts = st.session_state.data_history[st.session_state.data_history['الحالة'] != "طبيعي"]
        if not alerts.empty:
            for i, row in alerts.iterrows():
                st.markdown(f"<p style='color:{row['اللون']}; font-weight:bold;'>• [{row['الوقت']}] تنبيه {row['الحالة']}: النبض وصل إلى {row['النبض']}</p>", unsafe_allow_html=True)
        else:
            st.success("لا توجد تنبيهات خطيرة حتى الآن.")

    st.write("---")
    # الروبوت التفاعلي (Chatbot)
    st.subheader("🤖 اسألي JAI (الروبوت التفاعلي)")
    user_query = st.text_input("اكتبي سؤالك عن حالتك أو عن المشروع هنا:")
    if user_query:
        response = jai_robot(user_query)
        st.markdown(f"<div class='chat-box'><b>JAI:</b> {response}</div>", unsafe_allow_html=True)

    if st.button("🚪 تسجيل الخروج"):
        st.session_state.page = "home"
        st.session_state.user_name = ""
        st.rerun()

st.markdown("<br><center><b>صُنع بحب بواسطة المبرمجة جوري 👑</b></center>", unsafe_allow_html=True)
