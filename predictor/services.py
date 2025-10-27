"""
Servicio de predicción de malware.
Implementa el patrón Singleton para cargar el modelo una sola vez.
Principios SOLID aplicados: Single Responsibility Principle.
"""
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional
import joblib
import numpy as np
import pandas as pd
import requests
from django.conf import settings


logger = logging.getLogger(__name__)


class ModelLoadError(Exception):
    """Excepción personalizada para errores al cargar el modelo."""
    pass


class PredictionError(Exception):
    """Excepción personalizada para errores en la predicción."""
    pass


def download_file_from_url(url: str, destination: Path) -> bool:
    """
    Descarga un archivo desde una URL.
    
    Args:
        url: URL del archivo a descargar
        destination: Ruta donde guardar el archivo
        
    Returns:
        True si se descargó exitosamente, False en caso contrario
    """
    try:
        logger.info(f"Descargando archivo desde: {url}")
        response = requests.get(url, stream=True, timeout=300)
        response.raise_for_status()
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        logger.info(f"Archivo descargado exitosamente en: {destination}")
        return True
    except Exception as e:
        logger.error(f"Error al descargar archivo: {str(e)}")
        return False


class MalwareDetectorService:
    """
    Servicio singleton para detección de malware.
    
    Esta clase es responsable únicamente de:
    - Cargar el modelo de Machine Learning
    - Realizar predicciones
    - Validar datos de entrada
    
    Attributes:
        _instance: Instancia única del servicio (Singleton)
        _model: Modelo de Random Forest cargado
        _feature_columns: Lista de columnas esperadas por el modelo
        _is_loaded: Flag que indica si el modelo está cargado
    """
    
    _instance: Optional['MalwareDetectorService'] = None
    
    def __new__(cls):
        """Implementación del patrón Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = None
            cls._instance._feature_columns = None
            cls._instance._is_loaded = False
        return cls._instance
    
    def load_model(self, model_path: Optional[Path] = None, 
                   features_path: Optional[Path] = None) -> None:
        """
        Carga el modelo y las características desde disco.
        Si los archivos no existen y hay URLs en variables de entorno, los descarga.
        
        Args:
            model_path: Ruta al archivo del modelo
            features_path: Ruta al archivo de features
            
        Raises:
            ModelLoadError: Si no se puede cargar el modelo
        """
        if self._is_loaded:
            logger.info("Modelo ya está cargado")
            return
        
        try:
            model_path = model_path or settings.MODEL_PATH
            features_path = features_path or settings.FEATURES_PATH
            
            # Intentar descargar desde URLs si los archivos no existen
            if not model_path.exists():
                model_url = os.environ.get('MODEL_URL')
                if model_url:
                    logger.info("Modelo no encontrado localmente, descargando desde URL...")
                    if not download_file_from_url(model_url, model_path):
                        raise ModelLoadError(f"No se pudo descargar el modelo desde: {model_url}")
                else:
                    raise ModelLoadError(
                        f"Modelo no encontrado en: {model_path}. "
                        "Configura la variable de entorno MODEL_URL para descargarlo automáticamente."
                    )
            
            if not features_path.exists():
                features_url = os.environ.get('FEATURES_URL')
                if features_url:
                    logger.info("Features no encontradas localmente, descargando desde URL...")
                    if not download_file_from_url(features_url, features_path):
                        raise ModelLoadError(f"No se pudo descargar las features desde: {features_url}")
                else:
                    raise ModelLoadError(
                        f"Features no encontradas en: {features_path}. "
                        "Configura la variable de entorno FEATURES_URL para descargarlas automáticamente."
                    )
            
            logger.info(f"Cargando modelo desde: {model_path}")
            self._model = joblib.load(model_path)
            
            logger.info(f"Cargando features desde: {features_path}")
            self._feature_columns = joblib.load(features_path)
            
            self._is_loaded = True
            logger.info(f"Modelo cargado exitosamente con {len(self._feature_columns)} features")
            
        except Exception as e:
            logger.error(f"Error al cargar el modelo: {str(e)}")
            raise ModelLoadError(f"No se pudo cargar el modelo: {str(e)}")
    
    def _validate_features(self, data: Dict) -> None:
        """
        Valida que los datos de entrada contengan todas las features necesarias.
        
        Args:
            data: Diccionario con las features
            
        Raises:
            PredictionError: Si faltan features o hay features extras
        """
        if not self._is_loaded:
            raise PredictionError("El modelo no está cargado")
        
        input_features = set(data.keys())
        expected_features = set(self._feature_columns)
        
        missing_features = expected_features - input_features
        extra_features = input_features - expected_features
        
        if missing_features:
            raise PredictionError(
                f"Faltan las siguientes features: {sorted(missing_features)[:10]}..."
            )
        
        if extra_features:
            logger.warning(f"Features extra ignoradas: {sorted(extra_features)[:10]}...")
    
    def _prepare_input(self, data: Dict) -> pd.DataFrame:
        """
        Prepara los datos de entrada para el modelo.
        
        Args:
            data: Diccionario con las features
            
        Returns:
            DataFrame con las features en el orden correcto
        """
        # Crear DataFrame con las columnas en el orden correcto
        df = pd.DataFrame([data])
        df = df[self._feature_columns]
        
        # Convertir a tipos numéricos y manejar valores faltantes
        df = df.apply(pd.to_numeric, errors='coerce')
        df = df.fillna(0)
        
        return df
    
    def predict(self, data: Dict) -> Dict[str, any]:
        """
        Realiza una predicción de malware.
        
        Args:
            data: Diccionario con las features de la conexión de red
            
        Returns:
            Diccionario con:
                - prediction: 0 (benigno) o 1 (malware)
                - confidence: Array con probabilidades [prob_benigno, prob_malware]
                - label: 'benign' o 'malware'
                
        Raises:
            PredictionError: Si hay un error en la predicción
        """
        try:
            if not self._is_loaded:
                self.load_model()
            
            self._validate_features(data)
            input_df = self._prepare_input(data)
            
            # Realizar predicción
            prediction = self._model.predict(input_df)[0]
            probabilities = self._model.predict_proba(input_df)[0]
            
            result = {
                'prediction': int(prediction),
                'confidence': probabilities.tolist(),
                'label': 'malware' if prediction == 1 else 'benign',
                'confidence_percentage': float(max(probabilities) * 100)
            }
            
            logger.info(f"Predicción realizada: {result['label']} "
                       f"con {result['confidence_percentage']:.2f}% de confianza")
            
            return result
            
        except PredictionError:
            raise
        except Exception as e:
            logger.error(f"Error en la predicción: {str(e)}")
            raise PredictionError(f"Error al realizar la predicción: {str(e)}")
    
    def get_model_info(self) -> Dict[str, any]:
        """
        Obtiene información sobre el modelo cargado.
        
        Returns:
            Diccionario con información del modelo
        """
        if not self._is_loaded:
            return {
                'status': 'not_loaded',
                'message': 'El modelo no está cargado'
            }
        
        return {
            'status': 'loaded',
            'model_type': type(self._model).__name__,
            'n_features': len(self._feature_columns),
            'feature_columns': self._feature_columns[:10],  # Primeras 10 features
            'n_estimators': getattr(self._model, 'n_estimators', None),
            'max_depth': getattr(self._model, 'max_depth', None),
        }
    
    def get_model_statistics(self) -> Dict[str, any]:
        """
        Obtiene estadísticas y métricas del modelo.
        
        Returns:
            Diccionario con estadísticas del modelo entrenado
        """
        if not self._is_loaded:
            return {
                'status': 'not_loaded',
                'message': 'El modelo no está cargado'
            }
        
        # Información del modelo Random Forest
        stats = {
            'status': 'loaded',
            'model_type': type(self._model).__name__,
            'n_estimators': getattr(self._model, 'n_estimators', 100),
            'max_depth': getattr(self._model, 'max_depth', None),
            'n_features': len(self._feature_columns),
            
            # Métricas de rendimiento (valores del entrenamiento)
            # Estos son valores aproximados del notebook
            'metrics': {
                'f1_score': 0.9334,  # Del Random Forest sin escalado
                'accuracy': 0.9346,
                'precision': 0.9334,
                'recall': 0.9346
            },
            
            # Información del dataset (del notebook)
            'dataset_info': {
                'total_samples': 631955,
                'n_features': 80,  # 79 features + 1 target
                'class_distribution': {
                    'benign': {
                        'count': 471597,
                        'percentage': 74.6
                    },
                    'adware': {
                        'count': 155613,
                        'percentage': 24.6
                    },
                    'malware': {
                        'count': 4745,
                        'percentage': 0.8
                    }
                }
            },
            
            # Comparación con otros modelos
            'model_comparison': {
                'decision_tree': {
                    'f1_score': 0.9326,
                    'accuracy': 0.9330,
                    'precision': 0.9324,
                    'recall': 0.9330,
                    'performance': 'Baseline'
                },
                'random_forest': {
                    'f1_score': 0.9334,
                    'accuracy': 0.9346,
                    'precision': 0.9334,
                    'recall': 0.9346,
                    'performance': 'Mejor'
                },
                'forest_regression': {
                    'f1_score': 0.9312,
                    'accuracy': 0.9318,
                    'precision': 0.9310,
                    'recall': 0.9318,
                    'performance': 'Alternativa'
                }
            }
        }
        
        return stats
    
    @property
    def is_ready(self) -> bool:
        """Indica si el servicio está listo para hacer predicciones."""
        return self._is_loaded
    
    @property
    def feature_columns(self) -> List[str]:
        """Retorna la lista de columnas requeridas."""
        return self._feature_columns if self._is_loaded else []


# Instancia global del servicio (Singleton)
detector_service = MalwareDetectorService()
