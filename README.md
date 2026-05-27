

# Bioinformatics Sample Management System

## Project Purpose
A Django web application serving as an internal database
for managing biological samples, sequencing
and bioinformatic analysis.
## Main Applications
- samples – biological samples (Sample, Donor, Tissue)
- sequencing – sequencing (Run, Platform)
- analysis – bioinformatic analyses and QC metrics
- files – file metadata (FASTQ, BAM, VCF)
## Data Logic (high-level)
Donor
→ Sample
 → SequencingRun
  → Analysis
   → Metrics / Reports
## Running the project:
Clone the repository
`git clone https://github.com/dianayanko/database_django_sequencing-repository.git\`
`cd database_django_sequencing-repository`
Create a virtual environment
`python -m venv venv
source venv/bin/activate # Linux / Mac`
`venv\Scripts\activate # Windows`
Install requirements
`pip install -r requirements.txt`
Run migrations (create the database)
`python manage.py migrate`
Start the Django server
`python manage.py runserver`


Uruchomić serwer Django

`python manage.py runserver`

