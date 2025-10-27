# 🧪 Ejemplos de Pruebas con cURL

Colección de comandos cURL para probar todos los endpoints de la API.

## 🌐 URLs

```bash
# Local
export API_URL="http://localhost:8000"

# Producción (reemplaza con tu URL)
export API_URL="https://tu-app.onrender.com"
```

---

## 1️⃣ Health Check

Verifica que la API esté funcionando.

```bash
curl -X GET "${API_URL}/api/health/" \
  -H "Accept: application/json"
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-10-26T12:00:00Z",
  "version": "1.0.0"
}
```

---

## 2️⃣ Model Info

Información sobre el modelo cargado.

```bash
curl -X GET "${API_URL}/api/model-info/" \
  -H "Accept: application/json"
```

**Respuesta esperada:**
```json
{
  "status": "loaded",
  "model_type": "RandomForestClassifier",
  "n_features": 79,
  "feature_columns": ["flow_duration", "Header_Length", ...],
  "n_estimators": 100,
  "max_depth": null
}
```

---

## 3️⃣ Features List

Lista completa de features requeridas.

```bash
curl -X GET "${API_URL}/api/features/" \
  -H "Accept: application/json"
```

**Respuesta esperada:**
```json
{
  "features": [
    "flow_duration",
    "Header_Length",
    "Protocol Type",
    ...
  ],
  "total": 79
}
```

---

## 4️⃣ Predicción (Ejemplo Mínimo)

**NOTA:** Este ejemplo usa valores ficticios. En producción, debes proporcionar las 79 features correctas.

```bash
curl -X POST "${API_URL}/api/predict/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "features": {
      "flow_duration": 1234567.0,
      "Header_Length": 20.0,
      "Protocol Type": 6.0,
      "Duration": 5000.0,
      "Rate": 1.5,
      "Srate": 2.3,
      "Drate": 1.8,
      "fin_flag_number": 1.0,
      "syn_flag_number": 1.0,
      "rst_flag_number": 0.0,
      "psh_flag_number": 1.0,
      "ack_flag_number": 1.0,
      "ece_flag_number": 0.0,
      "cwr_flag_number": 0.0,
      "ack_count": 5.0,
      "syn_count": 1.0,
      "fin_count": 1.0,
      "urg_count": 0.0,
      "rst_count": 0.0
    }
  }'
```

**NOTA:** Necesitas todas las 79 features. Usa el endpoint `/api/features/` para obtener la lista completa.

**Respuesta esperada:**
```json
{
  "prediction": 1,
  "label": "malware",
  "confidence": [0.15, 0.85],
  "confidence_percentage": 85.0
}
```

---

## 5️⃣ Script Completo de Pruebas

Guardar como `test_api.sh`:

```bash
#!/bin/bash

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# URL de la API (cambiar según entorno)
API_URL="${1:-http://localhost:8000}"

echo -e "${BLUE}🧪 Probando API de Malware Detection${NC}"
echo -e "${BLUE}URL: ${API_URL}${NC}"
echo ""

# 1. Health Check
echo -e "${BLUE}[1/4]${NC} Health Check..."
RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}/api/health/")
HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✓${NC} Health Check OK (HTTP $HTTP_CODE)"
    echo "$BODY" | python3 -m json.tool
else
    echo -e "${RED}✗${NC} Health Check FAILED (HTTP $HTTP_CODE)"
    echo "$BODY"
fi
echo ""

# 2. Model Info
echo -e "${BLUE}[2/4]${NC} Model Info..."
RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}/api/model-info/")
HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✓${NC} Model Info OK (HTTP $HTTP_CODE)"
    echo "$BODY" | python3 -m json.tool
else
    echo -e "${RED}✗${NC} Model Info FAILED (HTTP $HTTP_CODE)"
    echo "$BODY"
fi
echo ""

# 3. Features List
echo -e "${BLUE}[3/4]${NC} Features List..."
RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}/api/features/")
HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✓${NC} Features List OK (HTTP $HTTP_CODE)"
    TOTAL=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['total'])")
    echo "Total features: $TOTAL"
else
    echo -e "${RED}✗${NC} Features List FAILED (HTTP $HTTP_CODE)"
    echo "$BODY"
fi
echo ""

# 4. Predicción (requiere todas las features)
echo -e "${BLUE}[4/4]${NC} Predicción (ejemplo)..."
echo -e "${RED}⚠️  Esta prueba probablemente fallará si no se proporcionan todas las 79 features${NC}"
echo ""

echo -e "${GREEN}✅ Pruebas completadas${NC}"
```

