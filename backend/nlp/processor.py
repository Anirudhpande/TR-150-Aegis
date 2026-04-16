import re
import numpy as np
from typing import List, Dict, Any
from difflib import SequenceMatcher

class MedicalNLPProcessor:
    """Simplified NLP processor without heavy ML dependencies"""
    
    def __init__(self):
        # Basic medical term mappings
        self.condition_synonyms = {
            'diabetes': ['diabetes mellitus', 'dm', 'diabetic', 'hyperglycemia'],
            'hypertension': ['high blood pressure', 'htn', 'elevated bp'],
            'copd': ['chronic obstructive pulmonary disease', 'emphysema', 'chronic bronchitis'],
            'asthma': ['bronchial asthma', 'allergic asthma'],
            'cancer': ['carcinoma', 'tumor', 'malignancy', 'neoplasm'],
            'heart disease': ['cardiac disease', 'coronary artery disease', 'cad', 'heart failure'],
            'kidney disease': ['renal disease', 'chronic kidney disease', 'ckd', 'nephropathy']
        }
        
        # Normal lab value ranges (simplified)
        self.lab_ranges = {
            'glucose': (70, 100),
            'hemoglobin': (12, 16),
            'creatinine': (0.6, 1.2),
            'cholesterol': (100, 200)
        }
    
    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Create simple embeddings using word frequency"""
        # Create vocabulary from all texts
        vocab = set()
        for text in texts:
            words = self._tokenize(text.lower())
            vocab.update(words)
        
        vocab = list(vocab)
        vocab_size = len(vocab)
        
        # Create embeddings matrix
        embeddings = np.zeros((len(texts), vocab_size))
        
        for i, text in enumerate(texts):
            words = self._tokenize(text.lower())
            word_counts = {}
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1
            
            # Fill embedding vector
            for j, vocab_word in enumerate(vocab):
                if vocab_word in word_counts:
                    embeddings[i, j] = word_counts[vocab_word]
        
        # Normalize
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1  # Avoid division by zero
        embeddings = embeddings / norms
        
        return embeddings
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity using string matching and synonyms"""
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        
        # Direct string similarity
        direct_sim = SequenceMatcher(None, text1_lower, text2_lower).ratio()
        
        # Check for medical synonyms
        synonym_sim = 0
        words1 = self._tokenize(text1_lower)
        words2 = self._tokenize(text2_lower)
        
        for word1 in words1:
            for condition, synonyms in self.condition_synonyms.items():
                if word1 in synonyms or word1 == condition:
                    for word2 in words2:
                        if word2 in synonyms or word2 == condition:
                            synonym_sim = max(synonym_sim, 0.8)
        
        return max(direct_sim, synonym_sim)
    
    def extract_medical_concepts(self, text: str) -> Dict[str, List[str]]:
        """Extract medical concepts from text"""
        text_lower = text.lower()
        concepts = {'conditions': [], 'symptoms': [], 'medications': []}
        
        # Look for conditions
        for condition, synonyms in self.condition_synonyms.items():
            if condition in text_lower or any(syn in text_lower for syn in synonyms):
                concepts['conditions'].append(condition)
        
        # Simple medication detection (ends with common suffixes)
        med_suffixes = ['in', 'ol', 'ide', 'ine', 'ate', 'pril']
        words = self._tokenize(text_lower)
        for word in words:
            if any(word.endswith(suffix) for suffix in med_suffixes) and len(word) > 4:
                concepts['medications'].append(word)
        
        return concepts
    
    def is_lab_value_normal(self, lab_name: str, value: float) -> bool:
        """Check if lab value is in normal range"""
        if lab_name.lower() in self.lab_ranges:
            min_val, max_val = self.lab_ranges[lab_name.lower()]
            return min_val <= value <= max_val
        return True  # Assume normal if range unknown
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization"""
        # Remove punctuation and split
        text = re.sub(r'[^\w\s]', ' ', text)
        return [word for word in text.split() if len(word) > 2]