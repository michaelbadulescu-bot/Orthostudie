import pandas as pd
import streamlit as st

# Urgency Levels as specified by the user (German translation)
URGENCY_LEVELS = [
    "Termin in 1 Tag",
    "5 Tage",
    "1 Woche",
    "2 Wochen",
    "5 Wochen",
    "Nicht dringend"
]

MOCK_CASES = [
    {
        "id": "CASE_001",
        "title": "Fall 1: 45-jähriger Mann, Schulterschmerzen links",
        "patient_history": "45-jähriger Mann stellt sich mit akut aufgetretenen linken Schulterschmerzen nach einem Sturz beim Skifahren vor. Patient berichtet über eine Unfähigkeit, den Arm aktiv abzuspreizen. Schwäche bei Außenrotation. Keine Taubheit oder Kribbeln in der Hand.",
        "image_path": "mock_xray.png"
    },
    {
        "id": "CASE_002",
        "title": "Fall 2: 62-jährige Frau, chronische linke Schulterschmerzen",
        "patient_history": "62-jährige Frau mit einer 6-monatigen Anamnese von zunehmenden linken Schulterschmerzen. Nachtschmerzen sind signifikant. Überkopfarbeiten sind stark eingeschränkt. Vorherige konservative Behandlung mit NSAR und Physiotherapie brachten kaum Linderung.",
        "image_path": "mock_xray_case2.png"
    },
    {
        "id": "CASE_003",
        "title": "Fall 3: 28-jähriger Mann, rezidivierende Schulterinstabilität",
        "patient_history": "28-jähriger Mann mit einer Vorgeschichte von rezidivierenden vorderen Luxationen der rechten Schulter. Die erste Luxation trat vor 3 Jahren beim Rugby spielen auf. Seitdem hatte er 4 weitere Luxationen, einige davon im Schlaf.",
        "image_path": "mock_xray_case3.png"
    }
]

def init_session_state():
    """Initialize necessary session state variables for tracking."""
    if "cases" not in st.session_state:
        st.session_state.cases = list(MOCK_CASES)
    if "referrals" not in st.session_state:
        st.session_state.referrals = []
    if "current_case_index" not in st.session_state:
        st.session_state.current_case_index = 0
    if "start_time" not in st.session_state:
        st.session_state.start_time = None

def add_custom_case(title, history, image_path):
    """Appends a custom user-uploaded case to the session state."""
    new_case = {
        "id": f"CASE_CUSTOM_{len(st.session_state.cases) + 1}",
        "title": title,
        "patient_history": history,
        "image_path": image_path
    }
    st.session_state.cases.append(new_case)

def save_referral(case_id, group, time_spent, urgency, diagnosis, treatment):
    """Save the referral data to session state."""
    st.session_state.referrals.append({
        "Case ID": case_id,
        "Experimental Group": group,
        "Time Spent (seconds)": time_spent,
        "Urgency": urgency,
        "Working Diagnosis": diagnosis,
        "Recommended Treatment": treatment
    })

def export_results_csv():
    """Convert session state referrals to a CSV string."""
    if not st.session_state.referrals:
        return None
    df = pd.DataFrame(st.session_state.referrals)
    return df.to_csv(index=False).encode('utf-8')
