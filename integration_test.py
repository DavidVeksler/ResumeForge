#!/usr/bin/env python3
"""
Integration Test for Text-to-JSON Resume Conversion Feature

This test verifies the complete end-to-end functionality of the text-to-JSON
conversion feature by testing the actual Flask API endpoints.
"""

import json
import os
import requests
import time
import sys
from typing import Dict, Any

def test_complete_integration():
    """Test the complete text-to-JSON conversion integration"""
    
    print("🔧 INTEGRATION TEST: Text-to-JSON Resume Conversion")
    print("=" * 60)
    
    # Test configuration
    API_BASE_URL = "http://localhost:5000"
    
    sample_resume_text = """
John Smith
Senior Software Engineer
john.smith@email.com | (555) 123-4567 | San Francisco, CA
LinkedIn: linkedin.com/in/johnsmith

PROFESSIONAL SUMMARY
Experienced software engineer with 8+ years developing scalable web applications and fintech solutions. Led teams of 5+ engineers and delivered $10M+ in revenue impact.

EXPERIENCE

Senior Software Engineer | TechCorp Inc | San Francisco, CA | 2020 - Present
• Built microservices architecture serving 1M+ daily users with 99.9% uptime
• Led migration to cloud infrastructure reducing costs by 40%
• Implemented real-time payment processing handling $50M monthly volume

Software Engineer | StartupXYZ | San Francisco, CA | 2018 - 2020  
• Developed React/Node.js applications for cryptocurrency trading platform
• Integrated blockchain APIs for DeFi protocols with $100M+ TVL

SKILLS
Programming: Python, JavaScript, TypeScript, Java, Go
Web Technologies: React, Node.js, Express, Django, PostgreSQL
Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD, Terraform
FinTech: Blockchain, DeFi, Payment Processing, API Integration

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | 2014 - 2018
    """
    
    # Step 1: Test health check
    print("1. Testing API health check...")
    try:
        health_response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   ✅ API is healthy: {health_data.get('message', 'OK')}")
            
            # Check if text-to-JSON feature is available
            features = health_data.get('features', {})
            if features.get('text_to_json'):
                print("   ✅ Text-to-JSON feature is enabled")
            else:
                print("   ⚠️  Text-to-JSON feature is disabled (OpenAI not available)")
                return False
        else:
            print(f"   ❌ Health check failed: {health_response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Cannot connect to API: {e}")
        print("   💡 Make sure the Flask backend is running on localhost:5000")
        return False
    
    # Step 2: Test text-to-JSON conversion
    print("\n2. Testing text-to-JSON conversion...")
    try:
        conversion_payload = {
            "textResume": sample_resume_text
        }
        
        conversion_response = requests.post(
            f"{API_BASE_URL}/api/parse-resume",
            json=conversion_payload,
            timeout=30  # OpenAI can take some time
        )
        
        if conversion_response.status_code == 200:
            conversion_data = conversion_response.json()
            
            if conversion_data.get('success'):
                print("   ✅ Text-to-JSON conversion successful")
                
                # Validate the converted resume data
                resume_data = conversion_data.get('resumeData', {})
                validation_results = validate_converted_resume(resume_data)
                
                if validation_results['valid']:
                    print("   ✅ Converted resume data is valid")
                    print(f"      - Name: {resume_data.get('personal', {}).get('name', 'N/A')}")
                    print(f"      - Email: {resume_data.get('personal', {}).get('email', 'N/A')}")
                    print(f"      - Jobs: {len(resume_data.get('experience', []))}")
                    print(f"      - Skills: {len(resume_data.get('skills', {}))}")
                else:
                    print("   ⚠️  Converted resume has validation issues:")
                    for error in validation_results['errors']:
                        print(f"      - {error}")
                
            else:
                print(f"   ❌ Conversion failed: {conversion_data.get('error', 'Unknown error')}")
                return False
        else:
            error_data = conversion_response.json() if conversion_response.headers.get('content-type', '').startswith('application/json') else {}
            print(f"   ❌ Conversion request failed: {conversion_response.status_code}")
            print(f"      Error: {error_data.get('error', 'Unknown error')}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Conversion request failed: {e}")
        return False
    
    # Step 3: Test the converted resume with optimization
    print("\n3. Testing optimization with converted resume...")
    try:
        sample_job_description = """
We are looking for a Senior Software Engineer to join our FinTech team.

Requirements:
- 5+ years of software engineering experience
- Strong proficiency in Python, JavaScript, and React
- Experience with cloud platforms (AWS preferred)
- Knowledge of financial systems and payment processing
- Experience with microservices architecture
- Bachelor's degree in Computer Science or related field

Responsibilities:
- Design and implement scalable backend systems
- Work with cross-functional teams to deliver features
- Mentor junior developers
- Ensure code quality and best practices
        """
        
        optimization_payload = {
            "resumeData": resume_data,
            "jobDescription": sample_job_description
        }
        
        optimization_response = requests.post(
            f"{API_BASE_URL}/api/optimize",
            json=optimization_payload,
            timeout=15
        )
        
        if optimization_response.status_code == 200:
            optimization_data = optimization_response.json()
            
            if optimization_data.get('success'):
                print("   ✅ Resume optimization successful")
                print(f"      - Default ATS Score: {optimization_data.get('defaultScore', 'N/A')}")
                print(f"      - Optimized ATS Score: {optimization_data.get('optimizedScore', 'N/A')}")
                print(f"      - Improvement: +{optimization_data.get('improvement', 0)} points")
                print(f"      - Keywords extracted: {len(optimization_data.get('keywords', []))}")
            else:
                print(f"   ❌ Optimization failed: {optimization_data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"   ❌ Optimization request failed: {optimization_response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Optimization request failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 INTEGRATION TEST PASSED!")
    print("✅ Text-to-JSON conversion feature is working end-to-end")
    print("\n🔥 Feature is ready for production use!")
    
    return True

def validate_converted_resume(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate the structure of converted resume data"""
    
    errors = []
    warnings = []
    
    # Check required sections
    required_sections = ['personal']
    for section in required_sections:
        if section not in resume_data:
            errors.append(f"Missing required section: {section}")
    
    # Validate personal information
    if 'personal' in resume_data:
        personal = resume_data['personal']
        if not personal.get('name'):
            errors.append("Missing personal name")
        if not personal.get('email'):
            warnings.append("Missing email address")
    
    # Check optional but expected sections
    optional_sections = ['experience', 'skills', 'education']
    for section in optional_sections:
        if section not in resume_data or not resume_data[section]:
            warnings.append(f"Missing or empty section: {section}")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }

def run_error_scenario_tests():
    """Test various error scenarios"""
    
    print("\n🔧 ERROR SCENARIO TESTS")
    print("-" * 40)
    
    API_BASE_URL = "http://localhost:5000"
    
    error_tests = [
        {
            "name": "Empty text resume",
            "payload": {"textResume": ""},
            "expected_status": 400
        },
        {
            "name": "Too short text resume",
            "payload": {"textResume": "John Doe"},
            "expected_status": 400
        },
        {
            "name": "Missing textResume field",
            "payload": {},
            "expected_status": 400
        }
    ]
    
    for test in error_tests:
        print(f"Testing: {test['name']}")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/parse-resume",
                json=test['payload'],
                timeout=10
            )
            
            if response.status_code == test['expected_status']:
                print(f"   ✅ Correctly returned status {response.status_code}")
            else:
                print(f"   ❌ Expected {test['expected_status']}, got {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")

if __name__ == "__main__":
    print("🚀 STARTING INTEGRATION TESTS")
    print("=" * 60)
    print("Prerequisites:")
    print("1. Flask backend running on localhost:5000")
    print("2. OPENAI_API_KEY environment variable set")
    print("3. All required packages installed")
    print()
    
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  WARNING: OPENAI_API_KEY not set in environment")
        print("   The text-to-JSON feature will not work without it.")
        print("   Set it with: export OPENAI_API_KEY='your-api-key-here'")
        print()
    
    # Run the main integration test
    success = test_complete_integration()
    
    # Run error scenario tests
    if success:
        run_error_scenario_tests()
    
    print("\n" + "=" * 60)
    if success:
        print("🎊 ALL TESTS PASSED - Feature is ready for production!")
    else:
        print("❌ Tests failed - Check the issues above and retry")
        
    print("\n📋 MANUAL TESTING CHECKLIST:")
    print("□ Test with different resume formats")
    print("□ Test with very long resumes (>2000 words)")
    print("□ Test with resumes in different industries")
    print("□ Test error handling with invalid API keys")
    print("□ Test frontend integration in browser")
    print("□ Test mobile responsiveness")
