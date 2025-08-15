#!/usr/bin/env python3
"""
Translation Engine Demo Script
Demonstrates the translation capabilities with various examples
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_separator():
    """Print a separator line"""
    print("=" * 80)

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*20} {title} {'='*20}")

def demo_translations():
    """Demonstrate various translation examples"""
    print_header("Translation Examples")
    
    examples = [
        {
            "text": "Hello, welcome to our translation service!",
            "target": "es",
            "description": "English to Spanish"
        },
        {
            "text": "Bonjour, comment allez-vous aujourd'hui?",
            "target": "en",
            "description": "French to English"
        },
        {
            "text": "Guten Tag! Wie geht es Ihnen?",
            "target": "fr",
            "description": "German to French"
        },
        {
            "text": "こんにちは、お元気ですか？",
            "target": "en",
            "description": "Japanese to English"
        },
        {
            "text": "Привет! Как дела?",
            "target": "zh",
            "description": "Russian to Chinese"
        },
        {
            "text": "مرحبا! كيف حالك؟",
            "target": "en",
            "description": "Arabic to English"
        },
        {
            "text": "नमस्ते! आप कैसे हैं?",
            "target": "pt",
            "description": "Hindi to Portuguese"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['description']}")
        print(f"   Input: {example['text']}")
        print(f"   Target: {example['target']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/translate",
                json={
                    "text": example["text"],
                    "target_language": example["target"]
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Detected: {result['detected_language']}")
                print(f"   ✅ Confidence: {result['confidence_level']:.2f}")
                print(f"   ✅ Translation: {result['translated_text']}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                try:
                    error_detail = response.json().get('detail', 'Unknown error')
                    print(f"      Error: {error_detail}")
                except:
                    print(f"      Error: {response.text}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Small delay between requests
        time.sleep(1)

def demo_language_detection():
    """Demonstrate language detection capabilities"""
    print_header("Language Detection Examples")
    
    detection_examples = [
        "Hello world!",
        "Bonjour le monde!",
        "Hola mundo!",
        "Ciao mondo!",
        "Hallo Welt!",
        "Olá mundo!",
        "Привет мир!",
        "こんにちは世界！",
        "안녕하세요 세계!",
        "مرحبا بالعالم!"
    ]
    
    for text in detection_examples:
        try:
            response = requests.post(
                f"{BASE_URL}/api/translate",
                json={
                    "text": text,
                    "target_language": "en"
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ '{text}' -> Detected: {result['detected_language']} (Confidence: {result['confidence_level']:.2f})")
            else:
                print(f"❌ '{text}' -> Failed to detect")
                
        except Exception as e:
            print(f"❌ '{text}' -> Error: {e}")
        
        time.sleep(0.5)

def demo_supported_languages():
    """Show supported languages"""
    print_header("Supported Languages")
    
    try:
        response = requests.get(f"{BASE_URL}/api/languages")
        if response.status_code == 200:
            languages = response.json()
            print(f"Total supported languages: {len(languages)}")
            
            # Group languages by region
            regions = {
                "European": ["en", "fr", "de", "es", "it", "pt", "ru", "nl", "sv", "no", "da", "fi", "pl", "cs", "hu", "ro", "bg", "el", "tr", "uk"],
                "Asian": ["zh", "ja", "ko", "th", "vi", "hi", "bn", "ta", "te", "mr", "gu", "kn", "ml", "pa", "ur", "fa", "ar", "he"],
                "African": ["sw", "ha", "yo", "zu", "xh", "af", "am"],
                "Other": ["la", "eo", "haw", "mi"]
            }
            
            for region, codes in regions.items():
                print(f"\n{region} Languages:")
                region_langs = [lang for lang in languages if lang['code'] in codes]
                for lang in region_langs[:10]:  # Show first 10
                    print(f"  • {lang['name']} ({lang['native_name']})")
                if len(region_langs) > 10:
                    print(f"  ... and {len(region_langs) - 10} more")
                    
        else:
            print(f"Failed to get languages: {response.status_code}")
            
    except Exception as e:
        print(f"Error getting languages: {e}")

def demo_error_handling():
    """Demonstrate error handling"""
    print_header("Error Handling Examples")
    
    error_cases = [
        {
            "text": "",
            "target": "es",
            "expected_error": "Text cannot be empty"
        },
        {
            "text": "Hello",
            "target": "invalid_lang",
            "expected_error": "Target language not supported"
        }
    ]
    
    for i, case in enumerate(error_cases, 1):
        print(f"\n{i}. Testing: '{case['text']}' -> '{case['target']}'")
        print(f"   Expected error: {case['expected_error']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/translate",
                json={
                    "text": case["text"],
                    "target_language": case["target"]
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 400:
                try:
                    error_detail = response.json().get('detail', 'Unknown error')
                    print(f"   ✅ Got expected error: {error_detail}")
                except:
                    print(f"   ✅ Got expected error status: {response.status_code}")
            else:
                print(f"   ❌ Unexpected response: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Request error: {e}")

def main():
    """Main demo function"""
    print("🌍 Translation Engine - Demo Script")
    print("This script demonstrates the capabilities of the Translation Engine")
    print_separator()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code != 200:
            print("❌ Server is not responding properly")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Please start the server first:")
        print("   Run: python start.py")
        return
    
    print("✅ Server is running and responding")
    
    # Run demos
    demo_supported_languages()
    demo_language_detection()
    demo_translations()
    demo_error_handling()
    
    print_separator()
    print("🎉 Demo completed!")
    print("Visit http://localhost:8000 to use the web interface")

if __name__ == "__main__":
    main() 