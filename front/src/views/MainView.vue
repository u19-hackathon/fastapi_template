<template>
  <div class="main-view">
    <!-- Боковая панель -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1>DocHub</h1>
      </div>
      <nav class="sidebar-nav">
        <a href="#" class="nav-item active">
          <span class="nav-icon">📊</span>
          Dashboard
        </a>
        <a href="#" class="nav-item">
          <span class="nav-icon">📄</span>
          Documents
        </a>
        <a href="#" class="nav-item">
          <span class="nav-icon">📈</span>
          Analytics
        </a>
        <a href="#" class="nav-item">
          <span class="nav-icon">⚙️</span>
          Settings
        </a>
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
              placeholder="Search documents..." 
              class="search-input"
            >
          </div>
          <button @click="showUploadModal = true" class="btn btn-primary upload-btn">
              📎 Загрузить документ
            </button>
          <div class="header-buttons">
            <div class="user-menu">
              <span class="user-name">Иван Иванов</span>
              <button @click="handleLogout" class="logout-btn">Выйти</button>
            </div>
          </div>
        </div>
      </header>

      <!-- Фильтры -->
      <div class="filters-section">
        <div class="filters-grid">
          <div class="filter-group">
            <label>Type</label>
            <select class="filter-select">
              <option>Any</option>
              <option>Договор</option>
              <option>Счёт</option>
              <option>Акт</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Tag</label>
            <select class="filter-select">
              <option>Any</option>
              <option>Юридический</option>
              <option>Кадровый</option>
              <option>Финансовый</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Counterparty</label>
            <select class="filter-select">
              <option>All</option>
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
            <h2>Documents</h2>
          </div>
          
          <!-- Заголовки таблицы -->
          <div class="documents-header">
            <div class="doc-header-column">Document</div>
            <div class="doc-header-column">Type</div>
            <div class="doc-header-column">Counterparty</div>
            <div class="doc-header-column">Date</div>
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
              <div class="doc-column doc-counterparty">{{ document.counterparty }}</div>
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
              <label>Type</label>
              <span>{{ selectedDocument.type }}</span>
            </div>
            <div class="detail-item">
              <label>Counterparty</label>
              <span>{{ selectedDocument.counterparty }}</span>
            </div>
            <div class="detail-item">
              <label>Date</label>
              <span>{{ selectedDocument.date }}</span>
            </div>
            <div class="detail-item">
              <label>Status</label>
              <span class="status-badge">{{ selectedDocument.status }}</span>
            </div>
            <div class="detail-item tags">
              <label>Tags</label>
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
      selectedDocument: null,
      showUploadModal: false,
      dragOver: false,
      uploadQueue: [],
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
    // 🔐 РЕАЛЬНЫЙ ВЫХОД
    async handleLogout() {
      console.log('🚪 Выход из системы...');
      apiService.clearTokens();
      this.$router.push('/login');
    },

    // 👤 ЗАГРУЗКА ДАННЫХ ПОЛЬЗОВАТЕЛЯ
    async loadUserData() {
      try {
        console.log('👤 Загружаем данные пользователя...');
        this.user = await apiService.getCurrentUser();

        if (this.user) {
          console.log('✅ Данные пользователя:', this.user);
        } else {
          console.log('❌ Не удалось загрузить пользователя');
          this.handleLogout();
        }
      } catch (error) {
        console.error('💥 Ошибка загрузки пользователя:', error);
        this.handleLogout();
      } finally {
        this.loading = false;
      }
    },

    // 📤 РЕАЛЬНАЯ ЗАГРУЗКА ФАЙЛОВ (ЗАГЛУШКА ДЛЯ БУДУЩЕГО)
    async uploadFileToServer(fileItem) {
      console.log('📤 Начинаем загрузку файла:', fileItem.name);

      // 🎯 ЗДЕСЬ БУДЕТ РЕАЛЬНЫЙ API ЗАПРОС КОГДА ПОЯВИТСЯ БЭКЕНД
      try {
        // Пример будущего кода:
        // const formData = new FormData();
        // formData.append('file', fileItem.file);
        // formData.append('user_id', this.user.id);
        //
        // const response = await apiService.request('/documents/upload', {
        //   method: 'POST',
        //   body: formData,
        //   headers: {
        //     'Authorization': `Bearer ${apiService.accessToken}`
        //   }
        // });

        // Пока просто имитируем успешную загрузку
        await new Promise(resolve => setTimeout(resolve, 2000));

        console.log('✅ Файл успешно загружен:', fileItem.name);
        return { success: true, documentId: 'temp_' + Date.now() };

      } catch (error) {
        console.error('💥 Ошибка загрузки файла:', error);
        return { success: false, error: error.message };
      }
    },

    // 🔄 ОБНОВЛЕННАЯ ЗАГРУЗКА С РЕАЛЬНОЙ ЛОГИКОЙ
    async processUploadQueue() {
      const waitingFiles = this.uploadQueue.filter(f => f.status === 'waiting');

      for (const fileItem of waitingFiles) {
        fileItem.status = 'uploading';

        // 📤 РЕАЛЬНАЯ ЗАГРУЗКА НА СЕРВЕР
        const uploadResult = await this.uploadFileToServer(fileItem);

        if (uploadResult.success) {
          fileItem.status = 'processing';
          fileItem.documentId = uploadResult.documentId;

          // 🧠 ИМИТАЦИЯ КЛАССИФИКАЦИИ (ПОКА)
          await this.simulateDocumentProcessing(fileItem);

          fileItem.status = 'completed';
          fileItem.progress = 100;

          // 📝 ДОБАВЛЯЕМ В СПИСОК ДОКУМЕНТОВ
          this.addToDocumentsList(fileItem);
        } else {
          fileItem.status = 'error';
          fileItem.error = uploadResult.error;
        }
      }
    },

    // 📝 ДОБАВЛЕНИЕ ЗАГРУЖЕННОГО ФАЙЛА В СПИСОК
    addToDocumentsList(fileItem) {
      const newDocument = {
        id: fileItem.documentId,
        title: this.extractTitle(fileItem.name),
        filename: fileItem.name,
        type: 'Новый документ', // 🎯 БУДЕТ ОПРЕДЕЛЯТЬСЯ ПРИ КЛАССИФИКАЦИИ
        counterparty: 'Не указан',
        date: new Date().toLocaleDateString('ru-RU'),
        status: 'Обработан',
        tags: ['Новый']
      };

      this.documents.unshift(newDocument); // Добавляем в начало

      // 🎯 ЕСЛИ НЕТ ВЫБРАННОГО ДОКУМЕНТА - ВЫБИРАЕМ ПЕРВЫЙ
      if (!this.selectedDocument) {
        this.selectedDocument = newDocument;
      }
    },

    // 🧠 ИЗВЛЕЧЕНИЕ НАЗВАНИЯ ИЗ ИМЕНИ ФАЙЛА
    extractTitle(filename) {
      // Убираем расширение файла
      return filename.replace(/\.[^/.]+$/, "");
    },

    // 🧪 СИМУЛЯЦИЯ ОБРАБОТКИ (ПОКА)
    simulateDocumentProcessing(fileItem) {
      return new Promise((resolve) => {
        console.log('🧠 Классифицируем документ:', fileItem.name);
        setTimeout(resolve, 1500);
      });
    },

    // 🎯 СУЩЕСТВУЮЩИЕ МЕТОДЫ (ОСТАВЛЯЕМ)
    selectDocument(document) {
      this.selectedDocument = document;
    },

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

      this.processUploadQueue();
    },

    removeFromQueue(fileId) {
      this.uploadQueue = this.uploadQueue.filter(f => f.id !== fileId);
    }
  },

  // 🎯 MOUNTED ТЕПЕРЬ ИСПОЛЬЗУЕТСЯ!
  async mounted() {
    console.log('🔄 MainView mounted - загружаем данные...');

    // 1. 🔐 ЗАГРУЖАЕМ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ
    await this.loadUserData();

    // 2. 📄 ВЫБИРАЕМ ПЕРВЫЙ ДОКУМЕНТ ЕСЛИ ЕСТЬ
    if (this.documents.length > 0 && !this.selectedDocument) {
      this.selectedDocument = this.documents[0];
    }

    console.log('✅ MainView готов к работе!');
  }
}
</script>

<style scoped src="@/styles/components/MainView.css"></style>