from django.urls import path
from . import views
from .classviews.pipeline_view import PipelineView

urlpatterns = [
    path('execute-code/', views.execute_code, name='execute_code'),
    path('execute-pipeline/', PipelineView.as_view(), name='execute_pipeline')
]
