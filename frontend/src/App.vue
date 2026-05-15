<template>
  <el-config-provider :locale="zhCn">
    <div class="app-container">
      <header class="app-header">
        <div class="header-content">
          <router-link to="/" class="logo">
            <span class="logo-icon">☯</span>
            <span class="logo-text">易算</span>
          </router-link>
          <nav class="nav-links">
            <router-link to="/">首页</router-link>
            <router-link to="/bazi">八字算命</router-link>
            <router-link to="/ziwei">紫微斗数</router-link>
            <router-link to="/liuyao">六爻占卜</router-link>
            <router-link to="/history">历史记录</router-link>
          </nav>
          <div class="user-section">
            <template v-if="userStore.isLoggedIn">
              <span class="username">{{ userStore.username }}</span>
              <el-button text size="small" @click="handleLogout">退出</el-button>
            </template>
            <router-link v-else to="/login" class="login-link">登录</router-link>
          </div>
        </div>
      </header>

      <main class="app-main">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>

      <footer class="app-footer">
        <p>易算 - AI 命理分析 | 仅供娱乐参考</p>
      </footer>
    </div>
  </el-config-provider>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

onMounted(() => {
  if (userStore.token) {
    userStore.fetchUser()
  }
})

function handleLogout() {
  userStore.logout()
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: rgba(22, 33, 62, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(212, 168, 75, 0.2);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: var(--gold-color);
}

.logo-icon {
  font-size: 28px;
}

.logo-text {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 2px;
}

.nav-links {
  display: flex;
  gap: 32px;
}

.nav-links a {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 15px;
  transition: color 0.3s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: var(--gold-color);
}

.app-main {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  padding: 32px 24px;
}

.app-footer {
  text-align: center;
  padding: 24px;
  color: var(--text-secondary);
  font-size: 13px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.user-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  color: var(--gold-color);
  font-size: 14px;
}

.login-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  padding: 6px 16px;
  border: 1px solid rgba(212, 168, 75, 0.3);
  border-radius: 20px;
  transition: all 0.3s;
}

.login-link:hover {
  color: var(--gold-color);
  border-color: var(--gold-color);
}
</style>
