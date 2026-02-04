from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Analysis
from hello_world.sequencing.models import SequencingRun
from hello_world.files.models import FileAssociation
import json
from django.core.serializers.json import DjangoJSONEncoder

def model_to_json_safe(obj):
    """
    Convert any Django model instance to a dict that is 100% JSON-serializable.
    Recursively handles ForeignKey and ManyToMany fields.
    """
    if obj is None:
        return None

    if not hasattr(obj, '_meta'):
        # Not a model instance, return primitive types directly
        if isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        if isinstance(obj, (list, tuple)):
            return [model_to_json_safe(x) for x in obj]
        if isinstance(obj, dict):
            return {k: model_to_json_safe(v) for k, v in obj.items()}
        return str(obj)  # fallback for unknown types

    data = {}
    for field in obj._meta.get_fields():
        if getattr(field, 'auto_created', False) and not getattr(field, 'concrete', True):
            continue  # skip reverse/auto fields
        if getattr(field, 'many_to_many', False):
            m2m_qs = getattr(obj, field.name).all()
            data[field.name] = [x.pk for x in m2m_qs]
            continue
        value = getattr(obj, field.name, None)
        # If value is a model, use pk
        if hasattr(value, '_meta'):
            data[field.name] = value.pk
        else:
            data[field.name] = model_to_json_safe(value)
    return data


@require_http_methods(["GET"])
def analysis_list(request):
    analyses = Analysis.objects.select_related('sequencing_run', 'sample').all()
    return render(request, 'analysis/analysis_list.html', {'analyses': analyses})


@require_http_methods(["GET"])
def analyses_for_run(request, run_id):
    run = get_object_or_404(SequencingRun, run_id=run_id)
    analyses = Analysis.objects.filter(sequencing_run=run).select_related('sample')
    return render(request, 'analysis/analysis_list.html', {'analyses': analyses, 'run': run})


def _model_to_dict_safe(obj):
    """
    Convert a Django model instance to a dict, excluding private/internal attributes.
    Only includes fields that don't start with underscore.
    Returns None if obj is None.
    """
    if obj is None:
        return None
    
    data = {}
    if hasattr(obj, '_meta'):
        # Use model's concrete fields to build dict
        for field in obj._meta.get_fields():
            # Skip reverse relations, m2m, and auto-created fields
            if getattr(field, 'auto_created', False) and not getattr(field, 'concrete', True):
                continue
            if getattr(field, 'many_to_many', False):
                continue
            
            field_name = getattr(field, 'name', None)
            # Skip private/internal attributes
            if not field_name or field_name.startswith('_'):
                continue
            
            try:
                value = getattr(obj, field_name)
                data[field_name] = value
            except Exception:
                pass
    
    return data

@require_http_methods(["GET"])

def analysis_detail(request, analysis_id):
    """
    JSON API endpoint for Analysis details.
    """
    try:
        analysis = Analysis.objects.get(pk=analysis_id)
    except Analysis.DoesNotExist:
        return JsonResponse({'error': 'Analysis not found'}, status=404)

    response_data = {
        'id': analysis.pk,
        'name': str(analysis.analysis_id),  # ensure string
    }

    # Add metrics safely
    for metric_attr in ('expression_metrics', 'alignment_metrics', 'variant_metrics', 'qc_metrics'):
        metric_obj = getattr(analysis, metric_attr, None)
        if metric_obj:
            response_data[metric_attr] = model_to_json_safe(metric_obj)

    return JsonResponse(
    response_data,
    encoder=DjangoJSONEncoder,
    json_dumps_params={'indent': 4}  # <-- THIS MAKES JSON PRETTY
)


    # Build response with base analysis info
    response_data = {
        'id': analysis.pk,
        'name': analysis.analysis_id,
    }
    
    # Add metrics only if they exist
    for metric_attr in ('expression_metrics', 'alignment_metrics', 'variant_metrics', 'qc_metrics'):
        metric_obj = getattr(analysis, metric_attr, None)
        metric_dict = _model_to_dict_safe(metric_obj)
        # Only include in response if the metric exists and has data
        if metric_dict:
            response_data[metric_attr] = metric_dict
    
    return JsonResponse(response_data, encoder=DjangoJSONEncoder)
