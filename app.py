import streamlit as st
import google.generativeai as genai
from datetime import datetime
import PIL.Image
import io

# Configurazione Pagina
st.set_page_config(page_title="Decathlon Shift Converter", page_icon="📅")

# Recupero sicuro della chiave dai Secrets di Streamlit
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Configurazione chiave API mancante nei Secrets!")
    st.stop()

st.title("📅 Decathlon Planning to Calendar")
st.info("Carica lo screenshot del tuo planning e l'AI creerà il file per il tuo calendario.")

uploaded_file = st.file_uploader("Trascina qui lo screenshot dei turni", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = PIL.Image.open(uploaded_file)
    st.image(img, caption='Planning caricato', use_container_width=True)
    
    with st.spinner('L\'intelligenza artificiale sta leggendo i turni... attendi...'):
        prompt = """
        Analizza questa immagine di un planning di lavoro Decathlon. 
        Estrai tutti i turni di lavoro visibili. 
        Per ogni turno forniscimi: Data (formato AAAA-MM-GG), Ora Inizio (HH:MM), Ora Fine (HH:MM).
        Rispondi ESCLUSIVAMENTE con una lista in questo formato:
        DATA: 2026-02-17 | INIZIO: 08:30 | FINE: 18:00
        """
        response = model.generate_content([prompt, img])
        data_text = response.text

    if data_text:
        st.subheader("Turni Estratti:")
        st.code(data_text)
        
        # Generazione file ICS
        ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Decathlon App//IT\n"
        lines = data_text.strip().split('\n')
        for line in lines:
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
            label="📥 Scarica file .ics per il Calendario",
            data=ics_content,
            file_name="i_miei_turni.ics",
            mime="text/calendar"
        )
