import streamlit as st
import google.generativeai as genai
from datetime import datetime
import PIL.Image

st.set_page_config(page_title="Decathlon Shift Converter", page_icon="📅")

# Recupero API KEY dai Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Chiave API non trovata nei Secrets di Streamlit!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Sostituisci la vecchia riga del modello con QUESTA:
model = genai.GenerativeModel('gemini-1.5-flash-latest')
st.title("📅 Decathlon Planning to Calendar")

uploaded_file = st.file_uploader("Carica lo screenshot dei turni", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = PIL.Image.open(uploaded_file)
    st.image(img, caption='Immagine caricata', use_container_width=True)
    
    try:
        with st.spinner('L\'IA sta analizzando l\'immagine...'):
            prompt = "Analizza l'immagine e scrivi i turni di lavoro nel formato: DATA: AAAA-MM-GG | INIZIO: HH:MM | FINE: HH:MM. Scrivi solo la lista."
            # Chiamata corretta
            response = model.generate_content([prompt, img])
            data_text = response.text
            st.success("Analisi completata!")
            st.code(data_text)
            
            # Qui andrebbe il resto del codice per il file .ics (quello che avevamo già scritto)
            
    except Exception as e:
        st.error(f"Si è verificato un errore durante l'analisi: {e}")
        st.info("Controlla che la tua API KEY sia attiva su Google AI Studio.")
