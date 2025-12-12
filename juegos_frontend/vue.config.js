
const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: '0.0.0.0',   // escucha en todas las interfaces
    port: 8080,
    allowedHosts: 'all' // permite conexiones externas
  }
})