Hacer ejecutable y usar:

```bash
chmod +x test_api.sh

# Local
./test_api.sh http://localhost:8000

# Producción
./test_api.sh https://tu-app.onrender.com
```

---

## 6️⃣ Obtener Features Completas

Para hacer una predicción real, primero obtén las features:

```bash
# Guardar features en archivo
curl -s "${API_URL}/api/features/" | \
  python3 -c "import sys, json; features = json.load(sys.stdin)['features']; print('\n'.join(features))" \
  > features.txt

# Ver cantidad
wc -l features.txt
```

Luego crea un JSON con todas las features:

```bash
# Crear template JSON
python3 << 'EOF'
import json

# Lista de features (obtener de /api/features/)
features = [
    "flow_duration", "Header_Length", "Protocol Type", 
    # ... agregar todas las 79 features
]

# Crear diccionario con valores de ejemplo
features_dict = {feature: 0.0 for feature in features}

# Personalizar algunos valores
features_dict.update({
    "flow_duration": 1234567.0,
    "Header_Length": 20.0,
    "Protocol Type": 6.0,
})

# Guardar como JSON
with open('prediction_request.json', 'w') as f:
    json.dump({"features": features_dict}, f, indent=2)

print("✓ Archivo prediction_request.json creado")
EOF
```

Luego usar:

```bash
curl -X POST "${API_URL}/api/predict/" \
  -H "Content-Type: application/json" \
  -d @prediction_request.json
```

---

## 7️⃣ Monitoreo y Debugging

### Ver solo código HTTP

```bash
curl -s -o /dev/null -w "%{http_code}\n" "${API_URL}/api/health/"
```

### Ver headers de respuesta

```bash
curl -I "${API_URL}/api/health/"
```

### Ver tiempo de respuesta

```bash
curl -s -o /dev/null -w "Time: %{time_total}s\n" "${API_URL}/api/health/"
```

### Verbose mode (debugging)

```bash
curl -v "${API_URL}/api/health/"
```

---

## 8️⃣ Benchmarking

Probar rendimiento con múltiples requests:

```bash
#!/bin/bash

echo "🚀 Benchmarking API..."

for i in {1..10}; do
    TIME=$(curl -s -o /dev/null -w "%{time_total}" "${API_URL}/api/health/")
    echo "Request $i: ${TIME}s"
done
```

---

## 9️⃣ Formato Pretty JSON (con jq)

Si tienes `jq` instalado:

```bash
# Instalar jq (si no lo tienes)
sudo apt install jq  # Ubuntu/Debian
brew install jq      # macOS

# Usar con curl
curl -s "${API_URL}/api/health/" | jq .
curl -s "${API_URL}/api/model-info/" | jq .
curl -s "${API_URL}/api/features/" | jq '.features | length'
```

---

## 🔟 Automatización con Postman

Alternativamente, puedes usar Postman:

1. Crear nueva colección: "Malware Detection API"
2. Agregar requests:
   - GET Health Check
   - GET Model Info
   - GET Features
   - POST Predict

3. Configurar variable de entorno:
   - Variable: `base_url`
   - Valor local: `http://localhost:8000`
   - Valor producción: `https://tu-app.onrender.com`

4. Usar `{{base_url}}/api/health/` en las URLs

---

## 📊 Respuestas de Error Comunes

### 400 Bad Request
```json
{
  "error": "Datos de entrada inválidos",
  "details": {
    "features": ["Este campo es requerido"]
  }
}
```

### 500 Internal Server Error
```json
{
  "error": "Error interno del servidor",
  "message": "Ocurrió un error inesperado"
}
```

### 503 Service Unavailable
```json
{
  "status": "unhealthy",
  "model_loaded": false,
  "timestamp": "2025-10-26T12:00:00Z",
  "version": "1.0.0"
}
```

---

**📝 Nota:** Recuerda reemplazar `${API_URL}` con tu URL real o exportar la variable de entorno.

```bash
export API_URL="https://tu-app.onrender.com"
```

---

¡Usa estos ejemplos para probar y validar tu API! 🚀
