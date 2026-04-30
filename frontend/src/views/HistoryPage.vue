<template>
  <div class="history-page">
    <h1 class="page-title">历史记录</h1>

    <div class="filter-tabs">
      <span
        v-for="tab in tabs"
        :key="tab.key"
        class="tab"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >{{ tab.label }}</span>
    </div>

    <div v-if="loading" class="loading">
      <el-skeleton :rows="5" animated />
    </div>

    <div v-else-if="filteredRecords.length === 0" class="empty">
      <p>暂无算命记录</p>
      <div class="empty-actions">
        <router-link to="/bazi"><el-button type="primary">八字算命</el-button></router-link>
        <router-link to="/ziwei"><el-button>紫微斗数</el-button></router-link>
        <router-link to="/liuyao"><el-button>六爻占卜</el-button></router-link>
      </div>
    </div>

    <div v-else class="records-list">
      <div
        class="record-card"
        v-for="record in filteredRecords"
        :key="record._type + '-' + record.id"
        @click="goToDetail(record)"
      >
        <div class="record-header">
          <span class="record-type" :class="'type-' + record._type">{{ typeLabels[record._type] }}</span>
          <span class="record-date">{{ formatDate(record.created_at) }}</span>
        </div>
        <div class="record-info">
          <template v-if="record._type === 'bazi'">
            <span>{{ record.birth_date }} {{ record.birth_time }}</span>
            <span v-if="record.shengxiao">生肖: {{ record.shengxiao }}</span>
            <span v-if="record.nayin">纳音: {{ record.nayin }}</span>
          </template>
          <template v-else-if="record._type === 'ziwei'">
            <span>{{ record.birth_date }} {{ record.birth_time }}</span>
            <span>命宫: {{ record.ming_gong }}</span>
          </template>
          <template v-else-if="record._type === 'liuyao'">
            <span>{{ record.question }}</span>
            <span v-if="record.gua_name">{{ record.gua_name }}</span>
          </template>
        </div>
        <div class="record-preview" v-if="record.ai_analysis">
          {{ record.ai_analysis.slice(0, 80) }}...
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { baziApi } from '@/api'

const router = useRouter()
const loading = ref(true)
const activeTab = ref('all')
const records = ref<any[]>([])

const tabs = [
  { key: 'all', label: '全部' },
  { key: 'bazi', label: '八字' },
  { key: 'ziwei', label: '紫微' },
  { key: 'liuyao', label: '六爻' },
]

const typeLabels: Record<string, string> = {
  bazi: '八字',
  ziwei: '紫微',
  liuyao: '六爻',
}

const filteredRecords = computed(() => {
  if (activeTab.value === 'all') return records.value
  return records.value.filter(r => r._type === activeTab.value)
})

function formatDate(dt: string | null) {
  if (!dt) return ''
  return new Date(dt).toLocaleString('zh-CN')
}

function goToDetail(record: any) {
  router.push(`/result/${record._type}/${record.id}`)
}

onMounted(async () => {
  try {
    const [baziList, ziweiList, liuyaoList] = await Promise.all([
      baziApi.getHistory().catch(() => []),
      fetch('/api/ziwei/history').then(r => r.json()).catch(() => []),
      fetch('/api/liuyao/history').then(r => r.json()).catch(() => []),
    ])

    const all = [
      ...(baziList as any[]).map(r => ({ ...r, _type: 'bazi' })),
      ...(ziweiList as any[]).map(r => ({ ...r, _type: 'ziwei' })),
      ...(liuyaoList as any[]).map(r => ({ ...r, _type: 'liuyao' })),
    ]

    // 按时间倒序
    all.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    records.value = all
  } catch {
    // handle error
  }
  loading.value = false
})
</script>

<style scoped>
.history-page { max-width: 800px; margin: 0 auto; }
.page-title { font-size: 28px; color: var(--gold-color); text-align: center; margin-bottom: 24px; }

.filter-tabs {
  display: flex; justify-content: center; gap: 12px; margin-bottom: 24px;
}
.tab {
  padding: 6px 20px; border-radius: 20px; cursor: pointer;
  color: var(--text-secondary); font-size: 14px;
  border: 1px solid rgba(255,255,255,0.1); transition: all 0.3s;
}
.tab.active {
  color: var(--gold-color); border-color: var(--gold-color);
  background: rgba(212,168,75,0.1);
}

.empty { text-align: center; padding: 60px 0; color: var(--text-secondary); }
.empty-actions { display: flex; gap: 12px; justify-content: center; margin-top: 16px; }

.records-list { display: flex; flex-direction: column; gap: 16px; }

.record-card {
  background: var(--card-bg); border: 1px solid rgba(212,168,75,0.15);
  border-radius: 12px; padding: 20px 24px; cursor: pointer; transition: all 0.3s;
}
.record-card:hover { border-color: var(--gold-color); transform: translateY(-2px); }

.record-header { display: flex; justify-content: space-between; margin-bottom: 8px; }

.record-type {
  font-size: 12px; padding: 2px 10px; border-radius: 10px; font-weight: 600;
}
.record-type.type-bazi { background: rgba(196,30,58,0.2); color: #e63956; }
.record-type.type-ziwei { background: rgba(33,150,243,0.2); color: #2196f3; }
.record-type.type-liuyao { background: rgba(76,175,80,0.2); color: #4caf50; }

.record-date { color: var(--text-secondary); font-size: 13px; }

.record-info {
  display: flex; gap: 16px; color: var(--text-secondary);
  font-size: 14px; margin-bottom: 8px; flex-wrap: wrap;
}

.record-preview { color: var(--text-secondary); font-size: 13px; line-height: 1.5; }
</style>
