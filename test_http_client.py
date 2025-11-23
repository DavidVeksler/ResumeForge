#!/usr/bin/env python3
"""
Simple HTTP test for LM Studio endpoint using requests
"""

import requests
import json
import sys
import io

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_lm_studio_direct():
    """Test LM Studio endpoint directly with HTTP requests"""
    print("Testing LM Studio endpoint with direct HTTP requests...")
    
    try:
        # Test endpoint availability
        url = "http://172.28.144.1:1234/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer local-key"
        }
        
        payload = {
            "model": "local-model",
            "messages": [
                {"role": "user", "content": "Hello! Please respond with 'Hello World' to test the connection."}
            ],
            "temperature": 0.1,
            "max_tokens": 50
        }
        
        print(f"Sending POST request to: {url}")
        print("Payload:", json.dumps(payload, indent=2))
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success! LM Studio is responding.")
            print("Response:", json.dumps(result, indent=2))
            return True
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print("Response:", response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Cannot connect to LM Studio at http://172.28.144.1:1234")
        print("Please ensure:")
        print("1. LM Studio is running")
        print("2. A model is loaded")  
        print("3. Local Server is started in LM Studio")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_model_list():
    """Test getting available models from LM Studio"""
    print("\n" + "="*50)
    print("Testing model list endpoint...")
    
    try:
        url = "http://172.28.144.1:1234/v1/models"
        headers = {"Authorization": "Bearer local-key"}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            models = response.json()
            print("✅ Available models:")
            print(json.dumps(models, indent=2))
            return models
        else:
            print(f"❌ Error getting models: HTTP {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error getting models: {e}")
        return None

if __name__ == "__main__":
    print("Direct HTTP Test for LM Studio")
    print("=" * 50)
    
    # Test basic connectivity
    basic_test = test_lm_studio_direct()
    
    # Test model list
    models = test_model_list()
    
    if basic_test:
        print("\n🎉 LM Studio is working correctly!")
        if models and 'data' in models and models['data']:
            print(f"You can use model name: '{models['data'][0]['id']}' in your configuration")
        print("\nYour resume application should work with the local AI now.")
    else:
        print("\n❌ LM Studio is not accessible. Please check the setup.")