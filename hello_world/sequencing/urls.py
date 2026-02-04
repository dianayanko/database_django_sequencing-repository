"""
URL routing for sequencing app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    SequencingPlatformViewSet,
    SequencingProjectViewSet,
    LibraryPreparationViewSet,
    SequencingRunViewSet,
)

router = DefaultRouter()
router.register(r'platforms', SequencingPlatformViewSet, basename='platform')
router.register(r'projects', SequencingProjectViewSet, basename='project')
router.register(r'library-preparations', LibraryPreparationViewSet, basename='library-preparation')
router.register(r'runs', SequencingRunViewSet, basename='run')

# Web views for sequencing (simple internal UI)
from .views import sequencing_run_create_for_sample
from .views_lists import project_list, project_detail, sequencing_run_list, library_prep_list

web_urlpatterns = [
    path('samples/<str:sample_id>/runs/create/', sequencing_run_create_for_sample, name='sequencing_run_create_for_sample'),
    path('projects/list/', project_list, name='project_list'),
    path('projects/<project_id>/', project_detail, name='project_detail'),
    path('runs/list/', sequencing_run_list, name='sequencing_run_list'),
    path('library-preparations/list/', library_prep_list, name='library_prep_list'),
]

api_urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = web_urlpatterns + api_urlpatterns

