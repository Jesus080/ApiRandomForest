"""
Serializers para la API de detección de malware.
Valida y serializa los datos de entrada y salida.
"""
from rest_framework import serializers


class PredictionInputSerializer(serializers.Serializer):
    """
    Serializer para validar los datos de entrada de la predicción.
    
    Acepta un diccionario con las features de tráfico de red.
    Las features específicas se validan dinámicamente basándose 
    en las columnas del modelo cargado.
    """
    
    # Campo genérico que acepta cualquier dato JSON
    features = serializers.JSONField(
        help_text="Diccionario con todas las features de tráfico de red requeridas"
    )
    
    def validate_features(self, value):
        """
        Valida que features sea un diccionario con valores numéricos.
        
        Args:
            value: Diccionario de features
            
        Returns:
            Diccionario validado
            
        Raises:
            ValidationError: Si el formato no es correcto
        """
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "Las features deben ser un diccionario"
            )
        
        # Validar que todos los valores sean numéricos
        for key, val in value.items():
            if not isinstance(val, (int, float)):
                try:
                    float(val)
                except (ValueError, TypeError):
                    raise serializers.ValidationError(
                        f"El valor de '{key}' debe ser numérico, se recibió: {type(val).__name__}"
                    )
        
        return value


class PredictionOutputSerializer(serializers.Serializer):
    """
    Serializer para la respuesta de la predicción.
    """
    
    prediction = serializers.IntegerField(
        help_text="Predicción: 0 para benigno, 1 para malware"
    )
    label = serializers.CharField(
        help_text="Etiqueta de la predicción: 'benign' o 'malware'"
    )
    confidence = serializers.ListField(
        child=serializers.FloatField(),
        help_text="Array de probabilidades [prob_benigno, prob_malware]"
    )
    confidence_percentage = serializers.FloatField(
        help_text="Porcentaje de confianza de la predicción"
    )


class ModelInfoSerializer(serializers.Serializer):
    """
    Serializer para la información del modelo.
    """
    
    status = serializers.CharField(
        help_text="Estado del modelo: 'loaded' o 'not_loaded'"
    )
    model_type = serializers.CharField(
        required=False,
        help_text="Tipo de modelo de ML utilizado"
    )
    n_features = serializers.IntegerField(
        required=False,
        help_text="Número de features que requiere el modelo"
    )
    feature_columns = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Lista de nombres de las features (primeras 10)"
    )
    n_estimators = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Número de árboles en el Random Forest"
    )
    max_depth = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Profundidad máxima de los árboles"
    )
    message = serializers.CharField(
        required=False,
        help_text="Mensaje adicional sobre el estado"
    )


class HealthCheckSerializer(serializers.Serializer):
    """
    Serializer para el health check de la API.
    """
    
    status = serializers.CharField(
        help_text="Estado de la API: 'healthy' o 'unhealthy'"
    )
    model_loaded = serializers.BooleanField(
        help_text="Indica si el modelo está cargado correctamente"
    )
    timestamp = serializers.DateTimeField(
        help_text="Timestamp del health check"
    )
    version = serializers.CharField(
        help_text="Versión de la API"
    )
