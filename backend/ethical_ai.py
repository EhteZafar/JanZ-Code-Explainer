"""
Ethical AI Safeguards
Implements bias detection, content filtering, privacy protection, and safety measures
"""

import re
import logging
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)


class EthicalAIGuard:
    """
    Implement ethical AI safeguards including:
    - Bias detection and mitigation
    - Content filtering
    - Privacy protection
    - Code sanitization
    - Response validation
    """
    
    def __init__(self):
        """Initialize ethical AI safeguards."""
        # Sensitive patterns to detect
        self.sensitive_patterns = {
            'api_keys': [
                r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?([a-zA-Z0-9_-]+)["\']?',
                r'(?i)(secret[_-]?key|secretkey)\s*[:=]\s*["\']?([a-zA-Z0-9_-]+)["\']?',
                r'(?i)(access[_-]?token)\s*[:=]\s*["\']?([a-zA-Z0-9_-]+)["\']?'
            ],
            'credentials': [
                r'(?i)(password|passwd|pwd)\s*[:=]\s*["\']?([^\s"\']+)["\']?',
                r'(?i)(username|user)\s*[:=]\s*["\']?([^\s"\']+)["\']?',
                r'(?i)(email)\s*[:=]\s*["\']?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})["\']?'
            ],
            'personal_info': [
                r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
                r'\b\d{16}\b',  # Credit card
                r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'  # Phone
            ]
        }
        
        # Bias-related terms to flag
        self.bias_indicators = [
            'gender', 'race', 'age', 'religion', 'ethnicity',
            'disability', 'nationality', 'sexual orientation'
        ]
        
        # Malicious code patterns
        self.malicious_patterns = [
            r'(?i)(rm\s+-rf|rmdir\s+/s)',  # Dangerous deletion
            r'(?i)(eval|exec)\s*\(',  # Code execution
            r'(?i)(__import__|subprocess|os\.system)',  # System access
            r'(?i)(DROP\s+TABLE|DELETE\s+FROM)',  # SQL injection
            r'(?i)(<script|javascript:)',  # XSS
        ]
        
        logger.info("Ethical AI safeguards initialized")
    
    def sanitize_code(self, code: str) -> Tuple[str, List[str]]:
        """
        Sanitize code input by detecting and masking sensitive information.
        
        Args:
            code: Input code string
            
        Returns:
            Tuple of (sanitized_code, list_of_warnings)
        """
        warnings = []
        sanitized = code
        
        # Check for sensitive information
        for category, patterns in self.sensitive_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, sanitized)
                if matches:
                    # Mask sensitive values
                    sanitized = re.sub(
                        pattern,
                        lambda m: f"{m.group(1)}='***REDACTED***'",
                        sanitized
                    )
                    warnings.append(
                        f"⚠️ Detected {category}: Sensitive information masked"
                    )
                    logger.warning(f"Sensitive {category} detected and masked")
        
        # Check for malicious patterns
        malicious_found = []
        for pattern in self.malicious_patterns:
            if re.search(pattern, code):
                malicious_found.append(pattern)
        
        if malicious_found:
            warnings.append(
                "⚠️ Potentially dangerous code patterns detected. "
                "Please review carefully."
            )
            logger.warning(f"Malicious patterns detected: {malicious_found}")
        
        return sanitized, warnings
    
    def check_bias(self, text: str) -> Dict:
        """
        Check text for potential bias indicators.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with bias analysis results
        """
        found_indicators = []
        
        for indicator in self.bias_indicators:
            if re.search(rf'\b{indicator}\b', text, re.IGNORECASE):
                found_indicators.append(indicator)
        
        has_bias_risk = len(found_indicators) > 0
        
        result = {
            'has_bias_risk': has_bias_risk,
            'indicators_found': found_indicators,
            'severity': 'low' if len(found_indicators) <= 1 else 'medium',
            'recommendation': (
                'Content contains terms that may relate to protected categories. '
                'Ensure explanations are objective and unbiased.'
                if has_bias_risk else 'No bias indicators detected'
            )
        }
        
        if has_bias_risk:
            logger.info(f"Bias indicators found: {found_indicators}")
        
        return result
    
    def validate_response(self, response: str) -> Tuple[bool, str]:
        """
        Validate AI response for quality and safety.
        
        Args:
            response: AI-generated response
            
        Returns:
            Tuple of (is_valid, reason)
        """
        # Check minimum length
        if len(response.strip()) < 50:
            return False, "Response too short"
        
        # Check for incomplete responses
        incomplete_markers = [
            '...', '[truncated]', '[error]', 'I apologize, but'
        ]
        for marker in incomplete_markers:
            if marker.lower() in response.lower()[-100:]:
                return False, "Response appears incomplete"
        
        # Check for harmful content
        harmful_keywords = [
            'hack', 'exploit', 'bypass security', 'steal',
            'unauthorized access', 'malicious'
        ]
        harmful_found = sum(
            1 for keyword in harmful_keywords
            if keyword in response.lower()
        )
        if harmful_found >= 2:
            logger.warning("Response contains potentially harmful content")
            return False, "Response contains potentially harmful guidance"
        
        return True, "Response validated"
    
    def get_privacy_notice(self) -> Dict:
        """
        Get privacy and data handling notice.
        
        Returns:
            Dictionary with privacy information
        """
        return {
            'data_retention': {
                'code_snippets': 'Not stored permanently',
                'explanations': 'Not stored permanently',
                'metrics': 'Anonymous statistics only'
            },
            'data_usage': {
                'purpose': 'Generate code explanations only',
                'sharing': 'Code sent to Groq API for processing',
                'storage': 'Temporary in-memory processing'
            },
            'user_rights': {
                'access': 'No personal data collected',
                'deletion': 'Session-based, auto-deleted',
                'portability': 'Explanations can be copied/exported'
            },
            'security': {
                'encryption': 'HTTPS for API calls',
                'sanitization': 'Automatic sensitive data masking',
                'audit': 'Request logging for debugging only'
            },
            'compliance': {
                'gdpr': 'No personal data processing',
                'ccpa': 'No data selling or sharing',
                'educational_use': 'Intended for learning purposes'
            }
        }
    
    def check_code_quality(self, code: str) -> Dict:
        """
        Perform basic code quality checks.
        
        Args:
            code: Code to analyze
            
        Returns:
            Dictionary with quality metrics
        """
        lines = code.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        
        # Count comments
        comment_patterns = [
            r'^\s*#',  # Python
            r'^\s*//',  # JavaScript, Java, C++
            r'^\s*/\*',  # Block comments
        ]
        comment_lines = sum(
            1 for line in lines
            if any(re.match(p, line) for p in comment_patterns)
        )
        
        # Calculate metrics
        total_lines = len(lines)
        code_lines = len(non_empty_lines)
        comment_ratio = (
            (comment_lines / code_lines * 100)
            if code_lines > 0 else 0
        )
        
        # Check for best practices
        has_meaningful_names = bool(
            re.search(r'\b[a-z][a-zA-Z]{4,}\b', code)
        )
        has_functions = bool(
            re.search(r'def |function |func ', code)
        )
        
        quality_score = 50  # Base score
        if comment_ratio >= 10:
            quality_score += 20
        if has_meaningful_names:
            quality_score += 15
        if has_functions:
            quality_score += 15
        
        return {
            'total_lines': total_lines,
            'code_lines': code_lines,
            'comment_lines': comment_lines,
            'comment_ratio': round(comment_ratio, 1),
            'has_meaningful_names': has_meaningful_names,
            'has_functions': has_functions,
            'estimated_quality_score': min(quality_score, 100),
            'suggestions': self._get_quality_suggestions(
                comment_ratio, has_meaningful_names, has_functions
            )
        }
    
    def _get_quality_suggestions(
        self,
        comment_ratio: float,
        has_names: bool,
        has_functions: bool
    ) -> List[str]:
        """Generate code quality suggestions."""
        suggestions = []
        
        if comment_ratio < 10:
            suggestions.append(
                "Consider adding more comments to explain complex logic"
            )
        if not has_names:
            suggestions.append(
                "Use descriptive variable and function names"
            )
        if not has_functions:
            suggestions.append(
                "Consider breaking code into reusable functions"
            )
        
        if not suggestions:
            suggestions.append("Code structure looks good!")
        
        return suggestions


# Global instance
_guard = None


def get_ethical_guard() -> EthicalAIGuard:
    """Get or create global ethical AI guard instance."""
    global _guard
    if _guard is None:
        _guard = EthicalAIGuard()
    return _guard
