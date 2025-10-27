# 📦 Archivos del Modelo - Instrucciones

## ⚠️ Archivos NO incluidos en GitHub

Los siguientes archivos NO están incluidos en el repositorio debido a su tamaño:

- `malware_detector_rf.pkl` (~50MB)
- `feature_columns.pkl` (~5KB)
- `TotalFeatures-ISCXFlowMeter.csv` (~150MB)
- `Random_Forest.ipynb` (notebook original)

## 📥 Cómo obtener los archivos del modelo

### Opción 1: Google Drive / Dropbox (Recomendado para Render)

1. Sube los archivos `.pkl` a Google Drive o Dropbox
2. Obtén un enlace de descarga directo
3. Configura las variables de entorno en Render:
   ```
   MODEL_URL=https://drive.google.com/uc?export=download&id=TU_FILE_ID
   FEATURES_URL=https://drive.google.com/uc?export=download&id=TU_FILE_ID
   ```

### Opción 2: Subir manualmente a Render

1. Después del deploy, usa Render Shell
2. Sube los archivos directamente al servidor

### Opción 3: Entrenar el modelo nuevamente

Si tienes el dataset `TotalFeatures-ISCXFlowMeter.csv`:

```bash
# En tu entorno local
python manage.py shell
```

```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Cargar dataset
df = pd.read_csv('TotalFeatures-ISCXFlowMeter.csv')

# Preparar datos
X = df.drop('Label', axis=1)
y = df['Label']

# Entrenar modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Guardar modelo
with open('malware_detector_rf.pkl', 'wb') as f:
    pickle.dump(model, f)

# Guardar columnas
with open('feature_columns.pkl', 'wb') as f:
    pickle.dump(list(X.columns), f)
```

## 🚀 Para Deploy en Render

### Método Recomendado: Variables de Entorno

Agrega estas variables en Render:

```
MODEL_URL=<url_de_descarga_directa_del_modelo>
FEATURES_URL=<url_de_descarga_directa_de_features>
```

Luego, modifica `services.py` para descargar los archivos automáticamente:

```python
import os
import requests

def download_model_files():
    model_url = os.environ.get('MODEL_URL')
    features_url = os.environ.get('FEATURES_URL')
    
    if model_url:
        response = requests.get(model_url)
        with open('malware_detector_rf.pkl', 'wb') as f:
            f.write(response.content)
    
    if features_url:
        response = requests.get(features_url)
        with open('feature_columns.pkl', 'wb') as f:
            f.write(response.content)
```

## 📂 Ubicación de los archivos

Los archivos `.pkl` deben estar en el directorio raíz del proyecto:

```
ApiRandomForest/
├── malware_detector_rf.pkl    ← Aquí
├── feature_columns.pkl         ← Aquí
├── manage.py
├── predictor/
└── ...
```

## ✅ Verificación

Para verificar que los archivos están correctamente cargados:

```bash
curl http://localhost:8000/api/model-info/
```

Deberías ver:
```json
{
  "status": "loaded",
  "model_type": "RandomForestClassifier",
  "n_features": 79,
  ...
}
```
