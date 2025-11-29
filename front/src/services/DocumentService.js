import { apiService } from './api';

class DocumentService {
  /**
   * 📥 Получение списка документов
   */
 async getDocuments(filters = {}) {
  console.log('📋 [DocumentService] Запрос списка документов:', {
    filters
  });

  try {
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

    const queryString = queryParams.toString();
    const url = queryString ? `/storage?${queryString}` : '/storage';

    console.log('🔗 [DocumentService] Запрос к API:', url);

    const response = await apiService.request(url);

    console.log('✅ [DocumentService] Документы получены:', {
      count: response?.length || 0,
      response
    });

    // ПРЕОБРАЗУЕМ ДАННЫЕ ИЗ БЭКЕНДА В ФОРМАТ ФРОНТЕНДА
    const documents = this.transformBackendData(response || []);

    console.log('🔄 [DocumentService] Преобразованные документы:', documents);

    return documents;
  } catch (error) {
    console.error('❌ [DocumentService] Ошибка при получении документов:', error);

    console.log('📋 [DocumentService] Endpoint /storage не доступен, используем mock данные');
    return this.getMockDocuments();
  }
}

/**
 * Преобразует данные из бэкенда в формат фронтенда
 */
transformBackendData(backendDocuments) {
  if (!Array.isArray(backendDocuments)) {
    return [];
  }

  return backendDocuments.map(doc => {
    // Извлекаем имя файла из file_path
    const filename = doc.file_path ? doc.file_path.split('/').pop() : 'unknown.pdf';

    // Создаем title на основе filename или используем существующий title
    const title = doc.title || filename.replace(/\.[^/.]+$/, ""); // убираем расширение

    return {
      id: doc.id || doc.file_id,
      title: title,
      filename: filename,
      type: doc.file_type || 'document', // file_type → type
      counterparty: doc.counterparty || 'Не указан', // если нет в бэкенде
      date: this.formatDate(doc.created_at || doc.upload_date), // преобразуем дату
      status: doc.status || 'processed', // если нет статуса
      size: doc.file_size ? this.formatFileSize(doc.file_size) : 'Unknown',
      tags: doc.tags || [],
      file_path: doc.file_path, // сохраняем оригинальные поля если нужны
      file_type: doc.file_type,
      file_hash: doc.file_hash
    };
  });
}

/**
 * Форматирует дату в формат DD.MM.YYYY
 */
formatDate(dateString) {
  if (!dateString) return '01.01.2024';

  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU');
  } catch {
    return '01.01.2024';
  }
}

/**
 * Форматирует размер файла
 */
