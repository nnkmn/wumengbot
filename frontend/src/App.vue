<template>
  <div id="app">
    <el-container>
      <el-header class="app-header">
        <div class="header-content">
          <el-icon class="header-icon"><Logo /></el-icon>
          <h1 class="header-title">舞萌Bot</h1>
        </div>
      </el-header>
      <el-container>
        <el-aside width="220px" class="app-aside">
          <el-menu
            :default-active="$route.path"
            class="app-menu"
            @select="handleMenuSelect"
            background-color="#001529"
            text-color="#fff"
            active-text-color="#409eff"
            unique-opened
          >
            <el-menu-item index="/">
              <el-icon><House /></el-icon>
              <template #title>
                <span>首页</span>
              </template>
            </el-menu-item>
            <el-menu-item index="/player">
              <el-icon><User /></el-icon>
              <template #title>
                <span>玩家查询</span>
              </template>
            </el-menu-item>
            <el-menu-item index="/scores">
              <el-icon><DataAnalysis /></el-icon>
              <template #title>
                <span>成绩查询</span>
              </template>
            </el-menu-item>
            <el-menu-item index="/songs">
              <el-icon><Music /></el-icon>
              <template #title>
                <span>歌曲查询</span>
              </template>
            </el-menu-item>
            <el-menu-item index="/plates">
              <el-icon><Medal /></el-icon>
              <template #title>
                <span>牌子进度</span>
              </template>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="app-main">
          <router-view />
        </el-main>
      </el-container>
      <el-footer class="app-footer">
        <p>舞萌Bot © 2024 | 基于 maimai.py 开发</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const handleMenuSelect = (key) => {
  router.push(key)
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f7fa;
  color: #303133;
}

#app {
  height: 100vh;
}

.el-container {
  height: 100vh;
}

/* 头部样式 */
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 0 20px;
}

.header-icon {
  font-size: 32px;
  margin-right: 12px;
  color: white;
}

.header-title {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  letter-spacing: 1px;
}

/* 侧边栏样式 */
.app-aside {
  background-color: #001529;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.15);
}

.app-menu {
  height: 100%;
  border-right: none;
}

.app-menu .el-menu-item {
  padding: 0 20px;
  height: 60px;
  line-height: 60px;
  font-size: 15px;
  transition: all 0.3s ease;
}

.app-menu .el-menu-item:hover {
  background-color: #1890ff;
  color: white;
}

.app-menu .el-menu-item.is-active {
  background-color: #1890ff;
}

/* 主内容区样式 */
.app-main {
  padding: 24px;
  background-color: #f5f7fa;
  overflow-y: auto;
}

/* 页脚样式 */
.app-footer {
  text-align: center;
  padding: 15px 0;
  background-color: #fff;
  color: #606266;
  font-size: 14px;
  border-top: 1px solid #e4e7ed;
}

/* 卡片样式优化 */
.el-card {
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.el-card:hover {
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

/* 按钮样式优化 */
.el-button {
  border-radius: 6px;
  font-weight: 500;
}

/* 表单样式优化 */
.el-form-item {
  margin-bottom: 20px;
}

/* 表格样式优化 */
.el-table {
  border-radius: 8px;
  overflow: hidden;
}

.el-table__header-wrapper th {
  background-color: #fafafa;
  font-weight: 600;
}

/* 进度条样式优化 */
.el-progress {
  margin-bottom: 20px;
}

/* 标签样式优化 */
.el-tag {
  border-radius: 4px;
  font-size: 12px;
  padding: 0 8px;
}
</style>
