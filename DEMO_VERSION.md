# 🎭 VERSIÓN DE DEMOSTRACIÓN

## ⚠️ Modo Estático Activado

Esta versión del dashboard funciona con **datos estáticos simulados** para demostración.

### ¿Por qué datos estáticos?

Los archivos del modelo de Machine Learning (`malware_detector_rf.pkl` y `feature_columns.pkl`) son muy grandes (~50MB) y Google Drive requiere confirmación manual para descargarlos, lo que impide la descarga automática en Render.

### 📊 Datos Mostrados

El dashboard muestra:
- ✅ **631,955 muestras** del dataset CICAAGM
- ✅ **79 características** de tráfico de red
- ✅ **3 modelos ML**: Árbol de Decisión, Random Forest, Forest Regression
- ✅ **Métricas reales** del entrenamiento:
  - F1-Score: 0.9334
  - Accuracy: 0.9346
  - Precision: 0.9334
  - Recall: 0.9346

### 🎯 Funcionalidad

**LO QUE FUNCIONA:**
- ✅ Visualización completa del dashboard
- ✅ Todas las estadísticas y métricas
- ✅ Comparación de modelos
- ✅ Interfaz dark moderna
- ✅ Responsive design

**LO QUE NO FUNCIONA (temporalmente):**
- ❌ Predicciones en tiempo real (endpoint `/api/predict/`)
- ❌ Carga dinámica del modelo desde archivos

### 🔧 Para Habilitar Predicciones

Si necesitas habilitar las predicciones reales, sigue las instrucciones en [`MODEL_FILES.md`](MODEL_FILES.md) para subir los archivos del modelo usando Dropbox.

### 🚀 Deploy

Esta versión está **lista para deploy en Render** sin necesidad de configurar URLs de descarga de modelos.

**Variables de entorno necesarias:**
```bash
PYTHON_VERSION=3.12.3
SECRET_KEY=tu-clave-secreta
DEBUG=False
ALLOWED_HOSTS=.onrender.com
```

**NO necesitas:**
- ❌ MODEL_URL
- ❌ FEATURES_URL

### 📝 Notas

Esta es una **solución temporal** perfecta para:
- 🎓 Demostraciones
- 📊 Presentaciones
- 🎯 Pruebas de concepto
- 🖥️ Mostrar la interfaz y arquitectura

Para uso en producción con predicciones reales, consulta la documentación completa.

---

**Deploy URL**: https://apirandomforest.onrender.com/api/

**Repositorio**: https://github.com/Jesus080/ApiRandomForest
