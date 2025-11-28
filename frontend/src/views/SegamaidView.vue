<template>
  <div class="segamaid-view">
    <!-- 查询卡片 -->
    <el-card class="search-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon class="header-icon"><Key /></el-icon>
          <h3 class="header-title">Segamaid绑定</h3>
        </div>
      </template>
      
      <el-form :model="bindForm" class="bind-form" label-position="top">
        <el-row :gutter="24">
          <el-col :xs="24" :sm="12" :md="8">
            <el-form-item label="玩家ID">
              <el-input 
                v-model="bindForm.playerId" 
                placeholder="请输入玩家ID" 
                class="bind-input"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8">
            <el-form-item label="Segamaid Token">
              <el-input 
                v-model="bindForm.segamaidToken" 
                placeholder="请输入Segamaid Token" 
                class="bind-input"
                type="password"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="24" :md="8" class="button-col">
            <el-form-item>
              <el-button type="primary" @click="handleBind" :loading="loading" class="bind-button">
                <el-icon><Link /></el-icon>
                绑定Segamaid
              </el-button>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>

    <!-- 结果展示区域 -->
    <transition name="fade">
      <div v-if="bindResult" class="result-section">
        <el-card class="result-card" shadow="hover">
          <template #header>
            <div class="result-header">
              <el-icon class="result-icon"><Check /></el-icon>
              <h3 class="result-title">绑定结果</h3>
            </div>
          </template>
          
          <div class="result-content">
            <el-alert
              :title="bindResult.status === 'success' ? '绑定成功' : '绑定失败'"
              :description="bindResult.message"
              :type="bindResult.status === 'success' ? 'success' : 'error'"
              show-icon
              center
            ></el-alert>
            
            <div v-if="bindResult.status === 'success' && bindResult.data" class="bind-info">
              <el-descriptions :column="2" border>
                <el-descriptions-item label="玩家ID" :span="1">{{ bindResult.data.playerId }}</el-descriptions-item>
                <el-descriptions-item label="Segamaid ID" :span="1">{{ bindResult.data.segamaidId }}</el-descriptions-item>
                <el-descriptions-item label="绑定时间" :span="1">{{ bindResult.data.bindTime }}</el-descriptions-item>
                <el-descriptions-item label="状态" :span="1">
                  <el-tag type="success">已绑定</el-tag>
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </div>
        </el-card>
      </div>
    </transition>

    <!-- 错误提示 -->
    <transition name="fade">
      <div v-if="error" class="error-section">
        <el-alert
          title="绑定失败"
          :description="error"
          type="error"
          show-icon
          center
          :closable="true"
          @close="error = ''"
        ></el-alert>
      </div>
    </transition>

    <!-- 空状态 -->
    <transition name="fade">
      <div v-if="!loading && !bindResult && !error" class="empty-section">
        <el-empty
          description="请输入玩家ID和Segamaid Token进行绑定"
          image-size="120"
        >
          <el-button type="primary" @click="focusPlayerIdInput">
            <el-icon><Key /></el-icon>
            去绑定
          </el-button>
        </el-empty>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick } from 'vue'
import { api } from '../api'

const loading = ref(false)
const bindResult = ref(null)
const error = ref('')
const playerIdInputRef = ref(null)

const bindForm = reactive({
  playerId: '',
  segamaidToken: ''
})

const handleBind = async () => {
  if (!bindForm.playerId) {
    error.value = '请输入玩家ID'
    return
  }
  
  if (!bindForm.segamaidToken) {
    error.value = '请输入Segamaid Token'
    return
  }
  
  loading.value = true
  error.value = ''
  bindResult.value = null
  
  try {
    const result = await api.bindSegamaid(bindForm)
    bindResult.value = result
  } catch (err) {
    error.value = err.message || '绑定失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

// 聚焦玩家ID输入框
const focusPlayerIdInput = () => {
  nextTick(() => {
    if (playerIdInputRef.value) {
      playerIdInputRef.value.focus()
    }
  })
}
</script>

<style scoped>
.segamaid-view {
  max-width: 1200px;
  margin: 0 auto;
}

/* 查询卡片样式 */
.search-card {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon {
  font-size: 24px;
  color: #409eff;
}

.header-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.bind-form {
  padding: 16px 0;
}

.bind-input {
  width: 100%;
}

.button-col {
  display: flex;
  align-items: flex-end;
}

.bind-button {
  width: 100%;
  height: 40px;
}

/* 结果展示区域 */
.result-section {
  margin-top: 24px;
}

.result-card {
  margin-bottom: 24px;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.result-icon {
  font-size: 20px;
  color: #67c23a;
}

.result-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

/* 结果内容 */
.result-content {
  padding: 20px 0;
}

.bind-info {
  margin-top: 20px;
}

/* 错误提示 */
.error-section {
  margin-top: 24px;
}

.error-section .el-alert {
  border-radius: 8px;
}

/* 空状态 */
.empty-section {
  margin-top: 60px;
  text-align: center;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>