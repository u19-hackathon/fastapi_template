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
          <div class="header-buttons">
            <div class="user-menu">
              <span class="user-name">Иван Иванов</span>
              <button @click="handleLogout" class="logout-btn">Выйти</button>
            </div>
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
export default {
  name: 'AnalyticsView',
  data() {
    return {
      selectedYear: new Date().getFullYear(),
      availableYears: [2025, 2024, 2023, 2022],
      documents: [
        {
          id: '264917',
          title: 'Договор поставки',
          filename: 'Договор №154/2024.pdf',
          type: 'Договор поставки',
          company: 'ООО "Ромашка"',
          date: '12.02.2025',
          status: 'На оплате',
          tags: ['Проект X', 'Юридический', 'Поставка']
        },
        {
          id: '264918',
          title: 'Счёт на оплату',
          filename: 'Счёт №287.pdf',
          type: 'Счёт',
          company: 'ООО "Вектор"',
          date: '23.03.2024',
          status: 'Оплачен',
          tags: ['Финансовый', 'Срочный']
        },
        {
          id: '264919',
          title: 'Акт выполненных работ',
          filename: 'Акт №45/2023.pdf',
          type: 'Акт',
          company: 'ООО "Ромашка"',
          date: '15.11.2023',
          status: 'Подписан',
          tags: ['Проект Y', 'Финансовый']
        },
        {
          id: '264920',
          title: 'Договор аренды',
          filename: 'Договор №89/2022.pdf',
          type: 'Договор аренды',
          company: 'ООО "Стройсервис"',
          date: '05.08.2022',
          status: 'Завершен',
          tags: ['Аренда', 'Юридический']
        },
        {
          id: '264921',
          title: 'Счёт на оплату',
          filename: 'Счёт №301.pdf',
          type: 'Счёт',
          company: 'ООО "Ромашка"',
          date: '18.06.2024',
          status: 'Ожидает оплаты',
          tags: ['Финансовый']
        },
        {
          id: '264922',
          title: 'Договор оказания услуг',
          filename: 'Договор №201/2024.pdf',
          type: 'Договор оказания услуг',
          company: 'ООО "ТехноПрофи"',
          date: '10.04.2024',
          status: 'Активен',
          tags: ['Услуги', 'Технический']
        }
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
    handleLogout() {
      this.$router.push('/login');
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
        .slice(0, 5); // Топ 5 компаний
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
    this.updateStatistics();
  }
}
</script>

<style scoped src="@/styles/components/AnalyticsView.css"></style>