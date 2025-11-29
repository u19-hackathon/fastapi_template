import { apiService } from './api';

class FileUploadService {
  /**
   * 📤 Загрузка файла на сервер через apiService
   */
  async uploadFile(file) {
    console.log('📤 [FileUploadService] Начало загрузки файла:', {
      name: file.name,
      size: file.size,
      type: file.type
    });

    const formData = new FormData();
    formData.append('files', file);

    try {
      const response = await apiService.request('/storage/upload', {
        method: 'POST',
        body: formData
      });

      console.log('✅ [FileUploadService] Файл успешно загружен:', {
        name: file.name,
        response: response
      });
      return response;

    } catch (error) {
      console.error('💥 [FileUploadService] Ошибка загрузки файла:', {
        name: file.name,
        error: error.message
      });
      throw error;
    }
  }
}

export const fileUploadService = new FileUploadService();