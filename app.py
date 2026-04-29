import streamlit as st
import time
from data_manager import URGENCY_LEVELS, init_session_state, save_referral, export_results_csv, add_custom_case
from gemini_integration import extract_clinical_data

# Set up page configuration first
st.set_page_config(page_title="Orthopedic AI Research Prototype", layout="wide", page_icon="🦴")

# Inject custom CSS for premium styling
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Primary Headers */
    h1, h2, h3 {
        color: #1E293B;
    }
    
    /* Glassmorphism style for main case containers */
    .case-container {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        transition: transform 0.3s ease;
    }
    
    /* Enhance the sidebar */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    
    /* St.Button styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* AI Assistant Card */
    .ai-card {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border-left: 4px solid #22C55E;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        color: #166534;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize state
init_session_state()

# Sidebar Navigation
st.sidebar.title("🦴 OrthoStudy")
st.sidebar.markdown("---")
st.sidebar.subheader("Experimental Setup")
group = st.sidebar.radio(
    "Select Group Configuration",
    ["Control", "AI-assisted", "Gold Standard"],
    help="Determines the level of assistance provided to the GP."
)

st.sidebar.markdown("---")
with st.sidebar.expander("➕ Add Custom Case"):
    with st.form("custom_case_form", clear_on_submit=True):
        custom_title = st.text_input("Case Title")
        custom_history = st.text_area("Patient History")
        custom_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        
        if st.form_submit_button("Save Case"):
            if custom_title and custom_history and custom_image:
                import os
                if not os.path.exists("uploads"):
                    os.makedirs("uploads")
                
                img_path = os.path.join("uploads", custom_image.name)
                with open(img_path, "wb") as f:
                    f.write(custom_image.getbuffer())
                
                add_custom_case(custom_title, custom_history, img_path)
                st.success("Case added successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Please fill all fields and upload an image.")

st.sidebar.markdown("---")
if st.sidebar.button("Reset Session"):
    st.session_state.referrals = []
    st.session_state.current_case_index = 0
    st.session_state.start_time = None
    st.rerun()

# End of cases flow
if st.session_state.current_case_index >= len(st.session_state.cases):
    st.title("🎉 Session Complete")
    st.success("You have successfully completed all cases in this study module.")
    st.markdown("### Export Results")
    st.write("Click below to download the session data (Time to completion, urgency levels, and referral details) for statistical analysis.")
    
    csv_data = export_results_csv()
    if csv_data:
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name="ortho_study_results.csv",
            mime="text/csv"
        )
    st.stop()

# Start Timer if not started
if st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# Current Case details
current_case = st.session_state.cases[st.session_state.current_case_index]

# Header section
st.title(current_case["title"])
progress = f"Case {st.session_state.current_case_index + 1} of {len(st.session_state.cases)}"
st.caption(f"**{progress}** | Current Group: **{group}**")
st.markdown("---")

# Main Content Layout
col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown("<div class='case-container'>", unsafe_allow_html=True)
    st.subheader("Patient History")
    st.write(current_case["patient_history"])
    
    st.subheader("Imaging")
    try:
        st.image(current_case["image_path"], caption="Anterior-Posterior X-Ray", use_container_width=True)
    except FileNotFoundError:
        st.warning("Mock image not found. Please ensure mock_xray.png is in the same directory.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # --- AI ASSISTED LOGIC ---
    if group == "AI-assisted":
        st.markdown("### 🤖 AI Clinical Assistant")
        if st.button("Generate AI Extraction"):
            with st.spinner("Analyzing clinical data and image..."):
                ai_result = extract_clinical_data(
                    patient_history=current_case["patient_history"],
                    image_path=current_case["image_path"]
                )
                st.markdown(f"<div class='ai-card'><h4>AI Extraction Summary</h4>{ai_result}</div>", unsafe_allow_html=True)
    
    # --- GOLD STANDARD LOGIC ---
    elif group == "Gold Standard":
        st.markdown("### 🌟 Gold Standard Reference")
        st.info("**Expert Orthopedic Evaluation:**\n\nPatient exhibits clear signs of acute rotator cuff tear (given weakness in external rotation and abduction inability following trauma). Immediate MRI recommended. Urgency: Needs appointment in 5 days.")
    
    # --- GP REFERRAL FORM ---
    st.markdown("### 📝 GP Referral Submission")
    with st.form(key=f"form_{current_case['id']}"):
        working_diagnosis = st.text_input("Working Diagnosis")
        recommended_treatment = st.text_area("Recommended Treatment / Next Steps")
        urgency = st.selectbox("Specialist Urgency Level", URGENCY_LEVELS)
        
        submit_button = st.form_submit_button("Submit Referral & Next Case")
        
        if submit_button:
            # Calculate time spent
            end_time = time.time()
            time_spent = round(end_time - st.session_state.start_time, 2)
            
            # Save data
            save_referral(
                case_id=current_case["id"],
                group=group,
                time_spent=time_spent,
                urgency=urgency,
                diagnosis=working_diagnosis,
                treatment=recommended_treatment
            )
            
            # Progress to next case
            st.session_state.current_case_index += 1
            st.session_state.start_time = None # Reset timer for next case
            st.rerun()
