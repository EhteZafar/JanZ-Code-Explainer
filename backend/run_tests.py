"""
Automated Test Runner - Phase 3
Convenience script to run tests and generate reports.
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from test_suite import TestSuite


async def run_tests():
    """Run all tests with enhanced reporting."""
    print("\n🚀 Starting Phase 3 Test Suite...")
    print("="*70)
    
    suite = TestSuite()
    
    try:
        results = await suite.run_all_tests()
        
        # Save results with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.json"
        suite.save_results(filename)
        
        # Print detailed results
        print("\n" + "="*70)
        print("DETAILED RESULTS BY CATEGORY")
        print("="*70)
        
        # Accuracy Results
        if results["tests"]["accuracy"]:
            print("\n📊 ACCURACY TESTS:")
            for test in results["tests"]["accuracy"]:
                status = "✅" if test["passed"] else "❌"
                print(f"  {status} {test['language']} - {test['category']}")
                print(f"     Basic: {test['basic_score']*100:.0f}% | RAG: {test['rag_score']*100:.0f}% | Improvement: {test['improvement']}%")
        
        # Performance Results
        if results["tests"]["performance"]:
            print("\n⚡ PERFORMANCE TESTS:")
            for test in results["tests"]["performance"]:
                status = "✅" if test["passed"] else "❌"
                print(f"  {status} {test['size'].capitalize()} code ({test['code_length']} chars)")
                print(f"     Avg: {test['avg_time_ms']}ms | Min: {test['min_time_ms']}ms | Max: {test['max_time_ms']}ms")
        
        # RAG Relevance Results
        if results["tests"]["relevance"]:
            print("\n🎯 RAG RELEVANCE TESTS:")
            for test in results["tests"]["relevance"]:
                status = "✅" if test["passed"] else "❌"
                print(f"  {status} {test['language']}")
                print(f"     Retrieved: {test['retrieved_count']} docs | Avg relevance: {test['avg_relevance']*100:.1f}%")
        
        # Ethical Safeguards Results
        if results["tests"]["ethical"]:
            print("\n🛡️ ETHICAL SAFEGUARDS TESTS:")
            for test in results["tests"]["ethical"]:
                status = "✅" if test["passed"] else "❌"
                print(f"  {status} {test['name']}")
                print(f"     Expected: {test['expected_detection']} | Detected: {test['actual_detection']}")
        
        # Quality Results
        if results["tests"]["quality"]:
            print("\n✨ RESPONSE QUALITY TESTS:")
            for test in results["tests"]["quality"]:
                status = "✅" if test["passed"] else "❌"
                print(f"  {status} {test['language']}")
                print(f"     Length: {test['explanation_length']} chars | Words: {test['word_count']} | Valid: {test['is_valid']}")
        
        # Final Summary
        print("\n" + "="*70)
        print("FINAL SUMMARY")
        print("="*70)
        summary = results["summary"]
        print(f"✓ Tests Passed: {summary['passed']}/{summary['total_tests']} ({summary['success_rate']}%)")
        print(f"✗ Tests Failed: {summary['failed']}/{summary['total_tests']}")
        print(f"📈 RAG Accuracy Score: {summary['accuracy_score']}%")
        print(f"📊 RAG Improvement: {summary['rag_improvement']}%")
        print(f"⏱️ Average Response Time: {summary['avg_response_time_ms']}ms")
        print(f"⏳ Total Test Duration: {summary['total_time_seconds']}s")
        print(f"📄 Results saved to: {filename}")
        print("="*70)
        
        # Determine exit status
        if summary["failed"] == 0:
            print("\n✅ ALL TESTS PASSED!")
            return 0
        else:
            print(f"\n⚠️ {summary['failed']} TEST(S) FAILED")
            return 1
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    """Entry point for test runner."""
    exit_code = asyncio.run(run_tests())
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
