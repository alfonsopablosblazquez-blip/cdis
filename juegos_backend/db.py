import psycopg2
import psycopg2.extras

# Aqui pones tus datos para la conexion con postgresql (estos eran los nuestros)
DB_NAME = "gamesdb_i10j"
DB_USER = "postgres_cdis"       
DB_PASSWORD = "3kwrvXknIg2x9vNnxOiyNCiQueZEG63i"   
DB_HOST = "dpg-d4u0hcm3jp1c73f6ued0-a"
DB_PORT = "5432"


# crea gamesdb si no existe
def create_database_if_not_exists():
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
    exists = cur.fetchone()
    if not exists:
        print(f" Creando base de datos '{DB_NAME}'...")
        cur.execute(f'CREATE DATABASE "{DB_NAME}";')
    cur.close()
    conn.close()

# para conectar a la base de datos principal cada vez que se necesite
def get_connection():
     return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


# crela la tabla games si no existe
def init_db():
    create_database_if_not_exists()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            anio INTEGER,
            imagen TEXT,
            url TEXT,
            esinterno BOOLEAN DEFAULT FALSE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# se insertan los juegos que ya teniamos en el proyecto para tener como base
def insert_default_games():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM games;")
    count = cur.fetchone()[0]

    if count == 0:
        print("Insertando juegos iniciales...")
        default_games = [
        
        {
            "nombre": "Grand Theft Auto V",
            "descripcion": "Acción-aventura de mundo abierto",
            "anio": 2013,
            "imagen": "gtav.jpeg",
            "url": "https://es.wikipedia.org/wiki/Grand_Theft_Auto_V"
        },
        { 
            "nombre": "Super Mario Kart",
            "descripcion": "Carreras basada en la franquicia Mario, los jugadores compiten en carreras de karts usando diversos potenciadores, personajes y coches",
            "anio": 1992,
            "imagen": "H2x1_SNES_SuperMarioKart_image1280w.jpg",
            "url": "https://es.wikipedia.org/wiki/Super_Mario_Kart"
        },
        {
            "nombre": "Clash of Clans",
            "descripcion": "Estrategia y construcción de aldeas en línea, para dispositivos móviles. Desarrollado  por Supercell",
            "anio": 2012,
            "imagen": "91ORNgyTf2L.png",
            "url": "https://es.wikipedia.org/wiki/Clash_of_Clans"
        },
        {
            "nombre": "Clash Royale",
            "descripcion": "Estrategia y batalla en línea para dispositivos móviles, creado por Supercell. Basado en los personajes de Clash of Clans",
            "anio": 2016,
            "imagen": "clashroyale.png",
            "url": "https://es.wikipedia.org/wiki/Clash_Royale"

        },
        {
            "nombre": "Tres en Raya",
            "descripcion": "El “tres en raya” es un juego de tablero, en el cual el objetivo es conseguir poner tres piezas sobre el tablero (de 3 por 3 posiciones) de manera que estén en línea recta (horizontal, vertical o diagonal).",
            "anio": 2023,
            "imagen": "Tic_tac_toe.svg", 
            "url": "https://es.wikipedia.org/wiki/Tres_en_l%C3%ADnea",
            "esinterno": True
          },
          {
            "nombre": "Fall Guys",
            "descripcion": "Plataformas y battle royale gratuito. Consta de hasta 32 jugadores que compiten entre sí con distintos personajes en una serie de minijuegos seleccionados al azar",
            "anio": 2020,
            "imagen": "fg-fg-1920x1080-b25bc4113574.jpg",
            "url": "https://es.wikipedia.org/wiki/Fall_Guys"
          },
          {
            "nombre": "Valorant",
            "descripcion": "Valorant es un shooter táctico en primera persona de estilo hero shooter, desarrollado y publicado por Riot Games. ",
            "anio": 2014,
            "imagen": "valorant.png",
            "url": "https://en.wikipedia.org/wiki/Valorant"

        },        
        {
            "nombre": "Counter-Strike",
            "descripcion": "Counter-Strike (CS) es una serie de videojuegos multijugador de disparos en primera persona tácticos en los que equipos de terroristas luchan para perpetrar un acto de terror mientras que los antiterroristas intentan prevenirlo.",
            "anio": 2000,
            "imagen": "Counter-Strike.png",
            "url": "https://es.wikipedia.org/wiki/Counter-Strike_(serie)"

        },        
        {
            "nombre": "Cuphead",
            "descripcion": "Cuphead (subtitulado Don't deal with The Devil...)",
            "anio": 2017,
            "imagen": "cuphead.png",
            "url": "https://es.wikipedia.org/wiki/Cuphead"
        },
        {
            "nombre": "Crucigramas",
            "descripcion": "Un crucigrama es un pasatiempo en el que se deben descubrir palabras que se entrecruzan en una cuadrícula, a partir de unas definiciones o sugerencias que se proporcionan y de las pistas que van generándose con el conocimiento de las letras de otras palabras que hayamos acertado.",
            "anio": 100,
            "imagen": "crucigrama.png",
            "url": "https://elpais.com/juegos/crucigramas/experto/"

        } ] 
        for g in default_games:
            cur.execute("""
                INSERT INTO games (nombre, descripcion, anio, imagen, url, esinterno)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (g["nombre"], g["descripcion"], g["anio"], g["imagen"], g["url"], g.get("esinterno", False)))
        conn.commit()
        print("Juegos insertados correctamente.")
    else:
        print("Juegos ya existen, no se insertan de nuevo.")

    cur.close()
    conn.close()

