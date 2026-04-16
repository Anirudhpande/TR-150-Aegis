from typing import List, Dict, Any
from .models import TrialMatch

class MatchingEvaluator:
    """Simplified evaluation for matching results"""
    
    def evaluate_matches(self, matches: List[TrialMatch]) -> Dict[str, Any]:
        """Evaluate a list of trial matches"""
        if not matches:
            return {
                'total_matches': 0,
                'avg_match_score': 0,
                'high_confidence_matches': 0,
                'medium_confidence_matches': 0,
                'low_confidence_matches': 0
            }
        
        scores = [match.match_score for match in matches]
        
        high_confidence = sum(1 for score in scores if score > 0.8)
        medium_confidence = sum(1 for score in scores if 0.6 <= score <= 0.8)
        low_confidence = sum(1 for score in scores if score < 0.6)
        
        return {
            'total_matches': len(matches),
            'avg_match_score': sum(scores) / len(scores),
            'high_confidence_matches': high_confidence,
            'medium_confidence_matches': medium_confidence,
            'low_confidence_matches': low_confidence,
            'max_score': max(scores),
            'min_score': min(scores)
        }
    
    def calculate_latency_metrics(self, processing_times: List[float]) -> Dict[str, float]:
        """Calculate latency metrics"""
        if not processing_times:
            return {'avg_latency': 0, 'max_latency': 0, 'min_latency': 0}
        
        return {
            'avg_latency': sum(processing_times) / len(processing_times),
            'max_latency': max(processing_times),
            'min_latency': min(processing_times)
        }
    
    def generate_evaluation_report(self, matches: List[TrialMatch], processing_time: float) -> str:
        """Generate a human-readable evaluation report"""
        metrics = self.evaluate_matches(matches)
        
        report = f"""
=== EVALUATION REPORT ===
Total Matches Found: {metrics['total_matches']}
Average Match Score: {metrics['avg_match_score']:.3f}
Processing Time: {processing_time:.3f} seconds

High Confidence (>0.8): {metrics['high_confidence_matches']}
Medium Confidence (0.6-0.8): {metrics['medium_confidence_matches']}
Low Confidence (<0.6): {metrics['low_confidence_matches']}

Score Range: {metrics['min_score']:.3f} - {metrics['max_score']:.3f}
"""
        return report.strip()