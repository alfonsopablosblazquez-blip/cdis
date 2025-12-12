import Vue from "vue"
import Router from "vue-router"
import ListaJuegos from "@/components/ListaJuegos.vue"
import TresEnRaya from "@/components/TresEnRaya.vue"
import FormJuego from "@/components/FormJuego.vue"
import FormImagen from "@/components/FormImagen.vue"
import LogIn from "@/components/LogIn.vue"

Vue.use(Router)

const router = new Router({
  mode: "history",
  routes: [
    { path: "/", name: "lista", component: ListaJuegos },
    { path: "/nuevo-juego", name: "nuevo-juego", component: FormJuego },
    { path: "/subir-imagen", name: "subir-imagen", component: FormImagen },
    { path: "/tresenraya", name: "tresenraya", component: TresEnRaya },
    { path: "/editar-juego/:id", name: "editar-juego", component: FormJuego },
    { path: "/login", name: "login", component: LogIn }
  ]
})


router.beforeEach((to, from, next) => {
  const rutasProtegidas = ["/nuevo-juego", "/subir-imagen"]; // puedes añadir /editar-juego/:id si quieres
  const token = localStorage.getItem("auth");

  if (rutasProtegidas.includes(to.path) && !token) {
    alert("Debes iniciar sesión para acceder a esta sección");
    next("/login");
  } else {
    next();
  }
});

export default router;

