"""
URL routing for files app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import FileMetadataViewSet, FileAssociationViewSet

router = DefaultRouter()
router.register(r'file-metadata', FileMetadataViewSet, basename='file-metadata')
router.register(r'file-associations', FileAssociationViewSet, basename='file-association')

urlpatterns = [
    path('', include(router.urls)),
]

from .views_lists import files_list

urlpatterns += [
    path('list/', files_list, name='files_list'),
]
