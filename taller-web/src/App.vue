<template>
  <div class="container">
    <h1>Registro</h1>
    <form @submit.prevent="handleRegister">
      <input
        type="email"
        v-model="registerEmail"
        placeholder="Email"
        required
      />
      <input
        type="password"
        v-model="registerPassword"
        placeholder="Contraseña"
        required
      />
      <button type="submit">Registrarse</button>
    </form>
    <div v-if="registerMsg" class="msg">{{ registerMsg }}</div>

    <hr />

    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <input
        type="email"
        v-model="loginEmail"
        placeholder="Email"
        required
      />
      <input
        type="password"
        v-model="loginPassword"
        placeholder="Contraseña"
        required
      />
      <button type="submit">Iniciar sesión</button>
    </form>
    <div v-if="loginMsg" class="msg">{{ loginMsg }}</div>

    <hr />

    <h2>Usuarios registrados (debug)</h2>
    <button @click="loadUsers">Ver usuarios</button>
    <ul v-if="users.length" class="list">
      <li v-for="u in users" :key="u.email">
        {{ u.email }} — ****
      </li>
    </ul>
    <p v-else class="msg">No hay usuarios cargados</p>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      registerEmail: "",
      registerPassword: "",
      registerMsg: "",
      loginEmail: "",
      loginPassword: "",
      loginMsg: "",
      users: [], // lista de usuarios registrados
    };
  },
  methods: {
    async handleRegister() {
      this.registerMsg = "";
      try {
        const res = await fetch("http://127.0.0.1:5000/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: this.registerEmail,
            password: this.registerPassword,
          }),
        });
        const data = await res.json().catch(() => ({}));
        this.registerMsg =
          data.msg || (res.ok ? "Registro completado." : "Error en registro");
      } catch {
        this.registerMsg = "Error de conexión o servidor.";
      }
    },

    async handleLogin() {
      this.loginMsg = "";
      try {
        const res = await fetch("http://127.0.0.1:5000/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: this.loginEmail,
            password: this.loginPassword,
          }),
        });
        const data = await res.json().catch(() => ({}));
        this.loginMsg =
          data.msg || (res.ok ? "Login exitoso." : "Error en login");
      } catch {
        this.loginMsg = "Error de conexión o servidor.";
      }
    },

    async loadUsers() {
      try {
        const res = await fetch("http://127.0.0.1:5000/users");
        const data = await res.json();
        this.users = Array.isArray(data) ? data : [];
      } catch {
        this.users = [];
        this.loginMsg = "No se pudieron cargar los usuarios.";
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 350px;
  margin: 40px auto;
  padding: 24px;
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 8px #0001;
}
h1, h2 {
  font-size: 1.3em;
  margin-bottom: 10px;
}
form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
input {
  padding: 8px;
  border: 1px solid #bbb;
  border-radius: 4px;
  font-size: 1em;
}
button {
  padding: 8px;
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}
button:hover {
  background: #369870;
}
.msg {
  margin-top: 8px;
  color: #333;
  background: #e0ffe0;
  border: 1px solid #b2e5b2;
  border-radius: 4px;
  padding: 6px 10px;
  font-size: 0.98em;
}
.list {
  margin-top: 8px;
  padding-left: 18px;
}
hr {
  margin: 30px 0;
  border: none;
  border-top: 1px solid #ddd;
}
</style>