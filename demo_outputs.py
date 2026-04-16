#!/usr/bin/env python3
"""
Demo script showing sample outputs from the Clinical Trial Matching Engine
This demonstrates what the system produces without needing to run the full stack
"""

def show_sample_patient():
    """Show a sample patient profile"""
    print("👤 SAMPLE PATIENT PROFILE")
    print("=" * 50)
    print("Patient ID: P001")
    print("Age: 65 years")
    print("Gender: Male")
    print("Conditions: diabetes, hypertension")
    print("Medications: metformin, lisinopril")
    print("Lab Values:")
    print("  - Glucose: 145 mg/dL")
    print("  - Hemoglobin: 13.2 g/dL")
    print("  - Creatinine: 1.1 mg/dL")
    print("Clinical Notes:")
    print("  Patient has well-controlled type 2 diabetes mellitus and")
    print("  hypertension. Recent HbA1c 7.2%. No history of cardiovascular events.")

def show_sample_trial():
    """Show a sample clinical trial"""
    print("\n🧪 SAMPLE CLINICAL TRIAL")
    print("=" * 50)
    print("Trial ID: NCT001")
    print("Title: Novel Diabetes Drug for Type 2 Diabetes")
    print("Phase: Phase 3")
    print("Condition: diabetes")
    print("Location: Boston, MA")
    print("Sponsor: PharmaCorp")
    print("\nInclusion Criteria:")
    print("  ✓ Age 18-75 years")
    print("  ✓ Diagnosis of type 2 diabetes mellitus")
    print("  ✓ HbA1c between 7.0-10.0%")
    print("  ✓ On stable metformin therapy")
    print("\nExclusion Criteria:")
    print("  ✗ Type 1 diabetes")
    print("  ✗ Severe kidney disease")
    print("  ✗ History of diabetic ketoacidosis")

def show_matching_results():
    """Show sample matching results with explanations"""
    print("\n🎯 MATCHING RESULTS")
    print("=" * 50)
    print("Processing Time: 2.34 seconds")
    print("Trials Evaluated: 10")
    print("Matches Found: 3")
    print("\n" + "="*60)
    
    # Match 1 - Strong match
    print("🟢 MATCH #1 - STRONG MATCH")
    print("-" * 30)
    print("Trial: Novel Diabetes Drug for Type 2 Diabetes (NCT001)")
    print("Match Score: 0.89")
    print("Phase: Phase 3")
    print("Explanation: Meets 4/4 inclusion criteria. Strong match - highly recommended")
    
    print("\n📋 DETAILED CRITERION ANALYSIS:")
    print("  🟢 Age 18-75 years")
    print("     Status: MET")
    print("     Evidence: Patient age: 65")
    print("     Confidence: 0.95")
    
    print("  🟢 Diagnosis of type 2 diabetes mellitus")
    print("     Status: MET") 
    print("     Evidence: Patient conditions: diabetes, hypertension")
    print("     Confidence: 0.90")
    
    print("  🟢 HbA1c between 7.0-10.0%")
    print("     Status: MET")
    print("     Evidence: Clinical notes mention HbA1c 7.2%")
    print("     Confidence: 0.85")
    
    print("  🟢 On stable metformin therapy")
    print("     Status: MET")
    print("     Evidence: Patient medications: metformin, lisinopril")
    print("     Confidence: 0.90")
    
    print("\n  EXCLUSION CRITERIA:")
    print("  🟢 Type 1 diabetes")
    print("     Status: NOT MET (Good - not excluded)")
    print("     Evidence: Patient has type 2 diabetes")
    print("     Confidence: 0.88")
    
    print("\n" + "="*60)
    
    # Match 2 - Moderate match
    print("🟡 MATCH #2 - MODERATE MATCH")
    print("-" * 30)
    print("Trial: Hypertension Management in Elderly (NCT004)")
    print("Match Score: 0.67")
    print("Phase: Phase 4")
    print("Explanation: Meets 3/4 inclusion criteria. Good match - recommended")
    
    print("\n📋 DETAILED CRITERION ANALYSIS:")
    print("  🟢 Age 65 years or older")
    print("     Status: MET")
    print("     Evidence: Patient age: 65")
    print("     Confidence: 0.95")
    
    print("  🟡 Systolic blood pressure 140-180 mmHg")
    print("     Status: UNCLEAR")
    print("     Evidence: BP data not available in current record")
    print("     Confidence: 0.30")
    
    print("  🟢 On antihypertensive medication")
    print("     Status: MET")
    print("     Evidence: Patient medications: lisinopril")
    print("     Confidence: 0.90")
    
    print("\n" + "="*60)
    
    # Match 3 - Weak match
    print("🔴 MATCH #3 - WEAK MATCH")
    print("-" * 30)
    print("Trial: COPD Bronchodilator Combination Study (NCT003)")
    print("Match Score: 0.23")
    print("Phase: Phase 3")
    print("Explanation: Meets 1/4 inclusion criteria. Weak match - not recommended")
    
    print("\n📋 DETAILED CRITERION ANALYSIS:")
    print("  🟢 Age 40-80 years")
    print("     Status: MET")
    print("     Evidence: Patient age: 65")
    print("     Confidence: 0.95")
    
    print("  🔴 Confirmed COPD diagnosis")
    print("     Status: NOT MET")
    print("     Evidence: Patient conditions: diabetes, hypertension (no COPD)")
    print("     Confidence: 0.85")

