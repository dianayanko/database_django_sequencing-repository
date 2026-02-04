"""
Models for biological samples and donor metadata.
"""
from django.db import models


class Organism(models.Model):
    """Represents the biological organism of a sample."""
    
    TAXONOMY_CHOICES = [
        ('human', 'Homo sapiens'),
        ('mouse', 'Mus musculus'),
        ('rat', 'Rattus norvegicus'),
        ('zebrafish', 'Danio rerio'),
        ('c_elegans', 'Caenorhabditis elegans'),
        ('drosophila', 'Drosophila melanogaster'),
        ('arabidopsis', 'Arabidopsis thaliana'),
        ('yeast', 'Saccharomyces cerevisiae'),
        ('other', 'Other'),
    ]
    
    scientific_name = models.CharField(max_length=255, unique=True)
    common_name = models.CharField(max_length=255)
    taxonomy_id = models.CharField(max_length=50, choices=TAXONOMY_CHOICES, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scientific_name']
    
    def __str__(self):
        return f"{self.common_name} ({self.scientific_name})"


class TissueType(models.Model):
    """Represents tissue types for sample classification."""
    
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    ontology_id = models.CharField(max_length=50, blank=True, help_text="e.g., UBERON ID")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Donor(models.Model):
    """Represents a biological donor/individual."""
    
    DISEASE_STATE_CHOICES = [
        ('healthy', 'Healthy'),
        ('disease', 'Disease'),
        ('control', 'Control'),
        ('unknown', 'Unknown'),
    ]
    
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown'),
    ]
    
    donor_id = models.CharField(max_length=255, unique=True)
    organism = models.ForeignKey(Organism, on_delete=models.CASCADE, related_name='donors')
    age = models.IntegerField(null=True, blank=True, help_text="Age in years")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='U')
    disease_state = models.CharField(max_length=20, choices=DISEASE_STATE_CHOICES, default='unknown')
    genotype = models.CharField(max_length=500, blank=True)
    phenotype = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['donor_id']
        unique_together = [['organism', 'donor_id']]
    
    def __str__(self):
        return f"{self.donor_id} ({self.organism.common_name})"


class Sample(models.Model):
    """
    Represents a biological sample derived from a donor.
    One sample can be used in multiple sequencing runs.
    """
    
    SAMPLE_TYPE_CHOICES = [
        ('bulk', 'Bulk tissue'),
        ('single_cell', 'Single cell'),
        ('sorted_cell', 'Sorted cell'),
        ('organoid', 'Organoid'),
        ('primary_culture', 'Primary culture'),
        ('cell_line', 'Cell line'),
        ('other', 'Other'),
    ]
    
    sample_id = models.CharField(max_length=255, unique=True)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='samples')
    tissue_type = models.ForeignKey(TissueType, on_delete=models.SET_NULL, null=True, related_name='samples')
    sample_type = models.CharField(max_length=50, choices=SAMPLE_TYPE_CHOICES, default='bulk')
    
    # Collection metadata
    collection_date = models.DateField(null=True, blank=True)
    passage_number = models.IntegerField(null=True, blank=True, help_text="For cultured samples")
    
    # Characteristics
    cell_count = models.BigIntegerField(null=True, blank=True)
    viability = models.FloatField(null=True, blank=True, help_text="Percentage (0-100)")
    
    # Documentation
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    # Storage options (predefined locations)
    STORAGE_CHOICES = [
        ('freezer_1', 'Freezer 1 (-80°C)'),
        ('freezer_2', 'Freezer 2 (-20°C)'),
        ('fridge', 'Fridge (4°C)'),
        ('room_temp', 'Room Temperature'),
    ]

    # Storage/location where sample is kept
    # Using choices constrains user input while keeping field type/length the same
    storage_conditions = models.CharField(max_length=255, choices=STORAGE_CHOICES, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = [['donor', 'sample_id']]
    
    def __str__(self):
        return f"{self.sample_id} ({self.tissue_type})"
