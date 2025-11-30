import { apiService } from './api';

class FileUploadService {
  async uploadFile(file) {
    console.log('📤 [FileUploadService] Начало загрузки файла:', {
      name: file.name,
      size: file.size,
      type: file.type
    });
    // Если очень нужно проверить токен в FileUploadService
    const token = localStorage.getItem('accessToken'); // ← accessToken, не access_token
    console.log(token)
    const formData = new FormData();
    formData.append('files', file);

    try {
      // ✅ ПРОСТО ИСПОЛЬЗУЕМ apiService - ОН САМ ДОБАВИТ ТОКЕН
      const response = await apiService.request('/storage/upload', {
        method: 'POST',
        body: formData
      });

      console.log('✅ [FileUploadService] Файл успешно загружен');
      return response;

    } catch (error) {
      console.error('💥 [FileUploadService] Ошибка загрузки файла:', error.message);
      throw error;
    }
  }
}

export const fileUploadService = new FileUploadService();