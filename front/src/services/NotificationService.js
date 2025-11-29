class NotificationService {
  constructor() {
    this.notifications = [];
    this.nextId = 1;
  }

  /**
   * 🔔 Показать уведомление
   */
  show(message, type = 'info', duration = 5000) {
    const id = this.nextId++;
    const notification = {
      id,
      message,
      type,
      show: true,
      duration
    };

    this.notifications.push(notification);

    // Автоматическое скрытие
    if (duration > 0) {
      setTimeout(() => {
        this.hide(id);
      }, duration);
    }

    return id;
  }

  /**
   * ✅ Успешное уведомление
   */
  success(message, duration = 3000) {
    return this.show(message, 'success', duration);
  }

  /**
   * ❌ Ошибка
   */
  error(message, duration = 5000) {
    return this.show(message, 'error', duration);
  }

  /**
   * ℹ️ Информация
   */
  info(message, duration = 3000) {
    return this.show(message, 'info', duration);
  }

  /**
   * ⚠️ Предупреждение
   */
  warning(message, duration = 4000) {
    return this.show(message, 'warning', duration);
  }

  /**
   * 🚫 Скрыть уведомление
   */
  hide(id) {
    const index = this.notifications.findIndex(n => n.id === id);
    if (index !== -1) {
      this.notifications.splice(index, 1);
    }
  }

  /**
   * 🗑️ Очистить все уведомления
   */
  clear() {
    this.notifications = [];
  }

  /**
   * 📋 Получить текущие уведомления
   */
  getNotifications() {
    return this.notifications;
  }
}

export const notificationService = new NotificationService();