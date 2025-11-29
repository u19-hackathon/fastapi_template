import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Добавляем токен к каждому запросу
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Обработка ошибок авторизации
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: (credentials) => api.post('/api/users/login', credentials),
  register: (userData) => api.post('/api/users/register', userData),
  refresh: () => api.get('/api/users/refresh'),
  getUser: (userId) => api.get(`/api/users/${userId}`),
  deleteUser: (userId) => api.delete(`/api/users/${userId}`)
}

export const storageAPI = {
  getFiles: (params) => api.get('/api/storage', { params }),
  uploadFile: (file, tags) => {
    const formData = new FormData()
    formData.append('files', file)
    return api.post('/api/storage/upload', formData, {
      params: { tags: tags || [] },
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  deleteFile: (fileId) => api.delete(`/api/storage/${fileId}`),
  downloadFile: (fileId) => api.get(`/api/file-save/${fileId}`)
}

export const metadataAPI = {
  getTags: () => api.get('/api/tag'),
  getCounterparties: () => api.get('/api/counterparty')
}

export default api