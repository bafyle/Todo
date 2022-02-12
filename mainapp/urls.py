from django.urls import path
from .views import create_view, filter_view, overview_view, delete_view, update_view, update_complete_view

app_name = 'api'

urlpatterns = [
    path('overview/', overview_view, name='api-overview'),
    path('create/', create_view, name='api-create'),
    path('delete/<slug:id>/', delete_view, name='api-delete'),
    path('update/<slug:id>/', update_view, name='api-update'),
    path('update-completeness/<slug:id>/', update_complete_view, name='api-update-complete'),
    path('filter/', filter_view, name='api-filter'),
]