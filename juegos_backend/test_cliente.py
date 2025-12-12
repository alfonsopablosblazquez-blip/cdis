# en este .py probamos la API creada en app.py 
import requests

BASE = "http://localhost:5000"

def show(res):
    print(f"{res.status_code}: {res.text}")

# Crear
nuevo = {
    "nombre": "The Legend of Zelda",
    "descripcion": "Aventura",
    "anio": 2017,
    "imagen": "zelda.jpg",
    "url": "https://es.wikipedia.org/wiki/The_Legend_of_Zelda:_Breath_of_the_Wild",
}
r = requests.post(f"{BASE}/games", json=nuevo)
show(r)
game_id = r.json().get("id")

# Listar
r = requests.get(f"{BASE}/games")
show(r)

# Obtener
r = requests.get(f"{BASE}/games/{game_id}")
show(r)

# Actualizar 
update_data = {"nombre": "The Legend of Zelda",
    "descripcion": "Clásico de aventura",
    "anio": 2017,
    "imagen": "zelda.jpg",
    "url": "https://es.wikipedia.org/wiki/The_Legend_of_Zelda:_Breath_of_the_Wild",
}

# Borrar
r = requests.delete(f"{BASE}/games/{game_id}")
show(r)
