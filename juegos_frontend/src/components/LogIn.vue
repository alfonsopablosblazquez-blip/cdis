<!-- conectamos el frontend con la autentificación del backend-->
<template>
  <div class="login">
    <h2>Iniciar sesión</h2>
    <form @submit.prevent="login"> <!--ejecutamos el metodo login y evitamos que se recargue la pagina-->
      <input v-model="usuario" placeholder="Usuario" required />
      <input v-model="password" type="password" placeholder="Contraseña" required />
      <button type="submit">Entrar</button>
    </form>
    <p v-if="error" style="color:red">{{ error }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      usuario: "",
      password: "",
      error: "",
    };
  },
  methods: {
    login() {
      // verifica las credenciales con las del backend
      if (this.usuario === "admin" && this.password === "admindb") {
        // codificamos y guardamos el token
        const token = btoa(`${this.usuario}:${this.password}`);
        localStorage.setItem("auth", token);
        alert("Sesión iniciada correctamente");
        this.$router.push("/");
      } else {
        this.error = "Usuario o contraseña incorrectos";
      }
    },
  },
};
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: 40px auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
input {
  padding: 8px;
  font-size: 1em;
}
button {
  padding: 8px;
  cursor: pointer;
}
</style>
