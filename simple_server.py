#!/usr/bin/env python3
"""
Simple HTTP server for testing Resume Optimizer without dependencies
"""

import http.server
import socketserver
import json
import os
from urllib.parse import urlparse, parse_qs
import re
from datetime import datetime

PORT = 5000

class ResumeOptimizerHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'healthy', 'message': 'Simple server running without dependencies'}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/api/sample-resume':
            self.send_sample_resume()
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/optimize':
            self.handle_optimize()
        elif self.path == '/api/validate-resume':
            self.handle_validate()
        elif self.path == '/api/parse-resume':
            self.handle_parse_resume()
        else:
            self.send_error(404)
    
    def handle_optimize(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Simple optimization simulation
            resume_data = data.get('resume_data', {})
            job_description = data.get('job_description', '')
            
            # Extract keywords from job description
            keywords = self.extract_keywords(job_description)
            
            # Create optimized HTML
            optimized_html = self.generate_optimized_html(resume_data, keywords)
            
            response = {
                'success': True,
                'optimized_html': optimized_html,
                'default_html': self.generate_default_html(resume_data),
                'ats_score': 85,
                'keywords_found': keywords[:10],
                'optimization_summary': f'Added {len(keywords)} relevant keywords'
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def handle_validate(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            resume_data = data.get('resume_data', {})
            
            # Simple validation
            required_sections = ['personal', 'experience', 'skills']
            missing_sections = [section for section in required_sections if section not in resume_data]
            
            response = {
                'valid': len(missing_sections) == 0,
                'missing_sections': missing_sections,
                'message': 'Valid resume' if len(missing_sections) == 0 else f'Missing sections: {", ".join(missing_sections)}'
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def handle_parse_resume(self):
        # Mock response for text-to-JSON conversion
        response = {
            'success': False,
            'message': 'AI parsing requires OpenAI API key. Use JSON upload instead.',
            'resume_data': None
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def send_sample_resume(self):
        try:
            # Load sample resume if it exists
            if os.path.exists('david_resume_json.json'):
                with open('david_resume_json.json', 'r') as f:
                    sample_data = f.read()
            else:
                sample_data = json.dumps({
                    "personal": {
                        "name": "Sample User",
                        "email": "sample@example.com",
                        "phone": "555-0123"
                    },
                    "experience": [],
                    "skills": {},
                    "education": []
                })
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Content-Disposition', 'attachment; filename="sample_resume.json"')
            self.end_headers()
            self.wfile.write(sample_data.encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def extract_keywords(self, job_description):
        # Simple keyword extraction
        tech_keywords = ['python', 'javascript', 'react', 'node', 'sql', 'aws', 'docker', 'kubernetes', 'api', 'rest', 'agile', 'scrum']
        found_keywords = []
        
        job_lower = job_description.lower()
        for keyword in tech_keywords:
            if keyword in job_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def generate_default_html(self, resume_data):
        return f"""
        <html>
        <head><title>Resume - {resume_data.get('personal', {}).get('name', 'Unknown')}</title></head>
        <body>
        <h1>{resume_data.get('personal', {}).get('name', 'Unknown')}</h1>
        <p>Email: {resume_data.get('personal', {}).get('email', 'N/A')}</p>
        <p>Phone: {resume_data.get('personal', {}).get('phone', 'N/A')}</p>
        <h2>Experience</h2>
        {self.format_experience(resume_data.get('experience', []))}
        <h2>Skills</h2>
        {self.format_skills(resume_data.get('skills', {}))}
        </body>
        </html>
        """
    
    def generate_optimized_html(self, resume_data, keywords):
        html = self.generate_default_html(resume_data)
        # Add hidden keywords for ATS
        keyword_div = f'<div style="display:none">{" ".join(keywords)}</div>'
        return html.replace('</body>', f'{keyword_div}</body>')
    
    def format_experience(self, experience):
        if not experience:
            return '<p>No experience listed</p>'
        
        html = '<ul>'
        for job in experience:
            html += f'<li><strong>{job.get("title", "Unknown")}</strong> at {job.get("company", "Unknown")} ({job.get("duration", "Unknown")})</li>'
        html += '</ul>'
        return html
    
    def format_skills(self, skills):
        if not skills:
            return '<p>No skills listed</p>'
        
        html = '<ul>'
        for category, skill_list in skills.items():
            if isinstance(skill_list, dict):
                for level, items in skill_list.items():
                    html += f'<li><strong>{category} ({level}):</strong> {", ".join(items) if isinstance(items, list) else items}</li>'
            else:
                html += f'<li><strong>{category}:</strong> {", ".join(skill_list) if isinstance(skill_list, list) else skill_list}</li>'
        html += '</ul>'
        return html

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), ResumeOptimizerHandler) as httpd:
        print(f"🌐 Simple Resume Optimizer server running on http://localhost:{PORT}")
        print("🔧 This is a dependency-free version for testing")
        print("📋 Available endpoints:")
        print("   GET  /api/health")
        print("   POST /api/optimize")
        print("   POST /api/validate-resume")
        print("   GET  /api/sample-resume")
        print("   POST /api/parse-resume (mock)")
        print("")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")