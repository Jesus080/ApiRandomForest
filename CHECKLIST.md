# ✅ CHECKLIST - Antes de Desplegar

Usa este checklist para asegurarte de que todo está listo antes de hacer el deploy.

## 📋 Fase 1: Preparación Local

### ✅ Modelo de Machine Learning

- [ ] ✓ Ejecutar todas las celdas del notebook `Random_Forest.ipynb`
- [ ] ✓ Verificar que existe `models/malware_detector_rf.pkl`
- [ ] ✓ Verificar que existe `models/feature_columns.pkl`
- [ ] ✓ El modelo tiene ~79 features

```bash
# Verificar modelos
ls -lh models/
```

### ✅ Instalación y Configuración

- [ ] ✓ Python 3.12.3 instalado
- [ ] ✓ Ejecutar `./setup.sh` (Linux/Mac) o `setup.bat` (Windows)
- [ ] ✓ Entorno virtual creado en `venv/`
- [ ] ✓ Todas las dependencias instaladas correctamente
- [ ] ✓ Migraciones aplicadas (`python manage.py migrate`)
- [ ] ✓ Archivos estáticos recolectados

```bash
# Verificar instalación
python --version
pip list | grep Django
```

### ✅ Pruebas Locales

- [ ] ✓ Servidor se inicia sin errores: `python manage.py runserver`
- [ ] ✓ Endpoint health check funciona: `curl http://localhost:8000/api/health/`
- [ ] ✓ Endpoint model-info funciona: `curl http://localhost:8000/api/model-info/`
- [ ] ✓ Endpoint features funciona: `curl http://localhost:8000/api/features/`
- [ ] ✓ Interfaz web carga: `http://localhost:8000/api/`
- [ ] ✓ Botones de prueba en la web funcionan

```bash
# Probar todos los endpoints
python example_client.py
```

### ✅ Tests Unitarios

- [ ] ✓ Tests pasan sin errores: `python manage.py test predictor`
- [ ] ✓ No hay warnings críticos

```bash
# Ejecutar tests
python manage.py test predictor -v 2
```

---

## 📦 Fase 2: Preparación para Git

### ✅ Verificar Archivos

- [ ] ✓ `.gitignore` está presente y correcto
- [ ] ✓ `venv/` NO se va a subir (está en .gitignore)
- [ ] ✓ `db.sqlite3` NO se va a subir (está en .gitignore)
- [ ] ✓ `__pycache__/` NO se va a subir
- [ ] ✓ Archivos `.pkl` del modelo SÍ se van a subir

```bash
# Verificar qué se va a subir
git status
git add .
git status
```

### ✅ Archivos Esenciales Presentes

- [ ] ✓ `requirements.txt`
- [ ] ✓ `runtime.txt`
- [ ] ✓ `render.yaml`
- [ ] ✓ `build.sh`
- [ ] ✓ `manage.py`
- [ ] ✓ `README.md`
- [ ] ✓ Archivos del modelo en `models/`

### ✅ Git Configuración

- [ ] ✓ Git inicializado: `git init`
- [ ] ✓ Usuario configurado: `git config user.name "Tu Nombre"`
- [ ] ✓ Email configurado: `git config user.email "tu@email.com"`
- [ ] ✓ Primer commit hecho: `git commit -m "Initial commit"`

```bash
# Verificar configuración
git config --list
git log --oneline
```

---

## 🌐 Fase 3: GitHub

### ✅ Repositorio en GitHub

- [ ] ✓ Repositorio creado en GitHub
- [ ] ✓ Nombre del repo: `malware-detection-api` (o tu preferencia)
- [ ] ✓ Remote agregado: `git remote add origin <URL>`
- [ ] ✓ Código subido: `git push -u origin main`
- [ ] ✓ Todos los archivos visibles en GitHub

```bash
# Verificar remote
git remote -v

# Push
git push -u origin main
```

### ✅ Verificar en GitHub Web

- [ ] ✓ README.md se muestra correctamente
- [ ] ✓ Carpeta `models/` con archivos `.pkl`
- [ ] ✓ Carpeta `malware_api/`
- [ ] ✓ Carpeta `predictor/`
- [ ] ✓ `requirements.txt` presente
- [ ] ✓ No hay archivos `.pyc` o `__pycache__`

---

## 🚀 Fase 4: Render Deployment

### ✅ Cuenta y Conexión

