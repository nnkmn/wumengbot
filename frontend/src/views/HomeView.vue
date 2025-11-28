<template>
  <div class="home">
    <!-- 欢迎区域 -->
    <el-card class="welcome-card" shadow="hover">
      <div class="welcome-content">
        <div class="welcome-text">
          <h2 class="welcome-title">欢迎使用舞萌Bot</h2>
          <p class="welcome-desc">
            舞萌Bot是一个基于maimai.py开发的舞萌数据查询工具，
            支持查询玩家信息、成绩、歌曲和牌子进度，
            为舞萌玩家提供便捷的数据查询服务。
          </p>
        </div>
        <div class="welcome-icon">
          <Maimai class="main-icon" />
        </div>
      </div>
    </el-card>

    <!-- 功能介绍区域 -->
    <el-card class="features-card" shadow="hover">
      <template #header>
        <div class="features-header">
          <h3 class="features-title">功能介绍</h3>
        </div>
      </template>
      <el-row :gutter="24">
        <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="feature in features" :key="feature.id">
          <el-card class="feature-card" shadow="hover" @click="navigateTo(feature.path)">
            <div class="feature-content">
              <div class="feature-icon-wrapper">
                <el-icon class="feature-icon">
                  <component :is="getIconComponent(feature.icon)" />
                </el-icon>
              </div>
              <h4 class="feature-title">{{ feature.title }}</h4>
              <p class="feature-desc">{{ feature.desc }}</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>

    <!-- 技术栈区域 -->
    <el-card class="tech-card" shadow="hover">
      <template #header>
        <div class="tech-header">
          <h3 class="tech-title">技术栈</h3>
        </div>
      </template>
      <div class="tech-content">
        <el-row :gutter="20">
          <el-col :xs="12" :sm="8" :md="6" v-for="tech in techStack" :key="tech.name">
            <div class="tech-item">
              <el-icon class="tech-icon" :style="{ color: tech.color }">
                <component :is="getIconComponent(tech.icon)" />
              </el-icon>
              <span class="tech-name">{{ tech.name }}</span>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { User, DataAnalysis, Music, Medal, Vue, Server, Code, ElementPlus, Database } from '@element-plus/icons-vue'
import { Maimai } from '../components/MaimaiIcon.vue'

const router = useRouter()

// 功能列表数据
const features = [
  {
    id: 1,
    title: '玩家查询',
    desc: '查询舞萌玩家的基本信息，支持水鱼和落雪查分器',
    icon: 'User',
    path: '/player'
  },
  {
    id: 2,
    title: '成绩查询',
    desc: '查看玩家的成绩列表、Rating和b15成绩',
    icon: 'DataAnalysis',
    path: '/scores'
  },
  {
    id: 3,
    title: '歌曲查询',
    desc: '搜索和查看舞萌歌曲的详细信息',
    icon: 'Music',
    path: '/songs'
  },
  {
    id: 4,
    title: '牌子进度',
    desc: '查看玩家的舞将、舞霸等牌子完成进度',
    icon: 'Medal',
    path: '/plates'
  }
]

// 技术栈数据
const techStack = [
  { name: 'Vue 3', icon: 'Vue', color: '#4FC08D' },
  { name: 'FastAPI', icon: 'Server', color: '#009688' },
  { name: 'Python', icon: 'Code', color: '#3776AB' },
  { name: 'Element Plus', icon: 'ElementPlus', color: '#409EFF' },
  { name: 'maimai.py', icon: 'Maimai', color: '#FF6B6B' },
  { name: 'SQLite', icon: 'Database', color: '#003B57' }
]

// 图标组件映射
const iconComponents = {
  User,
  DataAnalysis,
  Music,
  Medal,
  Vue,
  Server,
  Code,
  ElementPlus,
  Database,
  Maimai
}

// 获取图标组件
const getIconComponent = (iconName) => {
  return iconComponents[iconName] || User
}

// 导航到对应页面
const navigateTo = (path) => {
  router.push(path)
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

/* 欢迎卡片样式 */
.welcome-card {
  margin-bottom: 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.welcome-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 0;
}

@media (max-width: 768px) {
  .welcome-content {
    flex-direction: column;
    text-align: center;
  }
}

.welcome-text {
  flex: 1;
  padding-right: 40px;
}

@media (max-width: 768px) {
  .welcome-text {
    padding-right: 0;
    margin-bottom: 20px;
  }
}

.welcome-title {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #303133;
}

.welcome-desc {
  font-size: 16px;
  line-height: 1.8;
  color: #606266;
  margin: 0;
}

.welcome-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-icon {
  font-size: 120px;
  color: #409eff;
  opacity: 0.8;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

/* 功能卡片样式 */
.features-card {
  margin-bottom: 24px;
}

.features-header {
  display: flex;
  justify-content: center;
}

.features-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.feature-card {
  height: 100%;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  border-color: #409eff;
}

.feature-content {
  text-align: center;
  padding: 20px 0;
}

.feature-icon-wrapper {
  width: 80px;
  height: 80px;
  margin: 0 auto 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 40px;
  color: white;
}

.feature-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #303133;
}

.feature-desc {
  font-size: 14px;
  line-height: 1.6;
  color: #606266;
  margin: 0;
}

/* 技术栈卡片样式 */
.tech-card {
  margin-bottom: 24px;
}

.tech-header {
  display: flex;
  justify-content: center;
}

.tech-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.tech-content {
  padding: 20px 0;
}

.tech-item {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 16px;
  transition: all 0.3s ease;
}

.tech-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-color: white;
}

.tech-icon {
  font-size: 24px;
  margin-right: 12px;
  color: #409eff;
}

.tech-name {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}
</style>
