from typing import List
from backend.models import PatientData, ClinicalTrial

def generate_sample_patients() -> List[PatientData]:
    """Generate 5 synthetic patient profiles"""
    
    patients = [
        PatientData(
            patient_id="P001",
            age=65,
            gender="Male",
            conditions=["diabetes", "hypertension"],
            medications=["metformin", "lisinopril"],
            lab_values={"glucose": 145, "hemoglobin": 13.2, "creatinine": 1.1},
            clinical_notes="Patient has well-controlled type 2 diabetes mellitus and hypertension. Recent HbA1c 7.2%. No history of cardiovascular events.",
            vital_signs={"bp_systolic": 135, "bp_diastolic": 85, "heart_rate": 72}
        ),
        
        PatientData(
            patient_id="P002",
            age=45,
            gender="Female",
            conditions=["breast cancer"],
            medications=["tamoxifen", "aspirin"],
            lab_values={"hemoglobin": 11.8, "glucose": 92, "cholesterol": 180},
            clinical_notes="Stage II breast cancer, ER+/PR+, HER2-. Completed chemotherapy 6 months ago. Currently on adjuvant tamoxifen therapy.",
            vital_signs={"bp_systolic": 120, "bp_diastolic": 78, "heart_rate": 68}
        ),
        
        PatientData(
            patient_id="P003",
            age=72,
            gender="Male",
            conditions=["copd", "heart disease"],
            medications=["albuterol", "metoprolol", "atorvastatin"],
            lab_values={"hemoglobin": 12.5, "creatinine": 1.3, "cholesterol": 220},
            clinical_notes="Moderate COPD with FEV1 55% predicted. History of myocardial infarction 2 years ago. Current smoker, 40 pack-year history.",
            vital_signs={"bp_systolic": 140, "bp_diastolic": 90, "heart_rate": 65}
        ),
        
        PatientData(
            patient_id="P004",
            age=28,
            gender="Female",
            conditions=["asthma"],
            medications=["albuterol", "fluticasone"],
            lab_values={"hemoglobin": 14.1, "glucose": 88, "creatinine": 0.8},
            clinical_notes="Mild persistent asthma, well-controlled on inhaled corticosteroids. No recent exacerbations. Allergic to penicillin.",
            vital_signs={"bp_systolic": 115, "bp_diastolic": 75, "heart_rate": 70}
        ),
        
        PatientData(
            patient_id="P005",
            age=58,
            gender="Male",
            conditions=["kidney disease", "diabetes"],
            medications=["insulin", "lisinopril", "furosemide"],
            lab_values={"creatinine": 2.1, "glucose": 160, "hemoglobin": 10.2},
            clinical_notes="Stage 3 chronic kidney disease secondary to diabetic nephropathy. Proteinuria present. eGFR 35 ml/min/1.73m2.",
            vital_signs={"bp_systolic": 150, "bp_diastolic": 95, "heart_rate": 78}
        )
    ]
    
    return patients

