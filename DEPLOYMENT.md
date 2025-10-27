# 🚀 Guía de Deployment - GitHub + Render

Esta guía te llevará paso a paso para desplegar tu API de detección de malware en Render usando GitHub.

## 📋 Prerequisitos

- ✅ Cuenta de GitHub ([crear cuenta](https://github.com/join))
- ✅ Cuenta de Render ([crear cuenta](https://render.com))
- ✅ Git instalado en tu máquina
- ✅ El modelo ya debe estar generado (ejecutar notebook primero)

---

## 🔧 PARTE 1: Preparación Local

### 1.1 Verificar que todo está en orden

```bash
# Verifica que el modelo existe
ls -la models/

# Deberías ver:
# - malware_detector_rf.pkl
# - feature_columns.pkl
```

### 1.2 Probar la API localmente (IMPORTANTE)

```bash
# Ejecutar setup
./setup.sh  # Linux/Mac
setup.bat   # Windows

# Iniciar servidor
python manage.py runserver

# Probar en otra terminal
curl http://localhost:8000/api/health/
```

Si todo funciona localmente, continúa al siguiente paso.

---

## 📦 PARTE 2: Subir a GitHub

### 2.1 Inicializar Git (si no está inicializado)

```bash
cd /home/jesus/Documentos/plf/ApiRandomForest

# Inicializar repositorio
git init

# Verificar archivos
git status
```

### 2.2 Configurar Git (primera vez)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@example.com"
```

### 2.3 Hacer el primer commit

```bash
# Agregar todos los archivos
git add .

# Verificar qué se va a subir
git status

# Hacer commit
git commit -m "Initial commit: Malware Detection API with Random Forest"
```

### 2.4 Crear repositorio en GitHub

1. Ve a [GitHub](https://github.com)
2. Click en el botón **"+"** arriba a la derecha → **"New repository"**
3. Configurar:
   - **Repository name**: `malware-detection-api` (o el nombre que prefieras)
   - **Description**: `API REST para detección de malware en Android usando Random Forest`
   - **Visibility**: Public o Private (tu elección)
   - ❌ **NO marques** "Initialize this repository with a README" (ya tenemos uno)
4. Click en **"Create repository"**

### 2.5 Conectar tu repositorio local con GitHub

GitHub te mostrará instrucciones. Usa estas:

```bash
# Agregar el remote (cambia <tu-usuario> por tu usuario de GitHub)
git remote add origin https://github.com/<tu-usuario>/malware-detection-api.git

# Renombrar la rama a main
git branch -M main

# Subir el código
git push -u origin main
```

**Ejemplo:**
```bash
git remote add origin https://github.com/jesus123/malware-detection-api.git
git branch -M main
git push -u origin main
```

🎉 ¡Tu código ya está en GitHub!

---

## 🌐 PARTE 3: Desplegar en Render

### 3.1 Crear cuenta en Render

1. Ve a [Render.com](https://render.com)
2. Click en **"Get Started"** o **"Sign Up"**
3. **Recomendado**: Sign up con tu cuenta de GitHub (más fácil)

### 3.2 Crear un nuevo Web Service

1. En el dashboard de Render, click en **"New +"** → **"Web Service"**

2. **Conectar tu repositorio:**
   - Si usaste GitHub para login: verás tus repositorios
   - Busca `malware-detection-api`
   - Click en **"Connect"**

3. **Configurar el servicio:**

   ```
   Name: malware-detection-api
   Region: Oregon (US West) o el más cercano
   Branch: main
   Root Directory: (dejar vacío)
   Environment: Python
   Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   Start Command: gunicorn malware_api.wsgi:application
   Instance Type: Free (o el que prefieras)
   ```

### 3.3 Configurar Variables de Entorno

En la sección **"Environment Variables"**, agregar:

1. Click en **"Add Environment Variable"**

2. Agregar estas variables:

   | Key | Value |
   |-----|-------|
   | `DJANGO_SECRET_KEY` | (click en "Generate Value") |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | (se llenará automáticamente después del deploy) |

### 3.4 Deploy

1. Click en **"Create Web Service"**
2. Render comenzará a construir tu aplicación
3. Espera 5-10 minutos (primera vez es más lento)
4. Verás logs en tiempo real

### 3.5 Verificar el Deploy

Una vez que el build termine:

1. Render te dará una URL como: `https://malware-detection-api.onrender.com`

2. Actualizar `ALLOWED_HOSTS`:
   - Ve a **Environment** en el panel izquierdo
   - Edita `ALLOWED_HOSTS`
   - Valor: `malware-detection-api.onrender.com` (tu URL sin https://)
   - Guardar (esto reiniciará el servicio)

3. Probar tu API:
   ```bash
   # Health check
   curl https://malware-detection-api.onrender.com/api/health/
   
   # Ver la interfaz web
   # Abre en navegador: https://malware-detection-api.onrender.com/api/
   ```

---

## 🔍 PARTE 4: Verificación y Testing

### 4.1 Verificar todos los endpoints

```bash
# Reemplaza <tu-app> con tu nombre de app

# 1. Health check
curl https://<tu-app>.onrender.com/api/health/

# 2. Model info
curl https://<tu-app>.onrender.com/api/model-info/

# 3. Features list
curl https://<tu-app>.onrender.com/api/features/

# 4. Predicción (necesitas todas las 79 features)
curl -X POST https://<tu-app>.onrender.com/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"features": {...}}'
```

### 4.2 Interfaz Web

Abre en tu navegador:
```
https://<tu-app>.onrender.com/api/
```

Deberías ver la interfaz HTML con botones para probar.

---

## 🛠️ PARTE 5: Actualizaciones Futuras

### 5.1 Hacer cambios y actualizar

```bash
# 1. Hacer cambios en tu código local
# 2. Probar localmente
python manage.py runserver

# 3. Commit los cambios
git add .
git commit -m "Descripción de los cambios"

# 4. Push a GitHub
git push origin main

# 5. Render detectará los cambios automáticamente y re-desplegará
```

### 5.2 Ver logs en Render

1. Ve a tu servicio en Render dashboard
2. Click en **"Logs"** en el panel izquierdo
3. Verás logs en tiempo real

---

## ⚠️ Troubleshooting

### Error: "Application failed to start"

1. Revisa los logs en Render
2. Verifica que todas las variables de entorno están configuradas
3. Asegúrate que el modelo `.pkl` está en el repositorio

### Error: "Model not found"

El modelo debe estar en el repositorio. Verifica:
```bash
git ls-files models/
# Debe mostrar:
# models/malware_detector_rf.pkl
# models/feature_columns.pkl
```

Si no están, agrégalos:
```bash
git add models/*.pkl
git commit -m "Add ML model files"
git push origin main
```

### Error 500 en producción

1. Activa DEBUG temporalmente:
   - En Render → Environment → `DEBUG=True`
   - Guarda y espera el reinicio
   - Revisa el error
   - ⚠️ **Recuerda volver a poner DEBUG=False**

### El sitio es muy lento

Render Free tier tiene limitaciones:
- Se duerme después de 15 min de inactividad
- Primer request tarda ~30 segundos (wake-up)
- Para mejor performance: upgrade a plan pago

---

## 📊 Métricas y Monitoreo

### Ver estadísticas en Render

1. Dashboard → Tu servicio
2. Pestaña **"Metrics"**
3. Verás: CPU, memoria, requests, etc.

### Health checks automáticos

Render hace ping a `/api/health/` automáticamente para verificar que tu app está corriendo.

---

## 🎓 Recursos Adicionales

- [Documentación de Render](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Django REST Framework](https://www.django-rest-framework.org/)

---

## ✅ Checklist Final

Antes de considerar el deployment completo:

- [ ] ✅ Código en GitHub
- [ ] ✅ Service creado en Render
- [ ] ✅ Variables de entorno configuradas
- [ ] ✅ Build exitoso
- [ ] ✅ `/api/health/` retorna 200
- [ ] ✅ `/api/model-info/` muestra info del modelo
- [ ] ✅ Interfaz web funciona
- [ ] ✅ README.md actualizado con la URL de producción
- [ ] ✅ DEBUG=False en producción

---

## 🎉 ¡Felicidades!

Tu API está desplegada y funcionando en producción. Ahora puedes:

1. Compartir la URL con otros
2. Integrarla en aplicaciones front-end
3. Usar el endpoint de predicción en aplicaciones reales
4. Monitorear su uso en Render dashboard

**URL de tu API:** `https://<tu-app>.onrender.com/api/`

---

**¿Preguntas o problemas?** Abre un issue en tu repositorio de GitHub.
