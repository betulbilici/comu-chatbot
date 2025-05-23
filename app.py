
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


# .env dosyasını yükle
load_dotenv()

# API anahtarı kontrolü
if not os.environ.get("GEMINI_API_KEY"):
    st.error("❌ API anahtarı bulunamadı. Lütfen .env dosyasına GEMINI_API_KEY ekleyin.")

# Gemini API istemcisi başlat
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
model = "models/gemini-2.0-flash"

# .txt dosyasındaki veriyi oku
def oku_veriler():
    try:
        with open("veriler.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Veri dosyası bulunamadı."

# Gemini API'den yanıt al
def gemini_cevapla(soru, veriler):
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""
Aşağıda üniversiteyle ilgili bilgiler var:

{veriler}

Soru: {soru}
""")
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    full_response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        full_response += chunk.text

    return full_response

# --- Streamlit Arayüzü ---
st.set_page_config(page_title="ÇOMÜ Bilgi Asistanı 🤖", page_icon="🎓")
st.title("🎓 ÇOMÜ Bilgi Asistanı")
st.markdown("Üniversite hakkında merak ettiğiniz soruları sorun!")

# Kullanıcıdan soru al
user_input = st.text_input("✍️ Soru girin", placeholder="")

# Cevapla butonuna basılınca
if st.button("Cevapla"):
    if user_input:
        veriler = oku_veriler()
        st.markdown("🧠 Cevap hazırlanıyor...")
        cevap = gemini_cevapla(user_input, veriler)
        st.markdown("### 🤖 Yanıt:")
        st.write(cevap)
    else:
        st.warning("Lütfen bir soru girin.") 
