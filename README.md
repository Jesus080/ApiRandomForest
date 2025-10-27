# 🛡️ Malware Detection API

API REST para detección de malware en aplicaciones Android mediante análisis de tráfico de red, utilizando un modelo Random Forest entrenado con el dataset CICAAGM.

> 📚 **[Ver Índice de Documentación Completa](INDEX.md)** | 📖 **[Guía de Deployment](DEPLOYMENT.md)** | 📐 **[Clean Code Aplicado](CLEAN_CODE.md)** | ✅ **[Checklist de Deploy](CHECKLIST.md)**

## 📋 Descripción

Esta API utiliza Machine Learning (Random Forest Classifier) para predecir si el tráfico de red de una aplicación Android es benigno o malicioso, basándose en 79 características extraídas del tráfico de red.

### Dataset

- **Nombre**: CICAAGM Android Adware and General Malware Dataset
- **Fuente**: Universidad de New Brunswick (UNB)
- **Clases**: Adware (250), Malware General (150), Benign (1500)
- **Features**: 79 características de tráfico de red

## 🚀 Características

- ✅ API REST con Django REST Framework
- ✅ Modelo Random Forest pre-entrenado
- ✅ Validación de datos con Serializers
- ✅ Arquitectura Clean Code (SOLID principles)
- ✅ Interfaz web HTML para pruebas
- ✅ Health checks y monitoring endpoints
- ✅ Configuración lista para producción
- ✅ Deploy-ready para Render

## 🛠️ Tecnologías

- **Backend**: Django 4.2, Django REST Framework
- **ML**: scikit-learn, pandas, numpy
- **Servidor**: Gunicorn + WhiteNoise
- **Python**: 3.12.3

## 📦 Instalación Local

### Requisitos Previos

- Python 3.12.3
- pip

### Pasos

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd ApiRandomForest
```

2. **Crear y activar entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar el notebook para generar el modelo**
```bash
jupyter notebook Random_Forest.ipynb
# Ejecutar todas las celdas para generar models/malware_detector_rf.pkl
```

5. **Aplicar migraciones de Django**
```bash
python manage.py migrate
```

6. **Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```

7. **Recolectar archivos estáticos**
```bash
python manage.py collectstatic --noinput
```

8. **Ejecutar el servidor**
```bash
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000`

## 🔌 Endpoints de la API

### 1. Health Check
```http
GET /api/health/
```
Verifica el estado de la API y si el modelo está cargado.

**Respuesta:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-10-26T12:00:00Z",
  "version": "1.0.0"
}
```

### 2. Información del Modelo
```http
GET /api/model-info/
```
Obtiene información sobre el modelo cargado.

**Respuesta:**
```json
{
  "status": "loaded",
  "model_type": "RandomForestClassifier",
  "n_features": 79,
  "n_estimators": 100,
  "max_depth": null
}
```

### 3. Lista de Features
```http
GET /api/features/
```
Retorna todas las features requeridas para hacer predicciones.

**Respuesta:**
```json
{
  "features": ["flow_duration", "Header_Length", ...],
  "total": 79
}
```

### 4. Predicción de Malware
```http
POST /api/predict/
Content-Type: application/json
```

**Request:**
```json
{
  "features": {
    "flow_duration": 1234567,
    "Header_Length": 20,
    "Protocol Type": 6,
    "Duration": 5000,
    ... // 79 features en total
  }
}
```

**Respuesta:**
```json
{
  "prediction": 1,
  "label": "malware",
  "confidence": [0.15, 0.85],
  "confidence_percentage": 85.0
}
```

## 📝 Ejemplos de Uso

### cURL
```bash
# Health check
curl http://localhost:8000/api/health/

# Predicción
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"features": {"flow_duration": 1234, "Header_Length": 20, ...}}'
```

### Python
```python
import requests

# Health check
response = requests.get('http://localhost:8000/api/health/')
print(response.json())

# Predicción
features = {
    "flow_duration": 1234567,
    "Header_Length": 20,
    # ... todas las 79 features
}

response = requests.post(
    'http://localhost:8000/api/predict/',
    json={'features': features}
)
result = response.json()
print(f"Resultado: {result['label']} ({result['confidence_percentage']:.2f}%)")
```

## 🏗️ Estructura del Proyecto

```
ApiRandomForest/
├── malware_api/           # Configuración principal de Django
│   ├── settings.py        # Settings con configuración para producción
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # WSGI para deployment
├── predictor/            # App principal
│   ├── services.py       # Lógica de negocio (Singleton ML Service)
│   ├── serializers.py    # Validación de datos
│   ├── views.py          # Endpoints REST
│   └── urls.py           # URLs de la app
├── templates/            # Templates HTML
│   └── predictor/
│       └── home.html     # Interfaz web
├── models/               # Modelos ML entrenados
│   ├── malware_detector_rf.pkl
│   └── feature_columns.pkl
├── manage.py             # CLI de Django
├── requirements.txt      # Dependencias Python
├── runtime.txt          # Versión de Python
├── .gitignore           # Archivos ignorados por Git
└── README.md            # Este archivo
```

## 🚢 Deploy en Render

### 1. Preparar el repositorio

1. Inicializar Git (si no está ya):
```bash
git init
git add .
git commit -m "Initial commit: Malware Detection API"
```

2. Crear repositorio en GitHub y subir:
```bash
git remote add origin <tu-repositorio-github>
git branch -M main
git push -u origin main
```

### 2. Configurar Render

1. Ir a [Render.com](https://render.com) y crear cuenta
2. Click en "New +" → "Web Service"
3. Conectar tu repositorio de GitHub
4. Configurar:
   - **Name**: malware-detection-api
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn malware_api.wsgi:application`
   - **Instance Type**: Free

5. Variables de entorno (Environment Variables):
```
DJANGO_SECRET_KEY=<tu-secret-key-segura>
DEBUG=False
ALLOWED_HOSTS=<tu-app>.onrender.com
```

6. Click en "Create Web Service"

### 3. Verificar el Deploy

Una vez desplegado, tu API estará en:
```
https://<tu-app>.onrender.com/api/
```

## 🧪 Testing

### Interfaz Web
Visita `http://localhost:8000` para acceder a la interfaz HTML con botones de prueba.

### Tests Automatizados (próximamente)
```bash
python manage.py test
```

## 📊 Modelo de Machine Learning

- **Algoritmo**: Random Forest Classifier
- **Estimadores**: 100 árboles
- **Features**: 79 características de tráfico de red
- **Métricas**: F1-Score > 0.95 en conjunto de validación
- **Datos de entrenamiento**: Dataset CICAAGM (1900 aplicaciones)

## 🔒 Seguridad

- ✅ Secret key configurable por variable de entorno
- ✅ CORS configurado
- ✅ WhiteNoise para archivos estáticos
- ✅ Validación de entrada con serializers
- ✅ Manejo robusto de excepciones
- ✅ Logging de errores

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👥 Autor

Tu Nombre - [GitHub](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- Dataset CICAAGM de la Universidad de New Brunswick
- Comunidad de Django y scikit-learn

## 📚 Referencias

- [Dataset CICAAGM](https://www.unb.ca/cic/datasets/android-adware.html)
- Paper: "Towards a Network-Based Framework for Android Malware Detection and Characterization" (PST 2017)

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!
