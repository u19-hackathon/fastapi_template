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
      // 🔧 ИСПРАВЛЯЕМ URL - используем правильный эндпоинт
      const response = await fetch(`${apiService.baseURL}/file-save/${documentId}`, {
        headers: {
          'Authorization': `Bearer ${apiService.accessToken}`
        }
      });

      console.log('📥 [DocumentActionsService] Ответ скачивания:', {
        status: response.status,
        ok: response.ok,
        headers: Object.fromEntries(response.headers.entries())
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Download failed: ${response.status} - ${errorText}`);
      }

      // Получаем blob
      const blob = await response.blob();

      // Создаем URL для скачивания
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;

      // Устанавливаем имя файла для скачивания
      link.download = filename || `document_${documentId}`;

      // Добавляем в DOM, кликаем и удаляем
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      // Освобождаем память
      window.URL.revokeObjectURL(url);

      console.log('✅ [DocumentActionsService] Документ скачан успешно:', {
        documentId: documentId,
        filename: filename,
        size: blob.size,
        type: blob.type
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

      await apiService.request(`/storage/${documentId}`, {
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

  /**
 * 📖 Открыть PDF в новой вкладке
 */
async openPdf(documentId, filename) {
  console.log('📖 [DocumentActionsService] Открытие PDF:', {
    documentId: documentId,
    filename: filename
  });

  try {
    const response = await fetch(`${apiService.baseURL}/file-save/${documentId}`, {
      headers: {
        'Authorization': `Bearer ${apiService.accessToken}`
      }
    });

    console.log('📥 Ответ сервера:', {
      status: response.status,
      contentType: response.headers.get('content-type'),
      contentLength: response.headers.get('content-length')
    });

    if (!response.ok) {
      throw new Error(`Open failed: ${response.status}`);
    }

    // Получаем blob с правильным типом
    const blob = await response.blob();

    console.log('📄 Blob информация:', {
      size: blob.size,
      type: blob.type
    });

    // Создаем blob URL с правильным типом
    const blobUrl = URL.createObjectURL(blob);

    // Открываем в новой вкладке
    const newWindow = window.open(blobUrl, '_blank');

    // Освобождаем память после загрузки
    if (newWindow) {
      newWindow.onload = () => {
        setTimeout(() => URL.revokeObjectURL(blobUrl), 1000);
      };
    } else {
      setTimeout(() => URL.revokeObjectURL(blobUrl), 5000);
    }

    console.log('✅ [DocumentActionsService] PDF открыт');

  } catch (error) {
    console.error('💥 [DocumentActionsService] Ошибка открытия PDF:', error);
    notificationService.error('Ошибка при открытии PDF');
    throw error;
  }
}
}

export const documentActionsService = new DocumentActionsService();