import os
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image

load_dotenv()

# Configure the Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY and API_KEY != "your_api_key_here":
    genai.configure(api_key=API_KEY)

def extract_clinical_data(patient_history, image_path):
    """
    Uses Gemini 1.5 to extract and structure clinical data from the provided history and image.
    """
    if not API_KEY or API_KEY == "your_api_key_here":
        return "⚠️ Gemini API key not configured. Please set GEMINI_API_KEY in the .env file."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are an expert orthopedic AI assistant. Analyze the provided clinical history and the medical image.
        Extract and structure the data logically to assist a General Practitioner in making a referral.
        
        Clinical History:
        {patient_history}
        
        Please provide a structured summary including:
        - Key Findings
        - Potential Diagnosis
        - Recommended Urgency Level for Specialist Review
        - Suggested Next Steps / Imaging
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
