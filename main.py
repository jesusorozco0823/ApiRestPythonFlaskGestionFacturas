import os, json
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask

# Cargar credenciales desde variable de entorno (GOOGLE_CREDENTIALS)
cred_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

# Cliente Firestore
db = firestore.client()


app = Flask(__name__)

FACTURAS_COL = "facturas"

# --- Endpoints API ---
@app.route("/api/facturas", methods=["GET"])
def get_facturas():
    """Obtener todas las facturas o filtradas por día/forma"""
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

    docs = query.stream()
    facturas = [doc.to_dict() | {"id": doc.id} for doc in docs]

    return jsonify(facturas), 200


@app.route("/api/facturas", methods=["POST"])
def add_factura():
    """Agregar una nueva factura"""
    data = request.json
    ref = db.collection(FACTURAS_COL).add(data)
    return jsonify({"status": "ok", "id": ref[1].id}), 201


@app.route("/api/facturas/<id>", methods=["DELETE"])
def delete_factura(id):
    """Eliminar una factura por id"""
    db.collection(FACTURAS_COL).document(id).delete()
    return jsonify({"status": "ok", "id": id}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
