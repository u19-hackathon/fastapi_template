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
              v-model="searchQuery"
            >
          </div>
          <button @click="showUploadModal = true" class="btn btn-primary upload-btn">
            Загрузить документ
          </button>

          <!-- Информация о пользователе -->
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
            <button @click="handleLogout" class="btn btn-secondary logout-btn" title="Выйти">
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
            <label class="filter-label">Тип документа</label>
            <select class="filter-select" v-model="filters.type">
              <option value="">Все типы</option>
              <option value="contract">Договор</option>
              <option value="invoice">Счёт</option>
              <option value="act">Акт</option>
              <option value="order">Приказ</option>
            </select>
          </div>
          <div class="filter-group">
            <label class="filter-label">Контрагент</label>
            <select class="filter-select" v-model="filters.counterparty">
              <option value="">Все контрагенты</option>
              <option v-for="company in uniqueCompanies" :key="company" :value="company">
                {{ company }}
              </option>
            </select>
          </div>
        </div>

        <div class="filters-actions">
          <button @click="clearFilters" class="btn btn-outline">
            Сбросить фильтры
          </button>
          <button @click="applyFilters" class="btn btn-primary">
            Применить
          </button>
        </div>
      </div>

      <div class="tags-filter-section" v-if="allTags.length > 0">
        <div class="tags-filter-header">
          <h4>Теги документов</h4>
        </div>
        <div class="tags-filter-list">
          <span
            v-for="tag in allTags"
            :key="tag"
            class="filter-tag"
            :class="{ active: filters.tags.includes(tag) }"
            @click="toggleTagFilter(tag)"
          >
            {{ tag }}
          </span>
        </div>
      </div>

      <!-- Основной контент с документами -->
      <div class="main-content">
        <div class="documents-section">
          <div class="section-header">
            <h2>Документы
              <span v-if="loadingDocuments" class="loading-indicator">🔄</span>
              <span v-else class="doc-count">({{ filteredDocuments.length }})</span>
            </h2>
            <div class="section-actions">
              <button @click="refreshDocuments" class="btn btn-outline" title="Обновить"
                      :disabled="loadingDocuments">
                🔄
              </button>
            </div>
          </div>

          <!-- Заголовки таблицы -->
          <div class="documents-header">
            <div class="doc-header-column">Документ</div>
            <div class="doc-header-column">Тип</div>
            <div class="doc-header-column">Контрагент</div>
          </div>

          <!-- Список документов -->
          <div class="documents-list">
            <div v-if="loadingDocuments" class="loading-state">
              <div class="loading-spinner large"></div>
              <p>Загрузка документов...</p>
            </div>

            <div v-else-if="filteredDocuments.length === 0" class="empty-state">
              <div class="empty-icon">📄</div>
              <h3>Документы не найдены</h3>
              <p>Попробуйте изменить параметры поиска или загрузите новые документы</p>
              <button @click="showUploadModal = true" class="btn btn-primary">
                Загрузить документы
              </button>
            </div>

            <div v-else>
              <div
                v-for="document in filteredDocuments"
                :key="document.id"
                class="document-item"
                :class="{
                  active: selectedDocument?.id === document.id,
                  [document.status]: true
                }"
                @click="selectDocument(document)"
              >
                <div class="doc-column document-name">
                  <div class="doc-icon">📄</div>
                  <div class="doc-info">
                    <div class="doc-title">{{ document.title }}</div>
                    <div class="doc-filename">{{ document.filename }}</div>
                    <div class="doc-meta">
                      <span class="doc-date">{{ document.date }}</span>
                      <span class="doc-size" v-if="document.size">{{ document.size }}</span>
                    </div>
                  </div>
                </div>

                <div class="doc-column doc-type">
                  <span class="type-badge" :class="document.type.toLowerCase()">
                    {{ document.type }}
                  </span>
                </div>

                <div class="doc-column doc-counterparty">
                  {{ document.counterparty }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Панель предпросмотра документа -->
        <div class="preview-section" v-if="selectedDocument">
          <div class="preview-header">
            <h3>Предпросмотр документа</h3>
            <div class="preview-actions">
              <button class="btn btn-outline" title="Скачать" @click="downloadDocument(selectedDocument)">📥</button>
              <button class="btn btn-outline" title="Удалить" @click="deleteDocument(selectedDocument)">🗑️</button>
            </div>
          </div>

          <div class="document-preview">
            <div class="preview-placeholder">
              <div class="preview-icon">📄</div>
              <p>Предпросмотр PDF</p>
              <button class="btn btn-outline">Открыть в полном размере</button>
            </div>
          </div>

          <div class="document-details">
            <h4>Информация о документе</h4>

            <div class="detail-item">
              <label>Название</label>
              <span>{{ selectedDocument.title }}</span>
            </div>

            <div class="detail-item">
              <label>Файл</label>
              <span>{{ selectedDocument.filename }}</span>
            </div>

            <div class="detail-item">
              <label>Тип</label>
              <span>{{ selectedDocument.type }}</span>
            </div>

            <div class="detail-item">
              <label>Контрагент</label>
              <span>{{ selectedDocument.counterparty }}</span>
            </div>

            <div class="detail-item">
              <label>Дата загрузки</label>
              <span>{{ selectedDocument.date }}</span>
            </div>

            <div class="detail-item" v-if="selectedDocument.size">
              <label>Размер</label>
              <span>{{ selectedDocument.size }}</span>
            </div>

            <div class="detail-item tags">
              <label>Теги</label>
              <div class="tags-list">
                <span
                  v-for="tag in selectedDocument.tags"
                  :key="tag"
                  class="tag"
                  @click="handleTagClick(tag, $event)"
                  @dblclick="startEditingTag(tag)"
                  :title="`Клик: фильтр по тегу\nДвойной клик: редактировать`"
                >
                  {{ tag }}
                  <span
                    v-if="editingTags"
                    class="tag-remove"
                    @click.stop="removeTag(tag)"
                  >×</span>
                </span>

                <!-- РЕДАКТИРОВАНИЕ ТЕГОВ -->
                <div v-if="editingTags" class="tag-input-container">
                  <input
                    v-model="newTag"
                    @keyup.enter="addTagToDocument"
                    @keyup.esc="cancelEditingTags"
                    placeholder="Введите тег..."
                    class="tag-input"
                    ref="tagInput"
                    @blur="onTagInputBlur"
                  />
                </div>

                <button
                  v-else
                  @click="startEditingTags"
                  class="btn-tag-add"
                  title="Добавить тег"
                >
                  +
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Состояние без выбранного документа -->
        <div class="preview-section empty-preview" v-else>
          <div class="empty-preview-content">
            <div class="empty-icon">👆</div>
            <h3>Выберите документ</h3>
            <p>Выберите документ из списка для просмотра деталей</p>
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
          <p>Поддерживаемые форматы: PDF, DOC, DOCX, XLS, XLSX, JPG, PNG</p>
          <p class="upload-limit">Максимальный размер файла: 50MB</p>
          <input
            type="file"
            ref="fileInput"
            @change="handleFileSelect"
            multiple
            class="file-input"
            accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.png"
          >
          <button class="btn btn-primary" @click="triggerFileInput">
            Выбрать файлы
          </button>
        </div>

        <!-- Список загружаемых файлов -->
        <div class="upload-list" v-if="uploadQueue.length > 0">
          <div class="upload-list-header">
            <span>Файлы для загрузки ({{ uploadQueue.filter(f => f.status !== 'completed').length }}/{{ uploadQueue.length }})</span>
            <button @click="clearUploadQueue" class="btn btn-outline btn-sm">
              Очистить все
            </button>
          </div>

          <div class="upload-items">
            <div v-for="file in uploadQueue" :key="file.id" class="upload-item">
              <div class="file-info">
                <div class="file-icon">📄</div>
                <div class="file-details">
                  <div class="file-name">{{ file.name }}</div>
                  <div class="file-meta">
                    <span class="file-size">{{ formatFileSize(file.size) }}</span>
                    <span class="file-status" :class="file.status">
                      <span v-if="file.status === 'uploading'">Загрузка...</span>
                      <span v-else-if="file.status === 'processing'">Обработка... {{ file.progress }}%</span>
                      <span v-else-if="file.status === 'completed'" class="status-completed">✅ Готово</span>
                      <span v-else-if="file.status === 'waiting'" class="status-waiting">⏳ Ожидание</span>
                      <span v-else-if="file.status === 'error'" class="status-error">❌ Ошибка</span>
                    </span>
                  </div>
                </div>
              </div>
              <div class="file-actions">
                <button
                  v-if="file.status === 'waiting' || file.status === 'error'"
                  @click="removeFromQueue(file.id)"
                  class="btn-remove"
                  title="Удалить"
                >
                  ×
                </button>
                <div v-else class="file-progress">
                  <div v-if="file.status === 'uploading' || file.status === 'processing'" class="progress-bar">
                    <div class="progress-fill" :style="{ width: file.progress + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="upload-actions">
            <button @click="processUploadQueue" class="btn btn-primary"
                    :disabled="uploadQueue.filter(f => f.status === 'waiting').length === 0">
              Начать загрузку
            </button>
            <button @click="clearUploadQueue" class="btn btn-outline">
              Отмена
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from '@/services/api';
import { documentService } from '@/services/DocumentService';
import { fileUploadService } from '@/services/FileUploadService';
import { filterService } from '@/services/FilterService';
import { notificationService } from '@/services/NotificationService';
import { documentActionsService } from '@/services/DocumentActionsService';

export default {
  name: 'MainView',
  data() {
    return {
      user: null,
      loading: true,
      showUploadModal: false,
      dragOver: false,
      selectedDocument: null,
      searchQuery: '',
      documents: [],
      filters: filterService.activeFilters,


       allTags: [],
       uniqueOwners: [],
      loadingDocuments: false,

      uploadQueue: [],

      editingTags: false,
      newTag: '',
      tagToEdit: null
    }
  },
  computed: {
    filteredDocuments() {
    // Всегда используем фронтенд-фильтрацию пока бэкенд не готов
    return filterService.filterDocuments(this.documents, this.searchQuery, this.filters);
  },
  uniqueCompanies() {
    return filterService.getUniqueCompanies(this.documents);
  },
  // Добавьте для владельцев (временно из документов)
  uniqueOwnersList() {
    const owners = this.documents.map(doc => ({
      id: doc.owner_id || doc.uploaded_by || doc.id,
      name: doc.owner_name || doc.uploaded_by_name || 'Неизвестно'
    }));
    return [...new Map(owners.map(owner => [owner.id, owner])).values()];
  }
  },
  methods: {
    async loadUserData() {
      try {
        this.loading = true;
        this.user = await apiService.getCurrentUser();
      } catch (error) {
        console.error('Ошибка загрузки пользователя:', error);
      } finally {
        this.loading = false;
      }
    },
    handleLogout() {
      apiService.clearTokens();
      this.$router.push('/login');
    },
    getInitials(fullName) {
      if (!fullName) return '??';
      return fullName.split(' ').map(name => name[0]).join('').toUpperCase();
    },





    async loadDocuments() {
      try {
        this.documents = await documentService.getDocuments();
      } catch (error) {
        console.error('Ошибка загрузки документов:', error);
      }
    },
     selectDocument(document) {
      this.selectedDocument = document;
      this.editingTags = false;
      this.newTag = '';
    },
    refreshDocuments() {
      this.loadDocuments();
      notificationService.info('Список документов обновлен');
    },

    async addTagToDocument() {
      if (!this.newTag.trim() || !this.selectedDocument) return;

      try {
        const tag = this.newTag.trim();

        // 🔧 ЕСЛИ РЕДАКТИРУЕМ СУЩЕСТВУЮЩИЙ ТЕГ - УДАЛЯЕМ СТАРЫЙ
        if (this.tagToEdit && this.tagToEdit !== tag) {
          this.selectedDocument.tags = this.selectedDocument.tags.filter(t => t !== this.tagToEdit);
        }

        // 🔧 ДОБАВЛЯЕМ НОВЫЙ ТЕГ (ЕСЛИ ЕГО ЕЩЕ НЕТ)
        if (!this.selectedDocument.tags.includes(tag)) {
          this.selectedDocument.tags.push(tag);
        }

        // 🔧 СОХРАНЯЕМ НА СЕРВЕРЕ
        await documentService.addTagsToDocument(this.selectedDocument.id, this.selectedDocument.tags);

        this.newTag = '';
        this.tagToEdit = null;

        notificationService.success(
          this.tagToEdit ? `Тег обновлен на "${tag}"` : `Тег "${tag}" добавлен`
        );

      } catch (error) {
        console.error('Ошибка работы с тегами:', error);
        notificationService.error('Ошибка при работе с тегами');
      }
    },
    async loadDocumentsByTag(tag) {
      try {
        this.documents = await documentService.getDocumentsByTag(tag);
        notificationService.info(`Загружены документы с тегом: ${tag}`);
      } catch (error) {
        console.error('Ошибка загрузки документов по тегу:', error);
        notificationService.error('Ошибка загрузки документов');
      }
    },





     startEditingTags() {
      this.editingTags = true;
      this.newTag = '';
      this.tagToEdit = null;

      this.$nextTick(() => {
        this.$refs.tagInput?.focus();
      });
    },
     async removeTag(tagToRemove) {
        if (!this.selectedDocument) return;

        try {
          // 🔧 УДАЛЯЕМ ТЕГ ИЗ СПИСКА
          this.selectedDocument.tags = this.selectedDocument.tags.filter(tag => tag !== tagToRemove);

          await documentService.removeTagFromDocument(this.selectedDocument.id, tagToRemove);

          notificationService.success(`Тег "${tagToRemove}" удален`);

        } catch (error) {
          console.error('Ошибка удаления тега:', error);
          notificationService.error('Ошибка при удалении тега');
        }
      },
     cancelEditingTags() {
      this.editingTags = false;
      this.newTag = '';
      this.tagToEdit = null;
    },
    handleTagClick(tag, event) {
      event.stopPropagation();
      this.filterByTag(tag);
    },
     onTagInputBlur() {
  // Увеличиваем таймаут для надежности
  setTimeout(() => {
    if (this.newTag.trim() === '' && !this.tagToEdit) {
      this.cancelEditingTags();
    }
  }, 300);
},
    startEditingTag(tag) {
      this.editingTags = true;
      this.newTag = tag;
      this.tagToEdit = tag;

      this.$nextTick(() => {
        this.$refs.tagInput?.focus();
        this.$refs.tagInput?.select();
      });
    },





    async applyFilters() {
    this.loadingDocuments = true;
    try {
      // 🔄 ПЫТАЕМСЯ ИСПОЛЬЗОВАТЬ БЭКЕНД-ФИЛЬТРАЦИЮ
      this.documents = await filterService.getFilteredDocuments(this.filters);
      notificationService.info('Фильтры применены');
    } catch (error) {
      if (error.message === 'BACKEND_FILTER_FAILED') {
        // 🔄 FALLBACK НА ФРОНТЕНД-ФИЛЬТРАЦИЮ
        console.log('Используем фронтенд-фильтрацию');
        // Документы уже загружены, фильтрация происходит в computed
        notificationService.info('Фильтры применены (локально)');
      } else {
        console.error('Ошибка применения фильтров:', error);
        notificationService.error('Ошибка применения фильтров');
      }
    } finally {
      this.loadingDocuments = false;
    }
  },

  async toggleTagFilter(tag) {
    const currentTags = [...this.filters.tags];
    const tagIndex = currentTags.indexOf(tag);

    if (tagIndex > -1) {
      currentTags.splice(tagIndex, 1);
    } else {
      currentTags.push(tag);
    }

    this.filters.tags = currentTags;
    await this.applyFilters();
  },
    clearFilters() {
      this.filters = filterService.resetFilters();
      notificationService.info('Фильтры сброшены');
    },
    filterByTag(tag) {
      this.searchQuery = tag;
    },
    triggerFileInput() {
      this.$refs.fileInput?.click();
    },
    async loadAllTags() {
  try {
    this.allTags = await filterService.getAllTags();
    // Если бэкенд вернул пустой массив, используем теги из документов
    if (this.allTags.length === 0) {
      this.allTags = [...new Set(this.documents.flatMap(doc => doc.tags || []))];
    }
  } catch (error) {
    console.error('Ошибка загрузки тегов:', error);
    // 🔄 FALLBACK - получаем теги из текущих документов
    this.allTags = [...new Set(this.documents.flatMap(doc => doc.tags || []))];
  }
},

  async loadUniqueOwners() {
  try {
    this.uniqueOwners = await filterService.getUniqueOwners();
    // Если бэкенд вернул пустой массив, используем владельцев из документов
    if (this.uniqueOwners.length === 0) {
      this.uniqueOwners = this.uniqueOwnersList;
    }
  } catch (error) {
    console.error('Ошибка загрузки владельцев:', error);
    // 🔄 FALLBACK
    this.uniqueOwners = this.uniqueOwnersList;
  }
},







    //ДОБАВЛЕНИЕ ФАЙЛОВ В ОЧЕРЕДЬ ПРИ ЗАГРУЗКЕ В ДИАЛОГОВОЕ ОКНО
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
      console.log('➕ [MainView] Добавление файлов в очередь:', {
        count: files.length,
        files: files.map(f => f.name)
      });

      const newFiles = files.map(file => ({
        id: Date.now() + Math.random(),
        name: file.name,
        file: file,
        size: file.size,
        status: 'waiting',
        progress: 0
      }));

      this.uploadQueue.push(...newFiles);

      console.log('📊 [MainView] Очередь обновлена:', {
        totalInQueue: this.uploadQueue.length,
        waiting: this.uploadQueue.filter(f => f.status === 'waiting').length
      });
    },


    async processUploadQueue() {
      const waitingFiles = this.uploadQueue.filter(f => f.status === 'waiting');

      console.log('🚀 [MainView] Начало обработки очереди:', {
        totalFiles: this.uploadQueue.length,
        waitingFiles: waitingFiles.length
      });

      for (const fileItem of waitingFiles) {
        try {
          // 🔧 ИМИТАЦИЯ ЗАГРУЗКИ С ПРОГРЕССОМ
          await this.simulateFileUpload(fileItem);

          // 🔧 ПОСЛЕ УСПЕШНОЙ ИМИТАЦИИ - ПЫТАЕМСЯ ЗАГРУЗИТЬ НА СЕРВЕР
          await fileUploadService.uploadFile(fileItem.file);

          this.updateFileStatus(fileItem.id, 'completed', 100);

          console.log('✅ [MainView] Файл обработан успешно:', fileItem.name);

        } catch (error) {
          console.error('💥 [MainView] Ошибка обработки файла:', fileItem.name, error);
          this.updateFileStatus(fileItem.id, 'error', 0, error.message);
        }
      }

      await this.loadDocuments();
      notificationService.success('Файлы успешно загружены');
    },


    simulateFileUpload(fileItem) {
      return new Promise((resolve, reject) => {
        console.log('🔄 [MainView] Имитация загрузки файла:', fileItem.name);

        let progress = 0;
        const totalSteps = 10; // 10 шагов до 100%
        const stepTime = 200; // 200ms на каждый шаг

        const interval = setInterval(() => {
          progress += 10;
          this.updateFileStatus(fileItem.id, 'uploading', progress);

          console.log(`📊 [MainView] Прогресс ${fileItem.name}: ${progress}%`);

          if (progress >= 100) {
            clearInterval(interval);
            console.log('✅ [MainView] Имитация загрузки завершена:', fileItem.name);
            resolve();
          }
        }, stepTime);
      });
    },

    updateFileStatus(fileId, status, progress = 0, error = null) {
      const fileIndex = this.uploadQueue.findIndex(f => f.id === fileId);
      if (fileIndex !== -1) {
        // 🔧 VUE АВТОМАТИЧЕСКИ ОБНОВИТ ИНТЕРФЕЙС ПРИ ИЗМЕНЕНИИ СВОЙСТВ
        const file = this.uploadQueue[fileIndex];
        file.status = status;
        file.progress = progress;
        if (error) file.error = error;
      }
    },

    removeFromQueue(fileId) {
      console.log('❌ [MainView] Удаление файла из очереди:', { fileId });

      const index = this.uploadQueue.findIndex(f => f.id === fileId);
      if (index !== -1) {
        this.uploadQueue.splice(index, 1);
        console.log('📊 [MainView] Файл удален из очереди');
      }
    },

    clearUploadQueue() {
      console.log('🗑️ [MainView] Очистка всей очереди');
      this.uploadQueue = [];
      console.log('✅ [MainView] Очередь очищена');
    },














    formatFileSize(bytes) {
      if (!bytes) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    downloadDocument(document) {
      documentActionsService.downloadDocument(document.id, document.filename);
    },
    deleteDocument(document) {
      documentActionsService.deleteDocument(document.id, document.title);
    },
  },
  async mounted() {
  await this.loadUserData();
  await Promise.all([
    this.loadDocuments(),
    this.loadAllTags(),
  ]);

  if (this.documents.length > 0 && !this.selectedDocument) {
    this.selectedDocument = this.documents[0];
  }
}
}
</script>

<style scoped src="@/styles/components/MainView.css"></style>