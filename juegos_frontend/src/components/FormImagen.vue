<template>
  <div>
    <h2>Subir imagen</h2>

    <form @submit.prevent="subirImagen">
      <input type="file" accept="image/*" @change="onFileChange" />
      <button type="submit">Subir</button>
    </form>

    <p v-if="mensaje">{{ mensaje }}</p>
  </div>
</template>

<script>
const API_URL = `http://${window.location.hostname}:5000`;

export default {
  data() {
    return {
      archivo: null,
      mensaje: ""
    };
  },
  methods: {
    onFileChange(e) {
      this.archivo = e.target.files[0];
    },

    async subirImagen() {
      if (!this.archivo) {
        this.mensaje = "Selecciona una imagen primero";
        return;
      }

      try {
        const auth = localStorage.getItem("auth");
        const formData = new FormData();
        formData.append("file", this.archivo);

        const res = await fetch(`${API_URL}/upload-image`, {
          method: "POST",
          headers: {
            "Authorization": `Basic ${auth}`
          },
          body: formData
        });

        if (!res.ok) {
          throw new Error("Error al subir la imagen");
        }

        const data = await res.json();
        this.mensaje = `${data.message} (${data.filename})`;

      } catch (e) {
        console.error(e);
        this.mensaje = "No se pudo subir la imagen";
      }
    }
  }
};
</script>
