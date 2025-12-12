<template>
  <div id="app">
    <h1>Portal de Videojuegos 🎮</h1>

    <button @click="$router.push('/login')">🔐 Login</button>
    <router-view /> <!-- aquí Vue carga la página que corresponda según el enrutado-->
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>





<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
