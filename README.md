# Bioinformatics Sample Management System

A Django web application designed as an internal database for managing biological samples, sequencing workflows, and bioinformatic analyses.

## Project Purpose

The application provides a centralized system for organizing and tracking biological samples, sequencing runs, and bioinformatic analysis results.

It supports the management of biological sample metadata and the relationships between samples, sequencing experiments, and downstream analyses.

## Main Applications

- **samples** – management of biological samples and related entities (Sample, Donor, Tissue).
- **sequencing** – management of sequencing experiments (Run, Platform).
- **analysis** – management of bioinformatic analyses and quality control (QC) metrics.
- **files** – management of file metadata and references to sequencing data files (FASTQ, BAM, VCF).

## Data Logic

The main data relationships follow this structure:

```text
Donor
  └── Sample
        └── SequencingRun
              └── Analysis
                    └── Metrics / Reports
```

## Requirements

- Python 3.12
- Git
- pip

## Installation and Setup

### 1. Clone the repository

```
git clone https://github.com/dianayanko/database_django_sequencing-repository.git
cd database_django_sequencing-repository
```

### 2. Create and activate a virtual environment

Create a virtual environment:

```
python -m venv venv
```

Activate it:

**macOS / Linux:**

```
source venv/bin/activate
```

**Windows:**

```
venv\Scripts\activate
```

### 3. Install dependencies

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file using the provided example:

**macOS / Linux:**

```
cp .env.example .env
```

**Windows:**

```
copy .env.example .env
```

Generate a Django secret key:

```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Open `.env` and replace the example `SECRET_KEY` with the generated value.

Make sure the configuration contains:

```
SECRET_KEY=your_generated_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

**Important:**
- Generate your own secret key.
- Do not commit your `.env` file to the repository.
- Keep `DEBUG=True` only for local development.

### 5. Set up the database

The project uses **SQLite** as its default database.

SQLite is included with Python, so no additional database server installation or configuration is required.

Run the migrations:

```
python manage.py migrate
```

This command automatically creates the `db.sqlite3` file in the project root directory and initializes all required database tables.

No manual database creation is necessary.

### 6. Start the development server

```
python manage.py runserver
```

Open the application in your browser:

http://127.0.0.1:8000/

To stop the server, press `Ctrl + C` in the terminal.

## Django Administration

To create an administrator account, run:

```
python manage.py createsuperuser
```

Follow the instructions in the terminal to configure your username, email address, and password.

Access the Django administration panel at:

http://127.0.0.1:8000/admin/

## Troubleshooting

### DisallowedHost error

Make sure your `.env` file contains:

```
ALLOWED_HOSTS=127.0.0.1,localhost
```

### SECRET_KEY must not be empty

Make sure that:
- The `.env` file exists in the project root directory.
- The `SECRET_KEY` variable is defined.
- A valid generated secret key is assigned.

### ModuleNotFoundError

Make sure your virtual environment is activated and install the dependencies again:

```
pip install -r requirements.txt
```

### Database errors

Make sure you are running commands from the project root directory, where `manage.py` is located.

Apply migrations:

```
python manage.py migrate
```

## Project Structure

```
database_django_sequencing-repository/
├── hello_world/
│   ├── analysis/
│   ├── core/
│   ├── files/
│   ├── samples/
│   ├── sequencing/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── sample_fixture.json
├── requirements.txt
├── manage.py
├── .env.example
├── .gitignore
└── README.md
```

## Technologies

- Python
- Django
- SQLite
- HTML
- CSS
- JavaScript

## Notes

This project is intended for local development and internal data management.

The Django development server is not suitable for production use. Additional configuration is required before deploying the application to a production environment.
