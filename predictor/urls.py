"""
URLs para la app predictor.
"""
from django.urls import path
from . import views


app_name = 'predictor'

urlpatterns = [
    # Vista principal
    path('', views.home_view, name='home'),
    
    # Endpoints de predicción
    path('predict/', views.predict_malware, name='predict'),
    
    # Endpoints de información
    path('model-info/', views.model_info, name='model-info'),
    path('health/', views.health_check, name='health'),
    path('features/', views.get_features_list, name='features'),
    path('statistics/', views.get_model_statistics, name='statistics'),
]
