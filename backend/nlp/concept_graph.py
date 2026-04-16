from typing import List, Dict, Set

class ClinicalConceptGraph:
    """Simplified clinical concept graph for medical term relationships"""
    
    def __init__(self):
        # Basic medical concept relationships
        self.concept_relationships = {
            'diabetes': {
                'synonyms': ['diabetes mellitus', 'dm', 'diabetic', 'hyperglycemia'],
                'related_conditions': ['hypertension', 'kidney disease', 'heart disease'],
                'symptoms': ['polyuria', 'polydipsia', 'fatigue'],
                'medications': ['metformin', 'insulin', 'glipizide']
            },
            'hypertension': {
                'synonyms': ['high blood pressure', 'htn', 'elevated bp'],
                'related_conditions': ['diabetes', 'heart disease', 'kidney disease'],
                'symptoms': ['headache', 'dizziness'],
                'medications': ['lisinopril', 'metoprolol', 'amlodipine']
            },
            'copd': {
                'synonyms': ['chronic obstructive pulmonary disease', 'emphysema', 'chronic bronchitis'],
                'related_conditions': ['asthma', 'heart disease'],
                'symptoms': ['dyspnea', 'cough', 'wheezing'],
                'medications': ['albuterol', 'tiotropium', 'prednisone']
            },
            'asthma': {
                'synonyms': ['bronchial asthma', 'allergic asthma'],
                'related_conditions': ['copd', 'allergies'],
                'symptoms': ['wheezing', 'cough', 'shortness of breath'],
                'medications': ['albuterol', 'fluticasone', 'montelukast']
            },
            'cancer': {
                'synonyms': ['carcinoma', 'tumor', 'malignancy', 'neoplasm'],
                'related_conditions': [],
                'symptoms': ['fatigue', 'weight loss', 'pain'],
                'medications': ['chemotherapy', 'radiation']
            },
            'breast cancer': {
                'synonyms': ['breast carcinoma', 'mammary cancer'],
                'related_conditions': ['cancer'],
                'symptoms': ['breast lump', 'breast pain'],
                'medications': ['tamoxifen', 'anastrozole', 'trastuzumab']
            },
            'heart disease': {
                'synonyms': ['cardiac disease', 'coronary artery disease', 'cad', 'heart failure'],
                'related_conditions': ['diabetes', 'hypertension', 'copd'],
                'symptoms': ['chest pain', 'dyspnea', 'fatigue'],
                'medications': ['metoprolol', 'atorvastatin', 'aspirin']
            },
            'kidney disease': {
                'synonyms': ['renal disease', 'chronic kidney disease', 'ckd', 'nephropathy'],
                'related_conditions': ['diabetes', 'hypertension'],
                'symptoms': ['edema', 'fatigue', 'decreased urine output'],
                'medications': ['lisinopril', 'furosemide', 'erythropoietin']
            }
        }
    
    def expand_search_terms(self, terms: List[str]) -> List[str]:
        """Expand search terms using medical concept relationships"""
        expanded_terms = set(terms)  # Start with original terms
        
        for term in terms:
            term_lower = term.lower()
            
            # Add synonyms
            for concept, relationships in self.concept_relationships.items():
                if (term_lower == concept or 
                    term_lower in relationships.get('synonyms', [])):
                    
                    # Add the main concept
                    expanded_terms.add(concept)
                    
                    # Add synonyms
                    expanded_terms.update(relationships.get('synonyms', []))
                    
                    # Add related conditions (with lower weight)
                    expanded_terms.update(relationships.get('related_conditions', []))
        
        return list(expanded_terms)
    
    def get_related_concepts(self, concept: str) -> Dict[str, List[str]]:
        """Get all related concepts for a given medical concept"""
        concept_lower = concept.lower()
        
        # Find the concept in our graph
        for main_concept, relationships in self.concept_relationships.items():
            if (concept_lower == main_concept or 
                concept_lower in relationships.get('synonyms', [])):
                return relationships
        
        return {}
    
    def calculate_concept_similarity(self, concept1: str, concept2: str) -> float:
        """Calculate similarity between two medical concepts"""
        concept1_lower = concept1.lower()
        concept2_lower = concept2.lower()
        
        # Exact match
        if concept1_lower == concept2_lower:
            return 1.0
        
        # Check if they're synonyms
        for main_concept, relationships in self.concept_relationships.items():
            synonyms = [main_concept] + relationships.get('synonyms', [])
            if concept1_lower in synonyms and concept2_lower in synonyms:
                return 0.9
        
        # Check if they're related conditions
        for main_concept, relationships in self.concept_relationships.items():
            if concept1_lower == main_concept or concept1_lower in relationships.get('synonyms', []):
                if concept2_lower in relationships.get('related_conditions', []):
                    return 0.6
            if concept2_lower == main_concept or concept2_lower in relationships.get('synonyms', []):
                if concept1_lower in relationships.get('related_conditions', []):
                    return 0.6
        
        return 0.0
    
    def get_concept_medications(self, concept: str) -> List[str]:
        """Get medications associated with a medical concept"""
        concept_lower = concept.lower()
        
        for main_concept, relationships in self.concept_relationships.items():
            if (concept_lower == main_concept or 
                concept_lower in relationships.get('synonyms', [])):
                return relationships.get('medications', [])
        
        return []
    
    def get_concept_symptoms(self, concept: str) -> List[str]:
        """Get symptoms associated with a medical concept"""
        concept_lower = concept.lower()
        
        for main_concept, relationships in self.concept_relationships.items():
            if (concept_lower == main_concept or 
                concept_lower in relationships.get('synonyms', [])):
                return relationships.get('symptoms', [])
        
        return []