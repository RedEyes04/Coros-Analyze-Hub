<script setup>
</script>

<template>
  <header class="header-nav">
    <div class="header-content">
      <!-- Logo & Brand -->
      <div class="brand">
        <div class="logo">
          <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- 外圆环 - 手表表盘 -->
            <circle cx="16" cy="16" r="14" stroke="currentColor" stroke-width="2"/>
            <!-- 内圆 -->
            <circle cx="16" cy="16" r="10" stroke="currentColor" stroke-width="1.5"/>
            <!-- 跑步者剪影 -->
            <g fill="currentColor">
              <!-- 头 -->
              <circle cx="16" cy="9" r="2"/>
              <!-- 身体 -->
              <path d="M14 12.5L17 15L14.5 18L12 16.5L14 12.5Z"/>
              <!-- 前腿 -->
              <path d="M17 15L20 19L18.5 20L15 17L17 15Z"/>
              <!-- 后腿 -->
              <path d="M14.5 18L12 22L10.5 21L12.5 17L14.5 18Z"/>
            </g>
            <!-- 表冠 -->
            <rect x="29" y="14" width="3" height="4" rx="1" fill="currentColor"/>
          </svg>
        </div>
        <div class="brand-text">
          <span class="brand-name">COROS</span>
          <span class="brand-sub">Analyze Hub</span>
        </div>
      </div>

      <!-- Status -->
      <div class="sync-status">
        <span class="status-dot"></span>
        <span class="status-text">已同步</span>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header-nav {
  height: 100%;
  display: flex;
  align-items: center;
}

.header-content {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-6);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.logo {
  width: 32px;
  height: 32px;
  color: var(--text-primary);
}

.logo svg {
  width: 100%;
  height: 100%;
}

.brand-text {
  display: flex;
  align-items: baseline;
  gap: var(--space-2);
}

.brand-name {
  font-size: 17px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 0.05em;
}

.brand-sub {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  letter-spacing: -0.01em;
}

.sync-status {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.status-dot {
  width: 8px;
  height: 8px;
  background: var(--green);
  border-radius: 50%;
}

.status-text {
  font-size: 13px;
  color: var(--text-secondary);
}
</style>
