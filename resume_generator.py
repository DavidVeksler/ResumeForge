#!/usr/bin/env python3
"""
Resume Generator - Converts JSON resume data to optimized HTML templates

Usage:
  python resume_generator.py                           # Generate default resume
  python resume_generator.py [json_file]               # Use custom JSON file
  python resume_generator.py [json_file] [template]    # Specify template type
  python resume_generator.py [json_file] [template] [job_description.txt]  # Customize for job

Examples:
  python resume_generator.py                           # Creates resume_ats_default_YYYYMMDD.html
  python resume_generator.py data.json ats job.txt    # Creates resume_ats_customized_YYYYMMDD.html
"""

import json
import sys
import re
import os
from datetime import datetime
from typing import Dict, List, Any

class ResumeGenerator:
    def __init__(self, resume_data: Dict[str, Any]):
        self.data = resume_data
    
    def generate_ats_template(self) -> str:
        """Generate modern, professional ATS-optimized HTML resume"""
        personal = self.data['personal']
        summary = self.data['summary']
        experience = self.data['experience']
        education = self.data['education']
        skills = self.data['skills']
        projects = self.data.get('projects', [])
        
        # Build sections
        contact_html = self._build_contact_section(personal)
        summary_html = self._build_summary_section(summary)
        experience_html = self._build_experience_section(experience)
        skills_html = self._build_skills_section(skills)
        projects_html = self._build_projects_section(projects)
        education_html = self._build_education_section(education)
        keywords = self._extract_keywords()
        
        # Load external template and CSS files
        template_path = os.path.join(os.path.dirname(__file__), 'template.html')
        css_path = os.path.join(os.path.dirname(__file__), 'template.css')
        
        try:
            with open(template_path, 'r') as f:
                template_content = f.read()
            with open(css_path, 'r') as f:
                css_content = f.read()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Template files not found: {e}")
        
        # Replace placeholders in template
        return template_content.format(
            personal_name=personal['name'],
            css_content=css_content,
            keywords=keywords,
            contact_html=contact_html,
            summary_html=summary_html,
            experience_html=experience_html,
            skills_html=skills_html,
            projects_html=projects_html,
            education_html=education_html
        )

    def _build_contact_section(self, personal: Dict) -> str:
        return f"""
        <header class="header">
            <h1 class="name">{personal['name']}</h1>
            <div class="contact-info">
                <div class="row g-3">
                    <div class="col-md-6">
                        <div><i class="bi bi-envelope-fill"></i>{personal['email']}</div>
                        <div><i class="bi bi-telephone-fill"></i>{personal['phone']}</div>
                    </div>
                    <div class="col-md-6">
                        <div><i class="bi bi-geo-alt-fill"></i>{personal['location']}</div>
                        <div><i class="bi bi-linkedin"></i>{personal.get('linkedin', '')}</div>
                    </div>
                </div>
            </div>
        </header>
        """

    def _build_summary_section(self, summary: Dict) -> str:
        highlights_html = "".join([
            f'<div class="highlight-item"><div class="highlight-label">{bullet.split(":")[0]}</div><div>{bullet.split(":", 1)[1].strip()}</div></div>'
            for bullet in summary['bullets']
        ])
        
        return f"""
        <section class="section">
            <h2 class="section-title">
                <i class="bi bi-person-badge-fill"></i>
                Professional Summary
            </h2>
            <p class="summary-text">{summary['headline']}</p>
            <div class="summary-highlights">
                {highlights_html}
            </div>
        </section>
        """

    def _build_experience_section(self, experience: List[Dict]) -> str:
        jobs_html = ""
        for job in experience:
            achievements_html = "".join([
                f'''<li class="achievement-item">
                    <i class="bi bi-circle-fill achievement-icon"></i>
                    <div class="achievement-text">{achievement['text']}</div>
                </li>''' 
                for achievement in job['achievements']
            ])
            
            description = f'<div style="font-size: 0.85rem; color: var(--secondary-color); font-style: italic;">{job["description"]}</div>' if job.get('description') else ''
            
            jobs_html += f'''
            <div class="job-card">
                <div class="job-header">
                    <h3 class="job-title">{job['title']}</h3>
                    <div class="company-info">
                        <span class="company-name">{job['company']}</span>
                        <span><i class="bi bi-geo-alt"></i>{job['location']}</span>
                        <span><i class="bi bi-calendar3"></i>{job['duration']}</span>
                    </div>
                    {description}
                </div>
                <ul class="achievements">
                    {achievements_html}
                </ul>
            </div>
            '''
        
        return f"""
        <section class="section">
            <h2 class="section-title">
                <i class="bi bi-briefcase-fill"></i>
                Professional Experience
            </h2>
            {jobs_html}
        </section>
        """

    def _build_skills_section(self, skills: Dict) -> str:
        skill_categories = {
            'fintech': ('FinTech & Blockchain', 'bi bi-currency-bitcoin'),
            'programming_languages': ('Programming Languages', 'bi bi-code-slash'),
            'web_technologies': ('Frameworks & Cloud', 'bi bi-layers'),
            'leadership': ('Leadership & Process', 'bi bi-people-fill')
        }
        
        categories_html = ""
        
        for skill_key, (title, icon) in skill_categories.items():
            if skill_key in skills:
                skill_data = skills[skill_key]
                tags = []
                
                if isinstance(skill_data, dict):
                    for category, skill_list in skill_data.items():
                        tags.extend(skill_list)
                elif isinstance(skill_data, list):
                    tags.extend(skill_data)
                
                # Add some key FinTech skills if this is fintech category
                if skill_key == 'fintech':
                    # Add blockchain skills if available
                    if 'blockchain' in skills:
                        for category, skill_list in skills['blockchain'].items():
                            tags.extend(skill_list[:3])  # Only take first 3 to avoid overcrowding
                
                tags_html = "".join([f'<span class="skill-tag">{tag}</span>' for tag in tags[:10]])  # Limit to 10 tags per category
                
                categories_html += f'''
                <div class="skill-category">
                    <h3 class="skill-category-title">
                        <i class="{icon}"></i>
                        {title}
                    </h3>
                    <div class="skill-tags">
                        {tags_html}
                    </div>
                </div>
                '''
        
        return f"""
        <section class="section">
            <h2 class="section-title">
                <i class="bi bi-gear-fill"></i>
                Technical Skills
            </h2>
            <div class="skills-grid">
                {categories_html}
            </div>
        </section>
        """

    def _build_projects_section(self, projects: List[Dict]) -> str:
        if not projects:
            return ""
        
        projects_html = ""
        for project in projects:
            achievements_html = "".join([
                f'''<li class="project-achievement">
                    <i class="bi bi-check-circle-fill text-success"></i>
                    <span>{achievement}</span>
                </li>'''
                for achievement in project['achievements']
            ])
            
            projects_html += f'''
            <div class="project-card">
                <h3 class="project-title">{project['name']}</h3>
                <p class="project-description">{project['description']}</p>
                <ul class="project-achievements">
                    {achievements_html}
                </ul>
            </div>
            '''
        
        return f"""
        <section class="section">
            <h2 class="section-title">
                <i class="bi bi-star-fill"></i>
                Key Projects
            </h2>
            {projects_html}
        </section>
        """

    def _build_education_section(self, education: List[Dict]) -> str:
        education_html = ""
        for edu in education:
            description = ""
            if edu.get('description'):
                description = f'''<div style="font-size: 0.9rem; color: var(--secondary-color); margin-top: 0.5rem;">
                    {edu['description']}
                </div>'''
            
            education_html += f'''
            <div class="education-item">
                <div class="degree">{edu['degree']}</div>
                <div class="school-info">
                    <span><i class="bi bi-building"></i>{edu['school']}</span>
                    <span><i class="bi bi-calendar3"></i>{edu['duration']}</span>
                </div>
                {description}
            </div>
            '''
        
        return f"""
        <section class="section">
            <h2 class="section-title">
                <i class="bi bi-mortarboard-fill"></i>
                Education
            </h2>
            {education_html}
        </section>
        """

    def _extract_keywords(self) -> str:
        """Extract keywords for ATS optimization with enhanced coverage"""
        keywords = []
        
        # Add keywords from the keywords section with priority weighting
        if 'keywords' in self.data:
            for category, keyword_list in self.data['keywords'].items():
                keywords.extend(keyword_list)
                # Duplicate high-priority keywords for better ATS recognition
                if category in ['fintech_primary', 'technical_primary']:
                    keywords.extend(keyword_list)
        
        # Add skills as keywords with enhanced extraction
        for skill_category_name, skill_category in self.data['skills'].items():
            if isinstance(skill_category, dict):
                for skill_level, skill_list in skill_category.items():
                    keywords.extend(skill_list)
                    # Add variations for common technologies
                    for skill in skill_list:
                        # Add common variations and synonyms
                        variations = self._get_skill_variations(skill)
                        keywords.extend(variations)
            elif isinstance(skill_category, list):
                keywords.extend(skill_category)
                for skill in skill_category:
                    variations = self._get_skill_variations(skill)
                    keywords.extend(variations)
        
        # Add achievement keywords
        for job in self.data['experience']:
            for achievement in job['achievements']:
                keywords.extend(achievement.get('keywords', []))
        
        # Add job titles and company names as keywords
        for job in self.data['experience']:
            # Extract meaningful words from job titles
            title_words = job['title'].split()
            keywords.extend([word for word in title_words if len(word) > 2])
            
            # Add company names for brand recognition
            company_words = job['company'].split()
            keywords.extend([word for word in company_words if len(word) > 2])
        
        # Add education keywords
        for edu in self.data['education']:
            degree_words = edu['degree'].split()
            keywords.extend([word for word in degree_words if len(word) > 2])
        
        # Add project keywords
        if 'projects' in self.data:
            for project in self.data['projects']:
                keywords.extend(project.get('keywords', []))
                # Extract from project descriptions
                desc_words = project['description'].split()
                keywords.extend([word for word in desc_words if len(word) > 3])
        
        # Remove duplicates while preserving important repetitions
        keyword_counts = {}
        for keyword in keywords:
            if keyword.lower() not in keyword_counts:
                keyword_counts[keyword.lower()] = 0
            keyword_counts[keyword.lower()] += 1
        
        # Build final keyword string with strategic repetition
        final_keywords = []
        for keyword, count in keyword_counts.items():
            # Repeat important keywords for better ATS recognition
            repetitions = min(count, 3) if self._is_high_priority_keyword(keyword) else 1
            final_keywords.extend([keyword] * repetitions)
        
        return " ".join(final_keywords)
    
    def _get_skill_variations(self, skill: str) -> List[str]:
        """Get common variations and synonyms for skills"""
        variations = []
        skill_lower = skill.lower()
        
        # Technology variations
        tech_variations = {
            'javascript': ['js', 'ecmascript', 'node.js', 'nodejs'],
            'typescript': ['ts'],
            'c#': ['csharp', 'c-sharp', 'dotnet', '.net'],
            '.net core': ['dotnet core', 'asp.net core', 'aspnet core'],
            'postgresql': ['postgres', 'psql'],
            'react': ['reactjs', 'react.js'],
            'aws': ['amazon web services', 'amazon cloud'],
            'ci/cd': ['continuous integration', 'continuous deployment', 'cicd'],
            'api': ['rest api', 'restful api', 'web api'],
            'blockchain': ['distributed ledger', 'crypto', 'web3'],
            'defi': ['decentralized finance', 'decentralised finance'],
            'fintech': ['financial technology', 'fin-tech']
        }
        
        if skill_lower in tech_variations:
            variations.extend(tech_variations[skill_lower])
        
        return variations
    
    def _is_high_priority_keyword(self, keyword: str) -> bool:
        """Determine if a keyword should be repeated for better ATS recognition"""
        high_priority_terms = {
            'fintech', 'blockchain', 'defi', 'python', 'javascript', 'react', 
            'aws', 'leadership', 'management', 'api', 'postgresql', 'docker',
            'microservices', 'payments', 'compliance', 'security', 'agile',
            'scrum', 'ethereum', 'trading', 'yield', 'tvl', 'custody'
        }
        return keyword.lower() in high_priority_terms

    def customize_for_role(self, job_description: str, role_keywords: List[str]) -> Dict[str, Any]:
        """Customize resume data for specific role with enhanced scoring"""
        customized_data = self.data.copy()
        
        # Create keyword importance weights
        keyword_weights = self._calculate_keyword_weights(role_keywords, job_description)
        
        # Boost relevant experience based on role keywords with weighted scoring
        for job in customized_data['experience']:
            for achievement in job['achievements']:
                # Calculate weighted relevance score
                achievement_keywords = achievement.get('keywords', [])
                relevance_score = 0
                
                # Direct keyword matches with weights
                for kw in achievement_keywords:
                    if kw.lower() in [rk.lower() for rk in role_keywords]:
                        weight = keyword_weights.get(kw.lower(), 1)
                        relevance_score += weight
                
                # Partial matches for compound keywords
                achievement_text = achievement['text'].lower()
                for role_kw in role_keywords:
                    if role_kw.lower() in achievement_text:
                        weight = keyword_weights.get(role_kw.lower(), 0.5)
                        relevance_score += weight * 0.7  # Partial match weight
                
                # Boost score for quantified achievements
                if achievement.get('metrics'):
                    relevance_score += 1
                
                achievement['relevance_score'] = relevance_score
        
        # Sort achievements by relevance with minimum score threshold
        for job in customized_data['experience']:
            # Sort achievements by relevance score
            job['achievements'].sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            # Ensure at least one high-scoring achievement per job is prioritized
            if job['achievements'] and job['achievements'][0].get('relevance_score', 0) < 1:
                # If no high-scoring achievements, boost the first one slightly
                job['achievements'][0]['relevance_score'] = 1
        
        # Enhance keywords section with role-specific terms
        if 'keywords' not in customized_data:
            customized_data['keywords'] = {}
        
        # Add extracted role keywords to enhance ATS matching
        customized_data['keywords']['role_specific'] = role_keywords[:20]  # Top 20 role keywords
        
        return customized_data
    
    def _calculate_keyword_weights(self, role_keywords: List[str], job_description: str) -> Dict[str, float]:
        """Calculate importance weights for keywords based on frequency and context"""
        keyword_weights = {}
        job_lower = job_description.lower()
        
        for keyword in role_keywords:
            kw_lower = keyword.lower()
            weight = 1.0
            
            # Count occurrences in job description
            occurrences = job_lower.count(kw_lower)
            if occurrences > 1:
                weight += min(occurrences * 0.2, 1.0)  # Max bonus of 1.0
            
            # Higher weight for keywords in requirements sections
            requirement_contexts = [
                'required', 'must have', 'essential', 'mandatory',
                'experience with', 'proficient in', 'expertise in'
            ]
            
            for context in requirement_contexts:
                if context in job_lower and kw_lower in job_lower[job_lower.find(context):job_lower.find(context) + 200]:
                    weight += 0.5
                    break
            
            # Higher weight for technical skills and leadership terms
            high_value_terms = {
                'fintech', 'blockchain', 'defi', 'leadership', 'management',
                'python', 'javascript', 'react', 'aws', 'api', 'payments'
            }
            
            if kw_lower in high_value_terms:
                weight += 0.3
            
            keyword_weights[kw_lower] = weight
        
        return keyword_weights

