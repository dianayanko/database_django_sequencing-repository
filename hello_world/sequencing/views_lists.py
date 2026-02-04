from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import SequencingProject, SequencingRun, LibraryPreparation


@require_http_methods(["GET"])
def project_list(request):
    projects = SequencingProject.objects.all()
    return render(request, 'sequencing/project_list.html', {'projects': projects})


@require_http_methods(["GET"])
def project_detail(request, project_id):
    """Display detailed information about a single project."""
    from django.db.models import Prefetch
    from hello_world.analysis.models import Analysis
    
    # Fetch project with samples
    project = get_object_or_404(
        SequencingProject.objects.prefetch_related('samples'),
        project_id=project_id
    )
    
    # Prefetch analyses for runs
    analyses_prefetch = Prefetch(
        'analyses',
        Analysis.objects.all()
    )
    
    # Prefetch runs with platform and sample, including analyses
    runs_prefetch = Prefetch(
        'sequencing_runs',
        SequencingRun.objects.select_related('platform', 'sample').prefetch_related(analyses_prefetch)
    )
    
    # Re-fetch project with all relations
    project = SequencingProject.objects.filter(project_id=project_id).prefetch_related(
        runs_prefetch,
        'samples'
    ).first()
    
    if not project:
        return get_object_or_404(SequencingProject, project_id=project_id)
    
    context = {
        'project': project,
        'title': f'Project: {project.project_id}',
    }
    return render(request, 'sequencing/project_detail.html', context)


@require_http_methods(["GET"])
def sequencing_run_list(request):
    runs = SequencingRun.objects.select_related('project', 'sample').all()
    return render(request, 'sequencing/run_list.html', {'runs': runs})


@require_http_methods(["GET"])
def library_prep_list(request):
    preps = LibraryPreparation.objects.all()
    return render(request, 'sequencing/library_prep_list.html', {'preps': preps})
