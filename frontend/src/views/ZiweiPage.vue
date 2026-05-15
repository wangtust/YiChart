<template>
  <div class="ziwei-page">
    <h1 class="page-title">紫微斗数</h1>
    <p class="page-desc">请输入您的出生信息，排紫微命盘，AI 为您详细解读</p>

    <div class="form-container">
      <el-form :model="form" label-width="100px" size="large">
        <el-form-item label="出生日期">
          <el-date-picker
            v-model="form.birth_date"
            type="date"
            placeholder="选择出生日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="出生时间">
          <el-time-picker
            v-model="form.birth_time"
            placeholder="选择出生时间"
            format="HH:mm"
            value-format="HH:mm"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="性别">
          <el-radio-group v-model="form.gender">
            <el-radio value="male">男</el-radio>
            <el-radio value="female">女</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleAnalyze"
            class="submit-btn"
          >
            {{ loading ? 'AI 分析中...' : '开始排盘' }}
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 紫微命盘 -->
    <div v-if="ziweiResult" class="result-section">
      <h2 class="section-title">紫微命盘</h2>

      <!-- 基本信息 -->
      <div class="info-bar">
        <span>五行局: {{ ziweiResult['五行局'] }}</span>
        <span>命宫: {{ ziweiResult.ming_gong }}</span>
        <span>身宫: {{ ziweiResult.shen_gong }}</span>
        <span>生肖: {{ ziweiResult.生肖 }}</span>
      </div>

      <!-- 十二宫格 -->
      <div class="palace-grid">
        <div
          v-for="(gong, name) in ziweiResult.palaces"
          :key="name"
          class="palace-cell"
          :class="{ 'is-ming': gong.是命宫, 'is-shen': gong.是身宫 }"
        >
          <div class="palace-name">{{ name }}</div>
          <div class="palace-zhi">{{ gong.地支 }}</div>
          <div class="palace-stars">
            <span v-for="star in gong.星曜" :key="star" class="star-tag">{{ star }}</span>
          </div>
          <div v-if="gong.是命宫" class="palace-marker">命</div>
          <div v-if="gong.是身宫" class="palace-marker shen">身</div>
        </div>
      </div>

      <!-- 四化 -->
      <div class="sihua-section">
        <h3>四化</h3>
        <div class="sihua-tags">
          <span class="sihua-tag lu" v-if="ziweiResult.sihua?.化禄">化禄: {{ ziweiResult.sihua.化禄 }}</span>
          <span class="sihua-tag quan" v-if="ziweiResult.sihua?.化权">化权: {{ ziweiResult.sihua.化权 }}</span>
          <span class="sihua-tag ke" v-if="ziweiResult.sihua?.化科">化科: {{ ziweiResult.sihua.化科 }}</span>
          <span class="sihua-tag ji" v-if="ziweiResult.sihua?.化忌">化忌: {{ ziweiResult.sihua.化忌 }}</span>
        </div>
      </div>
    </div>

    <!-- AI 分析 -->
    <div v-if="aiAnalysis" class="analysis-section">
      <h2 class="section-title">AI 命理分析</h2>
      <div class="analysis-content" v-html="formatAnalysisHtml(aiAnalysis)"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { streamAnalyze, ziweiApi } from '@/api'
import type { ZiweiInput, ZiweiResult } from '@/api'
import { formatAnalysisHtml } from '@/utils/formatAnalysis'

const loading = ref(false)
const ziweiResult = ref<ZiweiResult | null>(null)
const aiAnalysis = ref('')

const form = reactive<ZiweiInput>({
  birth_date: '',
  birth_time: '',
  gender: 'male',
})

async function handleAnalyze() {
  if (!form.birth_date || !form.birth_time) {
    ElMessage.warning('请填写完整的出生信息')
    return
  }

  loading.value = true
  ziweiResult.value = null
  aiAnalysis.value = ''

  try {
    // 先排盘
    const result = await ziweiApi.calculate({ ...form })
    ziweiResult.value = result

    // 流式获取 AI 分析
    await streamAnalyze('/ziwei/analyze', { ...form }, (chunk) => {
      aiAnalysis.value += chunk
    })
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '分析失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.ziwei-page { max-width: 900px; margin: 0 auto; }
.page-title { font-size: 32px; color: var(--gold-color); text-align: center; margin-bottom: 8px; }
.page-desc { text-align: center; color: var(--text-secondary); margin-bottom: 40px; }

.form-container {
  background: var(--card-bg); border: 1px solid rgba(212,168,75,0.2);
  border-radius: 16px; padding: 32px; margin-bottom: 32px;
}
.submit-btn {
  width: 100%;
  background: linear-gradient(135deg, var(--primary-color), #e63956) !important;
  border: none !important; font-size: 16px;
}

.result-section, .analysis-section {
  background: var(--card-bg); border: 1px solid rgba(212,168,75,0.2);
  border-radius: 16px; padding: 32px; margin-bottom: 32px;
}
.section-title { color: var(--gold-color); font-size: 22px; margin-bottom: 24px; text-align: center; }

.info-bar {
  display: flex; justify-content: center; gap: 24px;
  color: var(--text-secondary); font-size: 14px; margin-bottom: 24px;
}

/* 十二宫格 */
.palace-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;
}
.palace-cell {
  background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.05);
  border-radius: 8px; padding: 12px; min-height: 100px; position: relative;
}
.palace-cell.is-ming { border-color: var(--gold-color); }
.palace-cell.is-shen { border-color: var(--primary-color); }
.palace-name { color: var(--gold-color); font-size: 13px; font-weight: 600; }
.palace-zhi { color: var(--text-secondary); font-size: 11px; margin-bottom: 6px; }
.palace-stars { display: flex; flex-wrap: wrap; gap: 4px; }
.star-tag {
  background: rgba(212,168,75,0.15); color: var(--gold-color);
  font-size: 11px; padding: 1px 6px; border-radius: 4px;
}
.palace-marker {
  position: absolute; top: 4px; right: 4px;
  background: var(--gold-color); color: #000; font-size: 10px;
  width: 18px; height: 18px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; font-weight: 700;
}
.palace-marker.shen { background: var(--primary-color); color: #fff; }

/* 四化 */
.sihua-section { margin-top: 24px; }
.sihua-section h3 { color: var(--text-primary); font-size: 16px; margin-bottom: 12px; }
.sihua-tags { display: flex; gap: 12px; justify-content: center; }
.sihua-tag { padding: 4px 16px; border-radius: 20px; font-size: 14px; }
.sihua-tag.lu { background: rgba(76,175,80,0.2); color: #4caf50; }
.sihua-tag.quan { background: rgba(255,152,0,0.2); color: #ff9800; }
.sihua-tag.ke { background: rgba(33,150,243,0.2); color: #2196f3; }
.sihua-tag.ji { background: rgba(244,67,54,0.2); color: #f44336; }

.analysis-content { line-height: 1.8; color: var(--text-primary); font-size: 15px; }
.analysis-content :deep(.analysis-h3) { color: var(--gold-color); margin: 20px 0 8px; font-size: 17px; }
.analysis-content :deep(.analysis-h2) { color: var(--gold-color); margin: 24px 0 10px; font-size: 19px; }
.analysis-content :deep(.analysis-h1) { color: var(--gold-color); margin: 28px 0 12px; font-size: 22px; }
</style>
