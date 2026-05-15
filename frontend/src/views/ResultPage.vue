<template>
  <div class="result-page">
    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="10" animated />
    </div>

    <div v-else-if="record" class="record-detail">
      <h1 class="page-title">{{ typeLabels[recordType] }}分析报告</h1>
      <p class="record-meta">{{ metaText }}</p>

      <div class="analysis-content" v-html="formatAnalysisHtml(record.ai_analysis || '暂无分析结果')"></div>

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
import { baziApi, ziweiApi, liuyaoApi } from '@/api'
import type { BaziRecord, LiuYaoRecord, ZiweiRecord } from '@/api'
import { formatAnalysisHtml } from '@/utils/formatAnalysis'

const route = useRoute()
const loading = ref(true)
const record = ref<BaziRecord | ZiweiRecord | LiuYaoRecord | null>(null)
const recordType = ref((route.params.type as string) || 'bazi')

const typeLabels: Record<string, string> = {
  bazi: '八字命理',
  ziwei: '紫微斗数',
  liuyao: '六爻占卜',
}

const metaText = computed(() => {
  if (!record.value) return ''
  const r = record.value
  if (recordType.value === 'bazi') {
    const bazi = r as BaziRecord
    return `出生: ${bazi.birth_date} ${bazi.birth_time} | ${bazi.gender === 'male' ? '男' : '女'} | ${bazi.shengxiao || ''}`
  } else if (recordType.value === 'ziwei') {
    const ziwei = r as ZiweiRecord
    return `出生: ${ziwei.birth_date} ${ziwei.birth_time} | ${ziwei.gender === 'male' ? '男' : '女'} | 命宫: ${ziwei.ming_gong || ''}`
  } else if (recordType.value === 'liuyao') {
    const liuyao = r as LiuYaoRecord
    return `问题: ${liuyao.question} | ${liuyao.gua_name || ''}`
  }
  return ''
})

onMounted(async () => {
  const type = (route.params.type as string) || 'bazi'
  const id = route.params.id
  recordType.value = type

  if (id) {
    try {
      if (type === 'ziwei') {
        record.value = await ziweiApi.getRecord(Number(id))
      } else if (type === 'liuyao') {
        record.value = await liuyaoApi.getRecord(Number(id))
      } else {
        record.value = await baziApi.getRecord(Number(id))
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
