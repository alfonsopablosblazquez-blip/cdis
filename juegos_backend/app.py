import os
from flask import Flask, request, jsonify, send_from_directory
from db import init_db, get_connection, insert_default_games
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Carpeta para subir imágenes
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Inicializar DB y juegos por defecto
init_db()
insert_default_games()

# Credenciales básicas
USERNAME = "admin"
PASSWORD = "admindb"

# Decorador para autenticación básica
def require_basic_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != USERNAME or auth.password != PASSWORD:
            return jsonify({"error": "No autorizado"}), 401, {
                "WWW-Authenticate": 'Basic realm="Login Required"'
            }
        return f(*args, **kwargs)
    return decorated

# Listar juegos
@app.get("/games")
def list_games():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM games ORDER BY id;")
    colnames = [desc[0] for desc in cur.description]
    data = [dict(zip(colnames, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(data)

# Obtener juego por id
@app.get("/games/<int:game_id>")
def get_game(game_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM games WHERE id = %s;", (game_id,))
    row = cur.fetchone()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    if not row:
        return jsonify({"error": "Game not found"}), 404
    return jsonify(dict(zip(colnames, row)))

# Añadir juego
@app.post("/games")
@require_basic_auth
def add_game():
    data = request.get_json()
    if not data or not data.get("nombre"):
        return jsonify({"error": "Nombre is required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO games (nombre, descripcion, anio, imagen, url, esinterno)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        data.get("nombre"),
        data.get("descripcion"),
        data.get("anio"),
        data.get("imagen"),
        data.get("url"),
        data.get("esinterno", False)
    ))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Juego añadido", "id": new_id}), 201

# Actualizar juego
@app.put("/games/<int:game_id>")
@require_basic_auth
def update_game(game_id):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE games
        SET nombre=%s, descripcion=%s, anio=%s, imagen=%s, url=%s, esinterno=%s
        WHERE id=%s RETURNING id;
    """, (
        data.get("nombre"),
        data.get("descripcion"),
        data.get("anio"),
        data.get("imagen"),
        data.get("url"),
        data.get("esinterno", False),
        game_id
    ))
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not updated:
        return jsonify({"error": "Game not found"}), 404
    return jsonify({"message": "Game updated"})

# Eliminar juego
@app.delete("/games/<int:game_id>")
@require_basic_auth
def delete_game(game_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM games WHERE id = %s RETURNING id;", (game_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        return jsonify({"error": "Game not found"}), 404
    return jsonify({"message": "Game deleted"})

# Subir imagen
@app.post("/upload-image")
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No se ha enviado ningún archivo"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    return jsonify({
        "message": "Imagen subida correctamente",
        "filename": file.filename
    }), 201

# Servir imágenes subidas
@app.get("/uploads/<filename>")
def get_uploaded_image(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        mimetype={
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".svg": "image/svg+xml",
            ".webp": "image/webp"
        }.get(os.path.splitext(filename)[1].lower(), None)
    )

if __name__ == "__main__":
    # Servidor en 0.0.0.0 para accesibilidad desde la red
    print("🚀 Servidor iniciado en http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
