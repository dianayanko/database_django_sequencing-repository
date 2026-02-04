"""
URL routing for samples app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import OrganismViewSet, TissueTypeViewSet, DonorViewSet, SampleViewSet
from .views import sample_list, sample_create, sample_detail, storage_overview, sample_report

# API Router
api_router = DefaultRouter()
api_router.register(r'organisms', OrganismViewSet, basename='organism')
api_router.register(r'tissue-types', TissueTypeViewSet, basename='tissue-type')
api_router.register(r'donors', DonorViewSet, basename='donor')
api_router.register(r'samples', SampleViewSet, basename='sample')

# Web URL patterns
web_urlpatterns = [
    path('list/', sample_list, name='sample_list'),
    path('create/', sample_create, name='sample_create'),
    path('<int:pk>/', sample_detail, name='sample_detail'),
    path('storage/', storage_overview, name='storage_list'),
    path('<sample_id>/report/', sample_report, name='sample_report'),
]

# API URL patterns
api_urlpatterns = [
    path('', include(api_router.urls)),
]

urlpatterns = web_urlpatterns + api_urlpatterns