formatFileSize(bytes) {
  if (!bytes) return 'Unknown';

  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  if (bytes === 0) return '0 Bytes';

  const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
  return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Применяет фильтры к mock данным
 */
applyFiltersToMock(documents, filters) {
  let filtered = [...documents];

  // Поиск по тексту
  if (filters.search) {
    const query = filters.search.toLowerCase();
    filtered = filtered.filter(doc =>
      doc.title?.toLowerCase().includes(query) ||
      doc.filename?.toLowerCase().includes(query) ||
      doc.counterparty?.toLowerCase().includes(query)
    );
  }

  // Фильтрация по типу
  if (filters.type) {
    filtered = filtered.filter(doc =>
      doc.type?.toLowerCase() === filters.type.toLowerCase()
    );
  }

  // Фильтрация по контрагенту
  if (filters.counterparty) {
    filtered = filtered.filter(doc =>
      doc.counterparty === filters.counterparty
    );
  }

  return filtered;
}

/**
 * Mock данные для fallback
 */
getMockDocuments() {
  return [
    {
      id: 1,
      title: 'Договор поставки №123',
      filename: 'dogovor_postavki_123.pdf',
      type: 'contract',
      counterparty: 'ООО "Ромашка"',
      date: '15.12.2023',
      status: 'processed',
      size: '2.4 MB',
      tags: ['договор', 'поставка', '2023']
    },
    {
      id: 2,
      title: 'Счет на оплату №456',
      filename: 'schet_456.pdf',
      type: 'invoice',
      counterparty: 'ИП Иванов',
      date: '20.12.2023',
      status: 'pending',
      size: '1.1 MB',
      tags: ['счет', 'оплата']
    },
    {
      id: 3,
      title: 'Акт выполненных работ №789',
      filename: 'akt_vypolnennyh_rabot_789.pdf',
      type: 'act',
      counterparty: 'ООО "Лютик"',
      date: '25.12.2023',
      status: 'processed',
      size: '1.8 MB',
      tags: ['акт', 'работы']
    }
  ];
}

  /**
   * 📄 Получение документа по ID
   */
   async getDocumentById(id) {
    console.log('📄 [DocumentService] Запрос документа по ID:', id);

    try {
      const document = await apiService.request(`/documents/${id}`);

      console.log('✅ [DocumentService] Документ получен:', {
        id: document.id,
        title: document.title,
        hasContent: !!document.content
      });

      return document;
    } catch (error) {
      console.log('📄 [DocumentService] Endpoint /documents/{id} не найден, используем mock данные');

      const mockDocs = this.getMockDocuments();
      const foundDoc = mockDocs.find(doc => doc.id === id) || mockDocs[0];

      console.log('🔄 [DocumentService] Возвращаем mock документ:', {
        id: foundDoc.id,
        title: foundDoc.title
      });

      return foundDoc;
    }
  }

  async getDocumentsByTag(tag) {
    console.log('🏷️ [DocumentService] Документы по тегу:', {
      tag
    });

    try {
      const documents = await apiService.request(`/documents/tags/${encodeURIComponent(tag)}`);

      console.log('✅ [DocumentService] Документы по тегу получены:', {
        tag,
        count: documents.length
      });

      return documents;
    } catch (error) {
      console.log('🏷️ [DocumentService] Endpoint tags не найден, фильтруем локально');

      const mockDocs = this.getMockDocuments();
      const filtered = mockDocs.filter(doc =>
        doc.tags.some(t => t.toLowerCase() === tag.toLowerCase())
      );

      console.log('🔄 [DocumentService] Локальная фильтрация по тегу:', {
        tag,
        found: filtered.length
      });

      return filtered;
    }
  }


  /**
   * 🗑️ Удаление документа
   */
    async deleteDocument(id) {
    console.log('🗑️ [DocumentService] Удаление документа ID:', id);

    try {
      const result = await apiService.request(`/documents/${id}`, {
        method: 'DELETE'
      });

      console.log('✅ [DocumentService] Документ удален:', { id });
      return result;
    } catch (error) {
      console.log('🗑️ [DocumentService] Endpoint DELETE /documents/{id} не найден, эмулируем удаление');
      console.log('🔄 [DocumentService] Эмуляция удаления документа:', { id });

      return {
        status: 'success',
        message: 'Документ удален (mock)',
        deletedId: id
      };
    }
  }

  /**
   * 🏷️ Обновление тегов документа
   */
  async addTagsToDocument(id, tags) {
    console.log('🏷️ [DocumentService] Добавление тегов к документу:', {
      id,
      tags
    });

    try {
      const result = await apiService.request(`/documents/${id}/tags`, {
        method: 'POST',
        body: { tags }
      });

      console.log('✅ [DocumentService] Теги добавлены:', {
        id,
        addedTags: tags
      });

      return result;
    } catch (error) {
      console.log('🏷️ [DocumentService] Endpoint tags не найден, эмулируем добавление тегов');
      console.log('🔄 [DocumentService] Эмуляция добавления тегов:', { id, tags });

      return {
        status: 'success',
        message: 'Теги добавлены (mock)',
        documentId: id,
        addedTags: tags
      };
    }
  }

  async removeTagFromDocument(documentId, tag) {
    return await apiService.request(`/documents/${documentId}/tags`, {
      method: 'DELETE',
      body: JSON.stringify({ tag })
    });
  }

}

export const documentService = new DocumentService();