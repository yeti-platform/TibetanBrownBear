<template>
  <div class="signin">
    <form @submit="logIn" class="form">
      <h1>Login</h1>
      <div class="form-group">
        <label for="email">Email address</label>
        <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Enter email" v-model="email">
        <small id="emailHelp" class="form-text text-muted">Use yeticli to add users to Yeti.</small>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" class="form-control" id="password" v-model="password" placeholder="Password">
      </div>
      <button type="submit" v-bind:class="{ disabled: canSubmit }" class="btn btn-primary">Log in</button>
      <div v-if="error" class="card text-white bg-danger mt-3 login-error">
        <div class="card-body">
          <h5 class="card-title">Authentication error</h5>
          <p class="card-text">{{error}}</p>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      email: '',
      password: '',
      error: '',
      loading: false
    }
  },
  methods: {
    logIn (e) {
      e.preventDefault()
      this.loading = true
      this.$store.dispatch('login', { email: this.email, password: this.password })
        .then(() => {
          console.log('Successfully logged in!')
        })
        .catch(error => {
          this.error = error.response.data.error
        })
        .finally(() => { this.loading = false })
    }
  },
  computed: {
    canSubmit () {
      return !(this.email && this.password && !this.loading)
    }
  }

}
</script>

<style>

.signin {
  max-width: 420px;
  margin: auto;
  width: 100%;
  margin-top: 5rem;
}

.login-error {
  max-width: 18rem;
  margin: auto;
}

</style>
