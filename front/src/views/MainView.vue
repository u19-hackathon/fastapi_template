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
          <div class="search-box">
            <input
              type="text"
              placeholder="Поиск документов..."
              class="search-input"
            >
          </div>
          <button @click="showUploadModal = true" class="btn btn-primary upload-btn">
            📎 Загрузить документ
          </button>

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

      <!-- Фильтры -->
      <div class="filters-section">
        <div class="filters-grid">
          <div class="filter-group">
            <label>Тип</label>
            <select class="filter-select">
              <option>Любой</option>
              <option>Договор</option>
              <option>Счёт</option>
              <option>Акт</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Тег</label>
            <select class="filter-select">
              <option>Любой</option>
              <option>Юридический</option>
              <option>Кадровый</option>
              <option>Финансовый</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Компания</label>
            <select class="filter-select">
              <option>Все</option>
              <option>ООО "Ромашка"</option>
              <option>ООО "Вектор"</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Основной контент с документами -->
      <div class="main-content">
        <div class="documents-section">
          <div class="section-header">
            <h2>Документы</h2>
          </div>

          <!-- Заголовки таблицы -->
          <div class="documents-header">
            <div class="doc-header-column">Документ</div>
            <div class="doc-header-column">Тип</div>
            <div class="doc-header-column">Компания</div>
            <div class="doc-header-column">Дата</div>
          </div>

          <!-- Список документов -->
          <div class="documents-list">
            <div
              v-for="document in documents"
              :key="document.id"
              class="document-item"
              :class="{ active: selectedDocument?.id === document.id }"
              @click="selectDocument(document)"
            >
              <div class="doc-column document-name">
                <div class="doc-icon">📄</div>
                <div class="doc-info">
                  <div class="doc-title">{{ document.title }}</div>
                  <div class="doc-filename">{{ document.filename }}</div>
                </div>
              </div>
              <div class="doc-column doc-type">{{ document.type }}</div>
              <div class="doc-column doc-company">{{ document.company }}</div>
              <div class="doc-column doc-date">{{ document.date }}</div>
            </div>
          </div>
        </div>

        <!-- Панель предпросмотра документа -->
        <div class="preview-section" v-if="selectedDocument">
          <div class="preview-header">
            <h3>PDF</h3>
            <div class="document-title">{{ selectedDocument.filename }}</div>
          </div>

          <div class="document-details">
            <div class="detail-item">
              <label>ID</label>
              <span>{{ selectedDocument.id }}</span>
            </div>
            <div class="detail-item">
              <label>Тип</label>
              <span>{{ selectedDocument.type }}</span>
            </div>
            <div class="detail-item">
              <label>Компания</label>
              <span>{{ selectedDocument.company }}</span>
            </div>
            <div class="detail-item">
              <label>Дата</label>
              <span>{{ selectedDocument.date }}</span>
            </div>
            <div class="detail-item">
              <label>Статус</label>
              <span class="status-badge">{{ selectedDocument.status }}</span>
            </div>
            <div class="detail-item tags">
              <label>Теги</label>
              <div class="tags-list">
                <span 
                  v-for="tag in selectedDocument.tags" 
                  :key="tag"
                  class="tag"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Модальное окно загрузки документов -->
    <div v-if="showUploadModal" class="upload-modal-overlay" @click="showUploadModal = false">
      <div class="upload-modal" @click.stop>
        <div class="upload-modal-header">
          <h2>Загрузка документов</h2>
          <button class="close-btn" @click="showUploadModal = false">×</button>
        </div>
        
        <div class="upload-area" 
             @dragover.prevent="dragOver = true"
             @dragleave="dragOver = false"
             @drop="handleFileDrop"
             :class="{ 'drag-over': dragOver }">
          <div class="upload-icon">📤</div>
          <h3>Перетащите файлы сюда</h3>
          <p>или</p>
          <input 
            type="file" 
            ref="fileInput"
            @change="handleFileSelect"
            multiple 
            class="file-input"
            accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.png"
          >
          <button class="btn btn-outline" @click="triggerFileInput">
            Выбрать файл
          </button>
        </div>

        <!-- Список загружаемых файлов -->
        <div class="upload-list" v-if="uploadQueue.length > 0">
          <div class="upload-list-header">
            <span>Идёт загрузка {{ uploadQueue.filter(f => f.status !== 'completed').length }} из {{ uploadQueue.length }}</span>
          </div>
          
          <div class="upload-items">
            <div v-for="file in uploadQueue" :key="file.id" class="upload-item">
              <div class="file-info">
                <div class="file-icon">📄</div>
                <div class="file-details">
                  <div class="file-name">{{ file.name }}</div>
                  <div class="file-status">
                    <span v-if="file.status === 'uploading'">Классификация...</span>
                    <span v-else-if="file.status === 'processing'">Сканирование текста... {{ file.progress }}%</span>
                    <span v-else-if="file.status === 'completed'" class="status-completed">Готово</span>
                    <span v-else-if="file.status === 'waiting'" class="status-waiting">Ожидание</span>
                  </div>
                </div>
              </div>
              <div class="file-actions">
                <button v-if="file.status === 'waiting'" @click="removeFromQueue(file.id)" class="btn-remove">×</button>
                <div v-else class="file-progress">
                  <div v-if="file.status === 'uploading' || file.status === 'processing'" class="progress-bar">
                    <div class="progress-fill" :style="{ width: file.progress + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from '@/services/api';

