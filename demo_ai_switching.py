#!/usr/bin/env python3
"""
Demonstration script showing how to switch between OpenAI API and Local LLM
for the "Convert to JSON" feature in AI Resume Optimizer
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

def demo_configuration_switching():
    """Demonstrates how to switch between AI providers"""
    
    print("AI Resume Optimizer - Provider Switching Demo")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Sample resume text for testing
    sample_resume = """
    Jane Doe
    Full Stack Developer
    jane.doe@example.com
    (555) 987-6543
    San Francisco, CA
    
    PROFESSIONAL SUMMARY
    Experienced full-stack developer with 6+ years building scalable web applications.
    Expertise in React, Node.js, and cloud technologies. Led teams and delivered
    high-impact features for fintech applications.
    
    EXPERIENCE
    Senior Full Stack Developer | FinTech Solutions Inc | 2021 - Present
    • Built React dashboard serving 100K+ users with real-time data
    • Developed Node.js APIs handling $50M+ in daily transactions  
    • Led migration to AWS reducing infrastructure costs by 35%
    • Mentored 4 junior developers and established code review processes
    
    Full Stack Developer | TechStartup Co | 2018 - 2021
    • Developed payment processing system for cryptocurrency exchange
    • Integrated blockchain APIs with 99.9% uptime SLA
    • Built automated trading features generating 15% user growth
    
    SKILLS
    Frontend: React, Vue.js, TypeScript, HTML5, CSS3
    Backend: Node.js, Python, Express, Django, PostgreSQL
    Cloud: AWS, Docker, Kubernetes, CI/CD
    FinTech: Blockchain, DeFi, Payment Processing
    """
    
    print("Sample Resume Text (truncated):")
    print(sample_resume[:200] + "...\n")
    
    # 1. Test OpenAI Provider
    print("1. Testing OpenAI API Provider")
    print("-" * 30)
    test_openai_provider(sample_resume)
    
    print("\n")
    
    # 2. Show Local LLM Configuration
    print("2. Local LLM Provider Configuration")
    print("-" * 38)
    show_local_llm_config()
    
    print("\n")
    
    # 3. Show how to switch configurations
    print("3. How to Switch Between Providers")
    print("-" * 35)
    show_switching_instructions()

def test_openai_provider(sample_text):
    """Test OpenAI API provider"""
    
    api_key = os.getenv('OPENAI_API_KEY')
    model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    
    if not api_key:
        print("❌ OpenAI API key not configured")
        return
    
    print(f"✅ Provider: OpenAI API")
    print(f"✅ Model: {model}")
    print(f"✅ API Key: configured")
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Simple parsing prompt
        system_prompt = """Convert this resume text to JSON with fields: personal, experience, skills. Return only valid JSON."""
        
        print("\n🔄 Converting resume to JSON...")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Convert to JSON:\n{sample_text[:500]}..."}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        
        result = response.choices[0].message.content.strip()
        
        # Clean up JSON markers
        if result.startswith('```json'):
            result = result[7:]
        if result.endswith('```'):
            result = result[:-3]
        
        # Validate JSON
        try:
            parsed = json.loads(result)
            print("✅ Conversion successful!")
            print(f"   Name: {parsed.get('personal', {}).get('name', 'N/A')}")
            print(f"   Experience entries: {len(parsed.get('experience', []))}")
            print(f"   Skills available: {'Yes' if parsed.get('skills') else 'No'}")
            
        except json.JSONDecodeError:
            print("⚠️  Response was not valid JSON, but API call succeeded")
            print(f"   Response preview: {result[:100]}...")
        
    except Exception as e:
        print(f"❌ OpenAI API test failed: {e}")

def show_local_llm_config():
    """Show local LLM configuration"""
    
    base_url = os.getenv('LOCAL_LLM_BASE_URL', 'http://172.28.144.1:1234/v1')
    model = os.getenv('LOCAL_MODEL_NAME', 'local-model')
    
    print(f"🏠 Provider: Local LLM")
    print(f"🌐 Endpoint: {base_url}")
    print(f"🤖 Model: {model}")
    
    print(f"\n📋 To use Local LLM:")
    print(f"   1. Install and run LM Studio")
    print(f"   2. Load a model (e.g., Llama, Mistral)")
    print(f"   3. Start local server on {base_url}")
    print(f"   4. Set AI_PROVIDER=local in .env")
    
    # Test connectivity
    try:
        client = OpenAI(api_key="local-key", base_url=base_url)
        
        print(f"\n🔄 Testing local LLM connectivity...")
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hello! Respond with 'OK' if you can hear me."}],
            temperature=0.1,
            max_tokens=50,
            timeout=5.0
        )
        
        print("✅ Local LLM is accessible and responding!")
        print(f"   Response: {response.choices[0].message.content[:100]}")
        
    except Exception as e:
        print("❌ Local LLM not accessible")
        print(f"   Error: {str(e)[:100]}...")
        print("   This is expected if LM Studio is not running")

def show_switching_instructions():
    """Show instructions for switching providers"""
    
    current_provider = os.getenv('AI_PROVIDER', 'openai')
    
    print(f"Current provider: {current_provider}")
    print("\n🔧 To switch providers, update your .env file:\n")
    
    print("For OpenAI API:")
    print("   AI_PROVIDER=openai")
    print("   OPENAI_API_KEY=your-actual-api-key")
    print("   OPENAI_MODEL=gpt-4o-mini")
    
    print("\nFor Local LLM:")
    print("   AI_PROVIDER=local")
    print("   LOCAL_LLM_BASE_URL=http://172.28.144.1:1234/v1")
    print("   LOCAL_MODEL_NAME=local-model")
    
    print("\n📁 Example .env configuration:")
    print("""   # Choose your AI provider
   AI_PROVIDER=openai
   
   # OpenAI Configuration (when provider=openai)
   OPENAI_API_KEY=sk-your-api-key-here
   OPENAI_MODEL=gpt-4o-mini
   
   # Local LLM Configuration (when provider=local)  
   LOCAL_LLM_BASE_URL=http://172.28.144.1:1234/v1
   LOCAL_MODEL_NAME=local-model""")
    
    print("\n🚀 After changing .env:")
    print("   1. Restart the Flask backend server")
    print("   2. The React frontend will automatically use the new provider")
    print("   3. Test with the 'Convert to JSON' feature")

if __name__ == "__main__":
    demo_configuration_switching()
    
    print("\n" + "=" * 50)
    print("🎉 Demo complete!")
    print("\nYour AI Resume Optimizer now supports both:")
    print("   • OpenAI API (gpt-4o-mini) - for production use") 
    print("   • Local LLM - for privacy/offline use")
    print("\nSwitch between them by changing AI_PROVIDER in .env!")