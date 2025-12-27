import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
import time

# إعدادات الصفحة
st.set_page_config(page_title="JAI - رعاية القلب", page_icon="❤️", layout="wide")

# إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = "home"
if 'data_history' not in st.session_state:
    st.session_state.data_history = pd.DataFrame(columns=['الوقت', 'النبض', 'الضغط', 'الأكسجين', 'الحالة'])

# نموذج التنبؤ
def predict_risk(hr, bp, ox):
    if hr > 100 or bp > 140 or ox < 90: return "خطر"
    return "طبيعي"

# --- التنقل بين الصفحات ---
if st.session_state.page == "home":
    st.title("دور إنترنت الأشياء في رعاية مرضى القلب ❤️")
    st.markdown("### مرحباً بكِ في نظام JAI الذكي - المبرمجة جوري")
    col1, col2, col3 = st.columns(3)
    if col1.button("🚀 بدء المحاكاة"):
        st.session_state.page = "simulation"
        st.rerun()
    if col2.button("📊 بيانات المريض"):
        st.session_state.page = "data"
        st.rerun()
    if col3.button("⚠️ التنبيهات"):
        st.session_state.page = "alerts"
        st.rerun()

elif st.session_state.page in ["simulation", "data"]:
    st.header("📊 مراقبة المؤشرات الحيوية")
    hr, bp, ox = np.random.randint(60,115), np.random.randint(110,155), np.random.randint(88,100)
    status = predict_risk(hr, bp, ox)
    new_entry = pd.DataFrame({'الوقت': [time.strftime("%H:%M:%S")], 'النبض': [hr], 'الضغط': [bp], 'الأكسجين': [ox], 'الحالة': [status]})
    st.session_state.data_history = pd.concat([st.session_state.data_history, new_entry], ignore_index=True).tail(10)
    st.table(st.session_state.data_history)
    if status == "خطر": st.error("🚨 تنبيه ذكي من JAI: تم رصد حالة غير مستقرة!")
    if st.button("العودة للرئيسية"):
        st.session_state.page = "home"
        st.rerun()
    time.sleep(5)
    st.rerun()

elif st.session_state.page == "alerts":
    st.header("⚠️ سجل التنبيهات الذكية")
    st.write(st.session_state.data_history[st.session_state.data_history['الحالة'] == "خطر"])
    if st.button("العودة"):
        st.session_state.page = "home"
        st.rerun()
