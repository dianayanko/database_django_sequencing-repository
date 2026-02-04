# GitHub Codespaces ♥️ Django

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
