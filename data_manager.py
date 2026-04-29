import pandas as pd
import streamlit as st

# Urgency Levels as specified by the user
URGENCY_LEVELS = [
    "needs apointement in 1 day",
    "5 days",
    "1 week",
    "2 Weeks",
    "5 Weeks",
    "not urgent"
]

MOCK_CASES = [
    {
        "id": "CASE_001",
        "title": "Case 1: 45yo Male, Right Shoulder Pain",
        "patient_history": "45-year-old male presents with acute onset of right shoulder pain following a fall while skiing. Patient reports an inability to actively abduct the arm. Weakness in external rotation. No numbness or tingling in the hand.",
        "image_path": "mock_xray.png"
    },
    {
        "id": "CASE_002",
        "title": "Case 2: 62yo Female, Chronic Left Shoulder Pain",
        "patient_history": "62-year-old female with a 6-month history of progressive left shoulder pain. Night pain is significant. Overhead activities are severely limited. Prior conservative treatment with NSAIDs and physical therapy provided minimal relief.",
        "image_path": "mock_xray_case2.png"
    },
    {
        "id": "CASE_003",
        "title": "Case 3: 28yo Male, Recurrent Shoulder Instability",
        "patient_history": "28-year-old male with a history of recurrent anterior dislocations of the right shoulder. First dislocation occurred 3 years ago playing rugby. Since then, he has had 4 subsequent dislocations, some occurring during sleep.",
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
