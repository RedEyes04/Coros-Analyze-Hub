<script setup>
import { onMounted } from 'vue'
import { 
  NConfigProvider, 
  NLayout, 
  NLayoutHeader, 
  NLayoutContent,
  NMessageProvider,
  NDialogProvider
} from 'naive-ui'
import { useTrainingData } from '@/composables/useTrainingData'
import HeaderNav from '@/components/HeaderNav.vue'
import StatsOverview from '@/components/StatsOverview.vue'
import ActivityHeatmap from '@/components/ActivityHeatmap.vue'
import WeeklyDistanceChart from '@/components/WeeklyDistanceChart.vue'
import TrainingLoadChart from '@/components/TrainingLoadChart.vue'
import DailyDistanceChart from '@/components/DailyDistanceChart.vue'
import ACWRCard from '@/components/ACWRCard.vue'
import PersonalRecords from '@/components/PersonalRecords.vue'
import RecentActivities from '@/components/RecentActivities.vue'
import AITrainingPlan from '@/components/AITrainingPlan.vue'

const themeOverrides = {
  common: {
    primaryColor: '#0071e3',
    primaryColorHover: '#0077ed',
    primaryColorPressed: '#006edb',
    textColorBase: '#1d1d1f',
    textColor1: '#1d1d1f',
    textColor2: '#6e6e73',
    textColor3: '#86868b',
    bodyColor: '#ffffff',
    cardColor: '#ffffff',
    popoverColor: '#ffffff',
    inputColor: '#f5f5f7',
    borderColor: '#d2d2d7',
    borderRadius: '12px',
    borderRadiusSmall: '8px',
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', sans-serif",
    heightMedium: '44px'
  },
  Button: {
    colorPrimary: '#0071e3',
    colorHoverPrimary: '#0077ed',
    colorPressedPrimary: '#006edb',
    textColorPrimary: '#ffffff',
    borderRadiusMedium: '12px',
    fontWeight: '500'
  },
  Input: {
    color: '#f5f5f7',
    colorFocus: '#ffffff',
    borderColor: '#d2d2d7',
    borderColorFocus: '#0071e3',
    borderRadius: '12px',
    boxShadowFocus: '0 0 0 4px rgba(0, 113, 227, 0.15)'
  },
  Select: {
    peers: {
      InternalSelection: {
        color: '#f5f5f7',
        borderRadius: '12px',
        borderColor: '#d2d2d7'
      }
    }
  },
  Tooltip: {
    color: '#ffffff',
    textColor: '#1d1d1f',
    borderRadius: '12px',
    boxShadow: '0 4px 20px rgba(0, 0, 0, 0.12)',
    padding: '12px 16px'
  },
  Popover: {
    color: '#ffffff',
    textColor: '#1d1d1f',
    borderRadius: '12px',
    boxShadow: '0 4px 20px rgba(0, 0, 0, 0.12)'
  }
}

const { loadData } = useTrainingData()

onMounted(() => {
  loadData()
})
</script>

<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <n-message-provider>
      <n-dialog-provider>
        <n-layout class="app-layout">
          <n-layout-header class="app-header">
            <HeaderNav />
          </n-layout-header>

          <n-layout-content class="app-content">
            <div class="container">
              <!-- Hero Stats -->
              <section class="hero-section">
                <StatsOverview />
              </section>

              <!-- Row 1: Calendar + Weekly Chart -->
              <section class="row-grid row-1">
                <div class="card card-sm animate-fade-in-up delay-1">
                  <ActivityHeatmap />
                </div>
                <div class="card animate-fade-in-up delay-2">
                  <WeeklyDistanceChart />
                </div>
              </section>

              <!-- Row 2: Daily Charts -->
              <section class="row-grid row-2">
                <div class="card animate-fade-in-up delay-2">
                  <TrainingLoadChart />
                </div>
                <div class="card animate-fade-in-up delay-3">
                  <DailyDistanceChart />
                </div>
              </section>

              <!-- Row 3: Sidebar (ACWR + Records) + Recent Activities -->
              <section class="row-grid row-3">
                <div class="sidebar-col">
                  <div class="card card-sm animate-fade-in-up delay-3">
                    <ACWRCard />
                  </div>
                  <div class="card card-sm animate-fade-in-up delay-4">
                    <PersonalRecords />
                  </div>
                </div>
                <div class="card animate-fade-in-up delay-4">
                  <RecentActivities />
                </div>
              </section>

              <!-- Row 4: AI Training Plan -->
              <section class="row-single animate-fade-in-up delay-5">
                <div class="card">
                  <AITrainingPlan />
                </div>
              </section>
            </div>
          </n-layout-content>
        </n-layout>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
  background: var(--bg-primary);
}

.app-header {
  height: 52px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid var(--border-color-light);
  position: sticky;
  top: 0;
  z-index: 100;
}

.app-content {
  background: var(--bg-primary);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-6);
}

.hero-section {
  margin-bottom: var(--space-6);
}

/* Card Base */
.card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color-light);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
}

/* Row Grids */
.row-grid {
  display: grid;
  gap: var(--space-5);
  margin-bottom: var(--space-5);
}

.row-1 {
  grid-template-columns: 280px 1fr;
}

.row-2 {
  grid-template-columns: 1fr 1fr;
}

.row-3 {
  grid-template-columns: 280px 1fr;
  align-items: start;
}

.sidebar-col {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.row-single {
  margin-bottom: var(--space-5);
}

.card-sm {
  padding: var(--space-4);
}

/* Responsive */
@media (max-width: 1024px) {
  .row-1,
  .row-2,
  .row-3 {
    grid-template-columns: 1fr;
  }
  
  .sidebar-col {
    flex-direction: row;
  }
  
  .sidebar-col .card {
    flex: 1;
  }
}

@media (max-width: 600px) {
  .container {
    padding: var(--space-4);
  }
  
  .row-grid {
    gap: var(--space-4);
    margin-bottom: var(--space-4);
  }
  
  .sidebar-col {
    flex-direction: column;
  }
}
</style>
