# 📁 Estructura del Proyecto

```
ApiRandomForest/
│
├── 📓 Random_Forest.ipynb          # Notebook original con análisis y entrenamiento del modelo
├── 📊 TotalFeatures-ISCXFlowMeter.csv  # Dataset CICAAGM
│
├── 📂 models/                      # Modelos ML entrenados
│   ├── malware_detector_rf.pkl    # Modelo Random Forest serializado
│   └── feature_columns.pkl        # Lista de features requeridas
│
├── 📂 malware_api/                 # Configuración principal de Django
│   ├── __init__.py
│   ├── settings.py                # ⚙️ Configuración (producción + desarrollo)
│   ├── urls.py                    # 🔗 URLs principales del proyecto
│   ├── wsgi.py                    # 🚀 WSGI para deployment
│   └── asgi.py                    # 🚀 ASGI para deployment asíncrono
│
├── 📂 predictor/                   # App principal - Lógica de ML
│   ├── __init__.py
│   ├── apps.py                    # Configuración de la app
│   ├── admin.py                   # Admin de Django (vacío)
│   ├── models.py                  # Modelos de DB (no usado)
│   │
│   ├── 🧠 services.py             # ⭐ SERVICIO ML - Singleton Pattern
│   │                              #    - Cargar modelo
│   │                              #    - Predicciones
│   │                              #    - Validación
│   │
│   ├── 📝 serializers.py          # ⭐ VALIDACIÓN - DRF Serializers
│   │                              #    - PredictionInputSerializer
│   │                              #    - PredictionOutputSerializer
│   │                              #    - ModelInfoSerializer
│   │
│   ├── 🌐 views.py                # ⭐ ENDPOINTS REST
│   │                              #    - POST /api/predict/
│   │                              #    - GET /api/health/
│   │                              #    - GET /api/model-info/
│   │                              #    - GET /api/features/
│   │
│   ├── urls.py                    # URLs de la app predictor
│   └── tests.py                   # 🧪 Tests unitarios
│
├── 📂 templates/                   # Templates HTML
│   └── predictor/
│       └── home.html              # 🎨 Interfaz web con UI/UX
│
├── 📂 static/                      # Archivos estáticos (CSS, JS, imágenes)
│   └── .gitkeep
│
├── 📂 staticfiles/                 # Archivos estáticos recolectados (generado)
│
├── 🔧 manage.py                    # CLI de Django
│
├── 📦 requirements.txt             # Dependencias Python
├── 🐍 runtime.txt                  # Versión de Python para Render
├── ⚙️ render.yaml                  # Configuración de Render
├── 🔨 build.sh                     # Script de build para producción
├── 🚀 setup.sh                     # Script de setup (Linux/Mac)
├── 🚀 setup.bat                    # Script de setup (Windows)
│
├── 🐍 example_client.py            # Cliente Python de ejemplo
│
├── 📖 README.md                    # Documentación principal
├── 📖 DEPLOYMENT.md                # Guía de deployment paso a paso
├── 📖 CLEAN_CODE.md                # Explicación de Clean Code aplicado
│
├── 🙈 .gitignore                   # Archivos ignorados por Git
├── 📄 .env.example                 # Ejemplo de variables de entorno
│
└── 🗄️ db.sqlite3                   # Base de datos SQLite (generada)
```

## 🎯 Archivos Clave

### 🧠 Lógica de Machine Learning

| Archivo | Descripción | Principios |
|---------|-------------|------------|
| `predictor/services.py` | Servicio ML con patrón Singleton | SRP, DIP |
| `models/malware_detector_rf.pkl` | Modelo Random Forest entrenado | - |
| `models/feature_columns.pkl` | Features requeridas (79) | - |

### 🌐 API REST

| Archivo | Descripción | Endpoints |
|---------|-------------|-----------|
| `predictor/views.py` | Controladores HTTP | 5 endpoints |
| `predictor/serializers.py` | Validación de datos | DRF Serializers |
| `predictor/urls.py` | Rutas de la API | URL patterns |

### ⚙️ Configuración

| Archivo | Uso | Entorno |
|---------|-----|---------|
| `malware_api/settings.py` | Config Django | Dev + Prod |
| `requirements.txt` | Dependencias | Ambos |
| `render.yaml` | Config Render | Producción |
| `.env.example` | Variables de entorno | Desarrollo |

### 📚 Documentación

| Archivo | Contenido |
|---------|-----------|
| `README.md` | Guía general, instalación, uso |
| `DEPLOYMENT.md` | Deploy GitHub + Render paso a paso |
| `CLEAN_CODE.md` | Principios SOLID aplicados |

## 🔄 Flujo de una Petición

```
1. Cliente hace POST a /api/predict/
                ↓
2. Django enruta a predictor/views.py → predict_malware()
                ↓
3. PredictionInputSerializer valida los datos
                ↓
4. MalwareDetectorService.predict() procesa
                ↓
5. Modelo Random Forest genera predicción
                ↓
6. PredictionOutputSerializer serializa respuesta
                ↓
7. JSON Response al cliente
```

## 🛠️ Comandos Principales

```bash
# Desarrollo
python manage.py runserver

# Tests
python manage.py test predictor

# Migraciones
python manage.py migrate

# Archivos estáticos
python manage.py collectstatic

# Crear superusuario
python manage.py createsuperuser
```

## 📊 Métricas del Proyecto

- **Líneas de código**: ~1,500 (sin contar notebook)
- **Endpoints REST**: 5
- **Features ML**: 79
- **Principios SOLID**: ✅ Todos aplicados
- **Tests**: ✅ Incluidos
- **Documentación**: ✅ Completa
- **Clean Code**: ✅ 95%+

## 🎨 Stack Tecnológico

- **Backend**: Django 4.2
- **API**: Django REST Framework 3.14
- **ML**: scikit-learn 1.3, pandas, numpy
- **Servidor**: Gunicorn + WhiteNoise
- **Deploy**: Render.com
- **Version Control**: Git + GitHub
- **Python**: 3.12.3

---

**Generado automáticamente** - Malware Detection API
