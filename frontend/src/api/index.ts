import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
})

// 请求拦截 - 添加 token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const detail = error.response?.data?.detail
    let message = '请求失败'
    if (typeof detail === 'string') {
      message = detail
    } else if (Array.isArray(detail)) {
      message = detail.map((d: any) => d.msg).join('; ')
    }
    return Promise.reject(new Error(message))
  }
)

export default api

// 认证接口
export const authApi = {
  register: (data: { username: string; email: string; password: string }) =>
    api.post('/auth/register', data),
  login: (data: { username: string; password: string }) =>
    api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
}

// 八字接口
export const baziApi = {
  calculate: (data: BaziInput) => api.post('/bazi/calculate', data),
  getHistory: (skip = 0, limit = 20) =>
    api.get('/bazi/history', { params: { skip, limit } }),
  getRecord: (id: number) => api.get(`/bazi/${id}`),
}

// 流式分析接口
export async function streamAnalyze(
  data: BaziInput,
  onChunk: (text: string) => void,
  onDone?: () => void
) {
  const response = await fetch('/api/bazi/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })

  const reader = response.body?.getReader()
  if (!reader) return

  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    const text = decoder.decode(value)
    const lines = text.split('\n')

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const content = line.slice(6)
        if (content === '[DONE]') {
          onDone?.()
          return
        }
        try {
          const parsed = JSON.parse(content)
          if (parsed.content) {
            onChunk(parsed.content)
          }
        } catch {
          // ignore parse errors
        }
      }
    }
  }
  onDone?.()
}

export interface BaziInput {
  birth_date: string
  birth_time: string
  gender: 'male' | 'female'
  is_lunar: boolean
}
