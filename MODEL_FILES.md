# 📦 Archivos del Modelo - Instrucciones

## ⚠️ Archivos NO incluidos en GitHub

Los siguientes archivos NO están incluidos en el repositorio debido a su tamaño:

- `malware_detector_rf.pkl` (~50MB)
- `feature_columns.pkl` (~5KB)
- `TotalFeatures-ISCXFlowMeter.csv` (~150MB)
- `Random_Forest.ipynb` (notebook original)

## 📥 GUÍA PASO A PASO: Google Drive + Render

### **Paso 1: Subir archivos a Google Drive**

1. Ve a https://drive.google.com/
2. Sube estos 2 archivos:
   - `malware_detector_rf.pkl`
   - `feature_columns.pkl`

### **Paso 2: Obtener enlaces de descarga directa**

Para **CADA archivo**:

1. **Click derecho** en el archivo → **"Compartir"**
2. Click en **"Cambiar a cualquier persona con el enlace"**
3. Asegúrate que diga: **"Cualquier persona con el enlace puede ver"**
4. Click en **"Copiar enlace"**

Tendrás algo como:
```
https://drive.google.com/file/d/1AbCdEfGhIjKlMnOpQrStUvWxYz123456/view?usp=sharing
```

5. **Extrae el ID** (la parte entre `/d/` y `/view`):
```
1AbCdEfGhIjKlMnOpQrStUvWxYz123456
```

6. **Crea la URL de descarga directa**:
```
https://drive.google.com/uc?export=download&id=1AbCdEfGhIjKlMnOpQrStUvWxYz123456
```

### **Paso 3: Configurar Variables de Entorno en Render**

En Render Dashboard → Tu servicio → Settings → Environment:

**IMPORTANTE**: Usa las URLs completas que Google Drive te dio, NO las conviertas. El código ahora detecta automáticamente si es de Google Drive y extrae el ID.

```bash
# Google Drive URLs (usar las URLs originales de compartir)
MODEL_URL=https://drive.google.com/file/d/1CL1e6M_CcHBxtNZZeQppGM3oO5seQmCZ/view?usp=sharing
FEATURES_URL=https://drive.google.com/file/d/1jCvo9eddDg1s81FEdbJAo8CSCSSoBT0V/view?usp=sharing

# O puedes usar el formato corto con solo el ID
# MODEL_URL=https://drive.google.com/uc?id=1CL1e6M_CcHBxtNZZeQppGM3oO5seQmCZ
# FEATURES_URL=https://drive.google.com/uc?id=1jCvo9eddDg1s81FEdbJAo8CSCSSoBT0V

# Django Settings
PYTHON_VERSION=3.12.3
SECRET_KEY=tu-clave-secreta-super-segura-12345
DEBUG=False
ALLOWED_HOSTS=.onrender.com
```

### **Paso 4: Deploy**

El código ya está configurado para:
1. ✅ Detectar si los archivos `.pkl` existen localmente
2. ✅ Si NO existen, descargarlos automáticamente desde las URLs
3. ✅ Cargar el modelo y empezar a funcionar

**¡No necesitas hacer nada más!** El deploy automáticamente:
- Descargará los archivos desde Google Drive
- Cargará el modelo
- Estará listo para hacer predicciones

## 🔍 **Ejemplo Completo**

### Archivo: `malware_detector_rf.pkl`

1. **Enlace de Google Drive**:
   ```
   https://drive.google.com/file/d/1a2b3c4d5e6f7g8h9i0/view?usp=sharing
   ```

2. **ID extraído**:
   ```
   1a2b3c4d5e6f7g8h9i0
   ```

3. **URL de descarga directa** (para variable `MODEL_URL`):
   ```
   https://drive.google.com/uc?export=download&id=1a2b3c4d5e6f7g8h9i0
   ```

### Archivo: `feature_columns.pkl`

1. **Enlace de Google Drive**:
   ```
   https://drive.google.com/file/d/9i8h7g6f5e4d3c2b1a0/view?usp=sharing
   ```

2. **ID extraído**:
   ```
   9i8h7g6f5e4d3c2b1a0
   ```

3. **URL de descarga directa** (para variable `FEATURES_URL`):
   ```
   https://drive.google.com/uc?export=download&id=9i8h7g6f5e4d3c2b1a0
   ```

## ✅ Verificación

Después del deploy en Render, visita:
```
https://tu-app.onrender.com/api/health/
```

Deberías ver:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

Y en:
```
https://tu-app.onrender.com/api/model-info/
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

## 🚨 Troubleshooting

Si el modelo no carga:

1. **Revisa los logs en Render** → Tu servicio → Logs
2. Busca mensajes como: "Descargando archivo desde: ..."
3. Verifica que las URLs sean de **descarga directa** (con `uc?export=download`)
4. Asegúrate que los archivos en Drive sean **públicos** (cualquiera con el enlace puede ver)