export default {
  name: 'MainView',
  data() {
    return {
      user: null,
      loading: true,
      showUploadModal: false,
      dragOver: false,
      uploadQueue: [],
      selectedDocument: null,
      documents: [
        {
          id: '264917',
          title: 'Договор поставки',
          filename: 'Договор №154/2024.pdf',
          type: 'Договор поставки',
          counterparty: 'ООО "Ромашка"',
          date: '12.02.2024',
          status: 'На оплате',
          tags: ['Проект X', 'Юридический', 'Поставка']
        },
        {
          id: '264918',
          title: 'Счёт на оплату',
          filename: 'Счёт №287.pdf',
          type: 'Счёт',
          counterparty: 'ООО "Вектор"',
          date: '23.03.2024',
          status: 'Оплачен',
          tags: ['Финансовый', 'Срочный']
        }
      ]
    }
  },
  methods: {
    // 🔐 Загрузка данных пользователя
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

    // 🚪 Выход из системы
    handleLogout() {
      console.log('🚪 Выход из системы...');
      apiService.clearTokens();
      this.$router.push('/login');
    },

    // 👤 Получение инициалов для аватара
    getInitials(fullName) {
      if (!fullName) return '??';
      return fullName
          .split(' ')
          .map(name => name[0])
          .join('')
          .toUpperCase();
    },

    // 📄 Методы для работы с документами
    selectDocument(document) {
      this.selectedDocument = document;
    },

    // 📎 Загрузка файлов
    triggerFileInput() {
      this.$refs.fileInput?.click();
    },

    handleFileSelect(event) {
      const files = Array.from(event.target.files);
      this.addFilesToQueue(files);
      event.target.value = '';
    },

    handleFileDrop(event) {
      event.preventDefault();
      this.dragOver = false;
      const files = Array.from(event.dataTransfer.files);
      this.addFilesToQueue(files);
    },

    addFilesToQueue(files) {
      files.forEach(file => {
        const fileItem = {
          id: Date.now() + Math.random(),
          name: file.name,
          file: file,
          status: 'waiting',
          progress: 0
        };
        this.uploadQueue.push(fileItem);
      });

      // Автоматически начинаем загрузку
      this.processUploadQueue();
    },

    async processUploadQueue() {
      const waitingFiles = this.uploadQueue.filter(f => f.status === 'waiting');

      for (const fileItem of waitingFiles) {
        fileItem.status = 'uploading';

        // Имитация загрузки (заглушка)
        await this.simulateUpload(fileItem);

        // После загрузки - классификация
        fileItem.status = 'processing';
        await this.simulateProcessing(fileItem);

        // Завершено
        fileItem.status = 'completed';
        fileItem.progress = 100;
      }
    },

    simulateUpload(fileItem) {
      return new Promise((resolve) => {
        let progress = 0;
        const interval = setInterval(() => {
          progress += 10;
          fileItem.progress = progress;

          if (progress >= 100) {
            clearInterval(interval);
            resolve();
          }
        }, 200);
      });
    },

    simulateProcessing(fileItem) {
      return new Promise((resolve) => {
        let progress = 0;
        const interval = setInterval(() => {
          progress += 15;
          fileItem.progress = progress;

          if (progress >= 100) {
            clearInterval(interval);
            resolve();
          }
        }, 300);
      });
    },

    removeFromQueue(fileId) {
      this.uploadQueue = this.uploadQueue.filter(f => f.id !== fileId);
    }
  },

  // 🎯 Хуки жизненного цикла
  async mounted() {
    console.log('🔄 MainView mounted - загружаем данные...');
    await this.loadUserData();

    // Выбираем первый документ по умолчанию
    if (this.documents.length > 0 && !this.selectedDocument) {
      this.selectedDocument = this.documents[0];
    }

    console.log('✅ MainView готов к работе!');
  },

  // 👂 Обработчики событий drag & drop
  created() {
    // Сохраняем ссылки на функции
    this.handleDragOver = (e) => {
      e.preventDefault();
      this.dragOver = true;
    };

    this.handleDragLeave = (e) => {
      e.preventDefault();
      this.dragOver = false;
    };

    this.handleDrop = (e) => {
      e.preventDefault();
      this.dragOver = false;
      this.handleFileDrop(e);
    };

    // Добавляем обработчики
    document.addEventListener('dragover', this.handleDragOver);
    document.addEventListener('dragleave', this.handleDragLeave);
    document.addEventListener('drop', this.handleDrop);
  },

  beforeDestroy() {
    // Убираем обработчики
    document.removeEventListener('dragover', this.handleDragOver);
    document.removeEventListener('dragleave', this.handleDragLeave);
    document.removeEventListener('drop', this.handleDrop);
  }
}
</script>

<style scoped src="@/styles/components/MainView.css"></style>