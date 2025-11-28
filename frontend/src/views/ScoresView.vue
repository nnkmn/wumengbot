<template>
  <div class="scores-view">
    <!-- 查询卡片 -->
    <el-card class="search-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon class="header-icon"><DataAnalysis /></el-icon>
          <h3 class="header-title">成绩查询</h3>
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
      <div v-if="playerScores" class="result-section">
        <!-- Rating卡片 -->
        <el-card class="rating-card" shadow="hover">
          <template #header>
            <div class="rating-header">
              <el-icon class="rating-icon"><StarFilled /></el-icon>
              <h3 class="rating-title">玩家Rating</h3>
            </div>
          </template>
          
          <div class="rating-content">
            <div class="rating-main">
              <div class="rating-value">{{ playerScores.rating }}</div>
              <div class="rating-label">当前Rating</div>
            </div>
            <div class="rating-stats">
              <div class="stat-item">
                <div class="stat-label">b15数量</div>
                <div class="stat-value">{{ playerScores.scores_b15.length }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">总歌曲数</div>
                <div class="stat-value">{{ playerScores.scores_all ? playerScores.scores_all.length : 0 }}</div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- b15成绩表格 -->
        <el-card class="b15-card" shadow="hover">
          <template #header>
            <div class="b15-header">
              <el-icon class="b15-icon"><Trophy /></el-icon>
              <h3 class="b15-title">b15成绩</h3>
            </div>
          </template>
          
          <div class="table-wrapper">
            <el-table 
              :data="playerScores.scores_b15" 
              stripe 
              style="width: 100%"
              class="scores-table"
              v-loading="loading"
            >
              <el-table-column prop="song_id" label="歌曲ID" width="80" type="number"></el-table-column>
              <el-table-column prop="title" label="歌曲名称" min-width="200">
                <template #default="scope">
                  <div class="song-title">{{ scope.row.title }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="level" label="难度" width="80">
                <template #default="scope">
                  <el-tag :type="getLevelType(scope.row.level)">
                    {{ scope.row.level }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="score" label="分数" width="120" align="right">
                <template #default="scope">
                  <div class="score-value">{{ formatScore(scope.row.score) }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="dx_rating" label="Rating" width="120" align="right">
                <template #default="scope">
                  <div class="dx-rating">{{ scope.row.dx_rating }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="achievements" label="达成率" width="120" align="right">
                <template #default="scope">
                  <el-progress 
                    :percentage="parseFloat(scope.row.achievements) * 100" 
                    :color="getAchievementColor(scope.row.achievements)"
                    :stroke-width="8"
                    :show-text="true"
                    text-inside
                    format="percent"
                  ></el-progress>
                </template>
              </el-table-column>
            </el-table>
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
      <div v-if="!loading && !playerScores && !error" class="empty-section">
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
const playerScores = ref(null)
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
  playerScores.value = null
  
  try {
    const params = {
      provider: searchForm.provider
    }
    
    if (searchForm.searchType === 'username') {
      params.username = searchForm.searchValue
    } else {
      params.friend_code = searchForm.searchValue
    }
    
    const result = await api.getPlayerScores(params)
    playerScores.value = result
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

// 根据难度返回标签类型
const getLevelType = (level) => {
  if (!level) return 'info'
  
  const levelMap = {
    'Basic': 'success',
    'Advanced': 'warning',
    'Expert': 'danger',
    'Master': 'primary',
    'Re:MASTER': 'info',
    'DX Basic': 'success',
    'DX Advanced': 'warning',
    'DX Expert': 'danger',
    'DX Master': 'primary',
    'DX Re:MASTER': 'info'
  }
  
  return levelMap[level] || 'info'
}

// 格式化分数
const formatScore = (score) => {
  if (!score) return '0'
  return score.toLocaleString()
}

// 根据达成率返回颜色
const getAchievementColor = (achievement) => {
  if (!achievement) return '#409eff'
  
  const value = parseFloat(achievement)
  if (value >= 0.999) return '#67c23a' // SSS+
  if (value >= 0.995) return '#e6a23c' // SSS
  if (value >= 0.99) return '#f56c6c' // SS+
  if (value >= 0.98) return '#f56c6c' // SS
  if (value >= 0.95) return '#909399' // S+
  if (value >= 0.9) return '#909399' // S
  if (value >= 0.8) return '#909399' // AAA+
  if (value >= 0.7) return '#909399' // AAA
  if (value >= 0.6) return '#909399' // AA+
  if (value >= 0.5) return '#909399' // AA
  if (value >= 0.4) return '#909399' // A+
  if (value >= 0.3) return '#909399' // A
  return '#909399' // B及以下
}
</script>

<style scoped>
.scores-view {
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
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Rating卡片样式 */
.rating-card {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  border-radius: 12px;
}

.rating-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rating-icon {
  font-size: 20px;
  color: white;
}

.rating-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: white;
}

.rating-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 0;
}

@media (max-width: 768px) {
  .rating-content {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
}

.rating-main {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rating-value {
  font-size: 72px;
  font-weight: 700;
  margin-bottom: 8px;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.rating-label {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.rating-stats {
  display: flex;
  gap: 32px;
}

@media (max-width: 768px) {
  .rating-stats {
    gap: 48px;
  }
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 8px;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: white;
}

/* b15成绩卡片 */
.b15-card {
  border-radius: 12px;
}

.b15-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.b15-icon {
  font-size: 20px;
  color: #409eff;
}

.b15-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.table-wrapper {
  overflow-x: auto;
}

.scores-table {
  border-radius: 8px;
  overflow: hidden;
}

.scores-table .el-table__header-wrapper th {
  background-color: #fafafa;
  font-weight: 600;
}

.song-title {
  font-weight: 500;
  color: #303133;
}

.score-value {
  font-weight: 600;
  color: #303133;
}

.dx-rating {
  font-weight: 600;
  color: #e6a23c;
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
