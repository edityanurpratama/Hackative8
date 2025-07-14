import streamlit as st
import time

# Cek dan handle error import dependensi utama
try:
    from granite_utils import classify_document, summarize_document, extract_keywords, generate_recommendation
    ML_READY = True
except Exception as e:
    ML_READY = False
    ML_ERROR = str(e)

try:
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    import qrcode
    from PIL import Image
    import io
except ImportError as e:
    st.error(f"Error import library visualisasi: {e}")
    st.info("Coba install dengan: pip install streamlit matplotlib wordcloud qrcode pillow PyPDF2")
    st.stop()

# Konfigurasi halaman
st.set_page_config(page_title="DocuMind - IBM Granite", page_icon="📄")
st.title("📄 DocuMind: Document Intelligence Dashboard")
st.caption("Powered by IBM Granite Models via Hugging Face")

# Upload dokumen atau input teks
input_method = st.radio("Pilih metode input:", ["Input Teks", "Upload File"])
text = ""
if input_method == "Input Teks":
    text = st.text_area("Masukkan teks dokumen:", height=200)
else:
    uploaded_file = st.file_uploader("Unggah file teks atau PDF", type=["txt", "pdf"])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            try:
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                st.success("File PDF berhasil dibaca.")
            except Exception as e:
                st.error(f"Gagal membaca PDF: {e}. Pastikan file tidak terproteksi.")
        else:
            text = uploaded_file.read().decode("utf-8")

# Tombol analisis
def dummy_result(text):
    return "Lainnya", "(Demo) Ringkasan tidak tersedia.", ["demo", "kata", "kunci"], "(Demo) Rekomendasi tidak tersedia."

if st.button("Analisis Dokumen") and text:
    if not ML_READY:
        st.error(f"Fitur AI tidak tersedia: {ML_ERROR}")
        st.info("Pastikan semua dependensi ML (torch, transformers, sentencepiece, dsb) sudah terinstall dan gunakan Python 3.11 untuk hasil terbaik.")
        st.info("Coba install dengan: pip install torch transformers accelerate sentencepiece safetensors numpy pandas regex")
        # Fallback demo
        category, summary, keywords, recommendation = dummy_result(text)
        processing_time = 0.0
    else:
        with st.spinner("Menganalisis dokumen dengan IBM Granite. Mohon tunggu..."):
            start_time = time.time()
            try:
                category = classify_document(text)
                summary = summarize_document(text)
                keywords = extract_keywords(text)
                recommendation = generate_recommendation(category, text)
            except Exception as e:
                st.error(f"Error saat analisis dokumen: {e}")
                category, summary, keywords, recommendation = dummy_result(text)
            end_time = time.time()
            processing_time = end_time - start_time
    st.success(f"Analisis selesai! Waktu pemrosesan: {processing_time:.2f} detik")
    st.subheader(f"Kategori: :blue[{category}]")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📌 Ringkasan Dokumen")
        st.write(summary)
    with col2:
        st.subheader("🔑 Kata Kunci Utama")
        st.write(", ".join(keywords))
        try:
            wordcloud = WordCloud(width=400, height=200, background_color='white').generate(" ".join(keywords))
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot(plt)
        except Exception as e:
            st.warning(f"Gagal membuat wordcloud: {e}")
    st.subheader("🚀 Rekomendasi")
    st.info(recommendation)
    st.subheader("📲 Bagikan Hasil")
    try:
        qr_data = f"Kategori: {category}\n\nRingkasan: {summary}\n\nKata Kunci: {', '.join(keywords)}\n\nRekomendasi: {recommendation}"
        qr = qrcode.make(qr_data)
        img_bytes = io.BytesIO()
        qr.save(img_bytes, format='PNG')
        st.image(img_bytes, caption="Scan QR untuk melihat hasil analisis", width=200)
    except Exception as e:
        st.warning(f"Gagal membuat QR code: {e}")

# Penjelasan AI
st.divider()
with st.expander("ℹ️ Penjelasan Dukungan AI"):
    st.markdown("""
    **IBM Granite digunakan untuk:**
    - **Klasifikasi Dokumen**: Mengidentifikasi kategori konten (Hukum, Kesehatan, Teknologi, dll)
    - **Summarization**: Membuat ringkasan inti dokumen dalam 3 kalimat
    - **Keyword Extraction**: Menarik kata kunci paling representatif
    - **Recommendation Engine**: Memberikan rekomendasi berbasis insight
                
    **Model:** `ibm/granite-13b-instruct-v1` via Hugging Face Inference API
    """)
# Catatan
st.caption("Note: Aplikasi ini dibuat untuk Capstone Project SDI - Data Classification & Summarization with IBM Granite")
        