<template>
  <div class="liuyao-page">
    <h1 class="page-title">六爻占卜</h1>
    <p class="page-desc">心中默念所问之事，点击摇卦按钮，AI 为您解读卦象</p>

    <div class="form-container">
      <el-form :model="form" label-width="80px" size="large">
        <el-form-item label="所问之事">
          <el-input
            v-model="form.question"
            type="textarea"
            :rows="3"
            placeholder="请描述您想问的事情，例如：最近的事业发展方向如何？"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleShake"
            class="submit-btn shake-btn"
            :class="{ shaking: isShaking }"
          >
            {{ loading ? 'AI 解卦中...' : isShaking ? '摇卦中...' : '🪙 摇卦' }}
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 卦象结果 -->
    <div v-if="liuyaoResult" class="result-section">
      <h2 class="section-title">卦象</h2>

      <div class="gua-container">
        <!-- 本卦 -->
        <div class="gua-box">
          <h3>本卦: {{ liuyaoResult.gua_name }}</h3>
          <div class="gua-detail">
            {{ liuyaoResult.ben_gua?.上卦 }}上 {{ liuyaoResult.ben_gua?.下卦 }}下
          </div>
          <div class="gua-ci">{{ liuyaoResult.ben_gua?.卦辞 }}</div>
        </div>

        <!-- 变卦 -->
        <div class="gua-box" v-if="liuyaoResult.gua_name !== liuyaoResult.bian_gua_name">
          <h3>变卦: {{ liuyaoResult.bian_gua_name }}</h3>
          <div class="gua-detail">
            {{ liuyaoResult.bian_gua?.上卦 }}上 {{ liuyaoResult.bian_gua?.下卦 }}下
          </div>
          <div class="gua-ci">{{ liuyaoResult.bian_gua?.卦辞 }}</div>
        </div>
      </div>

      <!-- 六爻图 -->
      <div class="yao-diagram">
        <div
          v-for="yao in [...liuyaoResult.yao_lines].reverse()"
          :key="yao.爻位"
          class="yao-row"
          :class="{ 'is-shi': yao.是世爻, 'is-ying': yao.是应爻, 'is-changing': yao.动变 }"
        >
          <span class="yao-label">第{{ yao.爻位 }}爻</span>
          <span class="yao-liuqin">{{ yao.六亲 }}</span>
          <span class="yao-najia">{{ yao.纳甲 }}</span>
          <span class="yao-line">
            <span v-if="yao.阴阳 === '阳'" class="yang-line">⚊</span>
            <span v-else class="yin-line">⚋</span>
            <span v-if="yao.动变" class="dong-mark">○</span>
          </span>
          <span class="yao-markers">
            <span v-if="yao.是世爻" class="marker shi">世</span>
            <span v-if="yao.是应爻" class="marker ying">应</span>
          </span>
        </div>
      </div>

      <!-- 世应提示 -->
      <div class="shi-ying-info">
        <span>世爻: 第{{ liuyaoResult.shi_yao }}爻</span>
        <span>应爻: 第{{ liuyaoResult.ying_yao }}爻</span>
      </div>
    </div>

    <!-- AI 分析 -->
    <div v-if="aiAnalysis" class="analysis-section">
      <h2 class="section-title">AI 解卦</h2>
      <div class="analysis-content" v-html="formatAnalysis(aiAnalysis)"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const isShaking = ref(false)
const liuyaoResult = ref<any>(null)
const aiAnalysis = ref('')

const form = reactive({
  question: '',
})

function formatAnalysis(text: string) {
  return text
    .replace(/\n/g, '<br>')
    .replace(/#{3}\s*(.+)/g, '<h3 class="analysis-h3">$1</h3>')
    .replace(/#{2}\s*(.+)/g, '<h2 class="analysis-h2">$1</h2>')
    .replace(/#{1}\s*(.+)/g, '<h1 class="analysis-h1">$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
}

async function handleShake() {
  if (!form.question.trim()) {
    ElMessage.warning('请先描述您想问的事情')
    return
  }

  // 摇卦动画
  isShaking.value = true
  loading.value = true
  liuyaoResult.value = null
  aiAnalysis.value = ''

  // 模拟摇卦延迟
  await new Promise(resolve => setTimeout(resolve, 1500))
  isShaking.value = false

  try {
    // 起卦
    const result = await fetch('/api/liuyao/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: form.question, method: 'random' }),
    }).then(r => r.json())
    liuyaoResult.value = result

    // 流式获取 AI 解卦
    const response = await fetch('/api/liuyao/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: form.question, method: 'random' }),
    })

    const reader = response.body?.getReader()
    if (!reader) return

    const decoder = new TextDecoder()
    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const text = decoder.decode(value)
      for (const line of text.split('\n')) {
        if (line.startsWith('data: ')) {
          const content = line.slice(6)
          if (content === '[DONE]') {
            loading.value = false
            return
          }
          try {
            const parsed = JSON.parse(content)
            if (parsed.content) aiAnalysis.value += parsed.content
          } catch {}
        }
      }
    }
    loading.value = false
  } catch (error: any) {
    ElMessage.error(error.message || '起卦失败')
    loading.value = false
  }
}
</script>

