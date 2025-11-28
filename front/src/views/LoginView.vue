<template>
  <div class="login-view">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1>DocHub</h1>
          <p>Войдите в систему</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label class="form-label">Email</label>
            <input
              v-model="email"
              type="email"
              class="form-input"
              placeholder="Введите ваш email"
              required
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Пароль</label>
            <input
              v-model="password"
              type="password"
              class="form-input"
              placeholder="Введите пароль"
              required
            >
          </div>
          
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
          
          <button 
            type="submit" 
            class="btn btn-primary login-btn"
            :disabled="loading"
          >
            <span v-if="loading">Вход...</span>
            <span v-else>Войти</span>
          </button>
        </form>

        <div class="register-section">
          <p class="register-text">Нет аккаунта?</p>
          <button 
            @click="goToRegister" 
            class="btn btn-secondary register-btn"
          >
            Зарегистрироваться
          </button>
        </div>
        
        <div class="demo-credentials">
          <p><strong>Демо доступ:</strong></p>
          <p>Email: user@company.com</p>
          <p>Пароль: password</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from '@/services/api';

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      error: ''
    }
  },
  methods: {
   validateEmail(email) {
  if (!email) return 'Email обязателен для заполнения';

  // Проверяем наличие @
  if (!email.includes('@')) return 'Email должен содержать @';

  const parts = email.split('@');
  if (parts.length !== 2) return 'Некорректный формат email';

  const localPart = parts[0];  // часть до @
  const domain = parts[1];     // часть после @

  // Проверяем local part
  if (localPart.length === 0) return 'Введите имя пользователя до @';
  if (!/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+$/.test(localPart)) {
    return 'Имя пользователя содержит недопустимые символы';
  }

  // Проверяем domain part
  if (!domain.includes('.')) return 'Домен должен содержать точку';

  const domainParts = domain.split('.');
  if (domainParts.length < 2) return 'Некорректный домен';

  const domainName = domainParts[0]; // example в example.com
  const tld = domainParts[1];        // com в example.com

  if (domainName.length < 2) return 'Название домена должно содержать минимум 2 символа';
  if (tld.length < 2) return 'Домен верхнего уровня должен содержать минимум 2 символа';

  // Проверяем что домен не заканчивается на точку
  if (domain.endsWith('.')) return 'Домен не может заканчиваться точкой';

  return null; // Ошибок нет
},

    async handleLogin() {
      this.loading = true
      this.error = ''

      const emailError = this.validateEmail(this.email);
      if (emailError) {
        this.error = emailError;
        this.loading = false;
        return;
      }

      try {
        console.log('🔄 Начинаем процесс входа...');

        const credentials = {
          email: this.email,
          password: this.password
        };

        // 🚀 РЕАЛЬНЫЙ ЗАПРОС К API
        await apiService.login(credentials);

        console.log('✅ Успешный вход! Перенаправляем на главную...');
        this.$router.push('/')

      } catch (error) {
        console.error('💥 Ошибка входа:', error);

        if (error.message.includes('403') || error.message.includes('Wrong email or password')) {
          this.error = 'Неверный email или пароль'
        } else if (error.message.includes('Network') || error.message.includes('Failed to fetch')) {
          this.error = 'Ошибка соединения с сервером'
        } else if (error.message.includes('400')) {
          this.error = 'Неверный формат данных'
        } else {
          this.error = 'Произошла ошибка при входе'
        }
      } finally {
        this.loading = false
      }
    },

    goToRegister() {
      this.$router.push('/register')
    }
  },

  mounted() {
    if (apiService.isAuthenticated()) {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped src="@/styles/components/LoginView.css"></style>