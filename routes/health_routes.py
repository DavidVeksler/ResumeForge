"""
Health Check Routes - System health and status monitoring
"""

import datetime
import subprocess
import platform
import os
from typing import Dict, Any

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from services.ai_service import OPENAI_AVAILABLE, AIService


def get_health_status() -> Dict[str, Any]:
    """
    Get comprehensive system health status

    Returns:
        Dictionary with health check information
    """
    health_data = {
        'status': 'healthy',
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'version': '1.0.0',
        'message': 'Resume Optimizer API is running'
    }

    # Add all health check sections
    health_data['system'] = _get_system_info()
    health_data['dependencies'] = _check_dependencies()
    health_data['files'] = _check_critical_files()
    health_data['environment'] = _get_environment_config()
    health_data['ai_provider'] = _check_ai_provider()
    health_data['features'] = _get_feature_availability(health_data)

    # Overall health assessment
    health_data['issues'] = _assess_health_issues(health_data)

    # Update overall status based on issues
    if health_data['issues']['critical']:
        health_data['status'] = 'unhealthy'
        health_data['message'] = 'Critical issues detected'
    elif health_data['issues']['warnings']:
        health_data['status'] = 'warning'
        health_data['message'] = 'Service operational with warnings'

    return health_data


def _get_system_info() -> Dict[str, Any]:
    """Get system information"""
    system_info = {
        'platform': platform.platform(),
        'python_version': platform.python_version()
    }

    if PSUTIL_AVAILABLE:
        try:
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            system_info.update({
                'memory': {
                    'total_gb': round(memory.total / (1024**3), 2),
                    'available_gb': round(memory.available / (1024**3), 2),
                    'used_percent': memory.percent
                },
                'disk': {
                    'total_gb': round(disk.total / (1024**3), 2),
                    'free_gb': round(disk.free / (1024**3), 2),
                    'used_percent': round((disk.used / disk.total) * 100, 1)
                }
            })
        except Exception as e:
            system_info['psutil_error'] = f'Could not retrieve detailed system info: {str(e)}'
    else:
        system_info['note'] = 'Install psutil for detailed memory and disk usage information'

    return system_info


def _check_dependencies() -> Dict[str, bool]:
    """Check availability of required dependencies"""
    dependencies = {
        'flask': True,  # Already imported if we're here
        'openai': OPENAI_AVAILABLE,
        'pdfkit': _check_pdfkit_available(),
        'wkhtmltopdf': _check_wkhtmltopdf(),
        'psutil': PSUTIL_AVAILABLE,
        'dotenv': _check_dotenv_available()
    }

    return dependencies


def _check_pdfkit_available() -> bool:
    """Check if pdfkit is available"""
    try:
        import pdfkit
        return True
    except ImportError:
        return False


def _check_wkhtmltopdf() -> bool:
    """Check if wkhtmltopdf binary is available"""
    paths = ['wkhtmltopdf', '/usr/bin/wkhtmltopdf', '/usr/local/bin/wkhtmltopdf']

    for path in paths:
        try:
            subprocess.run(
                [path, '--version'],
                capture_output=True,
                check=True,
                timeout=5
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            continue

    return False


def _check_dotenv_available() -> bool:
    """Check if python-dotenv is available"""
    try:
        import dotenv
        return True
    except ImportError:
        return False


def _check_critical_files() -> Dict[str, Dict[str, Any]]:
    """Check existence and accessibility of critical files"""
    critical_files = [
        'david_resume_json.json',
        'resume_generator.py',
        '.env'
    ]

    file_checks = {}

    for file_path in critical_files:
        try:
            if os.path.exists(file_path):
                stat_info = os.stat(file_path)
                file_checks[file_path] = {
                    'exists': True,
                    'readable': os.access(file_path, os.R_OK),
                    'size_bytes': stat_info.st_size,
                    'last_modified': datetime.datetime.fromtimestamp(
                        stat_info.st_mtime
                    ).isoformat()
                }
            else:
                file_checks[file_path] = {'exists': False}
        except Exception as e:
            file_checks[file_path] = {'error': str(e)}

    return file_checks


def _get_environment_config() -> Dict[str, Any]:
    """Get environment configuration"""
    return {
        'AI_PROVIDER': os.getenv('AI_PROVIDER', 'local'),
        'OPENAI_MODEL': os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
        'OPENAI_API_KEY_SET': bool(os.getenv('OPENAI_API_KEY')),
        'LOCAL_LLM_BASE_URL': os.getenv('LOCAL_LLM_BASE_URL', 'http://172.28.144.1:1234/v1'),
        'LOCAL_MODEL_NAME': os.getenv('LOCAL_MODEL_NAME', 'local-model'),
        'FLASK_ENV': os.getenv('FLASK_ENV', 'production')
    }


def _check_ai_provider() -> Dict[str, Any]:
    """Check AI provider configuration and connectivity"""
    ai_provider = os.getenv('AI_PROVIDER', 'local').lower()
    ai_status = {
        'provider': ai_provider,
        'configured': False,
        'connectivity_test': False
    }

    if not OPENAI_AVAILABLE:
        ai_status['error'] = 'OpenAI package not available'
        return ai_status

    try:
        ai_service = AIService()
        test_result = ai_service.test_connectivity()

        ai_status.update({
            'configured': True,
            'connectivity_test': test_result['success'],
            'model': test_result['model']
        })

        if not test_result['success']:
            ai_status['connectivity_error'] = test_result.get('error', 'Unknown error')
        else:
            ai_status['last_test'] = datetime.datetime.utcnow().isoformat() + 'Z'

    except Exception as e:
        ai_status['error'] = str(e)

    return ai_status


def _get_feature_availability(health_data: Dict[str, Any]) -> Dict[str, bool]:
    """Determine which features are available"""
    dependencies = health_data.get('dependencies', {})
    ai_status = health_data.get('ai_provider', {})
    files = health_data.get('files', {})
    text_to_json_available = OPENAI_AVAILABLE and ai_status.get('configured', False)

    return {
        'resume_optimization': True,
        'pdf_export': dependencies.get('pdfkit', False) and dependencies.get('wkhtmltopdf', False),
        'text_to_json_parsing': text_to_json_available,
        'text_to_json': text_to_json_available,
        'resume_validation': True,
        'sample_template': files.get('david_resume_json.json', {}).get('exists', False),
        'keyword_extraction': True,
        'ats_scoring': True
    }


def _assess_health_issues(health_data: Dict[str, Any]) -> Dict[str, list]:
    """Assess health issues and warnings"""
    critical_issues = []
    warnings = []

    dependencies = health_data.get('dependencies', {})
    ai_status = health_data.get('ai_provider', {})
    files = health_data.get('files', {})

    # Check for critical issues
    if not files.get('resume_generator.py', {}).get('exists'):
        critical_issues.append('Core resume generator module missing')

    if not ai_status.get('configured'):
        critical_issues.append('AI provider not properly configured')

    # Check for warnings
    if not dependencies.get('wkhtmltopdf'):
        warnings.append('wkhtmltopdf not available - PDF export disabled')

    if not PSUTIL_AVAILABLE:
        warnings.append('psutil not available - system monitoring limited')

    if not ai_status.get('connectivity_test'):
        provider = ai_status.get('provider', 'unknown')
        warnings.append(f'{provider.capitalize()} provider connectivity could not be verified')

    return {
        'critical': critical_issues,
        'warnings': warnings
    }