<style scoped>
.liuyao-page { max-width: 800px; margin: 0 auto; }
.page-title { font-size: 32px; color: var(--gold-color); text-align: center; margin-bottom: 8px; }
.page-desc { text-align: center; color: var(--text-secondary); margin-bottom: 40px; }

.form-container {
  background: var(--card-bg); border: 1px solid rgba(212,168,75,0.2);
  border-radius: 16px; padding: 32px; margin-bottom: 32px;
}
.submit-btn {
  width: 100%;
  background: linear-gradient(135deg, var(--primary-color), #e63956) !important;
  border: none !important; font-size: 18px;
}

/* 摇卦动画 */
.shake-btn.shaking {
  animation: shake 0.15s infinite;
}
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px) rotate(-2deg); }
  75% { transform: translateX(5px) rotate(2deg); }
}

.result-section, .analysis-section {
  background: var(--card-bg); border: 1px solid rgba(212,168,75,0.2);
  border-radius: 16px; padding: 32px; margin-bottom: 32px;
}
.section-title { color: var(--gold-color); font-size: 22px; margin-bottom: 24px; text-align: center; }

/* 卦象 */
.gua-container { display: flex; gap: 24px; justify-content: center; margin-bottom: 32px; flex-wrap: wrap; }
.gua-box {
  background: rgba(0,0,0,0.2); border-radius: 12px; padding: 20px;
  text-align: center; min-width: 200px;
}
.gua-box h3 { color: var(--gold-color); margin-bottom: 8px; }
.gua-detail { color: var(--text-secondary); font-size: 14px; margin-bottom: 8px; }
.gua-ci { color: var(--text-primary); font-size: 13px; font-style: italic; }

/* 六爻图 */
.yao-diagram {
  max-width: 500px; margin: 0 auto;
}
.yao-row {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 16px; border-bottom: 1px solid rgba(255,255,255,0.05);
}
.yao-row.is-shi { background: rgba(212,168,75,0.1); }
.yao-row.is-ying { background: rgba(196,30,58,0.1); }
.yao-row.is-changing { border-left: 3px solid var(--gold-color); }

.yao-label { color: var(--text-secondary); font-size: 13px; width: 50px; }
.yao-liuqin { color: var(--primary-color); font-size: 14px; width: 50px; }
.yao-najia { color: var(--text-secondary); font-size: 13px; width: 50px; }
.yao-line { font-size: 28px; flex: 1; display: flex; align-items: center; gap: 8px; }
.yang-line { color: var(--gold-color); }
.yin-line { color: #666; }
.dong-mark { color: var(--primary-color); font-size: 16px; }

.yao-markers { display: flex; gap: 4px; }
.marker {
  font-size: 11px; padding: 2px 8px; border-radius: 10px; font-weight: 700;
}
.marker.shi { background: var(--gold-color); color: #000; }
.marker.ying { background: var(--primary-color); color: #fff; }

.shi-ying-info {
  display: flex; justify-content: center; gap: 24px;
  color: var(--text-secondary); font-size: 14px; margin-top: 16px;
}

.analysis-content { line-height: 1.8; color: var(--text-primary); font-size: 15px; }
.analysis-content :deep(.analysis-h3) { color: var(--gold-color); margin: 20px 0 8px; font-size: 17px; }
.analysis-content :deep(.analysis-h2) { color: var(--gold-color); margin: 24px 0 10px; font-size: 19px; }
.analysis-content :deep(.analysis-h1) { color: var(--gold-color); margin: 28px 0 12px; font-size: 22px; }
</style>
