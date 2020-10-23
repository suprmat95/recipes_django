<template lang="html">
  <div id="app">
    <NavbarComponent />
    <router-view />
  </div>
</template>
<script>
  import NavbarComponent from "./components/Navbar"
  import {apiService} from "./common/api.service";

  export default {
    name: "App",
    components: {
      NavbarComponent
    },
    data() {
      return {
        userUsername: null
      }
    },
    methods: {
      async setUserInfo() {
        await apiService("/api/user/")
                .then(result =>{
                  this.userUsername = result.username;
                  window.localStorage.setItem("username", this.userUsername);
                })
      }

    },
    created() {
      this.setUserInfo();
    }
  }

</script>

<style>
 * {
    font-family: "Playfair Display", serif;
  }
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
