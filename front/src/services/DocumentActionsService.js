import { apiService } from './api';
import { notificationService } from './NotificationService';

class DocumentActionsService {
  /**
   * 📥 Скачать документ
   */
  async downloadDocument(documentId, filename) {
    console.log('📥 [DocumentActionsService] Скачивание документа:', {
      documentId: documentId,
      filename: filename
    });

    try {
      const response = await fetch(`${apiService.baseURL}/documents/${documentId}/download`, {
        headers: {
          'Authorization': `Bearer ${apiService.accessToken}`
        }
      });

      console.log('📥 [DocumentActionsService] Ответ скачивания:', {
        status: response.status,
        ok: response.ok
      });

      if (!response.ok) {
        throw new Error(`Download failed: ${response.status}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      console.log('✅ [DocumentActionsService] Документ скачан успешно:', {
        documentId: documentId,
        filename: filename,
        size: blob.size
      });

      notificationService.success('Документ успешно скачан');

    } catch (error) {
      console.error('💥 [DocumentActionsService] Ошибка скачивания:', {
        documentId: documentId,
        error: error.message
      });
      notificationService.error('Ошибка при скачивании документа');
      throw error;
    }
  }

  /**
   * 🗑️ Удалить документ
   */
  async deleteDocument(documentId, documentName) {
    console.log('🗑️ [DocumentActionsService] Удаление документа:', {
      documentId: documentId,
      documentName: documentName
    });

    try {
      // Подтверждение удаления
      if (!confirm(`Вы уверены, что хотите удалить документ "${documentName}"?`)) {
        console.log('❌ [DocumentActionsService] Удаление отменено пользователем');
        return;
      }

      await apiService.request(`/documents/${documentId}`, {
        method: 'DELETE'
      });

      console.log('✅ [DocumentActionsService] Документ удален:', {
        documentId: documentId,
        documentName: documentName
      });

      notificationService.success('Документ успешно удален');
      return true;

    } catch (error) {
      console.error('💥 [DocumentActionsService] Ошибка удаления:', {
        documentId: documentId,
        error: error.message
      });
      notificationService.error('Ошибка при удалении документа');
      throw error;
    }
  }
}

export const documentActionsService = new DocumentActionsService();