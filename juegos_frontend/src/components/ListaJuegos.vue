<template>
  <div class="lista-juegos">

    <div class="acciones">
      <router-link to="/nuevo-juego" class="boton">Añadir juego ➕</router-link>
      |
      <router-link to="/subir-imagen" class="boton">Subir imagen 🖼️</router-link>
    </div>
    <p></p>

    <!-- Buscador -->
    <input 
      v-model="busqueda" 
      type="text" 
      placeholder="Buscar juegos..."
    />

    <!-- Botón para ordenar por año -->
    <button @click="ordenAsc = !ordenAsc">
      Ordenar por año: {{ ordenAsc ? 'Ascendente' : 'Descendente' }}
    </button>
    <p>
      Mostrando {{ juegosFiltrados.length }} de {{ juegos.length }} juegos.
    </p>

    <!-- Lista de juegos filtrada -->
    <div class="juegos">
      <div v-for="juego in juegosFiltrados" :key="juego.id" class="juego">
        <img :src="getImageUrl(juego.imagen)" :alt="'portada de ' + juego.nombre" />
        <h3>{{ juego.nombre }} ({{ juego.anio }})</h3>
        <p>{{ juego.descripcion }}</p>

        <div v-if="juego.esinterno">
          <router-link :to="{ name: 'tresenraya' }">Probar</router-link>
          <a :href="juego.url" target="_blank">Ver más</a>
        </div>
        <div v-else>
          <a :href="juego.url" target="_blank">Ver más</a>
        </div>

        <button @click="eliminarJuego(juego.id)" class="btn-eliminar">Eliminar</button>
        <button @click.stop="$router.push(`/editar-juego/${juego.id}`)">Editar</button>
      </div>
    </div>

    <!-- Palabras clave -->
    <footer class="keywords">
      <h4>Palabras clave comunes:</h4>
      <p>{{ keywords.join(", ") }}</p>
    </footer>
  </div>
</template>

<script>
const API_URL = "https://cdis-backend.onrender.com";

export default {
  name: "ListaJuegos",
  data() {
    return {
      busqueda: "",
      ordenAsc: true,
      juegos: [],
    };
  },

  async created() {
    try {
      const res = await fetch(`${API_URL}/games`);
      const data = await res.json();
      console.log("Juegos recibidos:", data);
      this.juegos = data;
    } catch (error) {
      console.error("Error al cargar juegos:", error);
    }
  },

  computed: {
    juegosFiltrados() {
      let filtrados = this.juegos.filter(j => 
        j.nombre.toLowerCase().includes(this.busqueda.toLowerCase()) ||
        j.descripcion.toLowerCase().includes(this.busqueda.toLowerCase())
      );
      return filtrados.sort((a, b) => 
        this.ordenAsc ? a.anio - b.anio : b.anio - a.anio
      );
    },
    keywords() {
      if (this.juegosFiltrados.length === 0) return [];
      let stopwords = ["de","en","y","el","la","los","las","un","una","para","por","con"];
      let conteo = {};
      this.juegosFiltrados.forEach(j => {
        let palabras = j.descripcion
          .toLowerCase()
          .replace(/[.,]/g, "")
          .split(/\s+/)
          .filter(p => !stopwords.includes(p));
        let unicas = new Set(palabras);
        unicas.forEach(p => { conteo[p] = (conteo[p] || 0) + 1; });
      });
      let ordenadas = Object.entries(conteo)
        .sort((a,b)=>b[1]-a[1])
        .map(([palabra])=>palabra);
      return ordenadas.slice(0, 15);
    }
  },

  methods: {
    getImageUrl(filename) {
      if (!filename) return "";
      if (filename.startsWith("http")) return filename;
      try {
        return require(`@/assets/${filename}`);
      } catch {
        return `${API_URL}/uploads/${filename}`;
      }
    },

    async eliminarJuego(id) {
      const auth = localStorage.getItem("auth");
      const res = await fetch(`${API_URL}/games/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Basic ${auth}` },
      });

      if (res.ok) {
        this.juegos = this.juegos.filter(j => j.id !== id);
      } else if (res.status === 401) {
        alert("No autorizado. Debes iniciar sesión para borrar juegos.");
        this.$router.push("/login");
      } else {
        alert("Error al borrar el juego.");
      }
    }
  }
};
</script>

<style scoped>
.lista-juegos { padding: 20px; }
.juegos { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; align-items: stretch; }
.juego { border: 1px solid #ccc; border-radius: 10px; padding: 15px; background: #f9f9f9; text-align: center; display: flex; flex-direction: column; justify-content: space-between; }
.juego img { width: 100%; height: 180px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; }
.juego p { flex-grow: 1; font-size: 0.9rem; margin: 10px 0; }
.juego a, .juego router-link { display: inline-block; margin: 5px; }
.keywords { margin-top: 40px; padding-top: 15px; text-align: center; }
.keywords h4 { margin-bottom: 10px; font-weight: bold; }
.keywords p { font-size: 0.9rem; color: #444; }
.btn-eliminar { background-color: #e74c3c; color: white; border: none; padding: 8px 12px; border-radius: 5px; cursor: pointer; margin-top: 8px; margin-bottom: 8px; transition: 0.2s; }
.btn-eliminar:hover { background-color: #c0392b; }
</style>
