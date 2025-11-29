<template>
  <div class="main-view">
    <!-- Боковая панель -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1>DocHub</h1>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item" :class="{ active: $route.name === 'Home' }">
          <span class="nav-icon">📄</span>
          Документы
        </router-link>
        <router-link to="/analytics" class="nav-item" :class="{ active: $route.name === 'Analytics' }">
          <span class="nav-icon">📈</span>
          Аналитика
        </router-link>
      </nav>
    </aside>

    <!-- Основной контент -->
    <main class="content">
      <!-- Хедер -->
      <header class="content-header">
        <div class="header-actions">
          <div v-if="loading" class="user-info compact">
      <div class="loading-spinner"></div>
      <span>Загрузка...</span>
    </div>

    <div v-else-if="user" class="user-info compact">
      <div class="user-avatar">
        {{ getInitials(user.full_name) }}
      </div>
      <div class="user-details">
        <div class="user-main">
          <span class="user-name">{{ user.full_name }}</span>
          <span class="user-badge">{{ user.position }}</span>
        </div>
        <div class="user-org">{{ user.organization_name }}</div>
      </div>
      <button @click="handleLogout" class="btn btn-secondary logout-btn">
        Выйти
      </button>
    </div>

    <div v-else class="user-info compact">
      <span>❌ Ошибка</span>
      <button @click="handleLogout" class="btn btn-secondary logout-btn">
        🚪
      </button>
    </div>
  </div>
