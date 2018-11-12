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

const LOGIN_URL = '/users/login/'

const state = {
  // token: localStorage.getItem('user-token') || ''
  token: ''
}

const actions = {
  login ({commit}, params) {
    return new Promise((resolve, reject) => {
      commit('authRequest')
      axios.post(LOGIN_URL, params)
        .then(response => {
          axios.defaults.headers.common['Authorization'] = `Bearer: ${response.data.token}`
          commit('authSuccess', response.data.token)
          resolve(response)
        })
        .catch(err => {
          commit('authError', err)
          reject(err)
        })
    })
  },
  logout ({commit}) {
    return new Promise((resolve, reject) => {
      commit('logout')
      delete axios.defaults.headers.common['Authorization']
      resolve()
    })
  }
}

const mutations = {
  authRequest (state) {
    state.token = ''
    // localStorage.setItem('user-token', '')
  },
  authSuccess (state, token) {
    state.token = token
    // localStorage.setItem('user-token', token)
  },
  authError (state, error) {
    console.log(error)
    state.token = ''
    // localStorage.removeItem('user-token')
  },
  logout (state) {
    state.token = ''
    // localStorage.removeItem('user-token')
  }
}

const getters = {
  isAuthenticated: state => !!state.token,
  tokenSubject: state => getJwtSubject(state.token)
}

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters
})

export default store
