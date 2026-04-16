from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
from typing import List
import uvicorn

from backend.models import MatchingRequest, MatchingResponse, PatientData, ClinicalTrial
from backend.matching.engine import HybridMatchingEngine
from data.sample_data import generate_sample_patients, generate_sample_trials

app = FastAPI(title="Clinical Trial Matching API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize matching engine
matching_engine = HybridMatchingEngine()
sample_trials = generate_sample_trials()
sample_patients = generate_sample_patients()

# Build trial index on startup
@app.on_event("startup")
async def startup_event():
    print("Building trial index...")
    matching_engine.build_trial_index(sample_trials)
    print(f"Indexed {len(sample_trials)} trials")

@app.get("/")
async def root():
    return {"message": "Clinical Trial Matching API", "version": "1.0.0"}

@app.get("/trials", response_model=List[ClinicalTrial])
async def get_trials():
    """Get all available clinical trials"""
    return sample_trials

@app.get("/patients", response_model=List[PatientData])
async def get_patients():
    """Get all sample patients"""
    return sample_patients

@app.get("/patients/{patient_id}", response_model=PatientData)
async def get_patient(patient_id: str):
    """Get a specific patient by ID"""
    for patient in sample_patients:
        if patient.patient_id == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.post("/match", response_model=MatchingResponse)
async def match_patient_to_trials(request: MatchingRequest):
    """Match a patient to clinical trials"""
    start_time = time.time()
    
    try:
        # Perform matching
        matches = matching_engine.match_patient_to_trials(
            patient=request.patient,
            max_trials=request.max_trials
        )
        
        # Filter unclear matches if requested
        if not request.include_unclear:
            filtered_matches = []
            for match in matches:
                # Keep match if it has at least one clear inclusion criterion met
                has_clear_inclusion = any(
                    criterion.status.value == "met" 
                    for criterion in match.inclusion_matches
                )
                if has_clear_inclusion:
                    filtered_matches.append(match)
            matches = filtered_matches
        
        processing_time = time.time() - start_time
        
        return MatchingResponse(
            patient_id=request.patient.patient_id,
            matches=matches,
            processing_time=processing_time,
            total_trials_evaluated=len(sample_trials)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matching failed: {str(e)}")

@app.get("/match/{patient_id}")
async def match_sample_patient(patient_id: str, max_trials: int = 10):
    """Match a sample patient to trials"""
    # Find the patient
    patient = None
    for p in sample_patients:
        if p.patient_id == patient_id:
            patient = p
            break
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Create matching request
    request = MatchingRequest(
        patient=patient,
        max_trials=max_trials,
        include_unclear=True
    )
    
    return await match_patient_to_trials(request)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "trials_indexed": len(sample_trials),
        "patients_available": len(sample_patients)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)