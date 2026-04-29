import os
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image
import streamlit as st

load_dotenv()

# Configure the Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY or API_KEY == "your_api_key_here":
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

if API_KEY and API_KEY != "your_api_key_here":
    genai.configure(api_key=API_KEY)

def extract_clinical_data(patient_history, image_path):
    """
    Uses Gemini 1.5 to extract and structure clinical data from the provided history and image.
    """
    if not API_KEY or API_KEY == "your_api_key_here":
        return "⚠️ Gemini API-Key fehlt! Bitte in den Streamlit Settings unter 'Secrets' eintragen."

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        Du bist ein orthopädischer KI-Expertenassistent. Analysiere die vorliegende Patientenanamnese und das medizinische Bild.
        Extrahiere und strukturiere die Daten logisch, um einen Hausarzt bei der Überweisung zu unterstützen.
        Bitte antworte zwingend auf Deutsch.
        
        Patientenanamnese:
        {patient_history}
        
        Bitte erstelle eine strukturierte Zusammenfassung mit:
        - Wichtigste Befunde
        - Verdachtsdiagnose
        - Empfohlene Dringlichkeit für eine fachärztliche Vorstellung
        - Empfohlene nächste Schritte / Bildgebung
        """
        
        contents = [prompt]
        
        # Load and append the image if it exists
        if os.path.exists(image_path):
            img = PIL.Image.open(image_path)
            contents.append(img)
            
        response = model.generate_content(contents)
        return response.text

    except Exception as e:
        return f"❌ Error during AI extraction: {str(e)}"
