<template>
  <div class="bazi-page">
    <h1 class="page-title">八字算命</h1>
    <p class="page-desc">请输入您的出生信息，AI 将为您进行详细的命理分析</p>

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

        <el-form-item label="历法">
          <el-radio-group v-model="form.is_lunar">
            <el-radio :value="false">公历</el-radio>
            <el-radio :value="true">农历</el-radio>
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
            {{ loading ? 'AI 分析中...' : '开始算命' }}
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 八字排盘结果 -->
    <div v-if="baziResult" class="result-section">
      <h2 class="section-title">八字排盘</h2>
      <div class="pillars">
        <div class="pillar" v-for="(pillar, key) in pillars" :key="key">
          <div class="pillar-label">{{ pillarLabels[key] }}</div>
          <div class="pillar-stem" :class="getWuxingClass(pillar.wuxing)">
            {{ pillar.heavenly_stem }}
          </div>
          <div class="pillar-branch" :class="getWuxingClass(getBranchWuxing(pillar.earthly_branch))">
            {{ pillar.earthly_branch }}
          </div>
          <div class="pillar-info">
            <span class="pillar-wuxing">{{ pillar.wuxing }}</span>
            <span class="pillar-shishen">{{ baziResult.shishen[pillarShishenKeys[key]] }}</span>
          </div>
        </div>
      </div>

      <!-- 五行统计 -->
      <div class="wuxing-section">
        <h3>五行分布</h3>
        <div class="wuxing-bars">
          <div class="wuxing-bar" v-for="(count, wx) in baziResult.wuxing" :key="wx">
            <span class="wuxing-name" :class="getWuxingClass(wx as string)">{{ wx }}</span>
            <div class="bar-track">
              <div class="bar-fill" :class="getWuxingBgClass(wx as string)" :style="{ width: count * 20 + '%' }"></div>
            </div>
            <span class="wuxing-count">{{ count }}</span>
          </div>
        </div>
        <div class="bazi-meta">
          <span>生肖: {{ baziResult.shengxiao }}</span>
          <span>纳音: {{ baziResult.nayin }}</span>
          <span>日主: {{ baziResult.day_master }} ({{ baziResult.day_master_wuxing }})</span>
        </div>
      </div>
    </div>

    <!-- AI 分析结果 -->
    <div v-if="aiAnalysis" class="analysis-section">
      <h2 class="section-title">AI 命理分析</h2>
      <div class="analysis-content" v-html="formatAnalysis(aiAnalysis)"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { streamAnalyze, baziApi } from '@/api'

const loading = ref(false)
const baziResult = ref<any>(null)
const aiAnalysis = ref('')

const form = reactive({
  birth_date: '',
  birth_time: '',
  gender: 'male',
  is_lunar: false,
})

const pillarLabels: Record<string, string> = {
  year_pillar: '年柱',
  month_pillar: '月柱',
  day_pillar: '日柱',
  hour_pillar: '时柱',
}

const pillarShishenKeys: Record<string, string> = {
  year_pillar: '年干',
  month_pillar: '月干',
  day_pillar: '日干',
  hour_pillar: '时干',
}

const pillars = ref<any>({})

const DIZHI_WUXING: Record<string, string> = {
  子: '水', 丑: '土', 寅: '木', 卯: '木', 辰: '土', 巳: '火',
  午: '火', 未: '土', 申: '金', 酉: '金', 戌: '土', 亥: '水',
}

function getBranchWuxing(branch: string) {
  return DIZHI_WUXING[branch] || ''
}

function getWuxingClass(wx: string) {
  const map: Record<string, string> = { 金: 'wx-jin', 木: 'wx-mu', 水: 'wx-shui', 火: 'wx-huo', 土: 'wx-tu' }
  return map[wx] || ''
}

function getWuxingBgClass(wx: string) {
  const map: Record<string, string> = { 金: 'bg-jin', 木: 'bg-mu', 水: 'bg-shui', 火: 'bg-huo', 土: 'bg-tu' }
  return map[wx] || ''
}

