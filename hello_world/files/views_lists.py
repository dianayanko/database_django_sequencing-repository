from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import FileMetadata


@require_http_methods(["GET"])
def files_list(request):
    files = FileMetadata.objects.all()
    return render(request, 'files/files_list.html', {'files': files})