</header>

      <!-- Основной контент -->
      <div class="main-content">
        <div class="analytics-container">
          <div class="section-header">
            <h2>Аналитика документов</h2>
          </div>

          <!-- Фильтры -->
          <div class="filters-section">
            <div class="filters-grid">
              <div class="filter-group">
                <label>Год</label>
                <select v-model="selectedYear" class="filter-select" @change="updateStatistics">
                  <option v-for="year in availableYears" :key="year" :value="year">
                    {{ year }}
                  </option>
                  <option value="all">Все годы</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Карточки статистики -->
          <div class="stats-cards">
            <div class="stat-card">
              <div class="stat-icon">📄</div>
              <div class="stat-info">
                <div class="stat-value">{{ totalDocuments }}</div>
                <div class="stat-label">Всего документов</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">📊</div>
              <div class="stat-info">
                <div class="stat-value">{{ yearlyDocuments }}</div>
                <div class="stat-label">
                  {{ selectedYear === 'all' ? 'За все время' : `За ${selectedYear} год` }}
                </div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">🔖</div>
              <div class="stat-info">
                <div class="stat-value">{{ documentTypesCount }}</div>
                <div class="stat-label">Типов документов</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">👥</div>
              <div class="stat-info">
                <div class="stat-value">{{ companiesCount }}</div>
                <div class="stat-label">Компаний</div>
              </div>
            </div>
          </div>

          <!-- Детальная аналитика -->
          <div class="analytics-detailed">
            <!-- Распределение по типам -->
            <div class="analytics-column">
              <div class="analytics-card">
                <div class="analytics-header">
                  <h3>Распределение по типам</h3>
                </div>
                <div class="analytics-content">
                  <div
                    v-for="type in typeDistribution"
                    :key="type.name"
                    class="distribution-item"
                  >
                    <div class="distribution-info">
                      <span class="distribution-name">{{ type.name }}</span>
                      <span class="distribution-count">{{ type.count }}</span>
                    </div>
                    <div class="distribution-bar">
                      <div
                        class="distribution-bar-fill"
                        :style="{ width: type.percentage + '%' }"
                      ></div>
                    </div>
                    <span class="distribution-percentage">{{ type.percentage }}%</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Компании -->
            <div class="analytics-column">
              <div class="analytics-card">
                <div class="analytics-header">
                  <h3>Топ компаний</h3>
                </div>
                <div class="analytics-content">
                  <div
                    v-for="company in topCompanies"
                    :key="company.name"
                    class="company-item"
                  >
                    <div class="company-info">
                      <span class="company-name">{{ company.name }}</span>
                      <span class="company-count">{{ company.count }}</span>
                    </div>
                    <div class="company-bar">
                      <div
                        class="company-bar-fill"
                        :style="{ width: company.percentage + '%' }"
                      ></div>
                    </div>
                    <span class="company-percentage">{{ company.percentage }}%</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Статусы документов -->
            <div class="analytics-column">
              <div class="analytics-card">
                <div class="analytics-header">
                  <h3>Статусы документов</h3>
                </div>
                <div class="analytics-content">
                  <div
                    v-for="status in statusDistribution"
                    :key="status.name"
                    class="status-item"
                  >
                    <div class="status-info">
                      <span class="status-name">{{ status.name + ' ' }}</span>
                      <span class="status-count">{{ status.count }} шт.</span>
                    </div>
                    <div class="status-bar">
                      <div
                        class="status-bar-fill"
                        :style="{ width: status.percentage + '%' }"
                      ></div>
                    </div>
                    <span class="status-percentage">{{ status.percentage }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { apiService } from '@/services/api';
export default {
  name: 'AnalyticsView',
  data() {
    return {
      selectedYear: new Date().getFullYear(),
      availableYears: [2025, 2024, 2023, 2022],
      loading: true,
      user: null,
      documents: [
        // ... ваш массив документов
      ],
      statistics: {
        total: 0,
        yearly: 0,
        typesCount: 0,
        companiesCount: 0,
        typeDistribution: [],
        topCompanies: [],
        statusDistribution: []
      }
    }
  },
  computed: {
    totalDocuments() {
      return this.statistics.total;
    },
    yearlyDocuments() {
      return this.statistics.yearly;
    },
    documentTypesCount() {
      return this.statistics.typesCount;
    },
    companiesCount() {
      return this.statistics.companiesCount;
    },
    typeDistribution() {
      return this.statistics.typeDistribution;
    },
    topCompanies() {
      return this.statistics.topCompanies;
    },
    statusDistribution() {
      return this.statistics.statusDistribution;
    }
  },
  methods: {
    async loadUserData() {
      try {
        this.user = await apiService.getCurrentUser();
        if (!this.user) this.handleLogout();
      } catch (error) {
        this.handleLogout();
      } finally {
        this.loading = false;
      }
    },

    handleLogout() {
      console.log('🚪 Выход из системы...');
      apiService.clearTokens();
      this.$router.push('/login');
    },

    getInitials(fullName) {
      if (!fullName) return '??';
      return fullName
          .split(' ')
          .map(name => name[0])
          .join('')
          .toUpperCase();
    },

    updateStatistics() {
      // Фильтрация документов по году
      const filteredDocs = this.documents.filter(doc => {
        const docYear = new Date(this.parseDate(doc.date)).getFullYear();
        return this.selectedYear === 'all' || docYear === this.selectedYear;
      });

      // Общая статистика
      this.statistics.total = this.documents.length;
      this.statistics.yearly = filteredDocs.length;

      // Уникальные типы и компании
      const uniqueTypes = new Set(filteredDocs.map(doc => doc.type));
      const uniqueCompanies = new Set(filteredDocs.map(doc => doc.company));

      this.statistics.typesCount = uniqueTypes.size;
      this.statistics.companiesCount = uniqueCompanies.size;

      // Распределения
      this.calculateTypeDistribution(filteredDocs);
      this.calculateCompanyStats(filteredDocs);
      this.calculateStatusDistribution(filteredDocs);
    },

    calculateTypeDistribution(docs) {
      const typeCounts = {};

      docs.forEach(doc => {
        typeCounts[doc.type] = (typeCounts[doc.type] || 0) + 1;
      });

      const total = docs.length;

      this.statistics.typeDistribution = Object.entries(typeCounts)
          .map(([name, count]) => ({
            name,
            count,
            percentage: total > 0 ? Math.round((count / total) * 100) : 0
          }))
          .sort((a, b) => b.count - a.count);
    },

    calculateCompanyStats(docs) {
      const companyCounts = {};

      docs.forEach(doc => {
        companyCounts[doc.company] = (companyCounts[doc.company] || 0) + 1;
      });

      const total = docs.length;

      this.statistics.topCompanies = Object.entries(companyCounts)
          .map(([name, count]) => ({
            name,
            count,
            percentage: total > 0 ? Math.round((count / total) * 100) : 0
          }))
          .sort((a, b) => b.count - a.count)
          .slice(0, 5);
    },

    calculateStatusDistribution(docs) {
      const statusCounts = {};

      docs.forEach(doc => {
        statusCounts[doc.status] = (statusCounts[doc.status] || 0) + 1;
      });

      const total = docs.length;

      this.statistics.statusDistribution = Object.entries(statusCounts)
          .map(([name, count]) => ({
            name,
            count,
            percentage: total > 0 ? Math.round((count / total) * 100) : 0
          }))
          .sort((a, b) => b.count - a.count);
    },

    parseDate(dateString) {
      const [day, month, year] = dateString.split('.');
      return `${year}-${month}-${day}`;
    }
  },
  mounted() {
    this.loadUserData();
    this.updateStatistics();
  }
}
</script>

<style scoped src="@/styles/components/AnalyticsView.css"></style>