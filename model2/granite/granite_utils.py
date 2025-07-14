import torch
import logging
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from functools import lru_cache
import re

# Konfigurasi Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("granite_system.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("GraniteAI")

# Konfigurasi Model
MODEL_CONFIG = {
    "classify": "cahya/distil-t5-base-indonesian",
    "summarize": "cahya/flan-t5-base-indonesian",
    "keywords": "cahya/distilbert-base-indonesian",
    "recommend": "cahya/flan-t5-base-indonesian"
}

# Inisialisasi Model dengan Cache
@lru_cache(maxsize=4)
def load_model(model_name):
    """Muat model dengan penanganan error dan optimasi"""
    try:
        logger.info(f"Memuat model: {model_name}")
        
        # Deteksi device otomatis
        device = 0 if torch.cuda.is_available() else -1
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            device_map="auto" if device == 0 else None,
            torch_dtype=torch.float16 if device == 0 else torch.float32,
            low_cpu_mem_usage=True
        )
        
        return pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            device=device
        )
    except Exception as e:
        logger.error(f"Gagal memuat model {model_name}: {str(e)}")
        raise RuntimeError(f"Kesalahan sistem: Model tidak dapat dimuat")

# Fungsi Utama dengan Error Handling
def classify_document(text):
    """Klasifikasikan dokumen ke dalam kategori"""
    try:
        truncated_text = text[:1000]
        pipe = load_model(MODEL_CONFIG["classify"])
        
        prompt = f"""
        ### Instruksi:
        Klasifikasikan teks berikut ke dalam satu kategori: 
        [Hukum, Kesehatan, Teknologi, Pendidikan, Bisnis, Lainnya]
        
        ### Teks:
        {truncated_text}
        
        ### Kategori:
        """
        
        response = pipe(
            prompt,
            max_new_tokens=10,
            temperature=0.1,
            num_beams=3,
            truncation=True
        )
        
        result = response[0]['generated_text'].strip()
        
        # Validasi output
        valid_categories = ["Hukum", "Kesehatan", "Teknologi", "Pendidikan", "Bisnis", "Lainnya"]
        if result not in valid_categories:
            logger.warning(f"Kategori tidak valid: {result}. Menggunakan 'Lainnya'")
            return "Lainnya"
            
        return result
    except Exception as e:
        logger.error(f"Error klasifikasi: {str(e)}")
        return "Lainnya"

def summarize_document(text):
    """Buat ringkasan dokumen"""
    try:
        truncated_text = text[:3000]
        pipe = load_model(MODEL_CONFIG["summarize"])
        
        prompt = f"""
        ### Instruksi:
        Buat ringkasan 3 kalimat dalam bahasa Indonesia yang formal dan jelas.
        
        ### Dokumen:
        {truncated_text}
        
        ### Ringkasan:
        """
        
        response = pipe(
            prompt,
            max_new_tokens=200,
            temperature=0.7,
            num_beams=5,
            truncation=True
        )
        
        summary = response[0]['generated_text'].strip()
        
        # Post-processing
        summary = re.sub(r"\s+", " ", summary)  # Hapus spasi berlebihan
        return summary
    except Exception as e:
        logger.error(f"Error summarisasi: {str(e)}")
        return "Ringkasan tidak tersedia. Silakan coba lagi."

def extract_keywords(text):
    """Ekstrak kata kunci penting"""
    try:
        truncated_text = text[:1000]
        pipe = load_model(MODEL_CONFIG["keywords"])
        
        prompt = f"""
        ### Instruksi:
        Ekstrak 5 kata kunci penting dari teks berikut. 
        Berikan dalam format: kata1, kata2, kata3, ...
        
        ### Teks:
        {truncated_text}
        
        ### Kata Kunci:
        """
        
        response = pipe(
            prompt,
            max_new_tokens=50,
            temperature=0.5,
            num_return_sequences=1,
            truncation=True
        )
        
        keywords = response[0]['generated_text'].strip()
        
        # Formatting
        keywords = [kw.strip() for kw in keywords.split(",") if kw.strip()]
        return keywords[:5]
    except Exception as e:
        logger.error(f"Error ekstraksi kata kunci: {str(e)}")
        return ["Kata kunci tidak tersedia"]

def generate_recommendation(category, text):
    """Buat rekomendasi berdasarkan kategori"""
    try:
        truncated_text = text[:1000]
        pipe = load_model(MODEL_CONFIG["recommend"])
        
        prompt = f"""
        ### Instruksi:
        Berikan satu rekomendasi konkret (1-2 kalimat) berdasarkan teks dan kategori.
        Rekomendasi harus actionable dan dalam bahasa Indonesia.
        
        ### Kategori:
        {category}
        
        ### Teks:
        {truncated_text}
        
        ### Rekomendasi:
        """
        
        response = pipe(
            prompt,
            max_new_tokens=100,
            temperature=0.5,
            num_beams=4,
            truncation=True
        )
        
        recommendation = response[0]['generated_text'].strip()
        return recommendation
    except Exception as e:
        logger.error(f"Error generasi rekomendasi: {str(e)}")
        return "Rekomendasi tidak tersedia. Silakan coba lagi."

# Fungsi Pengujian Sistem
def test_system():
    """Uji semua fungsi dengan teks contoh"""
    test_text = (
        "Pemerintah Indonesia baru saja mengeluarkan regulasi terbaru mengenai "
        "penggunaan teknologi finansial (fintech) dalam sektor perbankan. Regulasi "
        "ini bertujuan untuk melindungi konsumen dan meningkatkan stabilitas sistem "
        "keuangan nasional. Bank Indonesia akan menjadi regulator utama."
    )
    
    print("=== Uji Sistem GraniteAI ===")
    print("Teks Uji:", test_text[:100] + "...")
    
    print("\n1. Klasifikasi Dokumen:")
    category = classify_document(test_text)
    print("Hasil:", category)
    
    print("\n2. Ringkasan Dokumen:")
    summary = summarize_document(test_text)
    print("Hasil:", summary)
    
    print("\n3. Ekstraksi Kata Kunci:")
    keywords = extract_keywords(test_text)
    print("Hasil:", keywords)
    
    print("\n4. Generasi Rekomendasi:")
    recommendation = generate_recommendation(category, test_text)
    print("Hasil:", recommendation)

if __name__ == "__main__":
    test_system()