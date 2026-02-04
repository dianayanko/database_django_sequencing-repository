"""
Django management command to populate the database with realistic demo data
for the bioinformatics sequencing repository.

Creates:
- Organisms, Tissue Types, Donors, Samples
- Sequencing Platforms, Projects, Library Preparations, Runs
- Analyses (QC, Alignment, Expression, Variant Calling)
- Analysis Metrics (QCMetrics, AlignmentMetrics, ExpressionMetrics, VariantCallingMetrics)
- Reports
- FileMetadata and FileAssociation
"""

from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from hello_world.samples.models import Organism, TissueType, Donor, Sample
from hello_world.sequencing.models import (
    SequencingPlatform,
    SequencingProject,
    LibraryPreparation,
    SequencingRun,
)
from hello_world.analysis.models import (
    Analysis,
    Report,
    QCMetrics,
    AlignmentMetrics,
    VariantCallingMetrics,
    ExpressionMetrics,
)
from hello_world.files.models import FileMetadata, FileAssociation


class Command(BaseCommand):
    help = "Populate the database with realistic demo data for testing"

    def handle(self, *args, **options):
        """Main command handler."""
        try:
            self.stdout.write(self.style.SUCCESS("Starting demo data population..."))

            # Create organisms
            organisms = self._create_organisms()
            self.stdout.write(f"✓ Created {len(organisms)} organisms")

            # Create tissue types
            tissue_types = self._create_tissue_types()
            self.stdout.write(f"✓ Created {len(tissue_types)} tissue types")

            # Create donors
            donors = self._create_donors(organisms)
            self.stdout.write(f"✓ Created {len(donors)} donors")

            # Create samples
            samples = self._create_samples(donors, tissue_types)
            self.stdout.write(f"✓ Created {len(samples)} samples")

            # Create sequencing platforms
            platforms = self._create_sequencing_platforms()
            self.stdout.write(f"✓ Created {len(platforms)} sequencing platforms")

            # Create sequencing projects
            projects = self._create_sequencing_projects(samples)
            self.stdout.write(f"✓ Created {len(projects)} sequencing projects")

            # Create library preparations
            libraries = self._create_library_preparations()
            self.stdout.write(f"✓ Created {len(libraries)} library preparations")

            # Create sequencing runs
            runs = self._create_sequencing_runs(projects, samples, platforms, libraries)
            self.stdout.write(f"✓ Created {len(runs)} sequencing runs")

            # Create analyses and metrics
            analyses_data = self._create_analyses_and_metrics(runs, projects)
            self.stdout.write(
                f"✓ Created {analyses_data['analyses_count']} analyses with metrics"
            )

            # Create reports
            reports_count = self._create_reports(analyses_data['analyses'])
            self.stdout.write(f"✓ Created {reports_count} reports")

            # Create file metadata and associations
            files_count, associations_count = self._create_files_and_associations(
                runs, analyses_data['analyses']
            )
            self.stdout.write(f"✓ Created {files_count} file metadata entries")
            self.stdout.write(f"✓ Created {associations_count} file associations")

            self.stdout.write(
                self.style.SUCCESS(
                    "\n✓ Demo data population completed successfully!"
                )
            )

        except Exception as e:
            raise CommandError(f"Error populating demo data: {str(e)}")

    def _create_organisms(self):
        """Create organism records."""
        organisms_data = [
            {
                "scientific_name": "Homo sapiens",
                "common_name": "Human",
                "taxonomy_id": "human",
            },
            {
                "scientific_name": "Mus musculus",
                "common_name": "Mouse",
                "taxonomy_id": "mouse",
            },
        ]

        organisms = []
        for data in organisms_data:
            organism, created = Organism.objects.get_or_create(**data)
            organisms.append(organism)

        return organisms

    def _create_tissue_types(self):
        """Create tissue type records."""
        tissue_types_data = [
            {"name": "Blood", "description": "Whole blood sample"},
            {"name": "Liver", "description": "Liver tissue"},
            {"name": "Brain", "description": "Brain tissue"},
        ]

        tissue_types = []
        for data in tissue_types_data:
            tissue_type, created = TissueType.objects.get_or_create(**data)
            tissue_types.append(tissue_type)

        return tissue_types

    def _create_donors(self, organisms):
        """Create donor records."""
        human_organism = organisms[0]  # Homo sapiens

        donors_data = [
            {
                "donor_id": "D001",
                "organism": human_organism,
                "age": 34,
                "sex": "F",
                "disease_state": "healthy",
            },
            {
                "donor_id": "D002",
                "organism": human_organism,
                "age": 45,
                "sex": "M",
                "disease_state": "healthy",
            },
        ]

        donors = []
        for data in donors_data:
            donor, created = Donor.objects.get_or_create(**data)
            donors.append(donor)

        return donors

    def _create_samples(self, donors, tissue_types):
        """Create sample records."""
        blood_tissue = tissue_types[0]
        liver_tissue = tissue_types[1]
        brain_tissue = tissue_types[2]

        samples_data = [
            {
                "sample_id": "S001",
                "donor": donors[0],
                "tissue_type": blood_tissue,
                "sample_type": "bulk",
                "cell_count": 5_000_000,
                "viability": 96.5,
                "storage_conditions": "PBMC frozen at -80°C",
            },
            {
                "sample_id": "S002",
                "donor": donors[0],
                "tissue_type": liver_tissue,
                "sample_type": "bulk",
                "cell_count": 10_000_000,
                "viability": 94.2,
                "storage_conditions": "Tissue frozen at -80°C",
            },
            {
                "sample_id": "S003",
                "donor": donors[1],
                "tissue_type": brain_tissue,
                "sample_type": "bulk",
                "cell_count": 8_000_000,
                "viability": 92.1,
                "storage_conditions": "Tissue frozen at -80°C",
            },
        ]

        samples = []
        for data in samples_data:
            sample, created = Sample.objects.get_or_create(**data)
            samples.append(sample)

        return samples

    def _create_sequencing_platforms(self):
        """Create sequencing platform records."""
        platforms_data = [
            {
                "name": "Illumina NovaSeq 6000",
                "platform_type": "illumina",
                "manufacturer": "Illumina",
                "instrument_model": "NovaSeq 6000",
                "read_length_min": 50,
                "read_length_max": 150,
                "read_type": "paired",
            },
            {
                "name": "Oxford Nanopore PromethION",
                "platform_type": "ont",
                "manufacturer": "Oxford Nanopore Technologies",
                "instrument_model": "PromethION",
                "read_length_min": 5000,
                "read_length_max": 200000,
                "read_type": "long",
            },
        ]

        platforms = []
        for data in platforms_data:
            platform, created = SequencingPlatform.objects.get_or_create(**data)
            platforms.append(platform)

        return platforms

    def _create_sequencing_projects(self, samples):
        """Create sequencing project records."""
        base_date = timezone.now()

        projects_data = [
            {
                "project_id": "P001",
                "title": "Human RNA-seq Pilot Study",
                "description": "Pilot study on gene expression across human tissues",
                "pi_name": "Dr. Jane Smith",
                "institution": "Research Institute",
                "project_type": "rna_seq",
                "status": "completed",
                "start_date": (base_date - timedelta(days=90)).date(),
                "completion_date": (base_date - timedelta(days=10)).date(),
            },
            {
                "project_id": "P002",
                "title": "Human WES Variant Discovery",
                "description": "Whole exome sequencing for variant discovery",
                "pi_name": "Dr. John Doe",
                "institution": "Medical Center",
                "project_type": "wes",
                "status": "completed",
                "start_date": (base_date - timedelta(days=120)).date(),
                "completion_date": (base_date - timedelta(days=5)).date(),
            },
        ]

        projects = []
        for data in projects_data:
            project, created = SequencingProject.objects.get_or_create(
                project_id=data["project_id"], defaults=data
            )
            projects.append(project)

            # Add samples to project using many-to-many
            if data["project_id"] == "P001":
                project.samples.set([samples[0], samples[1]])
            elif data["project_id"] == "P002":
                project.samples.set([samples[2]])

        return projects

    def _create_library_preparations(self):
        """Create library preparation records."""
        base_date = timezone.now()

        libraries_data = [
            {
                "library_id": "LIB001",
                "library_kit": "truseq_stranded_mrna",
                "insert_size_bp": 300,
                "fragment_size_bp": 350,
                "library_concentration": 50.5,
                "library_volume_ul": 100,
                "qc_status": "pass",
                "rna_integrity_number": 8.5,
                "prep_date": (base_date - timedelta(days=85)).date(),
                "technician": "Alice Johnson",
                "index_name": "idx001",
                "index_sequence": "ATCGATCG",
            },
            {
                "library_id": "LIB002",
                "library_kit": "agilent_sureselect",
                "insert_size_bp": 200,
                "fragment_size_bp": 250,
                "library_concentration": 75.3,
                "library_volume_ul": 80,
                "qc_status": "pass",
                "dna_integrity": "High molecular weight",
                "prep_date": (base_date - timedelta(days=115)).date(),
                "technician": "Bob Smith",
                "index_name": "idx002",
                "index_sequence": "GCTAGCTA",
            },
        ]

        libraries = []
        for data in libraries_data:
            library, created = LibraryPreparation.objects.get_or_create(**data)
            libraries.append(library)

        return libraries

    def _create_sequencing_runs(self, projects, samples, platforms, libraries):
        """Create sequencing run records."""
        base_date = timezone.now()

        runs_data = [
            {
                "run_id": "R001",
                "project": projects[0],  # P001: RNA-seq
                "platform": platforms[0],  # Illumina NovaSeq
                "sample": samples[0],  # S001
                "library_preparation": libraries[0],
                "run_date": (base_date - timedelta(days=80)).date(),
                "status": "completed",
                "flowcell_id": "FLOWCELL_001",
                "total_reads": 150_000_000,
                "total_bases": 22_500_000_000,
                "q30_percentage": 92.5,
                "mean_read_length": 150,
                "completion_date": (base_date - timedelta(days=78)).date(),
                "technician": "Alice Johnson",
            },
            {
                "run_id": "R002",
                "project": projects[0],  # P001: RNA-seq
                "platform": platforms[0],  # Illumina NovaSeq
                "sample": samples[1],  # S002
                "library_preparation": libraries[0],
                "run_date": (base_date - timedelta(days=75)).date(),
                "status": "completed",
                "flowcell_id": "FLOWCELL_002",
                "total_reads": 175_000_000,
                "total_bases": 26_250_000_000,
                "q30_percentage": 93.2,
                "mean_read_length": 150,
                "completion_date": (base_date - timedelta(days=73)).date(),
                "technician": "Alice Johnson",
            },
            {
                "run_id": "R003",
                "project": projects[1],  # P002: WES
                "platform": platforms[0],  # Illumina NovaSeq
                "sample": samples[2],  # S003
                "library_preparation": libraries[1],
                "run_date": (base_date - timedelta(days=110)).date(),
                "status": "completed",
                "flowcell_id": "FLOWCELL_003",
                "total_reads": 125_000_000,
                "total_bases": 18_750_000_000,
                "q30_percentage": 91.8,
                "mean_read_length": 150,
                "completion_date": (base_date - timedelta(days=108)).date(),
                "technician": "Bob Smith",
            },
        ]

        runs = []
        for data in runs_data:
            run, created = SequencingRun.objects.get_or_create(
                run_id=data["run_id"], defaults=data
            )
            runs.append(run)

        return runs

    def _create_analyses_and_metrics(self, runs, projects):
        """Create analysis records and their associated metrics."""
        base_date = timezone.now()
        analyses = []

        for run in runs:
            project = run.project
            sample = run.sample
            is_rna_seq = project.project_type == "rna_seq"
            is_wes = project.project_type == "wes"

            # 1. QC Analysis
            qc_analysis, _ = Analysis.objects.get_or_create(
                analysis_id=f"{run.run_id}_QC",
                defaults={
                    "sequencing_run": run,
                    "sample": sample,
                    "analysis_type": "qc",
                    "pipeline_name": "fastqc",
                    "pipeline_version": "0.11.9",
                    "status": "completed",
                    "started_at": run.run_date and timezone.make_aware(
                        datetime.combine(run.run_date, datetime.min.time())
                    ),
                    "completed_at": run.completion_date and timezone.make_aware(
                        datetime.combine(
                            run.completion_date, datetime.min.time()
                        ) + timedelta(hours=2)
                    ),
                    "description": "Quality control analysis of raw sequencing reads",
                },
            )
            analyses.append(qc_analysis)

            # QC Metrics
            QCMetrics.objects.get_or_create(
                analysis=qc_analysis,
                defaults={
                    "total_sequences": run.total_reads,
                    "gc_content_percent": 52.3,
                    "n_content_percent": 0.02,
                    "mean_quality_score": 35.8,
                    "percentage_q30": run.q30_percentage,
                    "percentage_q20": 98.5,
                    "percent_duplicates": 3.2,
                    "adapter_content_percent": 0.5,
                    "qc_status": "pass",
                },
            )

            # 2. Alignment Analysis
            alignment_analysis, _ = Analysis.objects.get_or_create(
                analysis_id=f"{run.run_id}_ALIGN",
                defaults={
                    "sequencing_run": run,
                    "sample": sample,
                    "analysis_type": "alignment",
                    "pipeline_name": "bwa",
                    "pipeline_version": "0.7.17",
                    "status": "completed",
                    "started_at": run.completion_date and timezone.make_aware(
                        datetime.combine(run.completion_date, datetime.min.time())
                        + timedelta(hours=1)
                    ),
                    "completed_at": run.completion_date and timezone.make_aware(
                        datetime.combine(run.completion_date, datetime.min.time())
                        + timedelta(hours=6)
                    ),
                    "parameters": {
                        "reference_genome": "GRCh38",
                        "aligner": "bwa-mem",
                    },
                    "description": "Read alignment to reference genome",
                },
            )
            analyses.append(alignment_analysis)

            # Alignment Metrics
            total_reads = run.total_reads
            mapped_reads = int(total_reads * 0.96)
            AlignmentMetrics.objects.get_or_create(
                analysis=alignment_analysis,
                defaults={
                    "total_reads": total_reads,
                    "mapped_reads": mapped_reads,
                    "unmapped_reads": total_reads - mapped_reads,
                    "mapping_rate_percent": 96.0,
                    "properly_paired_percent": 94.5,
                    "median_insert_size": 300,
                    "percent_duplicates": 4.8,
                    "mean_coverage": 85.0,
                    "coverage_uniformity": 0.92,
                },
            )

            # 3. Expression Analysis (RNA-seq only)
            if is_rna_seq:
                expr_analysis, _ = Analysis.objects.get_or_create(
                    analysis_id=f"{run.run_id}_EXPR",
                    defaults={
                        "sequencing_run": run,
                        "sample": sample,
                        "analysis_type": "expression",
                        "pipeline_name": "salmon",
                        "pipeline_version": "1.10.0",
                        "status": "completed",
                        "started_at": run.completion_date and timezone.make_aware(
                            datetime.combine(run.completion_date, datetime.min.time())
                            + timedelta(hours=8)
                        ),
                        "completed_at": run.completion_date and timezone.make_aware(
                            datetime.combine(run.completion_date, datetime.min.time())
                            + timedelta(hours=10)
                        ),
                        "parameters": {
                            "reference_transcriptome": "Ensembl v107",
                            "libType": "ISR",
                        },
                        "description": "Gene expression quantification",
                    },
                )
                analyses.append(expr_analysis)

                # Expression Metrics
                ExpressionMetrics.objects.get_or_create(
                    analysis=expr_analysis,
                    defaults={
                        "genes_detected": 18_500,
                        "total_gene_count": 20_000,
                        "mapping_rate_percent": 92.3,
                        "percent_mtdna": 8.5,
                        "percent_rrna": 5.2,
                        "normalization_method": "tpm",
                        "mean_gene_expression": 12.5,
                        "median_gene_expression": 5.3,
                    },
                )

            # 4. Variant Calling Analysis (WES only)
            if is_wes:
                variant_analysis, _ = Analysis.objects.get_or_create(
                    analysis_id=f"{run.run_id}_VAR",
                    defaults={
                        "sequencing_run": run,
                        "sample": sample,
                        "analysis_type": "variant_calling",
                        "pipeline_name": "gatk",
                        "pipeline_version": "4.3.0",
                        "status": "completed",
                        "started_at": run.completion_date and timezone.make_aware(
                            datetime.combine(run.completion_date, datetime.min.time())
                            + timedelta(hours=7)
                        ),
                        "completed_at": run.completion_date and timezone.make_aware(
                            datetime.combine(run.completion_date, datetime.min.time())
                            + timedelta(hours=15)
                        ),
                        "parameters": {
                            "reference_genome": "GRCh38",
                            "caller": "HaplotypeCaller",
                        },
                        "description": "Germline variant calling",
                    },
                )
                analyses.append(variant_analysis)

                # Variant Calling Metrics
                VariantCallingMetrics.objects.get_or_create(
                    analysis=variant_analysis,
                    defaults={
                        "total_variants": 42_500,
                        "snp_count": 38_200,
                        "indel_count": 4_300,
                        "multi_allelic_count": 850,
                        "mean_variant_quality": 58.5,
                        "percent_variants_pass_filter": 96.2,
                        "titv_ratio": 2.1,
                        "percent_missense": 35.2,
                        "percent_synonymous": 28.5,
                        "percent_frameshift": 2.1,
                    },
                )

        return {
            "analyses": analyses,
            "analyses_count": len(analyses),
        }

    def _create_reports(self, analyses):
        """Create report records for each analysis."""
        report_count = 0

        for analysis in analyses:
            report_type_map = {
                "qc": "qc",
                "alignment": "alignment",
                "variant_calling": "variant",
                "expression": "expression",
            }

            report_type = report_type_map.get(analysis.analysis_type, "qc")

            report, created = Report.objects.get_or_create(
                analysis=analysis,
                defaults={
                    "report_type": report_type,
                    "summary": f"Analysis report for {analysis.analysis_id}",
                    "metrics": {
                        "pipeline": analysis.pipeline_name,
                        "version": analysis.pipeline_version,
                        "status": analysis.status,
                    },
                    "quality_flag": "pass" if analysis.status == "completed" else "warn",
                },
            )

            if created:
                report_count += 1

        return report_count

    def _create_files_and_associations(self, runs, analyses):
        """Create file metadata and file associations."""
        file_count = 0
        association_count = 0
        base_date = timezone.now()

        file_configs = []

        # Create FASTQ files for each run
        for run in runs:
            file_configs.extend([
                {
                    "file_id": f"{run.run_id}_R1.fastq.gz",
                    "file_path": f"/data/fastq/{run.run_id}_R1.fastq.gz",
                    "file_type": "fastq_gz",
                    "read_type": "R1",
                    "file_role": "raw_reads",
                    "sequencing_run": run,
                    "total_reads": run.total_reads,
                    "file_size_bytes": 12_500_000_000,
                    "checksum_md5": f"md5_{run.run_id}_R1",
                    "checksum_sha256": f"sha256_{run.run_id}_R1",
                },
                {
                    "file_id": f"{run.run_id}_R2.fastq.gz",
                    "file_path": f"/data/fastq/{run.run_id}_R2.fastq.gz",
                    "file_type": "fastq_gz",
                    "read_type": "R2",
                    "file_role": "raw_reads",
                    "sequencing_run": run,
                    "total_reads": run.total_reads,
                    "file_size_bytes": 12_500_000_000,
                    "checksum_md5": f"md5_{run.run_id}_R2",
                    "checksum_sha256": f"sha256_{run.run_id}_R2",
                },
            ])

        # Create BAM and VCF files for analyses
        for analysis in analyses:
            if analysis.analysis_type == "alignment":
                file_configs.append({
                    "file_id": f"{analysis.analysis_id}.bam",
                    "file_path": f"/data/bam/{analysis.analysis_id}.bam",
                    "file_type": "bam",
                    "file_role": "aligned_reads",
                    "analysis": analysis,
                    "total_reads": analysis.sequencing_run.total_reads,
                    "file_size_bytes": 45_000_000_000,
                    "checksum_md5": f"md5_{analysis.analysis_id}",
                    "checksum_sha256": f"sha256_{analysis.analysis_id}",
                    "index_file_path": f"/data/bam/{analysis.analysis_id}.bam.bai",
                })

            elif analysis.analysis_type == "variant_calling":
                file_configs.append({
                    "file_id": f"{analysis.analysis_id}.vcf.gz",
                    "file_path": f"/data/vcf/{analysis.analysis_id}.vcf.gz",
                    "file_type": "vcf_gz",
                    "file_role": "variants",
                    "analysis": analysis,
                    "file_size_bytes": 2_500_000_000,
                    "checksum_md5": f"md5_{analysis.analysis_id}",
                    "checksum_sha256": f"sha256_{analysis.analysis_id}",
                    "index_file_path": f"/data/vcf/{analysis.analysis_id}.vcf.gz.tbi",
                })

        # Create FileMetadata and FileAssociation records
        for config in file_configs:
            file_role = config.pop("file_role")
            sequencing_run = config.pop("sequencing_run", None)
            analysis = config.pop("analysis", None)

            file_metadata, created = FileMetadata.objects.get_or_create(
                file_id=config["file_id"],
                defaults={
                    **config,
                    "is_compressed": config["file_type"]
                    in ["fastq_gz", "vcf_gz"],
                    "compression_format": "gzip"
                    if config["file_type"] in ["fastq_gz", "vcf_gz"]
                    else "",
                    "storage_location": "local",
                },
            )

            if created:
                file_count += 1

            # Create FileAssociation
            association, assoc_created = FileAssociation.objects.get_or_create(
                file_metadata=file_metadata,
                sequencing_run=sequencing_run,
                analysis=analysis,
                defaults={"file_role": file_role},
            )

            if assoc_created:
                association_count += 1

        return file_count, association_count
