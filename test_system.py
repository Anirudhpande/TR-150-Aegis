#!/usr/bin/env python3
"""
Test script for the Clinical Trial Matching Engine
Run this to verify the system is working correctly
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from backend.models import PatientData, ClinicalTrial, MatchingRequest
        print("Models imported successfully")
        
        from backend.nlp.processor import MedicalNLPProcessor
        print("NLP processor imported successfully")
        
        from backend.nlp.criteria_parser import CriteriaParser
        print("Criteria parser imported successfully")
        
        from backend.nlp.concept_graph import ClinicalConceptGraph
        print("Concept graph imported successfully")
        
        from backend.matching.engine import HybridMatchingEngine
        print("Matching engine imported successfully")
        
        from data.sample_data import generate_sample_patients, generate_sample_trials
        print("Sample data imported successfully")
        
        return True
    except ImportError as e:
        print(f"Import failed: {e}")
        return False

def test_nlp_processing():
    """Test NLP processing functionality"""
    print("\nTesting NLP processing...")
    
    try:
        from backend.nlp.processor import MedicalNLPProcessor
        
        processor = MedicalNLPProcessor()
        
        # Test concept extraction
        text = "Patient has diabetes mellitus and hypertension. Taking metformin and lisinopril."
        concepts = processor.extract_medical_concepts(text)
        print(f"Extracted concepts: {concepts}")
        
        # Test embeddings
        embeddings = processor.get_embeddings(["diabetes", "hypertension"])
        print(f"Generated embeddings shape: {embeddings.shape}")
        
        # Test similarity
        similarity = processor.calculate_semantic_similarity("diabetes", "diabetes mellitus")
        print(f"Semantic similarity: {similarity:.3f}")
        
        return True
    except Exception as e:
        print(f"NLP processing failed: {e}")
        return False

def test_criteria_parsing():
    """Test criteria parsing functionality"""
    print("\nTesting criteria parsing...")
    
    try:
        from backend.nlp.criteria_parser import CriteriaParser
        
        parser = CriteriaParser()
        
        criteria = [
            "Age 18-65 years",
            "Diagnosis of type 2 diabetes",
            "No history of heart disease"
        ]
        
        parsed = parser.parse_criteria(criteria)
        print(f"Parsed {len(parsed)} criteria")
        
        for p in parsed:
            print(f"  - {p.criterion_type}: {p.operator} {p.value} (confidence: {p.confidence:.2f})")
        
        return True
    except Exception as e:
        print(f"Criteria parsing failed: {e}")
        return False

def test_concept_graph():
    """Test concept graph functionality"""
    print("\nTesting concept graph...")
    
    try:
        from backend.nlp.concept_graph import ClinicalConceptGraph
        
        graph = ClinicalConceptGraph()
        
        # Test related concepts
        related = graph.get_related_concepts("diabetes")
        print(f"Found {len(related)} related concepts to diabetes")
        
        # Test term expansion
        expanded = graph.expand_search_terms(["diabetes", "hypertension"])
        print(f"Expanded terms: {expanded}")
        
        return True
    except Exception as e:
        print(f"Concept graph failed: {e}")
        return False

def test_matching_engine():
    """Test the matching engine"""
    print("\nTesting matching engine...")
    
    try:
        from backend.matching.engine import HybridMatchingEngine
        from data.sample_data import generate_sample_patients, generate_sample_trials
        
        # Initialize engine
        engine = HybridMatchingEngine()
        
        # Load sample data
        patients = generate_sample_patients()
        trials = generate_sample_trials()
        
        print(f"Loaded {len(patients)} patients and {len(trials)} trials")
        
        # Build index
        engine.build_trial_index(trials)
        print("Built trial index")
        
        # Test matching
        patient = patients[0]  # First patient
        matches = engine.match_patient_to_trials(patient, max_trials=5)
        
        print(f"Found {len(matches)} matches for patient {patient.patient_id}")
        
        if matches:
            best_match = matches[0]
            print(f"  Best match: {best_match.title} (score: {best_match.match_score:.3f})")
            print(f"  Explanation: {best_match.explanation}")
        
        return True
    except Exception as e:
        print(f"Matching engine failed: {e}")
        return False

def test_sample_data():
    """Test sample data generation"""
    print("\nTesting sample data...")
    
    try:
        from data.sample_data import generate_sample_patients, generate_sample_trials
        
        patients = generate_sample_patients()
        trials = generate_sample_trials()
        
        print(f"Generated {len(patients)} sample patients")
        print(f"Generated {len(trials)} sample trials")
        
        # Verify data structure
        patient = patients[0]
        print(f"  Sample patient: {patient.patient_id}, age {patient.age}, conditions: {patient.conditions}")
        
        trial = trials[0]
        print(f"  Sample trial: {trial.trial_id}, {trial.title}")
        
        return True
    except Exception as e:
        print(f"Sample data failed: {e}")
        return False

def run_full_test():
    """Run a complete end-to-end test"""
    print("\nRunning full end-to-end test...")
    
    try:
        from backend.matching.engine import HybridMatchingEngine
        from data.sample_data import generate_sample_patients, generate_sample_trials
        from backend.evaluation import MatchingEvaluator
        
        # Setup
        engine = HybridMatchingEngine()
        patients = generate_sample_patients()
        trials = generate_sample_trials()
        evaluator = MatchingEvaluator()
        
        # Build index
        engine.build_trial_index(trials)
        
        # Test each patient
        all_matches = []
        processing_times = []
        
        for patient in patients:
            start_time = time.time()
            matches = engine.match_patient_to_trials(patient, max_trials=3)
            processing_time = time.time() - start_time
            
            all_matches.extend(matches)
            processing_times.append(processing_time)
            
            print(f"  Patient {patient.patient_id}: {len(matches)} matches in {processing_time:.3f}s")
        
        # Evaluate results
        if all_matches:
            metrics = evaluator.evaluate_matches(all_matches)
            latency_metrics = evaluator.calculate_latency_metrics(processing_times)
            
            print(f"\nOverall Results:")
            print(f"  Total matches: {metrics.get('total_matches', 0)}")
            print(f"  Average score: {metrics.get('avg_match_score', 0):.3f}")
            print(f"  Average latency: {latency_metrics.get('avg_latency', 0):.3f}s")
            print(f"  High confidence matches: {metrics.get('high_confidence_matches', 0)}")
        
        print("Full end-to-end test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Full test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Clinical Trial Matching Engine - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Sample Data", test_sample_data),
        ("NLP Processing", test_nlp_processing),
        ("Criteria Parsing", test_criteria_parsing),
        ("Concept Graph", test_concept_graph),
        ("Matching Engine", test_matching_engine),
        ("Full End-to-End", run_full_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        else:
            print(f"{test_name} test failed!")
    
    print(f"\n{'='*60}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Run 'python main.py' to start the full system")
        print("2. Open http://localhost:8501 for the dashboard")
        print("3. Try matching some patients to trials!")
    else:
        print("Some tests failed. Please check the error messages above.")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()