def extract_keywords_from_job_description(job_description: str) -> List[str]:
    """Extract relevant keywords from job description for resume customization"""
    
    # Enhanced FinTech and technical keywords with higher specificity
    priority_patterns = [
        # FinTech specific - High priority
        r'\b(fintech|financial technology|payments?|trading|defi|blockchain|cryptocurrency|crypto)\b',
        r'\b(compliance|kyc|aml|regulatory|custody|oracles?|yield)\b',
        r'\b(tvl|wrapped tokens?|proof of reserve|evm|layer 2|smart contracts?)\b',
        r'\b(ethereum|polygon|bitcoin|web3|metamask|chainlink)\b',
        
        # Technical leadership - High priority  
        r'\b(engineering manager|tech lead|architect|cto|director)\b',
        r'\b(team lead|leadership|management|mentoring|scaling)\b',
        
        # Programming languages - Enhanced patterns
        r'\b(python|javascript|typescript|react|node\.?js|django|flask)\b',
        r'\b(c#|\.net|asp\.net|java|spring|golang|rust|solidity)\b',
        
        # Infrastructure & DevOps - Enhanced
        r'\b(aws|azure|gcp|docker|kubernetes|microservices)\b',
        r'\b(api|rest|restful|graphql|grpc|websocket)\b',
        r'\b(ci/cd|devops|jenkins|github actions|gitlab)\b',
        
        # Databases & Caching - More specific
        r'\b(postgresql|mysql|mongodb|redis|elasticsearch|influxdb)\b',
        r'\b(sql server|oracle|cassandra|dynamodb|snowflake)\b',
        
        # Security & Compliance - Enhanced
        r'\b(security|oauth|jwt|encryption|authentication|authorization)\b',
        r'\b(pci dss|sox|gdpr|ccpa|hipaa|soc 2)\b',
        
        # Methodologies - Enhanced
        r'\b(agile|scrum|kanban|lean|safe|xp|tdd|bdd)\b',
        
        # Business impact & Metrics
        r'\b(revenue|cost reduction|efficiency|performance|scale|growth)\b',
        r'\b(million|billion|percent|\$\d+[mk]?\b|\d+\+?\s*years?)\b',
        r'\b(uptime|sla|latency|throughput|scalability)\b'
    ]
    
    keywords = []
    text_lower = job_description.lower()
    
    # Extract priority keywords with scoring
    keyword_scores = {}
    for i, pattern in enumerate(priority_patterns):
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        for match in matches:
            if match not in keyword_scores:
                keyword_scores[match] = 0
            # Higher score for patterns that appear earlier (more important)
            keyword_scores[match] += (len(priority_patterns) - i)
    
    # Extract technical terms and acronyms with better filtering
    tech_terms = re.findall(r'\b[A-Z]{2,6}\b', job_description)
    for term in tech_terms:
        term_lower = term.lower()
        # Filter out common non-technical acronyms
        if term_lower not in ['the', 'and', 'for', 'you', 'are', 'our', 'inc', 'llc', 'corp', 'ltd']:
            if term_lower not in keyword_scores:
                keyword_scores[term_lower] = 0
            keyword_scores[term_lower] += 1
    
    # Enhanced requirement phrase extraction
    requirement_patterns = [
        r'(?:required|must have|experience with|proficient in|knowledge of|familiar with|expertise in)\s+([^.!?\n]+)',
        r'(?:skills in|background in|strong|solid|deep understanding of|experience in)\s+([^.!?\n]+)',
        r'(?:proficiency|proficient|expert|advanced|intermediate) (?:in|with|knowledge of)\s+([^.!?\n]+)'
    ]
    
    for pattern in requirement_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        for match in matches:
            # Enhanced term extraction with compound terms
            terms = re.findall(r'\b[a-z]+(?:[.\-/][a-z]+)*\b', match)
            for term in terms:
                if len(term) > 2:
                    if term not in keyword_scores:
                        keyword_scores[term] = 0
                    keyword_scores[term] += 3  # Higher weight for requirement phrases
    
    # Extract technology stack sections
    tech_stack_patterns = [
        r'(?:tech stack|technology stack|technologies|tools|frameworks?):\s*([^.!?\n]+)',
        r'(?:using|working with|built with):\s*([^.!?\n]+)'
    ]
    
    for pattern in tech_stack_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        for match in matches:
            terms = re.findall(r'\b[a-z]+(?:[.\-/][a-z]+)*\b', match)
            for term in terms:
                if len(term) > 2:
                    if term not in keyword_scores:
                        keyword_scores[term] = 0
                    keyword_scores[term] += 2  # Medium weight for tech stack mentions
    
    # Remove duplicates and common words with enhanced stop word list
    stop_words = {
        'the', 'and', 'with', 'for', 'you', 'will', 'are', 'have', 'our', 'this', 'that', 'from', 
        'they', 'been', 'would', 'there', 'their', 'what', 'said', 'each', 'which', 'were', 'than', 
        'but', 'not', 'all', 'any', 'can', 'had', 'was', 'one', 'your', 'how', 'use', 'word', 'may', 
        'she', 'oil', 'its', 'now', 'him', 'could', 'did', 'get', 'has', 'his', 'her', 'let', 'put', 
        'too', 'also', 'back', 'call', 'came', 'come', 'just', 'like', 'long', 'look', 'made', 'make', 
        'many', 'over', 'such', 'take', 'very', 'well', 'work', 'who', 'where', 'when', 'why', 'some',
        'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'among',
        'able', 'team', 'role', 'position', 'company', 'business', 'opportunity', 'candidate'
    }
    
    # Sort keywords by score and filter
    filtered_keywords = [
        kw for kw, score in keyword_scores.items() 
        if kw.lower() not in stop_words and len(kw) > 2 and score > 0
    ]
    
    # Sort by score (descending) and take top keywords
    sorted_keywords = sorted(filtered_keywords, key=lambda x: keyword_scores[x], reverse=True)
    
    return sorted_keywords[:60]  # Increased to 60 keywords for better coverage

