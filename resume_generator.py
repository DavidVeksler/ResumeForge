#!/usr/bin/env python3
"""
Resume Generator - Refactored version with clean architecture

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
from datetime import datetime
from typing import Dict, Any

from resume.generator import ResumeGenerator, extract_keywords_from_job_description


def main():
    """Main entry point for resume generation"""
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
        # Load resume data
        with open(json_file, 'r') as f:
            resume_data = json.load(f)

        generator = ResumeGenerator(resume_data)

        # Customize for job description if provided
        if job_description:
            role_keywords = extract_keywords_from_job_description(job_description)
            customized_data = generator.customize_for_role(job_description, role_keywords)
            generator = ResumeGenerator(customized_data)
            print(f"Resume customized for job posting with {len(role_keywords)} key terms")

        # Generate HTML
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
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
