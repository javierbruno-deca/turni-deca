import streamlit as st
import google.generativeai as genai
from PIL import Image  # Modificato per evitare il NameError
import os
from datetime import datetime

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Decathlon Shift Converter", page_icon="📅")

# Recupero API KEY
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Chiave API non trovata nei Secrets!")
    st.stop()

# Configurazione AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Usiamo il modello con il nome standard
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("📅 Decathlon Planning to Calendar")

uploaded_file = st.file_uploader("Carica lo screenshot dei turni", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Usiamo Image.open() direttamente (corregge il NameError)
    img = Image.open(uploaded_file)
    st.image(img, caption='Planning caricato', use_container_width=True)
    
    try:
        with st.spinner('L\'IA sta leggendo i turni...'):
            prompt = """
            Analizza l'immagine del planning Decathlon. 
            Estrai i turni nel formato:
            DATA: AAAA-MM-GG | INIZIO: HH:MM | FINE: HH:MM
            Scrivi solo la lista, un turno per riga.
            """
            # Chiamata all'AI
            response = model.generate_content([prompt, img])
            data_text = response.text
            
            st.success("Analisi completata!")
            st.code(data_text)
            
            # --- GENERAZIONE FILE ICS ---
            ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Decathlon App//IT\n"
            lines = data_text.strip().split('\n')
            for line in lines:
                if "|" in line:
                    try:
                        parts = line.split('|')
                        date_str = parts[0].replace("DATA:", "").strip()
                        start_str = parts[1].replace("INIZIO:", "").strip()
                        end_str = parts[2].replace("FINE:", "").strip()
                        
                        dt_start = datetime.strptime(f"{date_str} {start_str}", "%Y-%m-%d %H:%M").strftime("%Y%m%dT%H%M%S")
                        dt_end = datetime.strptime(f"{date_str} {end_str}", "%Y-%m-%d %H:%M").strftime("%Y%m%dT%H%M%S")
                        
                        ics_content += f"BEGIN:VEVENT\nSUMMARY:Lavoro Decathlon\nDTSTART:{dt_start}\nDTEND:{dt_end}\nEND:VEVENT\n"
                    except:
                        continue
            ics_content += "END:VCALENDAR"

            st.download_button(
                label="📥 Scarica file .ics",
                data=ics_content,
                file_name="miei_turni.ics",
                mime="text/calendar"
            )

    except Exception as e:
        st.error(f"Errore durante l'analisi: {e}")
