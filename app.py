import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURAZIONE ROBUSTA ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Chiave API mancante nei Secrets!")
    st.stop()

# Forza l'uso della versione stabile delle API per evitare l'errore v1beta
os.environ["GOOGLE_API_USE_GVC"] = "true" 

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Usa questo nome esatto, che è il più compatibile in assoluto
model = genai.GenerativeModel('gemini-1.5-flash')
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
