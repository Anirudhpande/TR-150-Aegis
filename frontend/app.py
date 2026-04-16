import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
import json

# Configure page
st.set_page_config(
    page_title="Clinical Trial Matching Engine",
    page_icon="🏥",
    layout="wide"
)

# API base URL
API_BASE = "http://localhost:8000"

def get_api_data(endpoint: str):
    """Get data from API endpoint"""
    try:
        response = requests.get(f"{API_BASE}{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

def post_api_data(endpoint: str, data: dict):
    """Post data to API endpoint"""
    try:
        response = requests.post(f"{API_BASE}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

def display_criterion_match(match, is_inclusion=True):
    """Display a single criterion match"""
    status_colors = {
        "met": "🟢",
        "not_met": "🔴", 
        "unclear": "🟡"
    }
    
    status_icon = status_colors.get(match["status"], "⚪")
    criterion_type = "Inclusion" if is_inclusion else "Exclusion"
    
    with st.expander(f"{status_icon} {criterion_type}: {match['criterion'][:60]}..."):
        st.write(f"**Status:** {match['status'].replace('_', ' ').title()}")
        st.write(f"**Evidence:** {match['evidence']}")
        st.write(f"**Confidence:** {match['confidence']:.2f}")

def display_trial_match(match):
    """Display a single trial match"""
    # Color code based on match score
    if match["match_score"] > 0.8:
        score_color = "🟢"
    elif match["match_score"] > 0.6:
        score_color = "🟡"
    else:
        score_color = "🔴"
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(f"{score_color} {match['title']}")
            st.write(f"**Phase:** {match['phase']} | **Condition:** {match['condition']}")
            st.write(f"**Trial ID:** {match['trial_id']}")
        
        with col2:
            st.metric("Match Score", f"{match['match_score']:.2f}")
        
        # Explanation
        st.info(match["explanation"])
        
        # Detailed criteria analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Inclusion Criteria Analysis:**")
            for inclusion_match in match["inclusion_matches"]:
                display_criterion_match(inclusion_match, is_inclusion=True)
        
        with col2:
            st.write("**Exclusion Criteria Analysis:**")
            for exclusion_match in match["exclusion_matches"]:
                display_criterion_match(exclusion_match, is_inclusion=False)
        
        st.divider()

def create_match_summary_chart(matches):
    """Create a summary chart of match scores"""
    if not matches:
        return None
    
    df = pd.DataFrame([
        {
            "Trial": match["title"][:30] + "..." if len(match["title"]) > 30 else match["title"],
            "Match Score": match["match_score"],
            "Phase": match["phase"],
            "Condition": match["condition"]
        }
        for match in matches
    ])
    
    fig = px.bar(
        df, 
        x="Match Score", 
        y="Trial",
        color="Phase",
        title="Trial Match Scores",
        orientation='h'
    )
    fig.update_layout(height=400)
    return fig

def main():
    st.title("🏥 AI-Driven Clinical Trial Matching Engine")
    st.markdown("---")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "Patient Matching", 
        "Sample Patients", 
        "Available Trials",
        "System Status"
    ])
    
    if page == "Patient Matching":
        st.header("Patient-Trial Matching")
        
        # Two modes: sample patient or custom patient
        mode = st.radio("Select Mode:", ["Use Sample Patient", "Enter Custom Patient"])
        
        if mode == "Use Sample Patient":
            # Get sample patients
            patients = get_api_data("/patients")
            if patients:
                patient_options = {f"{p['patient_id']}: {p['age']}y {p['gender']} - {', '.join(p['conditions'][:2])}": p['patient_id'] 
                                 for p in patients}
                
                selected_patient_display = st.selectbox("Select a patient:", list(patient_options.keys()))
                selected_patient_id = patient_options[selected_patient_display]
                
                # Display patient details
                selected_patient = next(p for p in patients if p['patient_id'] == selected_patient_id)
                
                with st.expander("Patient Details", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Age:** {selected_patient['age']}")
                        st.write(f"**Gender:** {selected_patient['gender']}")
                    with col2:
                        st.write(f"**Conditions:** {', '.join(selected_patient['conditions'])}")
                        st.write(f"**Medications:** {', '.join(selected_patient['medications'])}")
                    with col3:
                        st.write("**Lab Values:**")
                        for lab, value in selected_patient['lab_values'].items():
                            st.write(f"- {lab}: {value}")
                    
                    st.write("**Clinical Notes:**")
                    st.write(selected_patient['clinical_notes'])
                
                # Matching parameters
                col1, col2 = st.columns(2)
                with col1:
                    max_trials = st.slider("Maximum trials to return:", 1, 20, 10)
                with col2:
                    include_unclear = st.checkbox("Include unclear matches", value=True)
                
                if st.button("Find Matching Trials", type="primary"):
                    with st.spinner("Analyzing patient and matching trials..."):
                        # Call matching API
                        result = get_api_data(f"/match/{selected_patient_id}?max_trials={max_trials}")
                        
                        if result:
                            st.success(f"Found {len(result['matches'])} matching trials in {result['processing_time']:.2f} seconds")
                            
                            # Summary metrics
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Total Matches", len(result['matches']))
                            with col2:
                                strong_matches = sum(1 for m in result['matches'] if m['match_score'] > 0.8)
                                st.metric("Strong Matches", strong_matches)
                            with col3:
                                avg_score = sum(m['match_score'] for m in result['matches']) / len(result['matches']) if result['matches'] else 0
                                st.metric("Avg Match Score", f"{avg_score:.2f}")
                            with col4:
                                st.metric("Trials Evaluated", result['total_trials_evaluated'])
                            
                            # Match score chart
                            if result['matches']:
                                fig = create_match_summary_chart(result['matches'])
                                if fig:
                                    st.plotly_chart(fig, use_container_width=True)
                            
                            # Detailed results
                            st.header("Detailed Match Results")
                            for i, match in enumerate(result['matches'], 1):
                                st.subheader(f"Match #{i}")
                                display_trial_match(match)
                            
                            # Export option
                            if st.button("Export Results as JSON"):
                                st.download_button(
                                    label="Download JSON",
                                    data=json.dumps(result, indent=2),
                                    file_name=f"trial_matches_{selected_patient_id}.json",
                                    mime="application/json"
                                )
        
        else:  # Custom patient mode
            st.subheader("Enter Custom Patient Data")
            
            col1, col2 = st.columns(2)
            with col1:
                patient_id = st.text_input("Patient ID:", "CUSTOM_001")
                age = st.number_input("Age:", min_value=0, max_value=120, value=50)
                gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
            
            with col2:
                conditions = st.text_area("Conditions (one per line):", "diabetes\nhypertension").split('\n')
                conditions = [c.strip() for c in conditions if c.strip()]
                
                medications = st.text_area("Medications (one per line):", "metformin\nlisinopril").split('\n')
                medications = [m.strip() for m in medications if m.strip()]
            
            clinical_notes = st.text_area("Clinical Notes:", 
                "Patient presents with well-controlled diabetes and hypertension. No recent complications.")
            
            # Lab values
            st.subheader("Lab Values")
            col1, col2, col3 = st.columns(3)
            with col1:
                glucose = st.number_input("Glucose:", value=100.0)
                hemoglobin = st.number_input("Hemoglobin:", value=13.0)
            with col2:
                creatinine = st.number_input("Creatinine:", value=1.0)
                cholesterol = st.number_input("Cholesterol:", value=180.0)
            with col3:
                bmi = st.number_input("BMI:", value=25.0)
            
            lab_values = {
                "glucose": glucose,
                "hemoglobin": hemoglobin,
                "creatinine": creatinine,
                "cholesterol": cholesterol,
                "bmi": bmi
            }
            
            # Vital signs
            col1, col2 = st.columns(2)
            with col1:
                bp_systolic = st.number_input("BP Systolic:", value=120)
                bp_diastolic = st.number_input("BP Diastolic:", value=80)
            with col2:
                heart_rate = st.number_input("Heart Rate:", value=70)
            
            vital_signs = {
                "bp_systolic": bp_systolic,
                "bp_diastolic": bp_diastolic,
                "heart_rate": heart_rate
            }
            
            if st.button("Match Custom Patient", type="primary"):
                # Create patient data
                custom_patient = {
                    "patient_id": patient_id,
                    "age": age,
                    "gender": gender,
                    "conditions": conditions,
                    "medications": medications,
                    "lab_values": lab_values,
                    "clinical_notes": clinical_notes,
                    "vital_signs": vital_signs
                }
                
                # Create matching request
                request_data = {
                    "patient": custom_patient,
                    "max_trials": 10,
                    "include_unclear": True
                }
                
                with st.spinner("Matching custom patient to trials..."):
                    result = post_api_data("/match", request_data)
                    
                    if result:
                        st.success(f"Found {len(result['matches'])} matching trials")
                        
                        # Display results (same as above)
                        for i, match in enumerate(result['matches'], 1):
                            st.subheader(f"Match #{i}")
                            display_trial_match(match)
    
    elif page == "Sample Patients":
        st.header("Sample Patient Profiles")
        
        patients = get_api_data("/patients")
        if patients:
            for patient in patients:
                with st.expander(f"Patient {patient['patient_id']}: {patient['age']}y {patient['gender']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Conditions:** {', '.join(patient['conditions'])}")
                        st.write(f"**Medications:** {', '.join(patient['medications'])}")
                    with col2:
                        st.write("**Lab Values:**")
                        for lab, value in patient['lab_values'].items():
                            st.write(f"- {lab}: {value}")
                    st.write(f"**Clinical Notes:** {patient['clinical_notes']}")
    
    elif page == "Available Trials":
        st.header("Available Clinical Trials")
        
        trials = get_api_data("/trials")
        if trials:
            # Summary statistics
            phases = [t['phase'] for t in trials]
            conditions = [t['condition'] for t in trials]
            
            col1, col2 = st.columns(2)
            with col1:
                phase_counts = pd.Series(phases).value_counts()
                fig = px.pie(values=phase_counts.values, names=phase_counts.index, title="Trials by Phase")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                condition_counts = pd.Series(conditions).value_counts()
                fig = px.bar(x=condition_counts.values, y=condition_counts.index, 
                           orientation='h', title="Trials by Condition")
                st.plotly_chart(fig, use_container_width=True)
            
            # Trial details
            for trial in trials:
                with st.expander(f"{trial['trial_id']}: {trial['title']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Phase:** {trial['phase']}")
                        st.write(f"**Condition:** {trial['condition']}")
                        st.write(f"**Location:** {trial['location']}")
                        st.write(f"**Sponsor:** {trial['sponsor']}")
                    with col2:
                        st.write("**Inclusion Criteria:**")
                        for criterion in trial['inclusion_criteria']:
                            st.write(f"- {criterion}")
                        st.write("**Exclusion Criteria:**")
                        for criterion in trial['exclusion_criteria']:
                            st.write(f"- {criterion}")
                    st.write(f"**Description:** {trial['description']}")
    
    elif page == "System Status":
        st.header("System Status")
        
        health = get_api_data("/health")
        if health:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("System Status", health['status'].title())
            with col2:
                st.metric("Trials Indexed", health['trials_indexed'])
            with col3:
                st.metric("Sample Patients", health['patients_available'])
            
            st.success("✅ All systems operational")
        else:
            st.error("❌ API not responding")

if __name__ == "__main__":
    main()