# Copilot Instructions for Django Sequencing Repository Backend

## Project Overview

This is a Django 5.2 bioinformatics backend system supporting RNA-seq, WES, and WGS data management. The system provides:
- Domain models for samples, sequencing runs, analyses, and QC metrics
- RESTful API endpoints for CRUD operations on all entities
- Django admin interface for data management
- File metadata tracking without storing raw binary data

## Architecture & Apps

Four specialized Django apps manage distinct domains:

### `samples/` - Biological Sample Management
- **Models**: Organism, TissueType, Donor, Sample
- **Key concept**: Organism → Donor → Sample (1:N relationships)
- **API prefix**: `/api/samples/`
- **Endpoints**: `organisms/`, `tissue-types/`, `donors/`, `samples/`

### `sequencing/` - Sequencing Execution & Metadata
- **Models**: SequencingPlatform, SequencingProject, LibraryPreparation, SequencingRun
- **Key concept**: Project contains Samples → Each Sample has Runs on Platforms
- **API prefix**: `/api/sequencing/`
- **Endpoints**: `platforms/`, `projects/`, `library-preparations/`, `runs/`
- **Library prep**: Metadata before sequencing (QC, indexing, kit info)

### `analysis/` - Bioinformatics Analysis & Metrics
- **Models**: Analysis, Report, QCMetrics, AlignmentMetrics, VariantCallingMetrics, ExpressionMetrics
- **Key concept**: Run → Analysis (QC/alignment/variant/expression) → Reports + Metrics
- **API prefix**: `/api/analysis/`
- **Endpoints**: `analyses/`, `reports/`, `qc-metrics/`, `alignment-metrics/`, `variant-metrics/`, `expression-metrics/`
- **Metrics detail**: One-to-one relationships with Analysis; populated by pipeline results

### `files/` - File Metadata & Tracking
- **Models**: FileMetadata, FileAssociation
- **Key concept**: Track file references (FASTQ/BAM/VCF) without storing binary data
- **API prefix**: `/api/files/`
- **Endpoints**: `file-metadata/`, `file-associations/`
- **File roles**: raw_reads, trimmed_reads, aligned_reads, variants, expression_matrix, qc_report, etc.

## Data Flow & Relationships

```
SequencingProject (one) → Samples (many)
         ↓
    SequencingRun (one per sample per project)
         ↓
    SequencingPlatform (one per run)
         ↓
    Analysis (many: QC, alignment, variant, expression)
         ↓
    Report + Metrics (one per analysis type)
         ↓
    FileAssociation → FileMetadata (tracks output files)
```

## API Usage Patterns

### List with Filters
```
GET /api/sequencing/runs/?status=completed&platform=2&ordering=-run_date
GET /api/analysis/analyses/?analysis_type=alignment&sequencing_run=5
GET /api/files/file-metadata/?file_type=bam&storage_location=s3
```

### Nested Detail Endpoints
```
GET /api/sequencing/projects/1/        # Includes samples_detail array
GET /api/sequencing/runs/5/             # Includes nested sample_detail, platform_detail
GET /api/analysis/analyses/10/          # Includes qc_metrics, alignment_metrics, reports
```

### Search
```
GET /api/samples/samples/?search=my_sample_id
GET /api/sequencing/runs/?search=flowcell_xyz
```

## Critical Patterns & Field Conventions

### Timestamps & Status
- All models: `created_at` (auto), `updated_at` (auto)
- Status fields use choices (e.g., `SequencingRun.status`: planned/in_progress/completed/failed)
- Nullable dates allow "not yet started" states

### File Integration
- **No binary storage**: FileMetadata stores path/URI, size, checksum, format only
- **Checksum fields**: MD5 and SHA256 for integrity verification
- **Index files**: BAI, TBI, CSI paths in separate field
- **Storage location**: local/s3/gcs/other for cloud-ready design

### Admin Customizations
- `SequencingProject`: filter_horizontal widget for sample selection
- `Analysis`: inline metrics (QCMetrics, AlignmentMetrics, etc.) for data entry
- Key fields use readonly_fields and fieldsets for organization
- List displays optimized for bioinformatics workflows

## Development Workflow

### Setup
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Adding Features
1. **New sample attributes**: Add fields to `Sample` model in `samples/models.py`
2. **New analysis type**: Create Analysis subclass or extend VariantCallingMetrics-style model
3. **New file formats**: Add to FileMetadata.FILE_TYPE_CHOICES
4. **New API endpoint**: Create viewset + add to router in `{app}/urls.py`

### Admin Access
- Admin at `/admin/` (superuser required)
- All models registered with customized admin classes
- Inline editing of nested objects (e.g., edit metrics while viewing analysis)

### Testing API
```bash
curl -H "Accept: application/json" http://localhost:8000/api/samples/samples/
curl -X POST http://localhost:8000/api/sequencing/projects/ \
  -H "Content-Type: application/json" \
  -d '{"project_id":"PRJ001","title":"My Project","project_type":"rna_seq","status":"planning"}'
```

## Key Design Decisions

- **One Analysis per run type**: An Analysis ties to one SequencingRun and has one metrics model (QC, Alignment, etc.)
- **FileAssociation bridge**: Allows tracking files without duplicating FileMetadata; associates with Run or Analysis
- **JSON parameters**: Analysis.parameters stores pipeline args; Report.metrics stores summary statistics
- **No data duplication**: Checksum fields prevent duplicate FileMetadata entries
- **Organism/TissueType catalog**: Normalized lookup tables for consistency

## Extension Points (Future)

- Add permission classes for user-based access control
- Integrate with workflow engines (Nextflow, CWL, Snakemake)
- Cloud storage backends (boto3 for S3, google-cloud-storage)
- Async task queuing for pipeline triggers (Celery)
- Variant annotation pipelines (VEP, SnpEff integration)

