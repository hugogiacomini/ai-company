"""
Test runner for AI Company.
Runs all tests without requiring API keys.
"""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Set dummy API key for testing
os.environ['OPENAI_API_KEY'] = 'test-key-for-structure-testing'


def run_all_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("\n" + "="*80)
    print("AI COMPANY - COMPREHENSIVE TEST SUITE")
    print("="*80 + "\n")
    
    success = run_all_tests()
    
    print("\n" + "="*80)
    if success:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("="*80 + "\n")
    
    sys.exit(0 if success else 1)