def generate_sample_trials() -> List[ClinicalTrial]:
    """Generate 10 sample clinical trials"""
    
    trials = [
        ClinicalTrial(
            trial_id="NCT001",
            title="Novel Diabetes Drug for Type 2 Diabetes",
            phase="Phase 3",
            condition="diabetes",
            inclusion_criteria=[
                "Age 18-75 years",
                "Diagnosis of type 2 diabetes mellitus",
                "HbA1c between 7.0-10.0%",
                "On stable metformin therapy"
            ],
            exclusion_criteria=[
                "Type 1 diabetes",
                "Severe kidney disease",
                "History of diabetic ketoacidosis"
            ],
            location="Boston, MA",
            sponsor="PharmaCorp",
            description="Randomized controlled trial of new diabetes medication vs placebo"
        ),
        
        ClinicalTrial(
            trial_id="NCT002",
            title="Immunotherapy for Advanced Breast Cancer",
            phase="Phase 2",
            condition="breast cancer",
            inclusion_criteria=[
                "Age 18 years or older",
                "Metastatic breast cancer",
                "ER-positive or triple-negative",
                "ECOG performance status 0-2"
            ],
            exclusion_criteria=[
                "Prior immunotherapy",
                "Active autoimmune disease",
                "Pregnancy"
            ],
            location="New York, NY",
            sponsor="OncoResearch",
            description="Study of checkpoint inhibitor in advanced breast cancer patients"
        ),
        
        ClinicalTrial(
            trial_id="NCT003",
            title="COPD Bronchodilator Combination Study",
            phase="Phase 3",
            condition="copd",
            inclusion_criteria=[
                "Age 40-80 years",
                "Confirmed COPD diagnosis",
                "FEV1 30-70% predicted",
                "Current or former smoker"
            ],
            exclusion_criteria=[
                "Asthma diagnosis",
                "Recent COPD exacerbation",
                "Oxygen dependency"
            ],
            location="Chicago, IL",
            sponsor="RespiraTech",
            description="Comparison of dual bronchodilator vs single agent in COPD"
        ),
        
        ClinicalTrial(
            trial_id="NCT004",
            title="Hypertension Management in Elderly",
            phase="Phase 4",
            condition="hypertension",
            inclusion_criteria=[
                "Age 65 years or older",
                "Systolic blood pressure 140-180 mmHg",
                "On antihypertensive medication",
                "Able to provide informed consent"
            ],
            exclusion_criteria=[
                "Secondary hypertension",
                "Recent stroke or MI",
                "Severe heart failure"
            ],
            location="Miami, FL",
            sponsor="CardioStudies",
            description="Intensive vs standard blood pressure control in elderly patients"
        ),
        
        ClinicalTrial(
            trial_id="NCT005",
            title="Kidney Disease Progression Prevention",
            phase="Phase 2",
            condition="kidney disease",
            inclusion_criteria=[
                "Age 18-75 years",
                "Chronic kidney disease stage 3-4",
                "eGFR 15-60 ml/min/1.73m2",
                "Proteinuria present"
            ],
            exclusion_criteria=[
                "Dialysis requirement",
                "Kidney transplant history",
                "Active kidney infection"
            ],
            location="Seattle, WA",
            sponsor="NephroTherapeutics",
            description="Novel agent to slow CKD progression"
        ),
        
        ClinicalTrial(
            trial_id="NCT006",
            title="Heart Failure with Preserved Ejection Fraction",
            phase="Phase 3",
            condition="heart disease",
            inclusion_criteria=[
                "Age 50 years or older",
                "Heart failure symptoms",
                "Ejection fraction ≥50%",
                "NT-proBNP elevated"
            ],
            exclusion_criteria=[
                "Reduced ejection fraction",
                "Severe valve disease",
                "Recent cardiac surgery"
            ],
            location="Houston, TX",
            sponsor="CardioVascular Inc",
            description="Treatment for heart failure with preserved ejection fraction"
        ),
        
        ClinicalTrial(
            trial_id="NCT007",
            title="Asthma Biologic Therapy Study",
            phase="Phase 3",
            condition="asthma",
            inclusion_criteria=[
                "Age 12-65 years",
                "Moderate to severe asthma",
                "Elevated eosinophils",
                "On inhaled corticosteroids"
            ],
            exclusion_criteria=[
                "COPD diagnosis",
                "Recent asthma exacerbation requiring hospitalization",
                "Immunodeficiency"
            ],
            location="Los Angeles, CA",
            sponsor="BioAsthma Research",
            description="Biologic therapy for eosinophilic asthma"
        ),
        
        ClinicalTrial(
            trial_id="NCT008",
            title="Cancer Prevention in High-Risk Individuals",
            phase="Phase 2",
            condition="cancer",
            inclusion_criteria=[
                "Age 40-70 years",
                "Family history of cancer",
                "BRCA mutation or high-risk genetic profile",
                "No current cancer diagnosis"
            ],
            exclusion_criteria=[
                "Active cancer",
                "Previous cancer within 5 years",
                "Pregnancy or nursing"
            ],
            location="San Francisco, CA",
            sponsor="PreventCancer Foundation",
            description="Chemoprevention study in high-risk individuals"
        ),
        
        ClinicalTrial(
            trial_id="NCT009",
            title="Diabetes and Cardiovascular Outcomes",
            phase="Phase 4",
            condition="diabetes",
            inclusion_criteria=[
                "Age 50 years or older",
                "Type 2 diabetes with cardiovascular risk",
                "HbA1c 7.0-9.0%",
                "History of cardiovascular disease or risk factors"
            ],
            exclusion_criteria=[
                "Type 1 diabetes",
                "Recent cardiovascular event",
                "Severe kidney or liver disease"
            ],
            location="Atlanta, GA",
            sponsor="Diabetes Cardiovascular Research",
            description="Long-term cardiovascular outcomes in diabetes patients"
        ),
        
        ClinicalTrial(
            trial_id="NCT010",
            title="Healthy Aging and Longevity Study",
            phase="Phase 1",
            condition="aging",
            inclusion_criteria=[
                "Age 65-85 years",
                "Generally healthy",
                "Able to walk independently",
                "Normal cognitive function"
            ],
            exclusion_criteria=[
                "Major chronic diseases",
                "Dementia or cognitive impairment",
                "Recent hospitalization"
            ],
            location="Portland, OR",
            sponsor="Longevity Research Institute",
            description="Study of interventions to promote healthy aging"
        )
    ]
    
    return trials