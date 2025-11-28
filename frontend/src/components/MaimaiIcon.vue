<template>
  <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
    <!-- 外圆背景 -->
    <circle cx="50" cy="50" r="45" fill="#FF6B6B" />
    <!-- 内圆 -->
    <circle cx="50" cy="50" r="35" fill="white" />
    <!-- 中间的M形状 -->
    <path d="M30 30 L40 55 L50 30 L60 55 L70 30" stroke="#FF6B6B" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
    <!-- 底部的波浪线 -->
    <path d="M35 65 Q50 75 65 65" stroke="#FF6B6B" stroke-width="4" stroke-linecap="round" fill="none" />
    <!-- 装饰点 -->
    <circle cx="40" cy="40" r="3" fill="#FF6B6B" />
    <circle cx="60" cy="40" r="3" fill="#FF6B6B" />
  </svg>
</template>

<script setup>
// Maimai图标组件
</script>

<style scoped>
svg {
  transition: transform 0.3s ease;
}

svg:hover {
  transform: scale(1.1);
}
</style>