- [ ] ✓ Cuenta creada en [Render.com](https://render.com)
- [ ] ✓ GitHub conectado a Render
- [ ] ✓ Repositorio `malware-detection-api` visible en Render

### ✅ Configuración del Web Service

- [ ] ✓ Web Service creado
- [ ] ✓ **Name**: malware-detection-api
- [ ] ✓ **Environment**: Python
- [ ] ✓ **Branch**: main
- [ ] ✓ **Build Command**: 
  ```
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
  ```
- [ ] ✓ **Start Command**: 
  ```
  gunicorn malware_api.wsgi:application
  ```
- [ ] ✓ **Instance Type**: Free (o el que elijas)

### ✅ Variables de Entorno

- [ ] ✓ `DJANGO_SECRET_KEY` - generada automáticamente
- [ ] ✓ `DEBUG` - valor: `False`
- [ ] ✓ `ALLOWED_HOSTS` - actualizado después del primer deploy

### ✅ Primer Deploy

- [ ] ✓ Deploy iniciado (puede tardar 5-10 minutos)
- [ ] ✓ Build completado sin errores
- [ ] ✓ Service en estado "Live"
- [ ] ✓ URL asignada: `https://tu-app.onrender.com`

---

## 🔍 Fase 5: Verificación en Producción

### ✅ Endpoints Funcionando

- [ ] ✓ Health check: `https://tu-app.onrender.com/api/health/`
- [ ] ✓ Model info: `https://tu-app.onrender.com/api/model-info/`
- [ ] ✓ Features: `https://tu-app.onrender.com/api/features/`
- [ ] ✓ Home page: `https://tu-app.onrender.com/api/`

```bash
# Probar endpoints
curl https://tu-app.onrender.com/api/health/
curl https://tu-app.onrender.com/api/model-info/
curl https://tu-app.onrender.com/api/features/
```

### ✅ Interfaz Web

- [ ] ✓ Página HTML carga correctamente
- [ ] ✓ Estilos CSS se aplican
- [ ] ✓ Botones de prueba funcionan
- [ ] ✓ JavaScript funciona (fetch API)

### ✅ Funcionalidad ML

- [ ] ✓ Modelo está cargado (model_loaded: true)
- [ ] ✓ Número correcto de features (79)
- [ ] ✓ Predicciones funcionan (POST /api/predict/)

### ✅ Logs y Monitoreo

- [ ] ✓ Revisar logs en Render dashboard
- [ ] ✓ No hay errores 500
- [ ] ✓ No hay warnings críticos
- [ ] ✓ Tiempo de respuesta aceptable

---

## 📝 Fase 6: Documentación Final

### ✅ README Actualizado

- [ ] ✓ URL de producción agregada al README
- [ ] ✓ Ejemplos actualizados con URL real
- [ ] ✓ Badges agregados (opcional)

```markdown
<!-- Agregar al README.md -->
## 🌐 Demo en Vivo

**URL de Producción**: https://tu-app.onrender.com/api/
```

### ✅ Commit y Push

- [ ] ✓ Cambios commiteados
- [ ] ✓ Push a GitHub
- [ ] ✓ Render detecta cambios y re-despliega

```bash
git add README.md
git commit -m "Update README with production URL"
git push origin main
```

---

## 🎓 Fase 7: Extras (Opcionales)

### ✅ Mejoras Adicionales

- [ ] ⭐ Agregar badges al README (build status, version, etc.)
- [ ] ⭐ Configurar dominio personalizado
- [ ] ⭐ Agregar más tests unitarios
- [ ] ⭐ Configurar CI/CD con GitHub Actions
- [ ] ⭐ Agregar rate limiting
- [ ] ⭐ Implementar autenticación con tokens
- [ ] ⭐ Agregar cache con Redis
- [ ] ⭐ Configurar PostgreSQL en lugar de SQLite

### ✅ Documentación Adicional

- [ ] ⭐ Crear video demo
- [ ] ⭐ Escribir artículo de blog
- [ ] ⭐ Agregar más ejemplos de uso
- [ ] ⭐ Crear colección de Postman

---

## ⚠️ Troubleshooting Checklist

Si algo falla, verifica:

### Error en Build
- [ ] ✓ `requirements.txt` está correcto
- [ ] ✓ `runtime.txt` tiene versión correcta de Python
- [ ] ✓ Build command está bien escrito
- [ ] ✓ Revisar logs de build en Render

### Error 500 en Producción
- [ ] ✓ `DEBUG=False` configurado
- [ ] ✓ `ALLOWED_HOSTS` incluye tu URL de Render
- [ ] ✓ Archivos estáticos recolectados
- [ ] ✓ Modelo `.pkl` está en el repo

### Modelo No Carga
- [ ] ✓ Archivos `.pkl` están en `models/`
- [ ] ✓ Archivos `.pkl` se subieron a GitHub
- [ ] ✓ Path del modelo es correcto en settings
- [ ] ✓ Revisar logs para ver error específico

### Endpoints No Responden
- [ ] ✓ URLs configuradas correctamente
- [ ] ✓ CORS habilitado si llamas desde navegador
- [ ] ✓ Método HTTP correcto (GET/POST)
- [ ] ✓ Content-Type: application/json

---

## ✅ Checklist Final de Deploy

**Antes de considerar el proyecto completo, marca TODO:**

- [ ] ✅ Código funciona localmente
- [ ] ✅ Tests pasan
- [ ] ✅ Código en GitHub
- [ ] ✅ Desplegado en Render
- [ ] ✅ Todos los endpoints funcionan en producción
- [ ] ✅ Interfaz web accesible
- [ ] ✅ Modelo carga correctamente
- [ ] ✅ Logs sin errores críticos
- [ ] ✅ README actualizado con URL
- [ ] ✅ Documentación completa

---

## 🎉 ¡Felicidades!

Si todos los items están marcados, ¡tu API está completamente desplegada y funcionando!

**URL de tu API**: `https://tu-app.onrender.com/api/`

---

**📅 Fecha de completado**: _________________

**🔗 URL de producción**: _________________

**📊 Estado**: ☐ En desarrollo | ☐ En testing | ☐ En producción

---

_Mantén este checklist como referencia para futuros deploys o actualizaciones._
