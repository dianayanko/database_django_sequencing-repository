"""
Forms for samples app.
"""
from django import forms
from .models import Sample, Donor, TissueType


class SampleForm(forms.ModelForm):
    """Form for creating and updating Sample objects."""
    
    class Meta:
        model = Sample
        fields = [
            'sample_id',
            'donor',
            'tissue_type',
            'sample_type',
            'collection_date',
            'passage_number',
            'cell_count',
            'viability',
            'storage_conditions',
            'description',
            'notes',
        ]
        widgets = {
            'sample_id': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., S-2026-001',
                'required': True,
            }),
            'donor': forms.Select(attrs={
                'class': 'form-input',
                'required': True,
            }),
            'tissue_type': forms.Select(attrs={
                'class': 'form-input',
            }),
            'sample_type': forms.Select(attrs={
                'class': 'form-input',
            }),
            'collection_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
            'passage_number': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
            }),
            'cell_count': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
            }),
            'viability': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '100',
                'step': '0.1',
            }),
            'storage_conditions': forms.Select(attrs={
                'class': 'form-input',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': '3',
                'placeholder': 'Sample description',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': '3',
                'placeholder': 'Additional notes',
            }),
        }
