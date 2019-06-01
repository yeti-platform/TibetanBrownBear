import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

function isValidJwt (jwt) {
  if (!jwt || jwt.split('.').length < 3) {
    return false
  }
  const data = JSON.parse(atob(jwt.split('.')[1]))
  const exp = new Date(data.exp * 1000) // JS deals with dates in milliseconds since epoch
  const now = new Date()
  return now < exp
}

function getJwtSubject (jwt) {
  if (isValidJwt(jwt)) {
    return JSON.parse(atob(jwt.split('.')[1])).sub
  }
  return ''
}

const state = {
  token: ''
}

const actions = {
  login ({ commit }, params) {
    return new Promise((resolve, reject) => {
      commit('authRequest')
      axios.post('/users/login/', params)
        .then(response => {
          console.log(response)
          commit('authSuccess', response.data.token)
          resolve(response)
        })
        .catch(err => {
          commit('authError', err)
          reject(err)
        })
    })
  },
  logout ({ commit }) {
    return new Promise((resolve, reject) => {
      axios.post('/users/logout/')
        .then(response => {
          commit('logout')
          resolve(response)
        })
        .catch(err => {
          commit('authError', err)
          reject(err)
        })
      resolve()
    })
  }
}

const mutations = {
  authRequest (state) {
    state.authenticated = false
    state.token = ''
  },
  authSuccess (state, token) {
    console.log('Auth cookie set!')
    state.authenticated = true
    state.token = token
  },
  authError (state, error) {
    state.authenticated = false
    console.log(error)
    state.token = ''
  },
  logout (state) {
    state.authenticated = false
    console.log('Cookie cleared.')
    state.token = ''
  }
}

const getters = {
  isAuthenticated: state => !!state.authenticated,
  tokenSubject: state => getJwtSubject(state.token)
}

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters
})

export default store
