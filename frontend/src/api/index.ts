import axios from 'axios'

const apiBaseURL = import.meta.env.VITE_API_BASE_URL || '/api'

const api = axios.create({
  baseURL: apiBaseURL,
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
    api.post<UserResponse, UserResponse>('/auth/register', data),
  login: (data: { username: string; password: string }) =>
    api.post<TokenResponse, TokenResponse>('/auth/login', data),
  getMe: () => api.get<UserResponse, UserResponse>('/auth/me'),
}

// 八字接口
export const baziApi = {
  calculate: (data: BaziInput) => api.post<BaziResult, BaziResult>('/bazi/calculate', data),
  getHistory: (skip = 0, limit = 20) =>
    api.get<BaziRecord[], BaziRecord[]>('/bazi/history', { params: { skip, limit } }),
  getRecord: (id: number) => api.get<BaziRecord, BaziRecord>(`/bazi/${id}`),
}

// 紫微接口
export const ziweiApi = {
  calculate: (data: ZiweiInput) => api.post<ZiweiResult, ZiweiResult>('/ziwei/calculate', data),
  getHistory: (skip = 0, limit = 20) =>
    api.get<ZiweiRecord[], ZiweiRecord[]>('/ziwei/history', { params: { skip, limit } }),
  getRecord: (id: number) => api.get<ZiweiRecord, ZiweiRecord>(`/ziwei/${id}`),
}

// 六爻接口
export const liuyaoApi = {
  calculate: (data: LiuYaoInput) => api.post<LiuYaoResult, LiuYaoResult>('/liuyao/calculate', data),
  getHistory: (skip = 0, limit = 20) =>
    api.get<LiuYaoRecord[], LiuYaoRecord[]>('/liuyao/history', { params: { skip, limit } }),
  getRecord: (id: number) => api.get<LiuYaoRecord, LiuYaoRecord>(`/liuyao/${id}`),
}

// 流式分析接口
export async function streamAnalyze<TData>(
  endpoint: '/bazi/analyze' | '/ziwei/analyze' | '/liuyao/analyze',
  data: TData,
  onChunk: (text: string) => void,
  onDone?: () => void
) {
  const token = localStorage.getItem('token')
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`

  const response = await fetch(`${apiBaseURL}${endpoint}`, {
    method: 'POST',
    headers,
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    throw new Error(await getResponseError(response))
  }

  const reader = response.body?.getReader()
  if (!reader) {
    throw new Error('服务器没有返回流式内容')
  }

  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const events = buffer.split('\n\n')
    buffer = events.pop() || ''

    for (const event of events) {
      const isDone = handleSseEvent(event, onChunk)
      if (isDone) {
        onDone?.()
        return
      }
    }
  }

  if (buffer) {
    handleSseEvent(buffer, onChunk)
  }
  onDone?.()
}

async function getResponseError(response: Response) {
  try {
    const body = await response.json()
    if (typeof body.detail === 'string') return body.detail
    if (Array.isArray(body.detail)) {
      return body.detail.map((item: { msg?: string }) => item.msg).filter(Boolean).join('; ')
    }
  } catch {
    // ignore non-json error body
  }
  return `请求失败 (${response.status})`
}

function handleSseEvent(event: string, onChunk: (text: string) => void) {
  for (const line of event.split('\n')) {
    if (!line.startsWith('data: ')) continue

    const content = line.slice(6)
    if (content === '[DONE]') return true

    try {
      const parsed = JSON.parse(content) as { content?: string; error?: string }
      if (parsed.error) throw new Error(parsed.error)
      if (parsed.content) onChunk(parsed.content)
    } catch (error) {
      if (error instanceof Error && error.name !== 'SyntaxError') throw error
    }
  }

  return false
}

export interface UserResponse {
  id: number
  username: string
  email: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface BaziInput {
  birth_date: string
  birth_time: string
  gender: 'male' | 'female'
  is_lunar: boolean
}

export interface BaziPillar {
  heavenly_stem: string
  earthly_branch: string
  hidden_stems: string[]
  wuxing: string
}

export interface BaziResult {
  year_pillar: BaziPillar
  month_pillar: BaziPillar
  day_pillar: BaziPillar
  hour_pillar: BaziPillar
  wuxing: Record<string, number>
  shengxiao: string
  nayin: string
  day_master: string
  day_master_wuxing: string
  shishen: Record<string, string>
}

export interface BaziRecord extends Partial<BaziResult> {
  id: number
  birth_date: string
  birth_time: string
  gender: 'male' | 'female'
  bazi_result?: Record<string, BaziPillar>
  wuxing_result?: Record<string, number>
  ai_analysis?: string | null
  created_at?: string
}

export interface ZiweiInput {
  birth_date: string
  birth_time: string
  gender: 'male' | 'female'
}

export interface ZiweiPalace {
  地支: string
  星曜: string[]
  是命宫?: boolean
  是身宫?: boolean
}

export interface ZiweiResult {
  palaces: Record<string, ZiweiPalace>
  sihua: Partial<Record<'化禄' | '化权' | '化科' | '化忌', string>>
  ming_gong: string
  shen_gong: string
  生肖?: string
  五行局?: string
}

export interface ZiweiRecord extends Partial<ZiweiResult> {
  id: number
  birth_date: string
  birth_time: string
  gender: 'male' | 'female'
  ai_analysis?: string | null
  created_at?: string
}

export interface LiuYaoInput {
  question: string
  method?: 'random' | 'manual'
  manual_yao?: number[]
}

export interface LiuYaoLine {
  爻位: number
  阴阳: '阳' | '阴'
  动变: boolean
  数值: number
  纳甲: string
  六亲: string
  是世爻: boolean
  是应爻: boolean
}

export interface GuaInfo {
  上卦: string
  下卦: string
  卦名: string
  卦辞: string
}

export interface LiuYaoResult {
  question: string
  yao_lines: LiuYaoLine[]
  ben_gua: GuaInfo
  bian_gua: GuaInfo
  gua_name: string
  bian_gua_name: string
  shi_yao: number
  ying_yao: number
  liu_qin: string[]
}

export interface LiuYaoRecord extends Partial<LiuYaoResult> {
  id: number
  ai_analysis?: string | null
  created_at?: string
}

export type HistoryRecord =
  | (BaziRecord & { _type: 'bazi' })
  | (ZiweiRecord & { _type: 'ziwei' })
  | (LiuYaoRecord & { _type: 'liuyao' })
