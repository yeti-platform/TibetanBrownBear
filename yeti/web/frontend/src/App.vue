<template>
  <div id="app">
    <!-- Top menu -->
    <navigation />
    <div class="container-fluid">
      <div class="row" v-if="isAuthenticated">
        <!-- sidebar column -->
        <sidebar />
        <main role="main" class="col-md-9 ml-sm-auto col-lg-10 pt-3 px-4">
          <router-view/>
        </main>
      </div> <!-- end row -->
      <div v-else>
        <log-in />
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/scaffolding/Sidebar'
import Navigation from '@/components/scaffolding/Navigation'
import LogIn from '@/components/LogIn'
import axios from 'axios'
axios.defaults.baseURL = '/api'

require('bootstrap')
require('bootstrap/dist/css/bootstrap.css')
require('@fortawesome/fontawesome-free/js/all.js')

export default {
  components: {
    Sidebar,
    Navigation,
    LogIn
  },
  name: 'App',
  metaInfo: {
    title: 'Yeti',
    titleTempalte: 'Yeti | %s',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1, shrink-to-fit=no' }
    ]
  },
  computed: {
    isAuthenticated () {
      return this.$store.getters.isAuthenticated
    }
  },
  created () {
    let component = this
    axios.interceptors.response.use(undefined, function (error) {
      if (error.response.status === 401 && !error.request.responseURL.includes('/api/users/login/')) {
        component.$store.dispatch('logout').then(() => {
          component.$router.push('/login')
        })
      }
      return Promise.reject(error)
    })
  }
}
</script>

<style>
body {
  font-size: .875rem;
}

.feather {
  width: 16px;
  height: 16px;
  vertical-align: text-bottom;
}

.border-top { border-top: 1px solid #e5e5e5; }
.border-bottom { border-bottom: 1px solid #e5e5e5; }

.nav-pills .nav-link.router-link-active, .nav-pills .show > .nav-link {
    color: #fff;
    background-color: #007bff;
}

h1.yeti-title {
  font-weight: 300;
  font-size: 3rem;
}

</style>
