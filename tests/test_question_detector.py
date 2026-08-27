from app.nlp.question_detector import is_query
from tests.query_detection_examples import TEST_CASES

def run_tests():
    passed = 0
    failed = 0
    
    print("Running query detection tests...")
    print("=" * 60)
    
    for test, expected in TEST_CASES:
        actual = is_query(test)
        
        if actual == expected:
            print(f"PASS: {test}")
            passed += 1
            
        else:
            print(f"FAIL: {test}")
            print(f"    Expected: {expected}")
            print(f"    Got:      {actual}")
            failed += 1
            
    print("=" * 60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {len(TEST_CASES)}")
    print("=" * 60)
    
    if failed == 0:
        print("All tests passed!")
        
    else:
        print("Some tests failed.")
        
if __name__ == "__main__":
    run_tests()