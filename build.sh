#!/usr/bin/env bash
# Build script para Render

echo "🔨 Iniciando build..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
python manage.py migrate --noinput

echo "✅ Build completado exitosamente!"
