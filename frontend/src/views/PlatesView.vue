<template>
  <div class="plates-view">
    <!-- 查询卡片 -->
    <el-card class="search-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon class="header-icon"><Medal /></el-icon>
          <h3 class="header-title">牌子进度</h3>
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
          <el-col :xs="24" :sm="12" :md="8">
            <el-form-item label="查询值">
              <el-input 
                v-model="searchForm.searchValue" 
                placeholder="请输入查询值" 
                class="search-input"
                @keyup.enter="handleSearch"
              >
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="6">
            <el-form-item label="牌子类型">
              <el-select v-model="searchForm.plateType" placeholder="请选择牌子类型" class="plate-select">
                <el-option label="舞将" value="舞将"></el-option>
                <el-option label="舞霸" value="舞霸"></el-option>
                <el-option label="舞神" value="舞神"></el-option>
                <el-option label="舞圣" value="舞圣"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="2" class="search-button-col">
            <el-form-item>
              <el-button type="primary" @click="handleSearch" :loading="loading" class="search-btn">
                <el-icon><Search /></el-icon>
                查询
              </el-button>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>

    <!-- 结果展示区域 -->
    <transition name="fade">
      <div v-if="plateProgress" class="result-section">
        <!-- 进度卡片 -->
        <el-card class="progress-card" shadow="hover">
          <template #header>
            <div class="progress-header">
              <el-icon class="progress-icon"><Progress /></el-icon>
              <h3 class="progress-title">{{ plateProgress.plate_type }}进度</h3>
            </div>
          </template>
          
          <div class="progress-content">
            <div class="progress-circle-wrapper">
              <el-progress
                type="circle"
                :percentage="parseFloat(plateProgress.completion_rate) * 100"
                :format="progressFormat"
                :width="180"
                :stroke-width="16"
                :color="progressColor"
              ></el-progress>
            </div>
            <div class="progress-stats">
              <div class="stat-item">
                <div class="stat-label">已完成</div>
                <div class="stat-value completed">{{ plateProgress.cleared_count }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">总数</div>
                <div class="stat-value total">{{ plateProgress.total_count }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">完成率</div>
                <div class="stat-value rate">{{ plateProgress.completion_rate }}</div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 牌子列表 -->
        <el-card class="plates-card" shadow="hover">
          <template #header>
            <div class="plates-header">
              <el-icon class="plates-icon"><List /></el-icon>
              <h3 class="plates-title">牌子列表</h3>
            </div>
          </template>
          
          <div class="table-wrapper">
            <el-table 
              :data="plateProgress.plates" 
              stripe 
              style="width: 100%"
              class="plates-table"
              v-loading="loading"
            >
              <el-table-column prop="name" label="牌子名称" min-width="200">
                <template #default="scope">
                  <div class="plate-name">
                    <el-icon class="plate-icon">
                      <Medal v-if="scope.row.cleared" />
                      <Trophy v-else />
                    </el-icon>
                    <span>{{ scope.row.name }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="description" label="描述" min-width="300"></el-table-column>
              <el-table-column prop="cleared" label="状态" width="120" align="center">
                <template #default="scope">
                  <el-tag :type="scope.row.cleared ? 'success' : 'warning'" size="large">
                    <el-icon>
                      <Check v-if="scope.row.cleared" />
                      <Close v-else />
                    </el-icon>
                    {{ scope.row.cleared ? '已完成' : '未完成' }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </div>
    </transition>

    <!-- 空状态 -->
    <transition name="fade">
      <div v-if="!loading && !plateProgress && !error" class="empty-section">
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
  </div>
</template>

<script setup>
import { ref, reactive, nextTick, computed } from 'vue'
import { api } from '../api'

const loading = ref(false)
const plateProgress = ref(null)
const error = ref('')
const searchInputRef = ref(null)

const searchForm = reactive({
  searchType: 'username',
  searchValue: '',
  plateType: '舞将',
  provider: 'divingfish'
})

// 进度条颜色，根据完成率动态变化
const progressColor = computed(() => {
  if (!plateProgress.value) return '#409eff'
  
  const completionRate = parseFloat(plateProgress.value.completion_rate)
  if (completionRate >= 0.9) return '#67c23a' // 90%+ 绿色
  if (completionRate >= 0.7) return '#e6a23c' // 70%-89% 黄色
  if (completionRate >= 0.5) return '#f56c6c' // 50%-69% 红色
  return '#909399' // 50%以下 灰色
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
  plateProgress.value = null
  
  try {
    const params = {
      plate_type: searchForm.plateType,
      provider: searchForm.provider
    }
    
    if (searchForm.searchType === 'username') {
      params.username = searchForm.searchValue
    } else {
      params.friend_code = searchForm.searchValue
    }
    
    const result = await api.getPlayerPlates(params)
    plateProgress.value = result
  } catch (err) {
    error.value = err.message || '查询失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

const progressFormat = (percentage) => {
  return `${percentage.toFixed(0)}%`
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
.plates-view {
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

.plate-select {
  width: 100%;
}

.search-button-col {
  display: flex;
  align-items: flex-end;
}

.search-btn {
  width: 100%;
}

/* 结果展示区域 */
.result-section {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 进度卡片样式 */
.progress-card {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  border-radius: 12px;
}

.progress-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progress-icon {
  font-size: 20px;
  color: white;
}

.progress-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: white;
}

.progress-content {
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 32px 0;
}

@media (max-width: 768px) {
  .progress-content {
    flex-direction: column;
    gap: 32px;
  }
}

.progress-circle-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.progress-stats {
  display: flex;
  gap: 48px;
}

@media (max-width: 768px) {
  .progress-stats {
    gap: 32px;
  }
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 12px;
  font-weight: 500;
}

.stat-value {
  font-size: 48px;
  font-weight: 700;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.stat-value.completed {
  color: #67c23a;
}

.stat-value.total {
  color: #e6a23c;
}

.stat-value.rate {
  font-size: 36px;
  color: #f56c6c;
}

/* 牌子列表卡片 */
.plates-card {
  border-radius: 12px;
}

.plates-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.plates-icon {
  font-size: 20px;
  color: #409eff;
}

.plates-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.table-wrapper {
  overflow-x: auto;
}

.plates-table {
  border-radius: 8px;
  overflow: hidden;
  margin-top: 16px;
}

.plates-table .el-table__header-wrapper th {
  background-color: #fafafa;
  font-weight: 600;
}

.plate-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: #303133;
}

.plate-icon {
  font-size: 18px;
}

.plate-icon :deep(.el-icon-medal) {
  color: #e6a23c;
}

.plate-icon :deep(.el-icon-trophy) {
  color: #909399;
}

/* 空状态 */
.empty-section {
  margin-top: 60px;
  text-align: center;
}

/* 错误提示 */
.error-section {
  margin-top: 24px;
}

.error-section .el-alert {
  border-radius: 8px;
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
