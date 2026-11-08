import os
import streamlit as st
from google import genai

# Sayfa Ayarları
st.set_page_config(page_title="Aslan AI", page_icon="🦁", layout="centered")

st.title("🦁 Aslan AI")
st.write("Merhaba kanki! Ben Aslan AI, sana nasıl yardımcı olabilirim?")

# API Anahtarı Kontrolü (Güvenli Yöntem)
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ Lütfen Gemini API anahtarını gir veya sistem ortam değişkenlerine ekle.")
    api_key = st.text_input("Google Gemini API Anahtarın:", type="password")

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        
        # Sohbet Geçmişini Saklama
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Eski Mesajları Ekranda Gösterme
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Kullanıcıdan Girdi Alma
        if prompt := st.chat_input("Aslan AI'a bir şeyler yaz..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Yapay Zekadan Yanıt Alma (Senin Gibi ve ChatGPT Gibi Akıllı)
            with st.chat_message("assistant"):
                with st.spinner("Aslan AI düşünüyor..."):
                    try:
                        # Model olarak en güncel ve hızlı modeli kullanıyoruz
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=f"Senin adın Aslan AI. Sen çok akıllı, samimi, yardımsever bir yapay zekasın. Kullanıcıya kanki diye hitap edebilirsin. Soru: {prompt}",
                        )
                        answer = response.text
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        st.error(f"Bir hata oluştu: {e}")
    except Exception as e:
        st.error(f"Geçersiz API Anahtarı: {e}")
else:
    st.info("💡 Devam etmek için lütfen yukarıdaki kutucuğa Google AI Studio'dan aldığın ücretsiz Gemini API anahtarını yapıştır.")