function formatAnalysis(text: string) {
  return text
    .replace(/^###\s*(.+)$/gm, '<h3 class="analysis-h3">$1</h3>')
    .replace(/^##\s*(.+)$/gm, '<h2 class="analysis-h2">$1</h2>')
    .replace(/^#\s*(.+)$/gm, '<h1 class="analysis-h1">$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>')
}

async function handleAnalyze() {
  if (!form.birth_date || !form.birth_time) {
    ElMessage.warning('请填写完整的出生信息')
    return
  }

  loading.value = true
  baziResult.value = null
  aiAnalysis.value = ''

  try {
    // 先排盘
    const result = await baziApi.calculate({
      birth_date: form.birth_date,
      birth_time: form.birth_time,
      gender: form.gender as 'male' | 'female',
      is_lunar: form.is_lunar,
    })
    baziResult.value = result
    pillars.value = {
      year_pillar: result.year_pillar,
      month_pillar: result.month_pillar,
      day_pillar: result.day_pillar,
      hour_pillar: result.hour_pillar,
    }

    // 流式获取 AI 分析
    await streamAnalyze(
      {
        birth_date: form.birth_date,
        birth_time: form.birth_time,
        gender: form.gender as 'male' | 'female',
        is_lunar: form.is_lunar,
      },
      (chunk) => {
        aiAnalysis.value += chunk
      },
      () => {
        loading.value = false
      }
    )
  } catch (error: any) {
    ElMessage.error(error.message || '分析失败')
    loading.value = false
  }
}
</script>

<style scoped>
.bazi-page {
  max-width: 800px;
  margin: 0 auto;
}

.page-title {
  font-size: 32px;
  color: var(--gold-color);
  text-align: center;
  margin-bottom: 8px;
}

.page-desc {
  text-align: center;
  color: var(--text-secondary);
  margin-bottom: 40px;
}

.form-container {
  background: var(--card-bg);
  border: 1px solid rgba(212, 168, 75, 0.2);
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 32px;
}

.submit-btn {
  width: 100%;
  background: linear-gradient(135deg, var(--primary-color), #e63956) !important;
  border: none !important;
  font-size: 16px;
}

.result-section, .analysis-section {
  background: var(--card-bg);
  border: 1px solid rgba(212, 168, 75, 0.2);
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 32px;
}

.section-title {
  color: var(--gold-color);
  font-size: 22px;
  margin-bottom: 24px;
  text-align: center;
}

/* 四柱 */
.pillars {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.pillar {
  text-align: center;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  padding: 20px 12px;
}

.pillar-label {
  color: var(--text-secondary);
  font-size: 13px;
  margin-bottom: 12px;
}

.pillar-stem, .pillar-branch {
  font-size: 36px;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 8px;
}

.pillar-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 12px;
  color: var(--text-secondary);
}

/* 五行颜色 */
.wx-jin, .bg-jin { color: #ffd700; }
.wx-mu, .bg-mu { color: #4caf50; }
.wx-shui, .bg-shui { color: #2196f3; }
.wx-huo, .bg-huo { color: #f44336; }
.wx-tu, .bg-tu { color: #ff9800; }
.bg-jin { background: #ffd700; }
.bg-mu { background: #4caf50; }
.bg-shui { background: #2196f3; }
.bg-huo { background: #f44336; }
.bg-tu { background: #ff9800; }

/* 五行柱状图 */
.wuxing-section h3 {
  color: var(--text-primary);
  margin-bottom: 16px;
  font-size: 16px;
}

.wuxing-bars {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.wuxing-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.wuxing-name {
  width: 24px;
  font-size: 16px;
  font-weight: 700;
}

.bar-track {
  flex: 1;
  height: 24px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 12px;
  transition: width 0.8s ease;
  opacity: 0.8;
}

.wuxing-count {
  width: 24px;
  text-align: center;
  color: var(--text-secondary);
}

.bazi-meta {
  display: flex;
  justify-content: center;
  gap: 24px;
  color: var(--text-secondary);
  font-size: 14px;
}

/* AI 分析 */
.analysis-content {
  line-height: 1.8;
  color: var(--text-primary);
  font-size: 15px;
}

.analysis-content :deep(.analysis-h3) {
  color: var(--gold-color);
  margin: 20px 0 8px;
  font-size: 17px;
}
.analysis-content :deep(.analysis-h2) {
  color: var(--gold-color);
  margin: 24px 0 10px;
  font-size: 19px;
}
.analysis-content :deep(.analysis-h1) {
  color: var(--gold-color);
  margin: 28px 0 12px;
  font-size: 22px;
}
</style>
