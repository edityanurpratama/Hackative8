import streamlit as st
import pandas as pd
from datetime import datetime

# ========================
# FUNGSI ANALISIS
# ========================
def hitung_risiko(data):
    return data['password_length'] * 2 + data['failed_attempts'] * 10

def generate_report(df):
    critical_users = df[df['risk_level'] == 'KRITIS']
    return f"🚨 {len(critical_users)} user berisiko kritis"

# ========================
# DATA CONTOH
# ========================
data = {
    'user_id': [1, 2, 3, 4, 5],
    'password_length': [8, 12, 10, 15, 13],
    'failed_attempts': [3, 1, 2, 4, 0],
    'last_login': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
    'is_locked': [False, False, False, True, False],
    'action_priority': ['HIGH', 'MEDIUM', 'LOW', 'CRITICAL', 'LOW'],
    'security_risk': ['HIGH', 'MEDIUM', 'LOW', 'HIGH', 'MEDIUM'],
    'behavior_pattern': ['BRUTE_FORCE', 'PHISHING', 'BRUTE_FORCE', 'PHISHING', 'NORMAL'],
    'compliance_status': ['NON_COMPLIANT', 'COMPLIANT', 'PARTIAL', 'COMPLIANT', 'NON_COMPLIANT']
}

df = pd.DataFrame(data)
df['last_login'] = pd.to_datetime(df['last_login'])
df['risk_score'] = df.apply(hitung_risiko, axis=1)
df['risk_level'] = df['risk_score'].apply(lambda x: 'KRITIS' if x > 50 else 'AMAN')

# ========================
# DASHBOARD STREAMLIT
# ========================
st.title('🔐 Password Security Analyzer')

# 1. METRICS UTAMA
col1, col2, col3 = st.columns(3)
col1.metric("Total User", len(df))
col2.metric("User KRITIS", len(df[df['risk_level'] == 'KRITIS']))
col3.metric("Rata Password", f"{df['password_length'].mean():.1f} karakter")

# 2. TABEL DATA
st.subheader("Detail User")
st.dataframe(df)

# 3. VISUALISASI
tab1, tab2 = st.tabs(["Distribusi Risiko", "Pattern Analysis"])

with tab1:
    st.bar_chart(df['risk_level'].value_counts())

with tab2:
    st.write("### Pola Perilaku")
    st.bar_chart(df['behavior_pattern'].value_counts())

# 4. LAPORAN OTOMATIS
st.subheader("Laporan Keamanan")
st.warning(generate_report(df))

# 5. FILTER INTERAKTIF
st.sidebar.header("Filter Data")
min_risk = st.sidebar.slider("Risk Score Minimum", 0, 100, 20)
filtered_df = df[df['risk_score'] >= min_risk]
st.sidebar.write(f"Menampilkan {len(filtered_df)} dari {len(df)} user")