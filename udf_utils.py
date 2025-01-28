import re
from datetime import datetime

def extract_file_name(path):
    # Extract the file name (simplified)
    return path.split("/")[-1] if path else None

def extract_class_code(text):
    # Extract class code (e.g., C789, B456, A123)
    match = re.search(r'\b[A-Za-z]+\d+\b', text)
    return match.group(0) if match else None

def extract_salary_end(text):
    # Extract salary end (e.g., 119462.83)
    match = re.search(r'(\d+\.\d{2})', text)
    return float(match.group(1)) if match else None

def extract_end_date(text):
    # Extract end date (e.g., 2022-10-31)
    match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
    return datetime.strptime(match.group(1), '%Y-%m-%d') if match else None

def extract_salary_start(value):
    try:
        # Your original logic here, for example:
        return datetime.strptime(value, '%Y-%m-%d')  # Ensure it's a datetime object
    except Exception as e:
        return None  # Return None if an error occurs
def extract_req(text):
    # Extract requirements (e.g., "In degree picture. Reason since likely.")
    match = re.search(r'([^.]+)\.', text)
    return match.group(1) if match else None

def extract_notes(text):
    # Extract notes (e.g., "Play bar half although executive.")
    match = re.search(r'([^.]+)\.', text)
    return match.group(1) if match else None

def extract_duties(text):
    # Extract duties (e.g., "Western growth service risk.")
    match = re.search(r'([^.]+)\.', text)
    return match.group(1) if match else None

def extract_experience_length(text):
    # Extract experience length (e.g., "5+ years")
    match = re.search(r'(\d+[-\+]*\s*years)', text)
    return match.group(1) if match else None

def extract_job_type(text):
    # Extract job type (e.g., "Contract", "Part-time", "Full-time")
    match = re.search(r'(Contract|Part-time|Full-time)', text)
    return match.group(1) if match else None

def extract_education(text):
    # Extract education (e.g., "Bachelor", "Master", "PhD")
    match = re.search(r'(Bachelor|Master|PhD)', text)
    return match.group(1) if match else None

def extract_school_type(text):
    # Extract school type (e.g., "Public", "Private", "Online")
    match = re.search(r'(Public|Private|Online)', text)
    return match.group(1) if match else None

def extract_application_location(text):
    # Extract application location (e.g., "Perkinsport", "Raymondshire", "New Brandi")
    match = re.search(r'([A-Za-z]+(?:[A-Za-z\s]*[A-Za-z]+)?)$', text)
    return match.group(1) if match else None
