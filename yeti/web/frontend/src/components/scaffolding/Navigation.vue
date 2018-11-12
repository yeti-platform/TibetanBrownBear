<template>
  <nav class="navbar navbar-expand-md navbar-dark sticky-top bg-dark flex-md-nowrap p-0">
    <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="#">Yeti</a>
    <div class="navbar-collapse" id="navbarCollapse">
      <ul class="navbar-nav px-3 ml-auto" v-if="!isAuthenticated">
        <li class="nav-item">
          <router-link class="nav-link active" :to="{name: 'LogIn'}">Log in</router-link>
        </li>
      </ul>
      <ul class="navbar-nav px-3 ml-auto" v-if="isAuthenticated">
        <li v-if="isAuthenticated" class="nav-item">
            <a class="nav-link active" href="#">{{tokenSubject}}</a>
        </li>
        <li v-if="isAuthenticated" class="nav-item">
          <router-link class="nav-link" :to="{name: 'AdminMain'}">Admin</router-link>
        </li>
        <li v-if="isAuthenticated" class="nav-item">
            <a class="nav-link" href="#" @click="logOut">Logout</a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  computed: {
    isAuthenticated () {
      return this.$store.getters.isAuthenticated
    },
    tokenSubject () {
      return this.$store.getters.tokenSubject
    }
  },
  methods: {
    logOut () {
      this.$store
        .dispatch('logout')
        .then(() => {
          this.$router.push('/login')
        })
        .catch(error => {
          console.log(error.response.data)
        })
    }
  }
}
</script>

<style lang="css">
.navbar-brand {
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
  font-size: 1rem;
  background-color: rgba(0, 0, 0, 0.25);
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, 0.25);
}

.navbar .form-control {
  padding: 0.75rem 1rem;
  border-width: 0;
  border-radius: 0;
}

.form-control-dark {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.1);
}

.form-control-dark:focus {
  border-color: transparent;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.25);
}
</style>
