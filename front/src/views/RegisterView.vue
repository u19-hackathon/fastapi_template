<template>
  <div class="register-view">
    <div class="register-container">
      <div class="register-card">
        <div class="register-header">
          <h1>DocHub</h1>
          <p>Создайте аккаунт</p>
        </div>
        
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label class="form-label">ФИО</label>
            <input
              v-model="fullName"
              type="text"
              class="form-input"
              placeholder="Введите ваше ФИО полностью"
              required
            >
          </div>

          <div class="form-group">
            <label class="form-label">Должность</label>
            <input
              v-model="position"
              type="text"
              class="form-input"
              placeholder="Введите вашу должность"
              required
            >
          </div>

          <div class="form-group">
            <label class="form-label">Название организации</label>
            <input
              v-model="organization"
              type="text"
              class="form-input"
              placeholder="Введите название вашей организации"
              required
            >
          </div>

           <div class="form-group">
            <label class="form-label">Отдел</label>
            <input
              v-model="department"
              type="text"
              class="form-input"
              placeholder="Введите ваш отдел"
              required
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Электронная почта</label>
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
              placeholder="Придумайте пароль(минимум 8 символов, заглавные и строчные латинские буквы и цифры"
              required
            >
          </div>
          
          <div v-if="error" class="error-message">
            {{ error }}
          </div>

          <div v-if="success" class="success-message">
            {{ success }}
          </div>
          
          <button 
            type="submit" 
            class="btn btn-primary register-btn"
            :disabled="loading"
          >
            <span v-if="loading">Регистрация...</span>
            <span v-else>Зарегистрироваться</span>
          </button>
        </form>

        <div class="login-section">
          <p class="login-text">Уже есть аккаунт?</p>
          <button 
            @click="goToLogin" 
            class="btn btn-secondary login-btn"
          >
            Войти
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from '@/services/api';

export default {
  name: 'RegisterView',
  data() {
    return {
      fullName: '',
      position: '',
      organization: '',
      department: '',
      email: '',
      password: '',
      loading: false,
      error: '',
      success: ''
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

    async handleRegister() {
      this.loading = true
      this.error = ''
      this.success = ''

      // Валидация
      if (this.password.length < 8) {
        this.error = 'Пароль должен содержать минимум 8 символов'
        this.loading = false
        return
      }

      if (!this.organization.trim()) {
        this.error = 'Название организации обязательно для заполнения'
        this.loading = false
        return
      }

      if (this.fullName.split(' ').length < 2) {
        this.error = 'Укажите имя и фамилию'
        this.loading = false
        return
      }

      const emailError = this.validateEmail(this.email);
      if (emailError) {
        this.error = emailError;
        this.loading = false;
        return;
      }
      
      try {
        console.log('🔄 Начинаем процесс регистрации...');

        // 🎯 ПОДГОТАВЛИВАЕМ ДАННЫЕ ДЛЯ БЭКА
        const userData = {
          full_name: this.fullName,
          email: this.email,
          organization_name: this.organization,
          position: this.position,
          department: this.department,
          password: this.password
        };

        console.log('📤 Отправляем данные регистрации:', userData);

        // 🚀 РЕАЛЬНЫЙ ЗАПРОС К API
        const response = await apiService.register(userData);

        console.log('✅ Успешная регистрация! Ответ:', response);

        this.success = 'Аккаунт успешно создан! Перенаправляем на главную страницу...'

        // ⏰ ЧЕРЕЗ 1 СЕКУНДЫ НА ГЛАВНУЮ
        setTimeout(() => {
          this.$router.push('/')
        }, 1000)
        
      } catch (error) {
        console.error('💥 Ошибка регистрации:', error);

        // 🎯 ТОЧНАЯ ОБРАБОТКА ОШИБОК ОТ БЭКА
        if (error.message.includes('400') || error.message.includes('Email is already in use')) {
          this.error = 'Пользователь с таким email уже существует'
        } else if (error.message.includes('422') || error.message.includes('Password')) {
          this.error = 'Пароль недостаточно надежный. Используйте заглавные и строчные буквы, цифры.'
        } else if (error.message.includes('Network') || error.message.includes('Failed to fetch')) {
          this.error = 'Ошибка соединения с сервером. Проверьте интернет.'
        } else {
          this.error = 'Произошла ошибка при регистрации. Попробуйте снова.'
        }
      } finally {
        this.loading = false
      }
    },
    
    goToLogin() {
      this.$router.push('/login')
    },

    mounted() {
    if (apiService.isAuthenticated()) {
      console.log('🔄 Уже авторизован, перенаправляем на главную...');
      this.$router.push('/');
    }
  }
  }
}
</script>

<style scoped src="@/styles/components/RegisterView.css"></style>