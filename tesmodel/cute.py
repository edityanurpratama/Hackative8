# ===== FILE: cute_password_app.py =====
import streamlit as st
import random
import string
import qrcode
from PIL import Image
import time

# ===== SETUP HALAMAN =====
st.set_page_config(
    page_title="🔐 Password Lucu Analyzer",
    page_icon="🐰",
    layout="centered"
)

# ===== DESAIN LUCU =====
st.markdown("""
<style>
    /* Background warna pelangi */
    .stApp {
        background: linear-gradient(45deg, #ff9a9e, #fad0c4, #fbc2eb, #a6c1ee, #c2e9fb, #d4fc79);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% {background-position: 0% 50%}
        50% {background-position: 100% 50%}
        100% {background-position: 0% 50%}
    }
    
    /* Judul lucu */
    .title {
        font-family: 'Comic Sans MS', cursive;
        color: #ff6b6b;
        text-align: center;
        font-size: 42px;
        text-shadow: 3px 3px 0px #ffd166;
    }
    
    /* Tombol lucu */
    .stButton>button {
        background-color: #ffd166 !important;
        color: #ff6b6b !important;
        border-radius: 20px !important;
        border: 3px dashed #ff6b6b !important;
        font-weight: bold;
        font-family: 'Comic Sans MS', cursive;
        font-size: 20px;
        padding: 10px 24px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.1);
        background-color: #ff6b6b !important;
        color: white !important;
    }
    
    /* Kartu hasil */
    .card {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 25px;
        padding: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border: 5px dotted #ff6b6b;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ===== HEADER LUCU =====
st.markdown('<h1 class="title">🐰 Password Lucu Analyzer 🔍</h1>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; font-family: 'Comic Sans MS'; color: #6a5acd; font-size: 20px">
    Lihat sekuat apa passwordmu! 💪<br>
    Dapatkan QR keren dan saran lucu 🦄
</div>
""", unsafe_allow_html=True)

# ===== FUNGSI SEDERHANA =====
def cek_password(password):
    """Fungsi sederhana cek password"""
    kekuatan = 0
    
    # Aturan sederhana
    if len(password) >= 8:
        kekuatan += 1
    if any(char in "!@#$%^&*()" for char in password):
        kekuatan += 1
    if any(char.isdigit() for char in password):
        kekuatan += 1
    if any(char.isupper() for char in password):
        kekuatan += 1
    
    # Teks lucu berdasarkan kekuatan
    pesan = {
        0: "Oh tidak! Passwordmu seperti kertas basah 😭",
        1: "Hmm.. Masih lemah seperti jelly 🍮",
        2: "Lumayan! Seperti biskuit renyah 🍪",
        3: "Keren! Kuat seperti superhero 💪",
        4: "WOW! Super kuat seperti naga! 🐉"
    }.get(kekuatan, "Error lucu 🐛")
    
    return kekuatan, pesan

def buat_password_panjang(panjang=10):
    """Buat password acak sederhana"""
    huruf = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(huruf) for i in range(panjang))

def buat_qr_lucu(teks):
    """Buat QR code dengan gambar lucu"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(teks)
    qr.make(fit=True)
    
    # Buat QR dengan warna lucu
    img = qr.make_image(fill_color="#ff6b6b", back_color="#ffd166")
    
    # Simpan sementara
    img_path = f"temp_qr_{time.time()}.png"
    img.save(img_path)
    return img_path

# ===== BAGIAN UTAMA APLIKASI =====
st.markdown("---")
st.header("🎈 Masukkan Passwordmu")

# Pilihan: Input manual atau generate
pilihan = st.radio("Mau pakai password:", 
                   ["Passwordku sendiri", "Buat password baru lucu!"],
                   horizontal=True)

password = ""

if pilihan == "Passwordku sendiri":
    password = st.text_input("Tulis password di sini:", type="password")
    st.caption("Psst.. jangan pakai password beneran ya! 😉")
else:
    panjang = st.slider("Pilih panjang password:", 8, 20, 12)
    if st.button("🎁 Buat Password Lucu!"):
        password = buat_password_panjang(panjang)
        st.success(f"Password barumu: **{password}**")
        st.balloons()

# Tombol analisis
if st.button("🔍 Analisis Sekarang!", key="analisis_btn") and password:
    with st.spinner("Menganalisis... Tunggu sebentar ya! 🐢"):
        time.sleep(1)  # Biar lucu kayak loading
        
        # Cek password
        kekuatan, pesan = cek_password(password)
        
        # Tampilkan hasil dalam kartu lucu
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            # Header hasil
            warna = ["#ff6b6b", "#ff9a9e", "#ffd166", "#a6c1ee", "#6a5acd"]
            emoji = ["😭", "😟", "😊", "😎", "🐉"]
            st.markdown(f"""
            <h2 style="text-align:center; color:{warna[kekuatan]}; font-family: 'Comic Sans MS'">
                {emoji[kekuatan]} Kekuatan Password: {kekuatan}/4
            </h2>
            """, unsafe_allow_html=True)
            
            # Pesan lucu
            st.info(f"### {pesan}")
            
            # Saran lucu
            st.markdown("### 💡 Saran Lucu:")
            saran = [
                "Tambahkan lebih banyak karakter!",
                "Pakai simbol lucu seperti @ atau #!",
                "Campur huruf besar dan kecil!",
                "Jangan pakai nama hewan peliharaan! 🐶"
            ]
            for s in random.sample(saran, 2):
                st.write(f"- {s}")
            
            # QR code lucu
            st.markdown("### 🎨 QR Code Passwordmu:")
            qr_img = buat_qr_lucu(password)
            st.image(qr_img, caption="Scan untuk menyimpan password lucumu!")
            
            st.markdown("</div>", unsafe_allow_html=True)
elif password == "":
    st.warning("Masukkan password dulu ya! 🐼")
else:
    st.info("Klik tombol 'Analisis Sekarang!' untuk mulai! 🚀")

# Footer lucu
st.markdown("---")
st.markdown("""
<div style="text-align:center; font-family: 'Comic Sans MS'; color: #6a5acd">
    Dibuat dengan ❤️ untuk pemula | Capstone Project SDI<br>
    🐰🦊🐻🐯🐨
</div>
""", unsafe_allow_html=True)