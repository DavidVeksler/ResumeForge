#!/usr/bin/env python3
"""
Basic integration test for Resume Optimizer core functionality
"""

import subprocess
import time
import requests
from pathlib import Path
import os
import sys


def get_python_cmd():
    """Get the correct Python command for the current platform"""
    return 'python' if sys.platform == 'win32' else 'python3'

def test_core_functionality():
    """Test core resume generation without external dependencies"""
    print("🧪 Testing core resume generation...")
    
    # Test basic resume generation
    result = subprocess.run([get_python_cmd(), 'resume_generator.py'],
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Basic resume generation failed: {result.stderr}")
        return False
    
    # Check if file was created
    resume_files = list(Path('.').glob('resume_ats_default_*.html'))
    if not resume_files:
        print("❌ Resume file not generated")
        return False
    
    # Check file size
    latest_file = max(resume_files, key=os.path.getmtime)
    file_size = latest_file.stat().st_size
    if file_size < 10000:  # Less than 10KB seems too small
        print(f"⚠️  Resume file seems small ({file_size} bytes)")
    else:
        print(f"✅ Resume generated successfully ({file_size} bytes)")
    
    return True

def test_backend_startup():
    """Test backend server functionality"""
    print("🧪 Testing backend server...")
    
    # Test health endpoint
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend health check passed: {data.get('message', 'OK')}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_job_customization():
    """Test job-specific resume customization"""
    print("🧪 Testing job customization...")
    
    # Create a test job description
    test_job = """
    We are looking for a Senior Software Engineer with experience in:
    - Python and Django
    - Financial technology (FinTech) 
    - API development
    - Database management
    - Agile methodologies
    """
    
    with open('test_job.txt', 'w') as f:
        f.write(test_job)
    
    # Test customized resume generation
    result = subprocess.run([get_python_cmd(), 'resume_generator.py', 'david_resume_json.json', 'ats', 'test_job.txt'], 
                          capture_output=True, text=True)
    
    # Clean up
    if os.path.exists('test_job.txt'):
        os.remove('test_job.txt')
    
    if result.returncode != 0:
        print(f"❌ Job customization failed: {result.stderr}")
        return False
    
    # Check if customized file was created
    customized_files = list(Path('.').glob('resume_ats_customized_*.html'))
    if not customized_files:
        print("❌ Customized resume file not generated")
        return False
    
    print("✅ Job customization works")
    return True

def test_setup_scripts():
    """Test setup and startup scripts"""
    print("🧪 Testing setup scripts...")
    
    scripts_to_test = ['setup_dev.sh', 'install_dependencies.sh']
    results = {}
    
    for script in scripts_to_test:
        if os.path.exists(script):
            print(f"  Checking {script}...")
            results[script] = {
                'exists': True,
                'executable': os.access(script, os.X_OK),
                'size': os.path.getsize(script)
            }
        else:
            results[script] = {'exists': False}
    
    all_good = True
    for script, info in results.items():
        if info.get('exists', False):
            if info.get('executable', False) and info.get('size', 0) > 0:
                print(f"  ✅ {script} exists and is executable")
            else:
                print(f"  ⚠️  {script} has issues")
                all_good = False
        else:
            print(f"  ❌ {script} missing")
            all_good = False
    
    return all_good

def test_file_structure():
    """Test that required files exist"""
    print("🧪 Testing file structure...")
    
    required_files = [
        'david_resume_json.json',
        'resume_generator.py',
        'start_backend.sh',
        'start_frontend.sh',
        'package.json',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Run comprehensive integration tests"""
    print("🚀 BASIC INTEGRATION TEST")
    print("=" * 50)
    
    test_results = {}
    
    # Run all tests
    test_results['file_structure'] = test_file_structure()
    test_results['core_functionality'] = test_core_functionality()
    test_results['backend_startup'] = test_backend_startup()
    test_results['job_customization'] = test_job_customization()
    test_results['setup_scripts'] = test_setup_scripts()
    
    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! Core system is ready.")
        return True
    else:
        print("⚠️  Some issues found. Check individual test results.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