def show_evaluation_report():
    """Show sample evaluation metrics"""
    print("\n📊 EVALUATION REPORT")
    print("=" * 50)
    print("=== CLINICAL TRIAL MATCHING EVALUATION REPORT ===")
    print()
    print("Total Matches Found: 8")
    print("Average Match Score: 0.742")
    print("Score Standard Deviation: 0.234")
    print("Processing Time: 2.341 seconds")
    print()
    print("--- Match Quality Distribution ---")
    print("High Confidence (>0.8): 3")
    print("Medium Confidence (0.6-0.8): 4") 
    print("Low Confidence (<0.6): 1")
    print()
    print("--- Inclusion Criteria Analysis ---")
    print("Met Rate: 78.5%")
    print("Unclear Rate: 12.3%")
    print("Average Confidence: 0.847")
    print()
    print("--- Exclusion Criteria Analysis ---")
    print("Met Rate: 8.7%")
    print("Unclear Rate: 15.2%")
    print("Average Confidence: 0.823")
    print()
    print("--- Recommendations ---")
    print("✅ Good matching performance")

def show_api_examples():
    """Show sample API requests and responses"""
    print("\n🔌 API EXAMPLES")
    print("=" * 50)
    
    print("GET /patients")
    print("Response: List of 5 sample patients")
    print()
    
    print("POST /match")
    print("Request Body:")
    print("""{
  "patient": {
    "patient_id": "P001",
    "age": 65,
    "gender": "Male",
    "conditions": ["diabetes", "hypertension"],
    "medications": ["metformin", "lisinopril"],
    "lab_values": {"glucose": 145, "hemoglobin": 13.2},
    "clinical_notes": "Well-controlled diabetes and hypertension..."
  },
  "max_trials": 10,
  "include_unclear": true
}""")
    
    print("\nResponse:")
    print("""{
  "patient_id": "P001",
  "matches": [
    {
      "trial_id": "NCT001",
      "title": "Novel Diabetes Drug for Type 2 Diabetes",
      "match_score": 0.89,
      "explanation": "Meets 4/4 inclusion criteria. Strong match.",
      "inclusion_matches": [...],
      "exclusion_matches": [...]
    }
  ],
  "processing_time": 2.34,
  "total_trials_evaluated": 10
}""")

def show_system_architecture():
    """Show the system architecture"""
    print("\n🏗️ SYSTEM ARCHITECTURE")
    print("=" * 50)
    print("""
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI       │    │   Matching      │
│   Frontend      │◄──►│    Backend       │◄──►│   Engine        │
│                 │    │                  │    │                 │
│ • Patient Input │    │ • REST API       │    │ • Rule-based    │
│ • Results View  │    │ • Data Models    │    │ • Semantic      │
│ • Explanations  │    │ • Validation     │    │ • LLM Reasoning │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Sample Data    │    │  NLP Pipeline   │
                       │                  │    │                 │
                       │ • 5 Patients     │    │ • Medical NLP   │
                       │ • 10 Trials      │    │ • Criteria Parse│
                       │ • Realistic      │    │ • Concept Graph │
                       │   Profiles       │    │ • Embeddings    │
                       └──────────────────┘    └─────────────────┘
""")

def show_key_innovations():
    """Show the key innovations of the system"""
    print("\n💡 KEY INNOVATIONS")
    print("=" * 50)
    
    innovations = [
        ("🧠 Hybrid Matching Engine", "Combines rule-based logic, semantic similarity, and LLM reasoning"),
        ("🔍 Explainable AI Layer", "Provides criterion-level explanations with evidence highlighting"),
        ("⚖️ Uncertainty Handling", "Labels criteria as Met/Not Met/Unclear with confidence scores"),
        ("🧬 Clinical Concept Graph", "Medical knowledge graph linking diseases, symptoms, and drugs"),
        ("🤖 LLM Criteria Parser", "Converts free-text eligibility criteria into structured JSON rules"),
        ("📊 Smart Ranking", "Combines match score, trial phase, and condition relevance"),
        ("⚡ Fast Retrieval", "FAISS vector search for sub-10-second performance")
    ]
    
    for title, description in innovations:
        print(f"{title}")
        print(f"   {description}")
        print()

def main():
    """Run the complete demo"""
    print("🏥 AI-DRIVEN CLINICAL TRIAL MATCHING ENGINE")
    print("🎯 HACKATHON DEMO - SAMPLE OUTPUTS")
    print("=" * 70)
    
    show_sample_patient()
    show_sample_trial()
    show_matching_results()
    show_evaluation_report()
    show_api_examples()
    show_system_architecture()
    show_key_innovations()
    
    print("\n🚀 READY FOR DEMO!")
    print("=" * 50)
    print("To run the full system:")
    print("1. python main.py")
    print("2. Open http://localhost:8501")
    print("3. Select 'Patient Matching' and try it out!")
    print("\nTo test the system:")
    print("python test_system.py")

if __name__ == "__main__":
    main()