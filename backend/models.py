from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum

class MatchStatus(str, Enum):
    MET = "met"
    NOT_MET = "not_met"
    UNCLEAR = "unclear"

class PatientData(BaseModel):
    patient_id: str
    age: int
    gender: str
    conditions: List[str]
    medications: List[str]
    lab_values: Dict[str, float]
    clinical_notes: str
    vital_signs: Dict[str, float]

class CriterionMatch(BaseModel):
    criterion: str
    status: MatchStatus
    evidence: str
    confidence: float

class TrialMatch(BaseModel):
    trial_id: str
    title: str
    phase: str
    condition: str
    match_score: float
    inclusion_matches: List[CriterionMatch]
    exclusion_matches: List[CriterionMatch]
    explanation: str
    geographic_score: float = 1.0

class ClinicalTrial(BaseModel):
    trial_id: str
    title: str
    phase: str
    condition: str
    inclusion_criteria: List[str]
    exclusion_criteria: List[str]
    location: str
    sponsor: str
    description: str

class MatchingRequest(BaseModel):
    patient: PatientData
    max_trials: int = 10
    include_unclear: bool = True

class MatchingResponse(BaseModel):
    patient_id: str
    matches: List[TrialMatch]
    processing_time: float
    total_trials_evaluated: int