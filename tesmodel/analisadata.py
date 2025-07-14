import pandas as pd  # Perbaikan: 'pandas' bukan 'panda'

data = {
    'user_id': [1, 2, 3, 4, 5],
    'password_length': [8, 12, 10, 15, 13],
    'failed_attempts': [3, 1, 2, 4, 0],
    'last_login': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
    'is_locked': [False, False, False, True, False],
    'action_priority': ['HIGH', 'MEDIUM', 'LOW', 'CRITICAL', 'LOW'],  # Diubah untuk variasi
    'security_risk': ['HIGH', 'MEDIUM', 'LOW', 'HIGH', 'MEDIUM'],
    'behavior_pattern': ['BRUTE_FORCE', 'PHISHING', 'BRUTE_FORCE', 'PHISHING', 'NORMAL'],  # Ditambahkan pola normal
    'compliance_status': ['NON_COMPLIANT', 'COMPLIANT', 'PARTIAL', 'COMPLIANT', 'NON_COMPLIANT']  # Ditambahkan partial
}

df = pd.DataFrame(data)

# Convert last_login to datetime
df['last_login'] = pd.to_datetime(df['last_login'])

print("\n📊 Dataframe Contoh:")
print(df)

print("\n🔍 Analisis Singkat:")
print(f"Total user: {len(df)}")
print(f"User terkunci: {df['is_locked'].sum()}")
print(f"Rata-rata panjang password: {df['password_length'].mean():.1f} karakter")

# Fungsi untuk menghitung risiko
def hitung_risiko(data):
    return data['password_length'] * 2 + data['failed_attempts'] * 10

# Menambahkan kolom risk_score dan risk_level
df['risk_score'] = df.apply(hitung_risiko, axis=1)
df['risk_level'] = df['risk_score'].apply(lambda x: 'KRITIS' if x > 50 else 'AMAN')

print("\n⚠️ Analisis Risiko:")
print(df)

#Laporan
def generate_report(df):
    critical_users = df[df['risk_level'] == 'KRITIS']
    return f"🚨 Laporan Keamanan:\n{len(critical_users)} user berisiko kritis"

print(generate_report(df))