<template>
  <div class="login-page">
    <div class="login-card">
      <h2>{{ isRegister ? '注册' : '登录' }}</h2>

      <el-form :model="form" size="large">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名" prefix-icon="User" />
        </el-form-item>

        <el-form-item v-if="isRegister">
          <el-input v-model="form.email" placeholder="邮箱" prefix-icon="Message" />
        </el-form-item>

        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock" show-password />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" class="submit-btn" :loading="loading" @click="handleSubmit">
            {{ isRegister ? '注册' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>

      <p class="switch-mode" @click="isRegister = !isRegister">
        {{ isRegister ? '已有账号？去登录' : '没有账号？去注册' }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const isRegister = ref(false)

const form = reactive({
  username: '',
  email: '',
  password: '',
})

async function handleSubmit() {
  if (!form.username || !form.password) {
    ElMessage.warning('请填写用户名和密码')
    return
  }

  loading.value = true
  try {
    if (isRegister.value) {
      await userStore.register(form.username, form.email, form.password)
      ElMessage.success('注册成功，请登录')
      isRegister.value = false
    } else {
      await userStore.login(form.username, form.password)
      ElMessage.success('登录成功')
      router.push('/')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
  loading.value = false
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.login-card {
  background: var(--card-bg);
  border: 1px solid rgba(212, 168, 75, 0.2);
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.login-card h2 {
  text-align: center;
  color: var(--gold-color);
  margin-bottom: 32px;
  font-size: 24px;
}

.submit-btn {
  width: 100%;
  background: linear-gradient(135deg, var(--primary-color), #e63956) !important;
  border: none !important;
}

.switch-mode {
  text-align: center;
  color: var(--text-secondary);
  cursor: pointer;
  margin-top: 16px;
  font-size: 14px;
}

.switch-mode:hover {
  color: var(--gold-color);
}
</style>
