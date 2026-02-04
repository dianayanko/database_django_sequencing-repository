

# Bioinformatics Sample Management System

## Cel projektu
Webowa aplikacja Django służąca jako wewnętrzna baza danych
do zarządzania próbkami biologicznymi, sekwencjonowaniem
i analizą bioinformatyczną.


## Główne aplikacje
- samples – próbki biologiczne (Sample, Donor, Tissue)
- sequencing – sekwencjonowanie (Run, Platform)
- analysis – analizy bioinformatyczne i metryki QC
- files – metadane plików (FASTQ, BAM, VCF)

## Logika danych (high-level)
Donor
 → Sample
   → SequencingRun
     → Analysis
       → Metrics / Reports


## uruchomienie projektu:
Sklonować repozytorium

`git clone https://github.com/dianayanko/database_django_sequencing-repository.git`

`cd database_django_sequencing-repository`


Stworzyć wirtualne środowisko

`python -m venv venv
source venv/bin/activate   # Linux / Mac`

`
venv\Scripts\activate # Windows`


Zainstalować wymagania

`pip install -r requirements.txt`


Uruchomić migracje (utworzyć bazę)

`python manage.py migrate`


Uruchomić serwer Django

`python manage.py runserver`

