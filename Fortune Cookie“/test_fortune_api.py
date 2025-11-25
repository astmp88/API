"""
Test script for the Mystical Fortune API
Run this after starting the API server to see it in action!
"""

import requests
import time

API_BASE_URL = "http://localhost:5001"

def print_separator():
    print("\n" + "="*70 + "\n")

def test_single_fortune():
    print("🔮 Testing Single Fortune Endpoint...")
    print_separator()
    
    response = requests.get(f"{API_BASE_URL}/fortune")
    if response.status_code == 200:
        data = response.json()
        print(f"✨ Fortune: {data['fortune']}")
        print(f"📿 Theme: {data['theme']}")
        print(f"🎭 Style: {data['style']}")
    else:
        print(f" Error: {response.status_code}")

def test_batch_fortunes():
    print("🔮 Testing Batch Fortune Endpoint (3 fortunes)...")
    print_separator()
    
    response = requests.get(f"{API_BASE_URL}/fortune/batch?count=3")
    if response.status_code == 200:
        data = response.json()
        for i, fortune in enumerate(data['fortunes'], 1):
            print(f"Fortune #{i}:")
            print(f"✨ {fortune['fortune']}")
            print(f"📿 Theme: {fortune['theme']}")
            print()
    else:
        print(f"❌ Error: {response.status_code}")

def test_lucky_numbers():
    print("🔮 Testing Lucky Numbers Endpoint...")
    print_separator()
    
    response = requests.get(f"{API_BASE_URL}/fortune/lucky-numbers")
    if response.status_code == 200:
        data = response.json()
        print(f"✨ Fortune: {data['fortune']}")
        print(f"🎲 Lucky Numbers: {', '.join(map(str, data['lucky_numbers']))}")
        print(f"🌈 Lucky Color: {data['lucky_color']}")
    else:
        print(f"❌ Error: {response.status_code}")

def main():
    print("🌟 MYSTICAL FORTUNE API TEST SUITE 🌟")
    print_separator()
    
    try:
        # Test if API is running
        response = requests.get(API_BASE_URL)
        if response.status_code != 200:
            print("❌ API is not running! Please start it with: python fortune_api.py")
            return
        
        print("✅ API is running!")
        print_separator()
        
        # Run tests with delays between them
        test_single_fortune()
        time.sleep(1)
        
        print_separator()
        test_batch_fortunes()
        time.sleep(1)
        
        print_separator()
        test_lucky_numbers()
        
        print_separator()
        print(" All tests completed! The spirits are pleased! 🔮✨")
        
    except requests.exceptions.ConnectionError:
        print("Cannot connect to API! Make sure it's running on http://localhost:5000")
        print("Start it with: python fortune_api.py")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
