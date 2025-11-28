<template>
  <div class="songs-view">
    <!-- 查询卡片 -->
    <el-card class="search-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon class="header-icon"><Music /></el-icon>
          <h3 class="header-title">歌曲查询</h3>
        </div>
      </template>
      
      <el-form :model="searchForm" class="search-form" label-position="top">
        <el-row :gutter="24">
          <el-col :xs="24" :sm="12" :md="8">
            <el-form-item label="歌曲标题">
              <el-input 
                v-model="searchForm.title" 
                placeholder="请输入歌曲标题" 
                class="search-input"
                @keyup.enter="handleSearch"
              >
                <template #prefix>
                  <el-icon><Document /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8">
            <el-form-item label="艺术家">
              <el-input 
                v-model="searchForm.artist" 
                placeholder="请输入艺术家" 
                class="search-input"
                @keyup.enter="handleSearch"
              >
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="24" :md="8" class="search-buttons">
            <el-form-item>
              <el-button type="primary" @click="handleSearch" :loading="loading" class="search-btn">
                <el-icon><Search /></el-icon>
                搜索
              </el-button>
              <el-button @click="handleReset" class="reset-btn">
                <el-icon><Refresh /></el-icon>
                重置
              </el-button>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>

    <!-- 结果统计 -->
    <transition name="fade">
      <el-card v-if="!loading && filteredSongs.length > 0" class="stats-card" shadow="hover">
        <div class="stats-content">
          <el-icon class="stats-icon"><DataLine /></el-icon>
          <span class="stats-text">共找到 <strong>{{ filteredSongs.length }}</strong> 首歌曲</span>
        </div>
      </el-card>
    </transition>

    <!-- 歌曲列表 -->
    <transition name="fade">
      <div v-if="filteredSongs.length > 0" class="songs-section">
        <el-card class="songs-card" shadow="hover">
          <template #header>
            <div class="songs-header">
              <el-icon class="songs-icon"><List /></el-icon>
              <h3 class="songs-title">歌曲列表</h3>
            </div>
          </template>
          
          <div class="table-wrapper">
            <el-table 
              :data="paginatedSongs" 
              stripe 
              style="width: 100%"
              class="songs-table"
              v-loading="loading"
            >
              <el-table-column prop="id" label="歌曲ID" width="80" type="number"></el-table-column>
              <el-table-column prop="title" label="歌曲名称" min-width="200">
                <template #default="scope">
                  <div class="song-title">{{ scope.row.title }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="artist" label="艺术家" min-width="150">
                <template #default="scope">
                  <div class="song-artist">{{ scope.row.artist }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="genre" label="类型" width="120">
                <template #default="scope">
                  <el-tag size="small" type="info">{{ scope.row.genre }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="version" label="版本" width="120">
                <template #default="scope">
                  <el-tag size="small" type="success">{{ scope.row.version }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="120">
                <template #default="scope">
                  <el-button size="small" type="primary" @click="handleViewDetails(scope.row)">
                    <el-icon><View /></el-icon>
                    详情
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <!-- 分页 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              :total="filteredSongs.length"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            ></el-pagination>
          </div>
        </el-card>
      </div>
    </transition>

    <!-- 空状态 -->
    <transition name="fade">
      <div v-if="!loading && filteredSongs.length === 0" class="empty-section">
        <el-empty
          description="未找到匹配的歌曲"
          image-size="120"
        >
          <el-button type="primary" @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置搜索
          </el-button>
        </el-empty>
      </div>
    </transition>

    <!-- 错误提示 -->
    <transition name="fade">
      <div v-if="error" class="error-section">
        <el-alert
          title="加载失败"
          :description="error"
          type="error"
          show-icon
          center
          :closable="true"
          @close="error = ''"
        ></el-alert>
      </div>
    </transition>

    <!-- 歌曲详情对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      title="歌曲详情" 
      width="60%"
      :close-on-click-modal="false"
    >
      <div v-if="selectedSong" class="song-details">
        <!-- 歌曲基本信息 -->
        <el-card class="song-info-card" shadow="hover">
          <div class="song-info-header">
            <h4 class="song-info-title">{{ selectedSong.title }}</h4>
            <span class="song-info-artist">{{ selectedSong.artist }}</span>
          </div>
          <el-descriptions :column="3" border class="song-info-descriptions">
            <el-descriptions-item label="歌曲ID" :span="1">{{ selectedSong.id }}</el-descriptions-item>
            <el-descriptions-item label="类型" :span="1">{{ selectedSong.genre }}</el-descriptions-item>
            <el-descriptions-item label="版本" :span="1">{{ selectedSong.version }}</el-descriptions-item>
            <el-descriptions-item label="BPM" :span="1">{{ selectedSong.bpm }}</el-descriptions-item>
            <el-descriptions-item label="谱面数量" :span="2">{{ selectedSong.charts ? selectedSong.charts.length : 0 }}</el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 谱面信息 -->
        <el-card class="charts-card" shadow="hover" v-if="selectedSong.charts && selectedSong.charts.length > 0">
          <template #header>
            <div class="charts-header">
              <el-icon class="charts-icon"><Menu /></el-icon>
              <span class="charts-title">谱面信息</span>
            </div>
          </template>
          <el-table :data="selectedSong.charts" stripe style="width: 100%" class="charts-table">
            <el-table-column prop="type" label="类型" width="120">
              <template #default="scope">
                <el-tag :type="getChartType(scope.row.type)">{{ scope.row.type }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="level" label="难度" width="100">
              <template #default="scope">
                <el-tag size="large" :type="getLevelType(scope.row.level)">{{ scope.row.level }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="notes" label="音符数" width="120"></el-table-column>
            <el-table-column prop="charter" label="谱师" width="150">
              <template #default="scope">
                <span>{{ scope.row.charter || '未知' }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { api } from '../api'

const loading = ref(false)
const allSongs = ref([])
const filteredSongs = ref([])
const selectedSong = ref(null)
const dialogVisible = ref(false)
const error = ref('')

// 分页相关
const currentPage = ref(1)
const pageSize = ref(20)

const searchForm = reactive({
  title: '',
  artist: ''
})

// 计算属性，根据搜索条件过滤歌曲
const songsFilter = computed(() => {
  return allSongs.value.filter(song => {
    let match = true
    if (searchForm.title && !song.title.toLowerCase().includes(searchForm.title.toLowerCase())) {
      match = false
    }
    if (searchForm.artist && !song.artist.toLowerCase().includes(searchForm.artist.toLowerCase())) {
      match = false
    }
    return match
  })
})

// 分页计算属性
const paginatedSongs = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredSongs.value.slice(start, end)
})

// 页面加载时获取所有歌曲
onMounted(async () => {
  await loadAllSongs()
})

const loadAllSongs = async () => {
  loading.value = true
  error.value = ''
  try {
    const songs = await api.getAllSongs()
    allSongs.value = songs
    filteredSongs.value = songs
    currentPage.value = 1 // 重置到第一页
  } catch (err) {
    error.value = err.message || '加载歌曲失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  filteredSongs.value = songsFilter.value
  currentPage.value = 1 // 搜索后重置到第一页
}

const handleReset = () => {
  searchForm.title = ''
  searchForm.artist = ''
  filteredSongs.value = allSongs.value
  currentPage.value = 1 // 重置后回到第一页
}

const handleViewDetails = (song) => {
  selectedSong.value = song
  dialogVisible.value = true
}

// 分页相关方法
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1 // 切换每页条数时回到第一页
}

const handleCurrentChange = (current) => {
  currentPage.value = current
}

// 根据谱面类型返回标签类型
const getChartType = (type) => {
  if (!type) return 'info'
  
  const typeMap = {
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
  
  return typeMap[type] || 'info'
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
</script>

<style scoped>
.songs-view {
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

.search-input {
  width: 100%;
}

.search-buttons {
  display: flex;
  align-items: flex-end;
}

.search-btn {
  margin-right: 12px;
  width: 120px;
}

.reset-btn {
  width: 120px;
}

/* 结果统计卡片 */
.stats-card {
  margin-bottom: 24px;
  background-color: #ecf5ff;
  border-color: #b3d8ff;
}

.stats-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stats-icon {
  font-size: 20px;
  color: #409eff;
}

.stats-text {
  font-size: 16px;
  color: #606266;
}

.stats-text strong {
  color: #409eff;
  font-weight: 600;
}

/* 歌曲列表区域 */
.songs-section {
  margin-top: 24px;
}

.songs-card {
  border-radius: 12px;
}

.songs-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.songs-icon {
  font-size: 20px;
  color: #409eff;
}

.songs-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.table-wrapper {
  overflow-x: auto;
}

.songs-table {
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

.songs-table .el-table__header-wrapper th {
  background-color: #fafafa;
  font-weight: 600;
}

.song-title {
  font-weight: 500;
  color: #303133;
}

.song-artist {
  color: #606266;
}

/* 分页样式 */
.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  padding: 16px 0 0;
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

/* 详情对话框样式 */
.song-details {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.song-info-card {
  border-radius: 12px;
}

.song-info-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  padding: 16px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
}

.song-info-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: white;
}

.song-info-artist {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
}

.song-info-descriptions {
  margin-top: 16px;
}

.song-info-descriptions .el-descriptions__label {
  font-weight: 500;
  color: #606266;
  background-color: #fafafa;
}

.charts-card {
  border-radius: 12px;
}

.charts-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.charts-icon {
  font-size: 18px;
  color: #409eff;
}

.charts-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.charts-table {
  margin-top: 16px;
  border-radius: 8px;
  overflow: hidden;
}

.charts-table .el-table__header-wrapper th {
  background-color: #fafafa;
  font-weight: 600;
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
