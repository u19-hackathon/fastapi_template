<template>
  <div class="user-profile">
    <h2>Профиль пользователя</h2>
    <div v-if="user">
      <p><strong>ID:</strong> {{ user.id }}</p>
      <p><strong>Имя:</strong> {{ user.full_name }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>Организация:</strong> {{ user.organization_name }}</p>
      <p><strong>Должность:</strong> {{ user.position }}</p>
      <p><strong>Отдел:</strong> {{ user.department }}</p>
      <button @click="deleteUser" class="btn-danger">Удалить пользователя</button>
    </div>
    <div v-else>
      <p>Загрузка...</p>
    </div>
  </div>
</template>

<script>
import { authAPI } from '../api'

export default {
  name: 'UserProfile',
  props: ['userId'],
  data() {
    return {
      user: null
    }
  },
  async mounted() {
    await this.loadUser()
  },
  methods: {
    async loadUser() {
      try {
        const response = await authAPI.getUser(this.userId)
        this.user = response.data
      } catch (error) {
        console.error('Ошибка загрузки пользователя:', error)
        alert('Ошибка загрузки профиля')
      }
    },
    async deleteUser() {
      if (confirm('Вы уверены, что хотите удалить пользователя?')) {
        try {
          await authAPI.deleteUser(this.userId)
          alert('Пользователь удален')
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          this.$emit('logout')
        } catch (error) {
          console.error('Ошибка удаления:', error)
          alert('Ошибка удаления пользователя')
        }
      }
    }
  }
}
</script>

<style scoped>
.user-profile {
  border: 1px solid #ddd;
  padding: 20px;
  margin: 10px 0;
  border-radius: 5px;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-danger:hover {
  background-color: #c82333;
}
</style>