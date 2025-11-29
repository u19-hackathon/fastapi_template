import { apiService } from './api';

class FilterService {
  constructor() {
    this.activeFilters = {
      type: '',
      status: '',
      counterparty: '',
      date: '',
      tags: [],
      search: ''
    };
  }

  /**
   * 🔍 Фронтенд-фильтрация документов (fallback)
   */
  filterDocuments(documents, searchQuery = '', filters = {}) {
    let filtered = [...documents];

    // Поиск по тексту
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(doc =>
        doc.title?.toLowerCase().includes(query) ||
        doc.filename?.toLowerCase().includes(query) ||
        doc.counterparty?.toLowerCase().includes(query) ||
        doc.tags?.some(tag => tag.toLowerCase().includes(query))
      );
    }

    // Фильтрация по типу
    if (filters.type) {
      filtered = filtered.filter(doc =>
        doc.type?.toLowerCase().includes(filters.type.toLowerCase())
      );
    }

    // Фильтрация по статусу
    if (filters.status) {
      filtered = filtered.filter(doc =>
        doc.status?.toLowerCase().includes(filters.status.toLowerCase())
      );
    }

    // Фильтрация по контрагенту
    if (filters.counterparty) {
      filtered = filtered.filter(doc => doc.counterparty === filters.counterparty);
    }

    // Фильтрация по тегам
    if (filters.tags && filters.tags.length > 0) {
      filtered = filtered.filter(doc =>
        doc.tags?.some(tag => filters.tags.includes(tag))
      );
    }

    // Фильтрация по владельцу
    if (filters.owner) {
      filtered = filtered.filter(doc => doc.owner_id === filters.owner);
    }

    // Фильтрация по дате
    if (filters.date) {
      filtered = this.filterByDate(filtered, filters.date);
    }

    return filtered;
  }

  /**
   * 📅 Фильтрация по дате
   */
  filterByDate(documents, dateFilter) {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    return documents.filter(doc => {
      const docDate = this.parseDate(doc.date);
      if (!docDate) return true;

      switch (dateFilter) {
        case 'today':
          return docDate.getTime() === today.getTime();
        case 'week':
          const weekAgo = new Date(today);
          weekAgo.setDate(weekAgo.getDate() - 7);
          return docDate >= weekAgo;
        case 'month':
          const monthAgo = new Date(today);
          monthAgo.setMonth(monthAgo.getMonth() - 1);
          return docDate >= monthAgo;
        default:
          return true;
      }
    });
  }

  /**
   * 📆 Парсинг даты из строки
   */
  parseDate(dateString) {
    try {
      const [day, month, year] = dateString.split('.');
      return new Date(year, month - 1, day);
    } catch {
      return null;
    }
  }

  /**
   * 🏢 Получение уникальных компаний
   */
  getUniqueCompanies(documents) {
  if (!documents || !Array.isArray(documents)) return [];
  return [...new Set(documents.map(doc => doc.counterparty).filter(Boolean))];
}

  /**
   * 🏢 Получение уникальных контрагентов из БД (с fallback)
   */
  async getUniqueCompaniesFromAPI() {
    try {
      const response = await apiService.request('/documents/counterparties');
      return response.counterparties || [];
    } catch (error) {
      console.error('Ошибка получения контрагентов:', error);
      // Fallback на фронтенд
      return [];
    }
  }

  /**
   * 🏷️ Получение всех тегов из БД (с fallback)
   */
  async getAllTags() {
    try {
      const response = await apiService.request('/tag');
      return response.tags || [];
    } catch (error) {
      console.error('Ошибка получения тегов:', error);
      // Fallback на фронтенд
      return [];
    }
  }

  /**
   * 👤 Получение уникальных владельцев из БД (с fallback)
   */
  async getUniqueOwners() {
    try {
      const response = await apiService.request('/documents/owners');
      return response.owners || [];
    } catch (error) {
      console.error('Ошибка получения владельцев:', error);
      // Fallback на фронтенд
      return [];
    }
  }

  /**
   * 🔍 Получение документов с фильтрацией с бэкенда (с fallback)
   */
  async getFilteredDocuments(filters = {}) {
    try {
      // Формируем query параметры
      const queryParams = new URLSearchParams();

      Object.entries(filters).forEach(([key, value]) => {
        if (value && value !== '' && (!Array.isArray(value) || value.length > 0)) {
          if (Array.isArray(value)) {
            value.forEach(v => queryParams.append(key, v));
          } else {
            queryParams.append(key, value);
          }
        }
      });

      const endpoint = `/documents?${queryParams.toString()}`;
      const response = await apiService.request(endpoint);

      return response.documents || [];
    } catch (error) {
      console.error('Ошибка получения документов:', error);
      // Fallback на фронтенд-фильтрацию
      throw new Error('BACKEND_FILTER_FAILED');
    }
  }

  /**
   * 🧹 Сброс фильтров
   */
  resetFilters() {
    this.activeFilters = {
      type: '',
      status: '',
      counterparty: '',
      date: '',
      tags: [],
      search: ''
    };
    return this.activeFilters;
  }

  /**
   * 🔄 Обновление фильтров
   */
  updateFilters(newFilters) {
    this.activeFilters = { ...this.activeFilters, ...newFilters };
    return this.activeFilters;
  }
}

export const filterService = new FilterService();