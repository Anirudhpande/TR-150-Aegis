import numpy as np
from typing import List, Dict, Tuple
from ..models import PatientData, ClinicalTrial, TrialMatch, CriterionMatch, MatchStatus
from ..nlp.processor import MedicalNLPProcessor
from ..nlp.criteria_parser import CriteriaParser, ParsedCriterion
from ..nlp.concept_graph import ClinicalConceptGraph

class HybridMatchingEngine:
    def __init__(self):
        self.nlp_processor = MedicalNLPProcessor()
        self.criteria_parser = CriteriaParser()
        self.concept_graph = ClinicalConceptGraph()
        self.trials_data = []

    def build_trial_index(self, trials: List[ClinicalTrial]):
        """Store trials for matching"""
        self.trials_data = trials
        print(f"Indexed {len(trials)} trials")

    def match_patient_to_trials(self, patient: PatientData, max_trials: int = 10) -> List[TrialMatch]:
        """Main matching function using simplified approach"""
        if not self.trials_data:
            return []
        
        # Perform detailed matching for all trials
        matches = []
        for trial in self.trials_data:
            match = self._detailed_match(patient, trial)
            if match.match_score > 0.1:  # Minimum threshold
                matches.append(match)
        
        # Rank and return top matches
        matches.sort(key=lambda x: x.match_score, reverse=True)
        return matches[:max_trials]

    def _create_patient_query(self, patient: PatientData) -> str:
        """Create search query from patient data"""
        query_parts = []
        
        # Add conditions
        query_parts.extend(patient.conditions)
        
        # Add medications
        query_parts.extend(patient.medications)
        
        # Add key terms from clinical notes
        if patient.clinical_notes:
            concepts = self.nlp_processor.extract_medical_concepts(patient.clinical_notes)
            query_parts.extend(concepts.get('conditions', []))
            query_parts.extend(concepts.get('symptoms', []))
        
        # Expand using concept graph
        expanded_terms = self.concept_graph.expand_search_terms(query_parts)
        
        return ' '.join(expanded_terms)

    def _detailed_match(self, patient: PatientData, trial: ClinicalTrial) -> TrialMatch:
        """Perform detailed matching between patient and trial"""
        
        # Parse criteria
        inclusion_parsed = self.criteria_parser.parse_criteria(trial.inclusion_criteria)
        exclusion_parsed = self.criteria_parser.parse_criteria(trial.exclusion_criteria)
        
        # Evaluate inclusion criteria
        inclusion_matches = []
        inclusion_score = 0
        
        for criterion in inclusion_parsed:
            match = self._evaluate_criterion(patient, criterion, is_inclusion=True)
            inclusion_matches.append(match)
            if match.status == MatchStatus.MET:
                inclusion_score += 1
            elif match.status == MatchStatus.UNCLEAR:
                inclusion_score += 0.5
        
        # Evaluate exclusion criteria
        exclusion_matches = []
        exclusion_penalty = 0
        
        for criterion in exclusion_parsed:
            match = self._evaluate_criterion(patient, criterion, is_inclusion=False)
            exclusion_matches.append(match)
            if match.status == MatchStatus.MET:  # Met exclusion = bad
                exclusion_penalty += 1
            elif match.status == MatchStatus.UNCLEAR:
                exclusion_penalty += 0.3
        
        # Calculate overall match score
        total_inclusion = len(inclusion_parsed) if inclusion_parsed else 1
        inclusion_ratio = inclusion_score / total_inclusion
        
        # Apply exclusion penalty
        match_score = max(0, inclusion_ratio - (exclusion_penalty * 0.2))
        
        # Add semantic similarity bonus
        semantic_score = self._calculate_semantic_match(patient, trial)
        match_score = (match_score * 0.8) + (semantic_score * 0.2)
        
        # Generate explanation
        explanation = self._generate_explanation(inclusion_matches, exclusion_matches, match_score)
        
        return TrialMatch(
            trial_id=trial.trial_id,
            title=trial.title,
            phase=trial.phase,
            condition=trial.condition,
            match_score=match_score,
            inclusion_matches=inclusion_matches,
            exclusion_matches=exclusion_matches,
            explanation=explanation
        )

    def _evaluate_criterion(self, patient: PatientData, criterion: ParsedCriterion, is_inclusion: bool) -> CriterionMatch:
        """Evaluate a single criterion against patient data"""
        
        if criterion.criterion_type == 'age':
            return self._evaluate_age_criterion(patient, criterion)
        elif criterion.criterion_type in ['condition_required', 'condition_excluded']:
            return self._evaluate_condition_criterion(patient, criterion)
        elif criterion.criterion_type == 'lab_value':
            return self._evaluate_lab_criterion(patient, criterion)
        else:
            return self._evaluate_general_criterion(patient, criterion)

    def _evaluate_age_criterion(self, patient: PatientData, criterion: ParsedCriterion) -> CriterionMatch:
        """Evaluate age-based criterion"""
        patient_age = patient.age
        
        if criterion.operator == '>=':
            met = patient_age >= criterion.value
        elif criterion.operator == '<=':
            met = patient_age <= criterion.value
        elif criterion.operator == 'between':
            min_age, max_age = criterion.value
            met = min_age <= patient_age <= max_age
        else:
            return CriterionMatch(
                criterion=criterion.original_text,
                status=MatchStatus.UNCLEAR,
                evidence=f"Patient age: {patient_age}",
                confidence=0.5
            )
        
        return CriterionMatch(
            criterion=criterion.original_text,
            status=MatchStatus.MET if met else MatchStatus.NOT_MET,
            evidence=f"Patient age: {patient_age}",
            confidence=0.95
        )

    def _evaluate_condition_criterion(self, patient: PatientData, criterion: ParsedCriterion) -> CriterionMatch:
        """Evaluate condition-based criterion"""
        required_condition = criterion.value.lower()
        patient_conditions = [c.lower() for c in patient.conditions]
        
        # Direct match
        direct_match = any(required_condition in condition for condition in patient_conditions)
        
        # Semantic similarity check
        if not direct_match and patient_conditions:
            similarities = [
                self.nlp_processor.calculate_semantic_similarity(required_condition, condition)
                for condition in patient_conditions
            ]
            max_similarity = max(similarities) if similarities else 0
            semantic_match = max_similarity > 0.7
        else:
            semantic_match = False
            max_similarity = 0
        
        # Check clinical notes
        notes_match = False
        if patient.clinical_notes:
            notes_match = required_condition in patient.clinical_notes.lower()
        
        # Determine status
        if direct_match or semantic_match or notes_match:
            status = MatchStatus.MET
            confidence = 0.9 if direct_match else (0.8 if semantic_match else 0.6)
        elif patient_conditions or patient.clinical_notes:
            status = MatchStatus.NOT_MET
            confidence = 0.8
        else:
            status = MatchStatus.UNCLEAR
            confidence = 0.3
        
        # For exclusion criteria, flip the logic
        if criterion.criterion_type == 'condition_excluded':
            if status == MatchStatus.MET:
                status = MatchStatus.NOT_MET  # Has excluded condition = not met
            elif status == MatchStatus.NOT_MET:
                status = MatchStatus.MET  # Doesn't have excluded condition = met
        
        evidence = f"Patient conditions: {', '.join(patient.conditions)}"
        if semantic_match:
            evidence += f" (semantic similarity: {max_similarity:.2f})"
        
        return CriterionMatch(
            criterion=criterion.original_text,
            status=status,
            evidence=evidence,
            confidence=confidence
        )

    def _evaluate_lab_criterion(self, patient: PatientData, criterion: ParsedCriterion) -> CriterionMatch:
        """Evaluate lab value criterion"""
        if criterion.operator == 'normal':
            lab_name = criterion.value
            if lab_name in patient.lab_values:
                value = patient.lab_values[lab_name]
                is_normal = self.nlp_processor.is_lab_value_normal(lab_name, value)
                return CriterionMatch(
                    criterion=criterion.original_text,
                    status=MatchStatus.MET if is_normal else MatchStatus.NOT_MET,
                    evidence=f"{lab_name}: {value}",
                    confidence=0.8
                )
        elif criterion.operator == 'between':
            lab_name, (min_val, max_val) = criterion.value
            if lab_name in patient.lab_values:
                value = patient.lab_values[lab_name]
                met = min_val <= value <= max_val
                
                return CriterionMatch(
                    criterion=criterion.original_text,
                    status=MatchStatus.MET if met else MatchStatus.NOT_MET,
                    evidence=f"{lab_name}: {value} (range: {min_val}-{max_val})",
                    confidence=0.9
                )
        else:
            lab_name, threshold = criterion.value
            if lab_name in patient.lab_values:
                value = patient.lab_values[lab_name]
                if criterion.operator == '>=':
                    met = value >= threshold
                else:  # '<='
                    met = value <= threshold
                
                return CriterionMatch(
                    criterion=criterion.original_text,
                    status=MatchStatus.MET if met else MatchStatus.NOT_MET,
                    evidence=f"{lab_name}: {value} (threshold: {threshold})",
                    confidence=0.9
                )
        
        return CriterionMatch(
            criterion=criterion.original_text,
            status=MatchStatus.UNCLEAR,
            evidence="Lab value not available",
            confidence=0.2
        )

    def _evaluate_general_criterion(self, patient: PatientData, criterion: ParsedCriterion) -> CriterionMatch:
        """Evaluate general text criterion using semantic similarity"""
        criterion_text = criterion.value
        
        # Check against all patient text
        patient_text = f"{' '.join(patient.conditions)} {' '.join(patient.medications)} {patient.clinical_notes}"
        
        similarity = self.nlp_processor.calculate_semantic_similarity(criterion_text, patient_text)
        
        if similarity > 0.7:
            status = MatchStatus.MET
            confidence = similarity
        elif similarity > 0.4:
            status = MatchStatus.UNCLEAR
            confidence = similarity
        else:
            status = MatchStatus.NOT_MET
            confidence = 1 - similarity
        
        return CriterionMatch(
            criterion=criterion.original_text,
            status=status,
            evidence=f"Semantic similarity: {similarity:.2f}",
            confidence=confidence
        )

    def _calculate_semantic_match(self, patient: PatientData, trial: ClinicalTrial) -> float:
        """Calculate semantic similarity between patient and trial"""
        patient_text = self._create_patient_query(patient)
        trial_text = f"{trial.title} {trial.condition} {trial.description}"
        
        return self.nlp_processor.calculate_semantic_similarity(patient_text, trial_text)

    def _generate_explanation(self, inclusion_matches: List[CriterionMatch], 
                            exclusion_matches: List[CriterionMatch], match_score: float) -> str:
        """Generate human-readable explanation"""
        explanations = []
        
        # Inclusion summary
        met_inclusion = sum(1 for m in inclusion_matches if m.status == MatchStatus.MET)
        total_inclusion = len(inclusion_matches)
        if total_inclusion > 0:
            explanations.append(f"Meets {met_inclusion}/{total_inclusion} inclusion criteria")
        
        # Exclusion summary
        met_exclusion = sum(1 for m in exclusion_matches if m.status == MatchStatus.MET)
        if met_exclusion > 0:
            explanations.append(f"Meets {met_exclusion} exclusion criteria (negative)")
        
        # Overall assessment
        if match_score > 0.8:
            explanations.append("Strong match - highly recommended")
        elif match_score > 0.6:
            explanations.append("Good match - recommended")
        elif match_score > 0.4:
            explanations.append("Moderate match - consider with caution")
        else:
            explanations.append("Weak match - not recommended")
        
        return ". ".join(explanations)