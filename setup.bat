@echo off
echo 🚀 Inicializando Malware Detection API...
echo.

REM 1. Verificar Python
echo [1/6] Verificando version de Python...
python --version
if errorlevel 1 (
    echo ⚠️  Python no encontrado. Instala Python 3.12.3
    pause
    exit /b 1
)
echo ✓ Python detectado
echo.

REM 2. Crear entorno virtual
echo [2/6] Creando entorno virtual...
if not exist "venv" (
    python -m venv venv
    echo ✓ Entorno virtual creado
) else (
    echo ℹ  Entorno virtual ya existe
)
echo.

REM 3. Activar entorno virtual
echo [3/6] Activando entorno virtual...
call venv\Scripts\activate.bat
echo ✓ Entorno virtual activado
echo.

REM 4. Instalar dependencias
echo [4/6] Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo ✓ Dependencias instaladas
echo.

REM 5. Configurar Django
echo [5/6] Configurando Django...
python manage.py migrate
python manage.py collectstatic --noinput
echo ✓ Django configurado
echo.

REM 6. Verificar modelo
echo [6/6] Verificando modelo...
if exist "models\malware_detector_rf.pkl" (
    echo ✓ Modelo encontrado
) else (
    echo ⚠️  Modelo no encontrado. Ejecuta el notebook Random_Forest.ipynb primero.
)
echo.

echo 🎉 ¡Configuración completada!
echo.
echo Para iniciar el servidor:
echo   python manage.py runserver
echo.
echo La API estará disponible en:
echo   http://localhost:8000/api/
echo.
pause
