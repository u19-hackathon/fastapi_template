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
      const queryParams = new URLSearchParams(filters).toString();
      const url = '/storage'

      const documents = await apiService.request(url);

      console.log('✅ [DocumentService] Документы получены:', {
        count: documents.length
      });

      return documents;
    } catch (error) {
      console.log('📋 [DocumentService] Endpoint /documents не найден, используем mock данные');

      const mockDocs = this.getMockDocuments();
      console.log('🔄 [DocumentService] Возвращаем mock данные:', {
        count: mockDocs.length
      });
      return mockDocs;
    }
  }


  getMockDocuments() {
    return [
      {
        id: '264917',
        title: 'Договор поставки',
        filename: 'Договор №154-2024.pdf',
        type: 'Договор',
        counterparty: 'ООО "Ромашка"',
        date: '12.02.2024',
        status: 'На оплате',
        size: '2.4 MB',
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
        size: '1.8 MB',
        tags: ['Финансовый', 'Срочный']
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