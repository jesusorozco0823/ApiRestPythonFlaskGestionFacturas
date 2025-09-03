import os, json
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger

# Cargar credenciales desde variable de entorno (GOOGLE_CREDENTIALS)
cred_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

# Cliente Firestore
db = firestore.client()


app = Flask(__name__)
CORS(app) 
Swagger(app)

FACTURAS_COL = "facturas"

@app.route("/api/facturas", methods=["GET"])
def get_facturas():
    """
    Obtener todas las facturas o filtradas por día y forma de pago
    ---
    parameters:
      - name: dia
        in: query
        type: string
        required: false
        description: Filtrar por día de la semana (ej. Lunes, Martes, etc.)
      - name: forma
        in: query
        type: string
        required: false
        description: Filtrar por forma de pago (ej. Efectivo, Tarjeta, etc.)
    responses:
      200:
        description: Lista de facturas
        examples:
          application/json: [
            {
              "id": "abc123",
              "factura_numero": "001",
              "cliente": "Juan Perez",
              "dia_semana": "Lunes",
              "forma_pago": "Efectivo",
              "valor": 120000
            }
          ]
    """
    dia = request.args.get("dia")
    forma = request.args.get("forma")

    facturas_ref = db.collection(FACTURAS_COL)

    if dia and forma:
        query = facturas_ref.where("dia_semana", "==", dia).where("forma_pago", "==", forma)
    elif dia:
        query = facturas_ref.where("dia_semana", "==", dia)
    elif forma:
        query = facturas_ref.where("forma_pago", "==", forma)
    else:
        query = facturas_ref
        
    query = query.order_by("factura_numero", direction=Query.ASCENDING)
    docs = query.stream()
    facturas = [doc.to_dict() | {"id": doc.id} for doc in docs]

    return jsonify(facturas), 200


@app.route("/api/facturas", methods=["POST"])
def add_factura():
    """
    Agregar una nueva factura
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            factura_numero:
              type: string
              example: "011"
            cliente:
              type: string
              example: "Juan Perez"
            dia_semana:
              type: string
              example: "Viernes"
            forma_pago:
              type: string
              example: "Tarjeta"
            valor:
              type: number
              example: 150000
    responses:
      201:
        description: Factura creada exitosamente
        examples:
          application/json: {
            "status": "ok",
            "id": "abc123"
          }
    """
    data = request.json
    ref = db.collection(FACTURAS_COL).add(data)
    return jsonify({"status": "ok", "id": ref[1].id}), 201


@app.route("/api/facturas/<id>", methods=["DELETE"])
def delete_factura(id):
    """
    Eliminar una factura por ID
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID del documento en Firestore
    responses:
      200:
        description: Factura eliminada exitosamente
        examples:
          application/json: {
            "status": "ok",
            "id": "abc123"
          }
    """
    db.collection(FACTURAS_COL).document(id).delete()
    return jsonify({"status": "ok", "id": id}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
