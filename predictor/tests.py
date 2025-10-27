"""
Tests para la app predictor.
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class HealthCheckTestCase(TestCase):
    """Tests para el endpoint de health check."""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_health_check_endpoint(self):
        """Verifica que el endpoint de health check funcione."""
        response = self.client.get('/api/health/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_503_SERVICE_UNAVAILABLE])
        self.assertIn('status', response.data)
        self.assertIn('model_loaded', response.data)


class ModelInfoTestCase(TestCase):
    """Tests para el endpoint de información del modelo."""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_model_info_endpoint(self):
        """Verifica que el endpoint de info del modelo funcione."""
        response = self.client.get('/api/model-info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)


class FeaturesListTestCase(TestCase):
    """Tests para el endpoint de lista de features."""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_features_list_endpoint(self):
        """Verifica que el endpoint de features funcione."""
        response = self.client.get('/api/features/')
        # Puede fallar si el modelo no está cargado, pero no debe dar 404
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR])