def main():
    # Default parameters for no-argument execution
    json_file = "david_resume_json.json"
    template_type = "ats"
    job_description = None
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    if len(sys.argv) > 2:
        template_type = sys.argv[2]
    if len(sys.argv) > 3:
        # Job description file path for customization
        job_description_file = sys.argv[3]
        try:
            with open(job_description_file, 'r') as f:
                job_description = f.read().strip()
        except FileNotFoundError:
            print(f"Job description file not found: {job_description_file}")
            sys.exit(1)
    
    try:
        with open(json_file, 'r') as f:
            resume_data = json.load(f)
        
        generator = ResumeGenerator(resume_data)
        
        # Customize for job description if provided
        if job_description:
            role_keywords = extract_keywords_from_job_description(job_description)
            customized_data = generator.customize_for_role(job_description, role_keywords)
            generator = ResumeGenerator(customized_data)
            print(f"Resume customized for job posting with {len(role_keywords)} key terms")
        
        if template_type == "ats":
            html_output = generator.generate_ats_template()
        else:
            print(f"Unknown template type: {template_type}")
            sys.exit(1)
        
        # Write output with descriptive filename
        suffix = "_customized" if job_description else "_default"
        output_file = f"resume_{template_type}{suffix}_{datetime.now().strftime('%Y%m%d')}.html"
        with open(output_file, 'w') as f:
            f.write(html_output)
        
        print(f"Resume generated: {output_file}")
        
    except FileNotFoundError:
        print(f"Resume data file not found: {json_file}")
        print("Make sure 'david_resume_json.json' exists in the current directory for default execution")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
