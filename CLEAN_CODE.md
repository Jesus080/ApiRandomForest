# 📐 Clean Code & SOLID Principles

Este documento explica cómo se aplicaron los principios de Clean Code y SOLID en la API de Malware Detection.

## 🎯 Principios Aplicados

### 1. Single Responsibility Principle (SRP)

**Cada clase tiene una única responsabilidad.**

#### ✅ Ejemplo: `MalwareDetectorService` (services.py)

```python
class MalwareDetectorService:
    """
    RESPONSABILIDAD ÚNICA: Gestionar el modelo de ML
    - Cargar el modelo
    - Realizar predicciones
    - Validar features
    """
```

**Separación de responsabilidades:**
- `services.py` → Lógica de ML
- `views.py` → Manejo de HTTP requests/responses
- `serializers.py` → Validación y serialización de datos
- `models.py` → Modelos de base de datos (vacío en este caso)

### 2. Open/Closed Principle (OCP)

**Abierto para extensión, cerrado para modificación.**

#### ✅ Ejemplo: Sistema de validación

```python
class PredictionInputSerializer(serializers.Serializer):
    """
    Puedes extender con nuevos validadores sin modificar el código base.
    """
    features = serializers.JSONField()
    
    def validate_features(self, value):
        # Validación base
        # Se puede extender sin modificar
        pass
```

### 3. Liskov Substitution Principle (LSP)

**Los subtipos deben ser sustituibles por sus tipos base.**

#### ✅ Ejemplo: Excepciones personalizadas

```python
class ModelLoadError(Exception):
    """Puede usarse donde se espere Exception"""
    pass

class PredictionError(Exception):
    """Puede usarse donde se espere Exception"""
    pass
```

### 4. Interface Segregation Principle (ISP)

**Los clientes no deben depender de interfaces que no usan.**

#### ✅ Ejemplo: Endpoints específicos

```python
# Cada endpoint hace UNA cosa específica
@api_view(['GET'])
def health_check(request):
    """Solo health check"""
    pass

@api_view(['POST'])
def predict_malware(request):
    """Solo predicciones"""
    pass
```

### 5. Dependency Inversion Principle (DIP)

**Depender de abstracciones, no de concreciones.**

#### ✅ Ejemplo: Servicio desacoplado

```python
# El view NO instancia el servicio directamente
# Usa una instancia global (podría ser inyectada)
from .services import detector_service

def predict_malware(request):
    result = detector_service.predict(features)
```

## 🧹 Clean Code Practices

### 1. Nombres Descriptivos

#### ❌ Mal
```python
def p(d):
    r = model.predict(d)
    return r
```

#### ✅ Bien
```python
def predict(self, data: Dict) -> Dict[str, any]:
    """
    Realiza una predicción de malware.
    
    Args:
        data: Diccionario con las features
        
    Returns:
        Diccionario con predicción y confianza
    """
    prediction_result = self._model.predict(input_data)
    return prediction_result
```

### 2. Funciones Pequeñas

**Cada función hace UNA cosa.**

#### ✅ Ejemplo
```python
def load_model(self):
    """Solo carga el modelo"""
    self._model = joblib.load(model_path)

def _validate_features(self, data):
    """Solo valida features"""
    if not self._is_loaded:
        raise PredictionError("Modelo no cargado")

def predict(self, data):
    """Solo predice - delega validación y preparación"""
    self._validate_features(data)
    input_df = self._prepare_input(data)
    return self._model.predict(input_df)
```

### 3. DRY (Don't Repeat Yourself)

**No repetir código.**

#### ✅ Ejemplo: Manejo de errores centralizado

```python
def predict_malware(request):
    try:
        # Lógica
        pass
    except PredictionError as e:
        return Response({'error': str(e)}, status=400)
    except ModelLoadError as e:
        return Response({'error': str(e)}, status=500)
    except Exception as e:
        return Response({'error': 'Error interno'}, status=500)
```

### 4. Type Hints

**Especificar tipos para mejor legibilidad.**

```python
def predict(self, data: Dict[str, float]) -> Dict[str, any]:
    """Tipos claros en firma de función"""
    pass

def load_model(self, 
                model_path: Optional[Path] = None,
                features_path: Optional[Path] = None) -> None:
    """Tipos opcionales donde aplique"""
    pass
```

### 5. Docstrings Descriptivos

**Documentar qué hace cada función.**

