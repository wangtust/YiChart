<template>
  <div class="result-page">
    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="10" animated />
    </div>

    <div v-else-if="record" class="record-detail">
      <h1 class="page-title">命理分析报告</h1>
      <p class="record-meta">
        出生: {{ record.birth_date }} {{ record.birth_time }}
        | {{ record.gender === 'male' ? '男' : '女' }}
        | {{ record.shengxiao }}
      </p>

      <div class="analysis-content" v-html="formatAnalysis(record.ai_analysis || '')"></div>

      <div class="actions">
        <el-button @click="$router.push('/bazi')">重新算命</el-button>
        <el-button @click="$router.push('/history')">历史记录</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { baziApi } from '@/api'

const route = useRoute()
const loading = ref(true)
const record = ref<any>(null)

function formatAnalysis(text: string) {
  return text
    .replace(/\n/g, '<br>')
    .replace(/### (.+)/g, '<h3>$1</h3>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
}

onMounted(async () => {
  const id = route.params.id
  if (id) {
    try {
      record.value = await baziApi.getRecord(Number(id))
    } catch {
      // handle error
    }
  }
  loading.value = false
})
</script>

<style scoped>
.result-page {
  max-width: 800px;
  margin: 0 auto;
}

.page-title {
  font-size: 28px;
  color: var(--gold-color);
  text-align: center;
  margin-bottom: 8px;
}

.record-meta {
  text-align: center;
  color: var(--text-secondary);
  margin-bottom: 32px;
}

.analysis-content {
  background: var(--card-bg);
  border: 1px solid rgba(212, 168, 75, 0.2);
  border-radius: 16px;
  padding: 32px;
  line-height: 1.8;
  margin-bottom: 24px;
}

.analysis-content :deep(h3) {
  color: var(--gold-color);
  margin: 20px 0 8px;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 16px;
}
</style>
