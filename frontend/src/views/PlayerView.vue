<template>
  <div class="player-view">
    <!-- 查询卡片 -->
    <el-card class="search-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon class="header-icon"><User /></el-icon>
          <h3 class="header-title">玩家查询</h3>
        </div>
      </template>
      
      <el-form :model="searchForm" class="search-form" label-position="top">
        <el-row :gutter="24">
          <el-col :xs="24" :sm="12" :md="8">
            <el-form-item label="查询方式">
              <el-radio-group v-model="searchForm.searchType" @change="handleSearchTypeChange" class="search-type-group">
                <el-radio-button label="username">用户名（水鱼）</el-radio-button>
                <el-radio-button label="friend_code">好友码（落雪）</el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="16" :md="12">
            <el-form-item label="查询值">
              <el-input 
                v-model="searchForm.searchValue" 
                placeholder="请输入查询值" 
                class="search-input"
                @keyup.enter="handleSearch"
              >
                <template #append>
                  <el-button type="primary" @click="handleSearch" :loading="loading">
                    <el-icon><Search /></el-icon>
                    查询
                  </el-button>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>

    <!-- 结果展示区域 -->
    <transition name="fade">
      <div v-if="playerInfo" class="result-section">
        <el-card class="result-card" shadow="hover">
          <template #header>
            <div class="result-header">
              <el-icon class="result-icon"><InfoFilled /></el-icon>
              <h3 class="result-title">玩家信息</h3>
            </div>
          </template>
          
          <div class="player-info-wrapper">
            <!-- 玩家基本信息卡片 -->
            <el-card class="basic-info-card" shadow="hover">
              <div class="basic-info-content">
                <div class="player-avatar">
                  <el-icon class="avatar-icon"><User /></el-icon>
                </div>
                <div class="player-basic">
                  <h4 class="player-name">{{ playerInfo.username }}</h4>
                  <div class="player-rating">
                    <el-tag type="primary" size="large">
                      <el-icon><Star /></el-icon>
                      Rating: {{ playerInfo.rating || 0 }}
                    </el-tag>
                  </div>
                </div>
              </div>
            </el-card>

            <!-- 详细信息 -->
            <el-card class="detail-info-card" shadow="hover">
              <template #header>
                <div class="detail-header">
                  <span>详细信息</span>
                </div>
              </template>
              <el-descriptions :column="3" border>
                <el-descriptions-item label="用户名" :span="1">{{ playerInfo.username }}</el-descriptions-item>
                <el-descriptions-item label="好友码" :span="1">{{ playerInfo.friend_code || '未提供' }}</el-descriptions-item>
                <el-descriptions-item label="等级" :span="1">{{ playerInfo.level || '未提供' }}</el-descriptions-item>
                <el-descriptions-item label="角色" :span="1">{{ playerInfo.character || '未提供' }}</el-descriptions-item>
                <el-descriptions-item label="头衔" :span="2">{{ playerInfo.title || '未提供' }}</el-descriptions-item>
              </el-descriptions>
            </el-card>
          </div>
        </el-card>
      </div>
    </transition>

    <!-- 错误提示 -->
    <transition name="fade">
      <div v-if="error" class="error-section">
        <el-alert
          title="查询失败"
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
      <div v-if="!loading && !playerInfo && !error" class="empty-section">
        <el-empty
          description="请输入查询条件进行搜索"
          image-size="120"
        >
          <el-button type="primary" @click="focusSearchInput">
            <el-icon><Search /></el-icon>
            去搜索
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
const playerInfo = ref(null)
const error = ref('')
const searchInputRef = ref(null)

const searchForm = reactive({
  searchType: 'username',
  searchValue: '',
  provider: 'divingfish'
})

const handleSearchTypeChange = (value) => {
  searchForm.provider = value === 'username' ? 'divingfish' : 'lxns'
}

const handleSearch = async () => {
  if (!searchForm.searchValue) {
    error.value = '请输入查询值'
    return
  }
  
  loading.value = true
  error.value = ''
  playerInfo.value = null
  
  try {
    const params = {
      provider: searchForm.provider
    }
    
    if (searchForm.searchType === 'username') {
      params.username = searchForm.searchValue
    } else {
      params.friend_code = searchForm.searchValue
    }
    
    const result = await api.searchPlayer(params)
    playerInfo.value = result
  } catch (err) {
    error.value = err.message || '查询失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

// 聚焦搜索输入框
const focusSearchInput = () => {
  nextTick(() => {
    if (searchInputRef.value) {
      searchInputRef.value.focus()
    }
  })
}
</script>

<style scoped>
.player-view {
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

.search-form {
  padding: 16px 0;
}

.search-type-group {
  width: 100%;
}

.search-type-group .el-radio-button {
  flex: 1;
  text-align: center;
}

.search-input {
  width: 100%;
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
  color: #409eff;
}

.result-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

/* 玩家信息包装器 */
.player-info-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 基本信息卡片 */
.basic-info-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
}

.basic-info-content {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 20px;
}

@media (max-width: 768px) {
  .basic-info-content {
    flex-direction: column;
    text-align: center;
  }
}

.player-avatar {
  width: 100px;
  height: 100px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.avatar-icon {
  font-size: 60px;
  color: white;
}

.player-basic {
  flex: 1;
}

.player-name {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 12px;
  color: white;
}

.player-rating {
  margin-top: 12px;
}

.player-rating .el-tag {
  font-size: 16px;
  padding: 8px 16px;
  border-radius: 20px;
  background-color: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

/* 详细信息卡片 */
.detail-info-card {
  border-radius: 12px;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-header span {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.detail-info-card .el-descriptions {
  margin-top: 16px;
}

.detail-info-card .el-descriptions__label {
  font-weight: 500;
  color: #606266;
  background-color: #fafafa;
}

.detail-info-card .el-descriptions__content {
  font-weight: 500;
  color: #303133;
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
