"""
Phase 3 Testing Suite - Code Explainer
Comprehensive testing framework for accuracy, performance, and quality metrics.
"""

import asyncio
import json
import time
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import statistics

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from groq_integration import get_code_explanation
from rag_system import get_rag_system
from ethical_ai import get_ethical_guard


class TestSuite:
    """Comprehensive testing suite for Phase 3 evaluation."""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {
                "accuracy": [],
                "performance": [],
                "relevance": [],
                "ethical": [],
                "quality": []
            },
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "accuracy_score": 0.0,
                "avg_response_time": 0.0,
                "rag_improvement": 0.0
            }
        }
        
        # Test cases: (code, language, expected_concepts)
        self.test_cases = [
            {
                "code": """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
""",
                "language": "Python",
                "category": "recursion",
                "expected_concepts": ["recursion", "base case", "factorial", "function"],
                "difficulty": "medium"
            },
            {
                "code": """
async function fetchData() {
    const response = await fetch('/api/data');
    return await response.json();
}
""",
                "language": "JavaScript",
                "category": "async",
                "expected_concepts": ["async", "await", "promise", "fetch"],
                "difficulty": "medium"
            },
            {
                "code": """
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id
HAVING COUNT(o.id) > 5;
""",
                "language": "SQL",
                "category": "database",
                "expected_concepts": ["join", "group by", "having", "aggregate"],
                "difficulty": "hard"
            },
            {
                "code": """
const numbers = [1, 2, 3, 4, 5];
const squared = numbers.map(x => x * x);
""",
                "language": "JavaScript",
                "category": "functional",
                "expected_concepts": ["array", "map", "arrow function", "higher-order"],
                "difficulty": "easy"
            },
            {
                "code": """
public class BinarySearch {
    public static int search(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }
}
""",
                "language": "Java",
                "category": "algorithms",
                "expected_concepts": ["binary search", "algorithm", "iteration", "array"],
                "difficulty": "medium"
            }
        ]
    
    async def test_accuracy(self) -> Dict[str, Any]:
        """Test explanation accuracy by checking for expected concepts."""
        print("\n=== Testing Accuracy ===")
        accuracy_results = []
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\nTest {i}/{len(self.test_cases)}: {test_case['language']} - {test_case['category']}")
            
            # Test Basic mode
            start_time = time.time()
            basic_result = await get_code_explanation(test_case["code"])
            basic_time = time.time() - start_time
            
            # Test RAG mode
            rag = get_rag_system()
            start_time = time.time()
            rag_result = await get_code_explanation(
                test_case["code"],
                custom_prompt=rag.build_rag_prompt(test_case["code"], rag.retrieve(test_case["code"]))
            )
            rag_time = time.time() - start_time
            
            # Calculate accuracy scores
            basic_score = self._calculate_concept_coverage(
                basic_result["explanation"],
                test_case["expected_concepts"]
            )
            rag_score = self._calculate_concept_coverage(
                rag_result["explanation"],
                test_case["expected_concepts"]
            )
            
            result = {
                "test_id": i,
                "language": test_case["language"],
                "category": test_case["category"],
                "difficulty": test_case["difficulty"],
                "basic_score": round(basic_score, 2),
                "rag_score": round(rag_score, 2),
                "improvement": round((rag_score - basic_score) / basic_score * 100, 1) if basic_score > 0 else 0,
                "basic_time": round(basic_time, 2),
                "rag_time": round(rag_time, 2),
                "passed": rag_score >= 0.6  # Pass if 60%+ concepts covered
            }
            
            accuracy_results.append(result)
            print(f"  Basic: {result['basic_score']*100:.0f}% | RAG: {result['rag_score']*100:.0f}% | Improvement: {result['improvement']}%")
        
        self.results["tests"]["accuracy"] = accuracy_results
        return accuracy_results
    
    def _calculate_concept_coverage(self, explanation: str, expected_concepts: List[str]) -> float:
        """Calculate what percentage of expected concepts are mentioned."""
        explanation_lower = explanation.lower()
        found_concepts = sum(1 for concept in expected_concepts if concept.lower() in explanation_lower)
        return found_concepts / len(expected_concepts) if expected_concepts else 0.0
    
    async def test_performance(self) -> Dict[str, Any]:
        """Test response time performance."""
        print("\n=== Testing Performance ===")
        performance_results = []
        
        # Test with different code lengths
        test_sizes = [
            ("small", "x = 5", 50),
            ("medium", "\n".join(["def func():", "    pass"]) * 10, 500),
            ("large", "\n".join(["# Comment line"] * 100), 2000)
        ]
        
        for size_name, code, expected_max_time_ms in test_sizes:
            print(f"\nTesting {size_name} code ({len(code)} chars)...")
            times = []
            
            # Run 3 trials
            for trial in range(3):
                start_time = time.time()
                result = await get_code_explanation(code)
                elapsed = (time.time() - start_time) * 1000  # Convert to ms
                times.append(elapsed)
                print(f"  Trial {trial + 1}: {elapsed:.0f}ms")
            
            avg_time = statistics.mean(times)
            result = {
                "size": size_name,
                "code_length": len(code),
                "avg_time_ms": round(avg_time, 1),
                "min_time_ms": round(min(times), 1),
                "max_time_ms": round(max(times), 1),
                "expected_max_ms": expected_max_time_ms,
                "passed": avg_time <= expected_max_time_ms
            }
            
            performance_results.append(result)
            print(f"  Average: {avg_time:.0f}ms (Pass: {result['passed']})")
        
        self.results["tests"]["performance"] = performance_results
        return performance_results
    
    async def test_rag_relevance(self) -> Dict[str, Any]:
        """Test RAG retrieval relevance."""
        print("\n=== Testing RAG Relevance ===")
        relevance_results = []
        
        rag = get_rag_system()
        
        # Test retrieval quality
        for i, test_case in enumerate(self.test_cases[:3], 1):  # Test first 3
            print(f"\nTest {i}: {test_case['language']} - {test_case['category']}")
            
            retrieved = rag.retrieve(test_case["code"], top_k=3)
            
            if retrieved:
                avg_score = statistics.mean([doc["relevance_score"] for doc in retrieved])
                max_score = max([doc["relevance_score"] for doc in retrieved])
                min_score = min([doc["relevance_score"] for doc in retrieved])
                
                result = {
                    "test_id": i,
                    "language": test_case["language"],
                    "retrieved_count": len(retrieved),
                    "avg_relevance": round(avg_score, 3),
                    "max_relevance": round(max_score, 3),
                    "min_relevance": round(min_score, 3),
                    "passed": avg_score >= 0.65  # Pass if average relevance >= 65%
                }
                
                print(f"  Retrieved: {len(retrieved)} docs | Avg relevance: {avg_score:.1%}")
            else:
                result = {
                    "test_id": i,
                    "language": test_case["language"],
                    "retrieved_count": 0,
                    "avg_relevance": 0.0,
                    "passed": False
                }
                print(f"  No documents retrieved")
            
            relevance_results.append(result)
        
        self.results["tests"]["relevance"] = relevance_results
        return relevance_results
    
    async def test_ethical_safeguards(self) -> Dict[str, Any]:
        """Test ethical AI safeguards."""
        print("\n=== Testing Ethical Safeguards ===")
        ethical_results = []
        
        ethical_guard = get_ethical_guard()
        
        # Test cases for ethical checks
        ethical_tests = [
            {
                "name": "Sensitive Data Detection",
                "code": "api_key = 'sk-1234567890abcdef'",
                "should_detect": True,
                "type": "sensitive_data"
            },
            {
                "name": "Malicious Code Detection",
                "code": "import os; os.system('rm -rf /')",
                "should_detect": True,
                "type": "malicious_code"
            },
            {
                "name": "Clean Code",
                "code": "def add(a, b): return a + b",
                "should_detect": False,
                "type": "clean"
            },
            {
                "name": "PII Detection",
                "code": "ssn = '123-45-6789'",
                "should_detect": True,
                "type": "pii"
            }
        ]
        
        for i, test in enumerate(ethical_tests, 1):
            print(f"\nTest {i}: {test['name']}")
            
            sanitized, warnings = ethical_guard.sanitize_code(test["code"])
            has_warnings = len(warnings) > 0
            
            result = {
                "test_id": i,
                "name": test["name"],
                "type": test["type"],
                "warnings_found": len(warnings),
                "expected_detection": test["should_detect"],
                "actual_detection": has_warnings,
                "passed": has_warnings == test["should_detect"]
            }
            
            ethical_results.append(result)
            print(f"  Expected: {test['should_detect']} | Detected: {has_warnings} | Pass: {result['passed']}")
        
        self.results["tests"]["ethical"] = ethical_results
        return ethical_results
    
    async def test_response_quality(self) -> Dict[str, Any]:
        """Test response quality metrics."""
        print("\n=== Testing Response Quality ===")
        quality_results = []
        
        ethical_guard = get_ethical_guard()
        
        for i, test_case in enumerate(self.test_cases[:3], 1):
            print(f"\nTest {i}: {test_case['language']}")
            
            result = await get_code_explanation(test_case["code"])
            
            if result["success"]:
                explanation = result["explanation"]
                is_valid, validation_msg = ethical_guard.validate_response(explanation)
                
                quality_result = {
                    "test_id": i,
                    "language": test_case["language"],
                    "explanation_length": len(explanation),
                    "word_count": len(explanation.split()),
                    "is_valid": is_valid,
                    "validation_message": validation_msg,
                    "passed": is_valid and len(explanation) >= 100  # At least 100 chars
                }
                
                quality_results.append(quality_result)
                print(f"  Length: {len(explanation)} chars | Words: {len(explanation.split())} | Valid: {is_valid}")
            else:
                print(f"  Failed to generate explanation")
        
        self.results["tests"]["quality"] = quality_results
        return quality_results
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all test suites and generate comprehensive report."""
        print("\n" + "="*60)
        print("PHASE 3 TESTING SUITE - CODE EXPLAINER")
        print("="*60)
        
        start_time = time.time()
        
        # Run all test categories
        await self.test_accuracy()
        await self.test_performance()
        await self.test_rag_relevance()
        await self.test_ethical_safeguards()
        await self.test_response_quality()
        
        # Calculate summary statistics
        total_tests = 0
        passed_tests = 0
        
        for category, tests in self.results["tests"].items():
            for test in tests:
                total_tests += 1
                if test.get("passed", False):
                    passed_tests += 1
        
        # Accuracy metrics
        if self.results["tests"]["accuracy"]:
            avg_basic_score = statistics.mean([t["basic_score"] for t in self.results["tests"]["accuracy"]])
            avg_rag_score = statistics.mean([t["rag_score"] for t in self.results["tests"]["accuracy"]])
            rag_improvement = ((avg_rag_score - avg_basic_score) / avg_basic_score * 100) if avg_basic_score > 0 else 0
        else:
            avg_rag_score = 0
            rag_improvement = 0
        
        # Performance metrics
        if self.results["tests"]["performance"]:
            avg_response_time = statistics.mean([t["avg_time_ms"] for t in self.results["tests"]["performance"]])
        else:
            avg_response_time = 0
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": total_tests - passed_tests,
            "success_rate": round(passed_tests / total_tests * 100, 1) if total_tests > 0 else 0,
            "accuracy_score": round(avg_rag_score * 100, 1),
            "avg_response_time_ms": round(avg_response_time, 1),
            "rag_improvement": round(rag_improvement, 1),
            "total_time_seconds": round(time.time() - start_time, 1)
        }
        
        # Print summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ({self.results['summary']['success_rate']}%)")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Accuracy Score: {self.results['summary']['accuracy_score']}%")
        print(f"RAG Improvement: {self.results['summary']['rag_improvement']}%")
        print(f"Avg Response Time: {self.results['summary']['avg_response_time_ms']}ms")
        print(f"Total Test Time: {self.results['summary']['total_time_seconds']}s")
        print("="*60)
        
        return self.results
    
    def save_results(self, filename: str = "test_results.json"):
        """Save test results to JSON file."""
        filepath = Path(__file__).parent / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to: {filepath}")


async def main():
    """Main test runner."""
    suite = TestSuite()
    results = await suite.run_all_tests()
    suite.save_results()
    
    # Exit with appropriate code
    sys.exit(0 if results["summary"]["failed"] == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())