```python
def predict(self, data: Dict) -> Dict[str, any]:
    """
    Realiza una predicción de malware.
    
    Args:
        data: Diccionario con las features de la conexión de red
        
    Returns:
        Diccionario con:
            - prediction: 0 (benigno) o 1 (malware)
            - confidence: Array con probabilidades
            - label: 'benign' o 'malware'
            
    Raises:
        PredictionError: Si hay un error en la predicción
    """
```

### 6. Manejo de Errores Explícito

**Usar excepciones personalizadas.**

```python
# Definir excepciones específicas
class ModelLoadError(Exception):
    """Excepción para errores al cargar el modelo"""
    pass

class PredictionError(Exception):
    """Excepción para errores en la predicción"""
    pass

# Usar excepciones específicas
if not model_path.exists():
    raise ModelLoadError(f"Modelo no encontrado: {model_path}")
```

### 7. Logging Apropiado

**Registrar eventos importantes.**

```python
import logging

logger = logging.getLogger(__name__)

def load_model(self):
    logger.info(f"Cargando modelo desde: {model_path}")
    try:
        self._model = joblib.load(model_path)
        logger.info("Modelo cargado exitosamente")
    except Exception as e:
        logger.error(f"Error al cargar modelo: {str(e)}")
        raise
```

## 🏗️ Arquitectura en Capas

```
┌─────────────────────────────────┐
│     Capa de Presentación        │
│  (views.py - HTTP endpoints)    │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│   Capa de Validación            │
│  (serializers.py - Validation)  │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│   Capa de Negocio               │
│  (services.py - ML Logic)       │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│   Capa de Datos                 │
│  (models/ - ML Model Files)     │
└─────────────────────────────────┘
```

## 📝 Patrón Singleton

**Un solo servicio de ML en memoria.**

```python
class MalwareDetectorService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = None
            cls._instance._is_loaded = False
        return cls._instance

# Instancia global
detector_service = MalwareDetectorService()
```

**Ventajas:**
- ✅ Modelo cargado una sola vez
- ✅ Ahorro de memoria
- ✅ Respuestas más rápidas

## 🔒 Principios de Seguridad

### 1. Validación de Entrada

```python
def validate_features(self, value):
    """Valida tipos y valores"""
    if not isinstance(value, dict):
        raise ValidationError("Debe ser un diccionario")
    
    for key, val in value.items():
        if not isinstance(val, (int, float)):
            raise ValidationError(f"Valor inválido: {key}")
```

### 2. Configuración Segura

```python
# settings.py
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'default-dev-key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
```

### 3. Manejo de Errores sin Exponer Detalles

```python
except Exception as e:
    logger.exception(f"Error detallado: {str(e)}")
    # Al usuario solo mensaje genérico
    return Response(
        {'error': 'Error interno del servidor'},
        status=500
    )
```

## 📊 Convenciones de Código

### Nombres de Variables
- **snake_case** para funciones y variables
- **PascalCase** para clases
- **UPPER_CASE** para constantes

```python
# Variables y funciones
model_path = Path("models/")
def load_model(): pass

# Clases
class MalwareDetectorService: pass

# Constantes
MAX_FEATURES = 79
DEFAULT_TIMEOUT = 30
```

### Imports Organizados

```python
# 1. Librerías estándar
import logging
from pathlib import Path
from typing import Dict, Optional

# 2. Librerías de terceros
import joblib
import pandas as pd
from django.conf import settings

# 3. Imports locales
from .services import detector_service
from .serializers import PredictionInputSerializer
```

## ✅ Checklist de Clean Code

- [x] Nombres descriptivos y significativos
- [x] Funciones pequeñas (< 20 líneas idealmente)
- [x] Un nivel de abstracción por función
- [x] Type hints en funciones públicas
- [x] Docstrings completos
- [x] Manejo explícito de errores
- [x] Logging apropiado
- [x] Sin código duplicado (DRY)
- [x] Separación de responsabilidades
- [x] Código autodocumentado
- [x] Tests unitarios (en tests.py)
- [x] Configuración externalizada

## 🎓 Recursos de Aprendizaje

- **Libro**: "Clean Code" - Robert C. Martin
- **Libro**: "The Pragmatic Programmer" - Hunt & Thomas
- **PEP 8**: Guía de estilo de Python
- **Django Best Practices**: Django Two Scoops

---

**Recuerda:** El código se lee muchas más veces de las que se escribe. Hazlo legible, mantenible y profesional. 🚀
