"""
Template Renderer - Generate HTML from resume data
"""

import os
from typing import Dict, Any


class TemplateRenderer:
    """Render resume data to HTML using templates"""

    TEMPLATE_DIR = os.path.dirname(os.path.dirname(__file__))

    def __init__(self, resume_data: Dict[str, Any]):
        """
        Initialize template renderer

        Args:
            resume_data: Structured resume data
        """
        self.data = resume_data

    def render(self) -> str:
        """
        Render resume to HTML

        Returns:
            Complete HTML document
        """
        template_content = self._load_template()
        css_content = self._load_css()

        return template_content.format(
            personal_name=self.data['personal']['name'],
            css_content=css_content,
            keywords=self._build_keywords(),
            contact_html=self._build_contact_section(),
            summary_html=self._build_summary_section(),
            experience_html=self._build_experience_section(),
            skills_html=self._build_skills_section(),
            projects_html=self._build_projects_section(),
            education_html=self._build_education_section()
        )

    def _load_template(self) -> str:
        """Load HTML template"""
        template_path = os.path.join(self.TEMPLATE_DIR, 'template.html')
        try:
            with open(template_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Template file not found at {template_path}. "
                "Ensure template.html exists in the project root directory."
            )
        except IOError as e:
            raise IOError(f"Failed to read template file: {e}")

    def _load_css(self) -> str:
        """Load CSS content"""
        css_path = os.path.join(self.TEMPLATE_DIR, 'template.css')
        try:
            with open(css_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"CSS file not found at {css_path}. "
                "Ensure template.css exists in the project root directory."
            )
        except IOError as e:
            raise IOError(f"Failed to read CSS file: {e}")

    def _build_keywords(self) -> str:
        """Build ATS keywords string"""
        from .skills_processor import SkillsProcessor

        keywords = []

        # Add keywords from the keywords section
        if 'keywords' in self.data:
            for category, keyword_list in self.data['keywords'].items():
                keywords.extend(keyword_list)
                # Duplicate high-priority keywords
                if category in ['fintech_primary', 'technical_primary']:
                    keywords.extend(keyword_list)

        # Add skills as keywords
        keywords.extend(
            SkillsProcessor.extract_skill_keywords(self.data.get('skills', {}))
        )

        # Add achievement keywords
        for job in self.data.get('experience', []):
            for achievement in job.get('achievements', []):
                keywords.extend(achievement.get('keywords', []))

        # Add job titles and company names
        for job in self.data.get('experience', []):
            title_words = [w for w in job['title'].split() if len(w) > 2]
            company_words = [w for w in job['company'].split() if len(w) > 2]
            keywords.extend(title_words + company_words)

        # Add education keywords
        for edu in self.data.get('education', []):
            degree_words = [w for w in edu['degree'].split() if len(w) > 2]
            keywords.extend(degree_words)

        # Add project keywords
        for project in self.data.get('projects', []):
            keywords.extend(project.get('keywords', []))

        # Build final keyword string with strategic repetition
        keyword_counts = {}
        for keyword in keywords:
            kw_lower = keyword.lower()
            keyword_counts[kw_lower] = keyword_counts.get(kw_lower, 0) + 1

        final_keywords = []
        for keyword, count in keyword_counts.items():
            repetitions = min(count, 3) if SkillsProcessor.is_high_priority(keyword) else 1
            final_keywords.extend([keyword] * repetitions)

        return " ".join(final_keywords)

    def _build_contact_section(self) -> str:
        """Build contact section HTML"""
        personal = self.data['personal']
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

    def _build_summary_section(self) -> str:
        """Build professional summary section"""
        summary = self.data['summary']

        highlights_html = "".join([
            f'<div class="highlight-item">'
            f'<div class="highlight-label">{bullet.split(":")[0]}</div>'
            f'<div>{bullet.split(":", 1)[1].strip()}</div>'
            f'</div>'
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

    def _build_experience_section(self) -> str:
        """Build professional experience section"""
        jobs_html = ""

        for job in self.data['experience']:
            achievements_html = "".join([
                f'''<li class="achievement-item">
                    <i class="bi bi-circle-fill achievement-icon"></i>
                    <div class="achievement-text">{achievement['text']}</div>
                </li>'''
                for achievement in job['achievements']
            ])

            description = ''
            if job.get('description'):
                description = (
                    f'<div style="font-size: 0.85rem; color: var(--secondary-color); '
                    f'font-style: italic;">{job["description"]}</div>'
                )

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

    def _build_skills_section(self) -> str:
        """Build technical skills section"""
        skill_categories = {
            'fintech': ('FinTech & Blockchain', 'bi bi-currency-bitcoin'),
            'programming_languages': ('Programming Languages', 'bi bi-code-slash'),
            'web_technologies': ('Frameworks & Cloud', 'bi bi-layers'),
            'leadership': ('Leadership & Process', 'bi bi-people-fill')
        }

        categories_html = ""
        skills = self.data['skills']

        for skill_key, (title, icon) in skill_categories.items():
            if skill_key in skills:
                skill_data = skills[skill_key]
                tags = []

                if isinstance(skill_data, dict):
                    for skill_list in skill_data.values():
                        tags.extend(skill_list)
                elif isinstance(skill_data, list):
                    tags.extend(skill_data)

                # Add blockchain skills if this is fintech category
                if skill_key == 'fintech' and 'blockchain' in skills:
                    for skill_list in skills['blockchain'].values():
                        tags.extend(skill_list[:3])

                tags_html = "".join([
                    f'<span class="skill-tag">{tag}</span>'
                    for tag in tags[:10]
                ])

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

    def _build_projects_section(self) -> str:
        """Build projects section"""
        projects = self.data.get('projects', [])

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

    def _build_education_section(self) -> str:
        """Build education section"""
        education_html = ""

        for edu in self.data['education']:
            description = ""
            if edu.get('description'):
                description = (
                    f'<div style="font-size: 0.9rem; color: var(--secondary-color); '
                    f'margin-top: 0.5rem;">{edu["description"]}</div>'
                )

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
