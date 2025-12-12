<template>
  <div class="form-juego">
    <h2>{{ editando ? "Editar juego" : "Registrar juego" }}</h2>

    <form @submit.prevent="guardarJuego">
      <input v-model="juego.nombre" placeholder="Nombre del juego" required />
      <input v-model="juego.descripcion" placeholder="Descripción" required />
      <input v-model.number="juego.anio" type="number" placeholder="Año" />
      <input v-model="juego.url" placeholder="URL" />
      <input v-model="juego.imagen" placeholder="Nombre de la imagen" /> 

      <label>
        <input type="checkbox" v-model="juego.esinterno" />
        Es un juego interno
      </label>

      <button type="submit">{{ editando ? "Actualizar" : "Guardar" }} juego</button>
    </form>

    <p>{{ mensaje }}</p>
  </div>
</template>

<script>
const API_URL = "https://cdis-backend.onrender.com";

export default {
  name: "FormJuego",
  data() {
    return {
      juego: {
        nombre: "",
        descripcion: "",
        anio: "",
        imagen: "",
        url: "",
        esinterno: false,
      },
      mensaje: "",
      editando: false,
    };
  },
  async mounted() {
    const id = this.$route.params.id;
    if (id) {
      this.editando = true;
      try {
        const res = await fetch(`${API_URL}/games/${id}`);
        if (!res.ok) throw new Error("Error al cargar el juego");
        this.juego = await res.json();
      } catch (e) {
        console.error(e);
        this.mensaje = "No se pudo cargar el juego";
      }
    }
  },
  methods: {
    async guardarJuego() {
      try {
        const url = this.editando
          ? `${API_URL}/games/${this.$route.params.id}`
          : `${API_URL}/games`;

        const metodo = this.editando ? "PUT" : "POST";

        const auth = localStorage.getItem("auth");
        
        const res = await fetch(url, {
          method: metodo,
          headers: { "Content-Type": "application/json", "Authorization": `Basic ${auth}` },
          body: JSON.stringify(this.juego),
        });

        if (!res.ok) throw new Error("Error al guardar/actualizar el juego");
         
        this.mensaje = this.editando
          ? "Juego actualizado correctamente"
          : "Juego guardado correctamente";

        if (!this.editando) {
          this.juego = { nombre: "", descripcion: "", anio: "", imagen: "", url: "", esinterno: false };
        }

        setTimeout(() => this.$router.push("/"), 1000);

      } catch (e) {
        console.error(e);
        this.mensaje = "No se pudo guardar o actualizar el juego";
      }
    },
  },
};
</script>

<style scoped>
.form-juego {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
