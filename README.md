# API de Gestión de Facturas (Flask + Firestore)

Esta API permite administrar facturas almacenadas en **Google Firestore**, 
desarrollada con **Python Flask** y desplegable en **Firebase Studio**.

---

## Endpoints disponibles

### 1. Obtener todas las facturas
```http
GET /api/facturas

**Ejemplo respuesta:**
```json
[
  {
    "id": "abc123",
    "factura_numero": "001",
    "cliente": "Jesus Orozco",
    "dia_semana": "Lunes",
    "forma_pago": "Efectivo",
    "valor": 120000
  },
  {
    "id": "def456",
    "factura_numero": "002",
    "cliente": "Maria Lopez",
    "dia_semana": "Martes",
    "forma_pago": "Tarjeta",
    "valor": 250000
  }
]
```

---

### 2. Filtrar facturas por **día de la semana**
```http
GET /api/facturas?dia=Lunes
```

---

### 3. Filtrar facturas por **forma de pago**
```http
GET /api/facturas?forma=Efectivo
```

---

### 4. Filtrar facturas por **día y forma de pago**
```http
GET /api/facturas?dia=Lunes&forma=Efectivo
```

---

### 5. Agregar nueva factura
```http
POST /api/facturas
Content-Type: application/json
```

**Ejemplo body:**
```json
{
  "factura_numero": "011",
  "cliente": "Juan Perez",
  "dia_semana": "Viernes",
  "forma_pago": "Tarjeta",
  "valor": 150000
}
```

**Respuesta:**
```json
{
  "status": "ok",
  "id": "XYZ987"
}
```

### 6. Eliminar una factura
```http
DELETE /api/facturas/<id>
```

## Ejemplos con cURL

- Obtener todas:
```bash
curl -X GET http://localhost:8080/api/facturas
```

- Filtrar por día:
```bash
curl -X GET "http://localhost:8080/api/facturas?dia=Lunes"
```

- Filtrar por forma:
```bash
curl -X GET "http://localhost:8080/api/facturas?forma=Efectivo"
```

- Agregar factura:
```bash
curl -X POST http://localhost:8080/api/facturas   -H "Content-Type: application/json"   -d '{"factura_numero":"012","cliente":"Laura Ruiz","dia_semana":"Jueves","forma_pago":"Transferencia","valor":180000}'
```

- Eliminar factura:
```bash
curl -X DELETE http://localhost:8080/api/facturas/<id>
```

---

## Notas importantes

- La colección en Firestore se llama **`facturas`**.  
- Cada documento debe tener estos campos:  
  - `factura_numero`  
  - `cliente`  
  - `dia_semana`  
  - `forma_pago`  
  - `valor`  

---

## Despliegue en App Engine

1. Crear archivo `app.yaml`:
```yaml
runtime: python311
entrypoint: gunicorn -b :$PORT main:app
```

2. Ejecutar:
```bash
gcloud app deploy
gcloud app browse
```

3. Obtendrás una URL pública del estilo:
```
https://<tu-proyecto>.uc.r.appspot.com/
```

---

## Autores
Jesus Daniel Orozco Orozco
Jhon Mario Castro Monterroza