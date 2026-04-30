<template>
  <div class="result-page">
    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="10" animated />
    </div>

    <div v-else-if="record" class="record-detail">
      <h1 class="page-title">{{ typeLabels[recordType] }}分析报告</h1>
      <p class="record-meta">{{ metaText }}</p>

      <div class="analysis-content" v-html="formatAnalysis(record.ai_analysis || '暂无分析结果')"></div>

      <div class="actions">
        <el-button @click="$router.push(`/${recordType}`)">重新算命</el-button>
        <el-button @click="$router.push('/history')">历史记录</el-button>
      </div>
    </div>

    <div v-else class="empty">
      <p>记录不存在</p>
      <el-button @click="$router.push('/history')">返回历史记录</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const loading = ref(true)
const record = ref<any>(null)
const recordType = ref(route.params.type as string || 'bazi')

const typeLabels: Record<string, string> = {
  bazi: '八字命理',
  ziwei: '紫微斗数',
  liuyao: '六爻占卜',
}

const metaText = computed(() => {
  if (!record.value) return ''
  const r = record.value
  if (recordType.value === 'bazi') {
    return `出生: ${r.birth_date} ${r.birth_time} | ${r.gender === 'male' ? '男' : '女'} | ${r.shengxiao || ''}`
  } else if (recordType.value === 'ziwei') {
    return `出生: ${r.birth_date} ${r.birth_time} | ${r.gender === 'male' ? '男' : '女'} | 命宫: ${r.ming_gong || ''}`
  } else if (recordType.value === 'liuyao') {
    return `问题: ${r.question} | ${r.gua_name || ''}`
  }
  return ''
})

function formatAnalysis(text: string) {
  return text
    .replace(/^###\s*(.+)$/gm, '<h3 class="analysis-h3">$1</h3>')
    .replace(/^##\s*(.+)$/gm, '<h2 class="analysis-h2">$1</h2>')
    .replace(/^#\s*(.+)$/gm, '<h1 class="analysis-h1">$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>')
}

onMounted(async () => {
  const type = route.params.type as string || 'bazi'
  const id = route.params.id
  recordType.value = type

  if (id) {
    try {
      const resp = await fetch(`/api/${type}/${id}`)
      if (resp.ok) {
        record.value = await resp.json()
      }
    } catch {
      // handle error
    }
  }
  loading.value = false
})
</script>

<style scoped>
.result-page { max-width: 800px; margin: 0 auto; }
.page-title { font-size: 28px; color: var(--gold-color); text-align: center; margin-bottom: 8px; }
.record-meta { text-align: center; color: var(--text-secondary); margin-bottom: 32px; }

.analysis-content {
  background: var(--card-bg); border: 1px solid rgba(212,168,75,0.2);
  border-radius: 16px; padding: 32px; line-height: 1.8; margin-bottom: 24px;
}
.analysis-content :deep(h3) { color: var(--gold-color); margin: 20px 0 8px; }
.analysis-content :deep(h2) { color: var(--gold-color); margin: 24px 0 10px; }
.analysis-content :deep(h1) { color: var(--gold-color); margin: 28px 0 12px; }

.actions { display: flex; justify-content: center; gap: 16px; }
.empty { text-align: center; padding: 60px 0; color: var(--text-secondary); }
</style>
