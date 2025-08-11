#!/usr/bin/env python3
"""
Test script for both AI providers (OpenAI and Local LLM)
Tests the configuration switching mechanism for text-to-JSON conversion
"""

import os
import json
import tempfile
from openai import OpenAI

def test_openai_provider():
    """Test OpenAI API provider"""
    print("Testing OpenAI API provider...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OpenAI API key not configured")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        
        print(f"Using model: {model}")
        
        # Simple test prompt
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Respond with a JSON object containing your name and status."}
            ],
            temperature=0.1,
            max_tokens=100
        )
        
        print("✅ OpenAI API connection successful!")
        print(f"Response: {response.choices[0].message.content[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API test failed: {e}")
        return False

def test_local_provider():
    """Test Local LLM provider"""
    print("\nTesting Local LLM provider...")
    
    base_url = os.getenv('LOCAL_LLM_BASE_URL', 'http://172.28.144.1:1234/v1')
    model = os.getenv('LOCAL_MODEL_NAME', 'local-model')
    
    try:
        client = OpenAI(
            api_key="local-key",  # Local LLM doesn't require real API key
            base_url=base_url
        )
        
        print(f"Using endpoint: {base_url}")
        print(f"Using model: {model}")
        
        # Simple test prompt
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Respond with a JSON object containing your name and status."}
            ],
            temperature=0.1,
            max_tokens=100
        )
        
        print("✅ Local LLM connection successful!")
        print(f"Response: {response.choices[0].message.content[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ Local LLM test failed: {e}")
        return False

def test_resume_parsing(provider):
    """Test resume parsing with specified provider"""
    print(f"\nTesting resume parsing with {provider} provider...")
    
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
    
    SKILLS
    Python, JavaScript, React, Django, AWS, Docker
    """
    
    try:
        if provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                print("❌ OpenAI API key not configured")
                return False
            
            client = OpenAI(api_key=api_key)
            model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        else:
            base_url = os.getenv('LOCAL_LLM_BASE_URL', 'http://172.28.144.1:1234/v1')
            client = OpenAI(
                api_key="local-key",
                base_url=base_url
            )
            model = os.getenv('LOCAL_MODEL_NAME', 'local-model')
        
        system_prompt = """You are a resume parsing expert. Convert the provided text resume into a structured JSON format. Return only valid JSON with fields: personal, experience, skills."""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Convert this resume to JSON:\n\n{sample_resume}"}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        
        result = response.choices[0].message.content.strip()
        
        # Try to parse as JSON
        if result.startswith('```json'):
            result = result[7:]
        if result.endswith('```'):
            result = result[:-3]
        
        try:
            parsed = json.loads(result)
            print(f"✅ Resume parsing with {provider} successful!")
            print(f"Parsed fields: {list(parsed.keys())}")
            return True
        except json.JSONDecodeError:
            print(f"⚠️ {provider} returned non-JSON response:")
            print(result[:300] + "...")
            return False
            
    except Exception as e:
        print(f"❌ Resume parsing with {provider} failed: {e}")
        return False

def test_configuration_switching():
    """Test switching between providers using environment variables"""
    print("\n" + "="*60)
    print("Testing Configuration Switching")
    print("="*60)
    
    # Test both providers
    results = {}
    
    # Test OpenAI
    original_provider = os.getenv('AI_PROVIDER')
    os.environ['AI_PROVIDER'] = 'openai'
    results['openai_basic'] = test_openai_provider()
    results['openai_parsing'] = test_resume_parsing('openai') if results['openai_basic'] else False
    
    # Test Local LLM
    os.environ['AI_PROVIDER'] = 'local'  
    results['local_basic'] = test_local_provider()
    results['local_parsing'] = test_resume_parsing('local') if results['local_basic'] else False
    
    # Restore original setting
    if original_provider:
        os.environ['AI_PROVIDER'] = original_provider
    
    # Summary
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20} {status}")
    
    # Configuration recommendations
    print("\nCONFIGURATION RECOMMENDATIONS:")
    if results['openai_basic']:
        print("✅ OpenAI API is properly configured and working")
        print("   Set AI_PROVIDER=openai to use OpenAI API")
    else:
        print("⚠️  OpenAI API needs configuration")
        print("   Check OPENAI_API_KEY environment variable")
    
    if results['local_basic']:
        print("✅ Local LLM is accessible and working")
        print("   Set AI_PROVIDER=local to use local LLM")
    else:
        print("⚠️  Local LLM not accessible")
        print("   Check LOCAL_LLM_BASE_URL and ensure LM Studio is running")
    
    success_count = sum(1 for result in results.values() if result)
    total_tests = len(results)
    
    print(f"\nOverall: {success_count}/{total_tests} tests passed")
    return success_count == total_tests

if __name__ == "__main__":
    print("AI Provider Configuration Test Suite")
    print("=" * 60)
    
    # Load environment from .env file if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Loaded environment from .env file")
    except ImportError:
        print("⚠️  python-dotenv not installed, using system environment")
    
    # Show current configuration
    print(f"\nCurrent Configuration:")
    print(f"AI_PROVIDER: {os.getenv('AI_PROVIDER', 'not set')}")
    print(f"OPENAI_MODEL: {os.getenv('OPENAI_MODEL', 'not set')}")  
    print(f"OPENAI_API_KEY: {'configured' if os.getenv('OPENAI_API_KEY') else 'not set'}")
    print(f"LOCAL_LLM_BASE_URL: {os.getenv('LOCAL_LLM_BASE_URL', 'not set')}")
    print(f"LOCAL_MODEL_NAME: {os.getenv('LOCAL_MODEL_NAME', 'not set')}")
    
    # Run tests
    all_passed = test_configuration_switching()
    
    if all_passed:
        print("\n🎉 All tests passed! Your AI provider configuration is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration and try again.")