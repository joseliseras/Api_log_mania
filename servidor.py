# servidor.py
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la base de datos
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    nombre_servicio = db.Column(db.String(50), nullable=False)
    nivel_severidad = db.Column(db.String(20), nullable=False)
    mensaje = db.Column(db.String(200), nullable=False)
    fecha_recepcion = db.Column(db.DateTime, default=datetime.utcnow)

# Endpoint para recibir logs
@app.route('/logs', methods=['POST'])
def recibir_log():
    data = request.json
    token = request.headers.get('Authorization')
    
    # Validar el token
    if not validar_token(token):
        return jsonify({"error": "Token no válido"}), 403

    # Crear un nuevo log
    nuevo_log = Log(
        fecha_evento=datetime.fromisoformat(data['timestamp']),
        nombre_servicio=data['service_name'],
        nivel_severidad=data['log_level'],
        mensaje=data['message']
    )

    # Guardar en la base de datos
    db.session.add(nuevo_log)
    db.session.commit()

    return jsonify({"mensaje": "Log recibido correctamente"}), 201

# Continuación de servidor.py

from flask import render_template  # Asegúrate de importar render_template

# Endpoint para visualizar los logs en el navegador
@app.route('/ver_logs', methods=['GET'])
def ver_logs():
    logs = Log.query.order_by(Log.fecha_evento.desc()).all()  # Ordena los logs por fecha
    return render_template('ver_logs.html', logs=logs)

# Validar tokens (simple ejemplo)
def validar_token(token):
    tokens_validos = ["token_servicio1", "token_servicio2"]
    return token.split()[-1] in tokens_validos

# Inicializar la base de datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(port=5001)
