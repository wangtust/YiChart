import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi } from '@/api'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const username = ref('')
  const isLoggedIn = ref(false)

  async function login(user: string, password: string) {
    const data = await authApi.login({ username: user, password })
    token.value = data.access_token
    localStorage.setItem('token', data.access_token)
    isLoggedIn.value = true
    username.value = user
  }

  async function register(user: string, email: string, password: string) {
    await authApi.register({ username: user, email, password })
  }

  async function fetchUser() {
    try {
      const data = await authApi.getMe()
      username.value = data.username
      isLoggedIn.value = true
    } catch {
      logout()
    }
  }

  function logout() {
    token.value = ''
    username.value = ''
    isLoggedIn.value = false
    localStorage.removeItem('token')
  }

  return { token, username, isLoggedIn, login, register, fetchUser, logout }
})
