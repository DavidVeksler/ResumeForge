#!/usr/bin/env python3
"""
Test script for local AI integration with LM Studio
"""

import os
import json
import sys
import io
from openai import OpenAI

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_local_ai():
    """Test the local LM Studio integration"""
    print("Testing local AI integration with LM Studio...")
    
    try:
        # Initialize client with local LM Studio endpoint
        client = OpenAI(
            api_key="local-key",  # LM Studio doesn't require real API key
            base_url="http://172.28.144.1:1234/v1"
        )
        
        # Test with a simple prompt
        test_prompt = "Hello! Please respond with a JSON object containing your name and status."
        model_name = os.getenv('LOCAL_MODEL_NAME', 'local-model')
        
        print(f"Using model: {model_name}")
        print(f"Endpoint: http://172.28.144.1:1234/v1")
        print(f"Test prompt: {test_prompt}")
        print("\nSending request...")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": test_prompt}
            ],
            temperature=0.1,
            max_tokens=200
        )
        
        print("✅ Success! Local AI is working.")
        print(f"Response: {response.choices[0].message.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing local AI: {e}")
        return False

def test_resume_parsing():
    """Test resume parsing functionality"""
    print("\n" + "="*50)
    print("Testing resume parsing...")
    
    sample_resume = """
    John Doe
    Software Engineer
    john.doe@email.com
    (555) 123-4567
    
    EXPERIENCE
    Senior Software Engineer at TechCorp (2020-2023)
    - Led a team of 5 developers
    - Built scalable APIs handling 1M+ requests daily
    - Improved system performance by 40%
    
    Software Engineer at StartupXYZ (2018-2020)  
    - Developed React applications
    - Worked with Python and Django
    - Implemented CI/CD pipelines
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology (2014-2018)
    
    SKILLS
    Python, JavaScript, React, Django, AWS, Docker
    """
    
    try:
        client = OpenAI(
            api_key="local-key",  # LM Studio doesn't require real API key
            base_url="http://172.28.144.1:1234/v1"
        )
        
        system_prompt = """You are a resume parsing expert. Convert the provided text resume into a structured JSON format. Return only valid JSON."""
        
        model_name = os.getenv('LOCAL_MODEL_NAME', 'local-model')
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Convert this resume to JSON:\n\n{sample_resume}"}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        
        print("✅ Resume parsing test successful!")
        print("Raw response:")
        print(response.choices[0].message.content[:500] + "..." if len(response.choices[0].message.content) > 500 else response.choices[0].message.content)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing resume parsing: {e}")
        return False

if __name__ == "__main__":
    print("Local AI Integration Test")
    print("=" * 50)
    
    # Test basic connectivity
    basic_test = test_local_ai()
    
    # Test resume parsing if basic test passes
    if basic_test:
        parsing_test = test_resume_parsing()
        
        if parsing_test:
            print("\n🎉 All tests passed! Your local AI integration is ready.")
        else:
            print("\n⚠️  Basic connectivity works, but resume parsing needs attention.")
    else:
        print("\n❌ Local AI integration is not working. Please check:")
        print("1. LM Studio is running at http://172.28.144.1:1234")
        print("2. A model is loaded in LM Studio")
        print("3. The local server is accessible")