"""
Ejemplo de cómo consumir la API de Malware Detection desde Python.

Este script muestra diferentes formas de interactuar con la API.

Uso:
    python example_client.py
"""

import requests
import json
from typing import Dict, Any


class MalwareDetectionClient:
    """Cliente para interactuar con la API de detección de malware."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Inicializa el cliente.
        
        Args:
            base_url: URL base de la API (sin /api/)
        """
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api"
    
    def health_check(self) -> Dict[str, Any]:
        """
        Verifica el estado de la API.
        
        Returns:
            Diccionario con el estado de la API
        """
        response = requests.get(f"{self.api_url}/health/")
        response.raise_for_status()
        return response.json()
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Obtiene información sobre el modelo cargado.
        
        Returns:
            Diccionario con información del modelo
        """
        response = requests.get(f"{self.api_url}/model-info/")
        response.raise_for_status()
        return response.json()
    
    def get_features_list(self) -> Dict[str, Any]:
        """
        Obtiene la lista de features requeridas.
        
        Returns:
            Diccionario con la lista de features
        """
        response = requests.get(f"{self.api_url}/features/")
        response.raise_for_status()
        return response.json()
    
    def predict(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Realiza una predicción de malware.
        
        Args:
            features: Diccionario con las 79 features de tráfico de red
            
        Returns:
            Diccionario con la predicción y confianza
        """
        payload = {"features": features}
        response = requests.post(
            f"{self.api_url}/predict/",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()


def main():
    """Función principal de ejemplo."""
    
    # Inicializar cliente
    # Para producción, cambia la URL:
    # client = MalwareDetectionClient("https://tu-app.onrender.com")
    client = MalwareDetectionClient("http://localhost:8000")
    
    print("🛡️  Cliente de Malware Detection API")
    print("=" * 50)
    print()
    
    # 1. Health Check
    print("1️⃣  Verificando estado de la API...")
    try:
        health = client.health_check()
        print(f"   Estado: {health['status']}")
        print(f"   Modelo cargado: {health['model_loaded']}")
        print(f"   Versión: {health['version']}")
        print("   ✅ API funcionando correctamente")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    print()
    
    # 2. Información del Modelo
    print("2️⃣  Obteniendo información del modelo...")
    try:
        info = client.get_model_info()
        print(f"   Tipo de modelo: {info.get('model_type', 'N/A')}")
        print(f"   Features requeridas: {info.get('n_features', 'N/A')}")
        print(f"   Estimadores: {info.get('n_estimators', 'N/A')}")
        print("   ✅ Información obtenida")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    # 3. Lista de Features
    print("3️⃣  Obteniendo lista de features...")
    try:
        features_data = client.get_features_list()
        features_list = features_data['features']
        print(f"   Total de features: {features_data['total']}")
        print(f"   Primeras 5 features: {features_list[:5]}")
        print("   ✅ Features obtenidas")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    print()
    
    # 4. Ejemplo de Predicción
    print("4️⃣  Realizando predicción de ejemplo...")
    print("   ⚠️  Nota: Este es un ejemplo con valores ficticios")
    print()
    
    # Crear un diccionario con todas las features
    # En un caso real, estos valores vendrían de análisis de tráfico de red
    example_features = {feature: 0.0 for feature in features_list}
    
    # Rellenar algunas features con valores de ejemplo
    example_features.update({
        'flow_duration': 1234567.0,
        'Header_Length': 20.0,
        'Protocol Type': 6.0,
        'Duration': 5000.0,
        'Rate': 1.5,
        'Srate': 2.3,
        'fin_flag_number': 1.0,
        'syn_flag_number': 1.0,
    })
    
    try:
        result = client.predict(example_features)
        
        print(f"   Predicción: {result['label'].upper()}")
        print(f"   Confianza: {result['confidence_percentage']:.2f}%")
        print(f"   Probabilidades: Benigno={result['confidence'][0]:.4f}, "
              f"Malware={result['confidence'][1]:.4f}")
        
        if result['label'] == 'malware':
            print("   🚨 ¡ALERTA! Posible malware detectado")
        else:
            print("   ✅ Aplicación probablemente benigna")
            
    except requests.exceptions.HTTPError as e:
        print(f"   ❌ Error HTTP: {e}")
        if e.response is not None:
            print(f"   Detalle: {e.response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    print("=" * 50)
    print("✅ Ejemplo completado")


def example_batch_predictions():
    """
    Ejemplo de cómo hacer múltiples predicciones.
    """
    client = MalwareDetectionClient("http://localhost:8000")
    
    # Obtener features requeridas
    features_data = client.get_features_list()
    features_list = features_data['features']
    
    # Simular múltiples muestras
    samples = [
        {feature: i * 100.0 for i, feature in enumerate(features_list)}
        for _ in range(5)
    ]
    
    print("\n📊 Realizando predicciones por lote...")
    results = []
    
    for i, sample in enumerate(samples, 1):
        try:
            result = client.predict(sample)
            results.append(result)
            print(f"   Muestra {i}: {result['label']} "
                  f"({result['confidence_percentage']:.1f}%)")
        except Exception as e:
            print(f"   Muestra {i}: Error - {e}")
    
    # Estadísticas
    malware_count = sum(1 for r in results if r['label'] == 'malware')
    benign_count = len(results) - malware_count
    
    print(f"\n   Total analizado: {len(results)}")
    print(f"   Malware detectado: {malware_count}")
    print(f"   Benigno: {benign_count}")


if __name__ == "__main__":
    main()
    
    # Descomentar para ver el ejemplo de predicciones por lote
    # example_batch_predictions()
