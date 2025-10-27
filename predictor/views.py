"""
Views para la API de detección de malware.
Implementa los endpoints REST siguiendo las mejores prácticas.
"""
import logging
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render

from .services import detector_service, PredictionError, ModelLoadError
from .serializers import (
    PredictionInputSerializer,
    PredictionOutputSerializer,
    ModelInfoSerializer,
    HealthCheckSerializer
)


logger = logging.getLogger(__name__)


@api_view(['GET'])
def home_view(request):
    """
    Vista principal que muestra la interfaz HTML.
    
    GET /api/
    """
    return render(request, 'predictor/home.html')


@api_view(['POST'])
def predict_malware(request):
    """
    Endpoint para realizar predicciones de malware.
    
    POST /api/predict/
    
    Request Body:
        {
            "features": {
                "feature1": value1,
                "feature2": value2,
                ...
            }
        }
    
    Response:
        {
            "prediction": 0 or 1,
            "label": "benign" or "malware",
            "confidence": [prob_benign, prob_malware],
            "confidence_percentage": 95.5
        }
    """
    try:
        # Validar datos de entrada
        input_serializer = PredictionInputSerializer(data=request.data)
        
        if not input_serializer.is_valid():
            logger.warning(f"Validación fallida: {input_serializer.errors}")
            return Response(
                {
                    'error': 'Datos de entrada inválidos',
                    'details': input_serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extraer features
        features = input_serializer.validated_data['features']
        
        # Realizar predicción
        logger.info("Iniciando predicción de malware")
        prediction_result = detector_service.predict(features)
        
        # Validar y serializar respuesta
        output_serializer = PredictionOutputSerializer(data=prediction_result)
        output_serializer.is_valid(raise_exception=True)
        
        return Response(
            output_serializer.data,
            status=status.HTTP_200_OK
        )
        
    except PredictionError as e:
        logger.error(f"Error en predicción: {str(e)}")
        return Response(
            {
                'error': 'Error en la predicción',
                'message': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    except ModelLoadError as e:
        logger.error(f"Error al cargar modelo: {str(e)}")
        return Response(
            {
                'error': 'Error al cargar el modelo',
                'message': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
    except Exception as e:
        logger.exception(f"Error inesperado: {str(e)}")
        return Response(
            {
                'error': 'Error interno del servidor',
                'message': 'Ocurrió un error inesperado'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def model_info(request):
    """
    Endpoint para obtener información del modelo cargado.
    
    GET /api/model-info/
    
    Response:
        {
            "status": "loaded",
            "model_type": "RandomForestClassifier",
            "n_features": 79,
            "feature_columns": ["feature1", "feature2", ...],
            "n_estimators": 100,
            "max_depth": null
        }
    """
    try:
        info = detector_service.get_model_info()
        
        serializer = ModelInfoSerializer(data=info)
        serializer.is_valid(raise_exception=True)
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.exception(f"Error al obtener info del modelo: {str(e)}")
        return Response(
            {
                'error': 'Error al obtener información del modelo',
                'message': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def health_check(request):
    """
    Endpoint de health check para monitoreo.
    
    GET /api/health/
    
    Response:
        {
            "status": "healthy",
            "model_loaded": true,
            "timestamp": "2025-10-26T12:00:00Z",
            "version": "1.0.0"
        }
    """
    try:
        # Intentar cargar el modelo si no está cargado
        if not detector_service.is_ready:
            try:
                detector_service.load_model()
            except Exception as load_error:
                logger.warning(f"Modelo no pudo cargarse en health check: {load_error}")
        
        health_data = {
            'status': 'healthy' if detector_service.is_ready else 'unhealthy',
            'model_loaded': detector_service.is_ready,
            'timestamp': datetime.now(),
            'version': '1.0.0'
        }
        
        serializer = HealthCheckSerializer(data=health_data)
        serializer.is_valid(raise_exception=True)
        
        response_status = (
            status.HTTP_200_OK if detector_service.is_ready 
            else status.HTTP_503_SERVICE_UNAVAILABLE
        )
        
        return Response(
            serializer.data,
            status=response_status
        )
        
    except Exception as e:
        logger.exception(f"Error en health check: {str(e)}")
        return Response(
            {
                'status': 'unhealthy',
                'model_loaded': False,
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0',
                'error': str(e)
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@api_view(['GET'])
def get_features_list(request):
    """
    Endpoint para obtener la lista completa de features requeridas.
    
    GET /api/features/
    
    Response:
        {
            "features": ["feature1", "feature2", ...],
            "total": 79
        }
    """
    try:
        if not detector_service.is_ready:
            detector_service.load_model()
        
        features = detector_service.feature_columns
        
        return Response(
            {
                'features': features,
                'total': len(features)
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.exception(f"Error al obtener features: {str(e)}")
        return Response(
            {
                'error': 'Error al obtener lista de features',
                'message': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_model_statistics(request):
    """
    Endpoint para obtener estadísticas y métricas del modelo.
    
    GET /api/statistics/
    
    Response:
        {
            "metrics": {
                "f1_score": 0.9334,
                "accuracy": 0.9346,
                "precision": 0.9334,
                "recall": 0.9346
            },
            "dataset_info": {
                "total_samples": 631955,
                "class_distribution": {...}
            }
        }
    """
    try:
        if not detector_service.is_ready:
            detector_service.load_model()
        
        stats = detector_service.get_model_statistics()
        
        return Response(
            stats,
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.exception(f"Error al obtener estadísticas: {str(e)}")
        return Response(
            {
                'error': 'Error al obtener estadísticas del modelo',
                'message': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
