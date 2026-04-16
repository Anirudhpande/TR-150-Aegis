import re
from typing import List, Dict, Any, Union, Tuple
from dataclasses import dataclass

@dataclass
class ParsedCriterion:
    original_text: str
    criterion_type: str  # 'age', 'condition_required', 'condition_excluded', 'lab_value', 'general'
    operator: str  # '>=', '<=', 'between', 'normal', 'contains'
    value: Any  # Could be int, str, tuple, etc.
    confidence: float

class CriteriaParser:
    """Simplified criteria parser using regex patterns"""
    
    def __init__(self):
        # Age patterns
        self.age_patterns = [
            (r'age (\d+)-(\d+) years?', 'between'),
            (r'age (\d+) years? or older', '>='),
            (r'age (\d+) years? or younger', '<='),
            (r'(\d+)-(\d+) years? of age', 'between'),
            (r'(\d+) years? or older', '>='),
            (r'(\d+) years? or younger', '<='),
        ]
        
        # Condition patterns
        self.condition_patterns = [
            r'diagnosis of (.+?)(?:\s|$|,)',
            r'confirmed (.+?) diagnosis',
            r'history of (.+?)(?:\s|$|,)',
            r'(.+?) patients?',
            r'with (.+?)(?:\s|$|,)',
        ]
        
        # Lab value patterns
        self.lab_patterns = [
            (r'(\w+) between ([\d.]+)-([\d.]+)', 'between'),
            (r'(\w+) ≥ ([\d.]+)', '>='),
            (r'(\w+) >= ([\d.]+)', '>='),
            (r'(\w+) ≤ ([\d.]+)', '<='),
            (r'(\w+) <= ([\d.]+)', '<='),
            (r'normal (\w+)', 'normal'),
        ]
        
        # Common medical conditions
        self.medical_conditions = {
            'diabetes', 'hypertension', 'cancer', 'asthma', 'copd', 
            'heart disease', 'kidney disease', 'breast cancer', 'lung cancer'
        }
    
    def parse_criteria(self, criteria_list: List[str]) -> List[ParsedCriterion]:
        """Parse a list of criteria strings"""
        parsed_criteria = []
        
        for criterion_text in criteria_list:
            parsed = self.parse_single_criterion(criterion_text)
            if parsed:
                parsed_criteria.append(parsed)
        
        return parsed_criteria
    
    def parse_single_criterion(self, text: str) -> ParsedCriterion:
        """Parse a single criterion string"""
        text_lower = text.lower().strip()
        
        # Try age parsing
        age_result = self._parse_age(text_lower)
        if age_result:
            return ParsedCriterion(
                original_text=text,
                criterion_type='age',
                operator=age_result['operator'],
                value=age_result['value'],
                confidence=0.9
            )
        
        # Try lab value parsing
        lab_result = self._parse_lab_value(text_lower)
        if lab_result:
            return ParsedCriterion(
                original_text=text,
                criterion_type='lab_value',
                operator=lab_result['operator'],
                value=lab_result['value'],
                confidence=0.8
            )
        
        # Try condition parsing
        condition_result = self._parse_condition(text_lower)
        if condition_result:
            # Determine if it's required or excluded based on context
            is_exclusion = any(word in text_lower for word in ['no', 'not', 'without', 'exclude', 'absence'])
            criterion_type = 'condition_excluded' if is_exclusion else 'condition_required'
            
            return ParsedCriterion(
                original_text=text,
                criterion_type=criterion_type,
                operator='contains',
                value=condition_result,
                confidence=0.7
            )
        
        # Default to general criterion
        return ParsedCriterion(
            original_text=text,
            criterion_type='general',
            operator='contains',
            value=text_lower,
            confidence=0.5
        )
    
    def _parse_age(self, text: str) -> Dict[str, Any]:
        """Parse age-related criteria"""
        for pattern, operator in self.age_patterns:
            match = re.search(pattern, text)
            if match:
                if operator == 'between':
                    return {
                        'operator': operator,
                        'value': (int(match.group(1)), int(match.group(2)))
                    }
                else:
                    return {
                        'operator': operator,
                        'value': int(match.group(1))
                    }
        return None
    
    def _parse_lab_value(self, text: str) -> Dict[str, Any]:
        """Parse lab value criteria"""
        for pattern, operator in self.lab_patterns:
            match = re.search(pattern, text)
            if match:
                if operator == 'normal':
                    return {
                        'operator': operator,
                        'value': match.group(1)
                    }
                elif operator == 'between':
                    return {
                        'operator': operator,
                        'value': (match.group(1), (float(match.group(2)), float(match.group(3))))
                    }
                else:
                    return {
                        'operator': operator,
                        'value': (match.group(1), float(match.group(2)))
                    }
        return None
    
    def _parse_condition(self, text: str) -> str:
        """Parse condition-related criteria"""
        # First try exact matches with known conditions
        for condition in self.medical_conditions:
            if condition in text:
                return condition
        
        # Then try pattern matching
        for pattern in self.condition_patterns:
            match = re.search(pattern, text)
            if match:
                condition = match.group(1).strip()
                # Clean up the condition text
                condition = re.sub(r'\s+', ' ', condition)
                condition = condition.replace('type 2', '').replace('stage', '').strip()
                if len(condition) > 3:  # Avoid very short matches
                    return condition
        
        return None