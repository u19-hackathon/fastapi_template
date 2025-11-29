<template>
  <div class="file-upload">
    <h2>Загрузка файлов</h2>
    <input type="file" @change="handleFileSelect" multiple>
    <input
      v-model="tagsInput"
      placeholder="Теги (через запятую)"
    >
    <button @click="uploadFiles" :disabled="!selectedFiles.length">
      Загрузить
    </button>
    <div v-if="uploading">Загрузка...</div>
  </div>
</template>

<script>
import { storageAPI } from '../api'

export default {
  name: 'FileUpload',
  data() {
    return {
      selectedFiles: [],
      tagsInput: '',
      uploading: false
    }
  },
  methods: {
    handleFileSelect(event) {
      this.selectedFiles = Array.from(event.target.files)
    },
    async uploadFiles() {
      if (!this.selectedFiles.length) return

      this.uploading = true
      const tags = this.tagsInput.split(',').map(tag => tag.trim()).filter(tag => tag)

      try {
        for (const file of this.selectedFiles) {
          await storageAPI.uploadFile(file, tags)
        }
        alert('Файлы успешно загружены')
        this.selectedFiles = []
        this.tagsInput = ''
        this.$emit('files-uploaded')
      } catch (error) {
        console.error('Ошибка загрузки:', error)
        alert('Ошибка загрузки файлов')
      } finally {
        this.uploading = false
      }
    }
  }
}
</script>

<style scoped>
.file-upload {
  border: 1px solid #ddd;
  padding: 20px;
  margin: 10px 0;
  border-radius: 5px;
}

input, button {
  margin: 5px;
  padding: 8px;
}

button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
</style>