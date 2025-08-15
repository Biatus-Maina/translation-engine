#!/usr/bin/env python3
"""
Test script for Translation Engine
Tests the main functionality of the FastAPI application
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_get_languages():
    """Test the languages endpoint"""
    print("\n🔍 Testing languages endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/languages")
        if response.status_code == 200:
            languages = response.json()
            print(f"✅ Languages endpoint passed - {len(languages)} languages available")
            print(f"   Sample languages: {[lang['name'] for lang in languages[:5]]}")
            return True
        else:
            print(f"❌ Languages endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Languages endpoint error: {e}")
        return False

def test_translation():
    """Test the translation endpoint"""
    print("\n🔍 Testing translation endpoint...")
    
    test_cases = [
        {
            "text": "Hello, world!",
            "target_language": "es",
            "expected_detected": "en"
        },
        {
            "text": "Bonjour le monde!",
            "target_language": "en",
            "expected_detected": "fr"
        },
        {
            "text": "Hola mundo!",
            "target_language": "de",
            "expected_detected": "es"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"   Testing case {i}: '{test_case['text']}' -> {test_case['target_language']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/translate",
                json={
                    "text": test_case["text"],
                    "target_language": test_case["target_language"]
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Translation successful")
                print(f"      Detected: {result['detected_language']} (expected: {test_case['expected_detected']})")
                print(f"      Confidence: {result['confidence_level']:.2f}")
                print(f"      Result: {result['translated_text']}")
            else:
                print(f"   ❌ Translation failed: {response.status_code}")
                try:
                    error_detail = response.json().get('detail', 'Unknown error')
                    print(f"      Error: {error_detail}")
                except:
                    print(f"      Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"   ❌ Translation error: {e}")
            return False
        
        # Small delay between requests
        time.sleep(1)
    
    return True

def test_error_handling():
    """Test error handling"""
    print("\n🔍 Testing error handling...")
    
    # Test empty text
    try:
        response = requests.post(
            f"{BASE_URL}/api/translate",
            json={"text": "", "target_language": "es"}
        )
        if response.status_code == 400:
            print("✅ Empty text validation working")
        else:
            print(f"❌ Empty text validation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Empty text test error: {e}")
        return False
    
    # Test invalid language
    try:
        response = requests.post(
            f"{BASE_URL}/api/translate",
            json={"text": "Hello", "target_language": "invalid_lang"}
        )
        if response.status_code == 400:
            print("✅ Invalid language validation working")
        else:
            print(f"❌ Invalid language validation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Invalid language test error: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🧪 Translation Engine - Test Suite")
    print("=" * 50)
    
    # Check if server is running
    if not test_health_check():
        print("\n❌ Server is not running. Please start the server first.")
        print("   Run: python start.py")
        return
    
    # Run tests
    tests = [
        ("Health Check", test_health_check),
        ("Languages Endpoint", test_get_languages),
        ("Translation", test_translation),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        else:
            print(f"\n❌ {test_name} failed!")
            break
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is working correctly.")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 