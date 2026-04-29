<template>
  <div class="history-page">
    <h1 class="page-title">历史记录</h1>

    <div v-if="loading" class="loading">
      <el-skeleton :rows="5" animated />
    </div>

    <div v-else-if="records.length === 0" class="empty">
      <p>暂无算命记录</p>
      <router-link to="/bazi">
        <el-button type="primary">去算命</el-button>
      </router-link>
    </div>

    <div v-else class="records-list">
      <div
        class="record-card"
        v-for="record in records"
        :key="record.id"
        @click="$router.push(`/result/${record.id}`)"
      >
        <div class="record-header">
          <span class="record-date">{{ record.birth_date }} {{ record.birth_time }}</span>
          <span class="record-gender">{{ record.gender === 'male' ? '男' : '女' }}</span>
        </div>
        <div class="record-info">
          <span v-if="record.shengxiao">生肖: {{ record.shengxiao }}</span>
          <span v-if="record.nayin">纳音: {{ record.nayin }}</span>
        </div>
        <div class="record-preview" v-if="record.ai_analysis">
          {{ record.ai_analysis.slice(0, 100) }}...
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { baziApi } from '@/api'

const loading = ref(true)
const records = ref<any[]>([])

onMounted(async () => {
  try {
    records.value = await baziApi.getHistory() as any
  } catch {
    // handle error
  }
  loading.value = false
})
</script>

<style scoped>
.history-page {
  max-width: 800px;
  margin: 0 auto;
}

.page-title {
  font-size: 28px;
  color: var(--gold-color);
  text-align: center;
  margin-bottom: 32px;
}

.empty {
  text-align: center;
  padding: 60px 0;
  color: var(--text-secondary);
}

.empty .el-button {
  margin-top: 16px;
}

.records-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.record-card {
  background: var(--card-bg);
  border: 1px solid rgba(212, 168, 75, 0.15);
  border-radius: 12px;
  padding: 20px 24px;
  cursor: pointer;
  transition: all 0.3s;
}

.record-card:hover {
  border-color: var(--gold-color);
  transform: translateY(-2px);
}

.record-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.record-date {
  color: var(--gold-color);
  font-weight: 600;
}

.record-gender {
  color: var(--text-secondary);
}

.record-info {
  display: flex;
  gap: 16px;
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 8px;
}

.record-preview {
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.5;
}
</style>
