<template>
  <div class="home">
    <section class="hero">
      <div class="hero-bg">
        <div class="bagua-symbol">☯</div>
      </div>
      <h1 class="hero-title">易算 · AI 命理分析</h1>
      <p class="hero-subtitle">融合千年命理智慧与人工智能，为您解读命运密码</p>
      <router-link to="/bazi" class="cta-button">
        开始算命
        <span class="cta-arrow">→</span>
      </router-link>
    </section>

    <section class="features">
      <div class="feature-card" v-for="feature in features" :key="feature.title">
        <div class="feature-icon">{{ feature.icon }}</div>
        <h3>{{ feature.title }}</h3>
        <p>{{ feature.desc }}</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const features = [
  { icon: '八字', title: '八字排盘', desc: '精准计算天干地支、五行分布，传统命理一目了然' },
  { icon: 'AI', title: 'AI 解读', desc: '大模型深度分析命格特点，给出个性化运势建议' },
  { icon: '五行', title: '五行分析', desc: '直观展示五行强弱，助您了解自身特质' },
  { icon: '运势', title: '运势指引', desc: '事业、感情、健康多维度分析，把握人生方向' },
]
</script>

<style scoped>
.home {
  text-align: center;
}

.hero {
  position: relative;
  padding: 80px 0 60px;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.06;
  pointer-events: none;
}

.bagua-symbol {
  font-size: 400px;
  color: var(--gold-color);
  animation: rotate 60s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.hero-title {
  font-size: 48px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--gold-color), #f0d68a);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 16px;
  position: relative;
}

.hero-subtitle {
  font-size: 18px;
  color: var(--text-secondary);
  margin-bottom: 40px;
  position: relative;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 16px 48px;
  background: linear-gradient(135deg, var(--primary-color), #e63956);
  color: white;
  border-radius: 50px;
  font-size: 18px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
  position: relative;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(196, 30, 58, 0.4);
}

.cta-arrow {
  transition: transform 0.3s;
}
.cta-button:hover .cta-arrow {
  transform: translateX(4px);
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-top: 40px;
}

.feature-card {
  background: var(--card-bg);
  border: 1px solid rgba(212, 168, 75, 0.15);
  border-radius: 16px;
  padding: 32px 24px;
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-4px);
  border-color: rgba(212, 168, 75, 0.4);
}

.feature-icon {
  font-size: 36px;
  margin-bottom: 16px;
}

.feature-card h3 {
  color: var(--gold-color);
  margin-bottom: 8px;
  font-size: 18px;
}

.feature-card p {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}
</style>
