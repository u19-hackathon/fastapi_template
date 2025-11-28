import { API_CONFIG } from "../config/api";

class ApiService {
    constructor() {
        this.baseURL = API_CONFIG.BASE_URL;
        this.timeout = API_CONFIG.TIMEOUT;
        this.retryAttempts = API_CONFIG.RETRY_ATTEMPTS;

        this.accessToken = localStorage.getItem('accessToken');
        this.refreshToken = localStorage.getItem('refreshToken');

        console.log('🟢 ApiService инициализирован:', {
            baseURL: this.baseURL,
            hasAccessToken: !!this.accessToken,
            hasRefreshToken: !!this.refreshToken
        });
    }


    /**
     * 🚀 ОСНОВНОЙ МЕТОД ДЛЯ ВСЕХ HTTP-ЗАПРОСОВ
     * Автоматически добавляет токены, обрабатывает ошибки и обновляет токены
     *
     * @param {string} endpoint - API endpoint (например: '/users/register')
     * @param {Object} options - Опции fetch (method, body, headers и т.д.)
     * @returns {Promise<any>} - Ответ от сервера в формате JSON
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);


        const config = {
            signal: controller.signal, // Для отмены запроса при таймауте
            headers: {
                'Content-Type': 'application/json', // Всегда отправляем JSON
                ...options.headers, // Дополнительные заголовки из опций
            },
            ...options, // method, body и другие опции
        };

        // 🔐 ДОБАВЛЯЕМ JWT ТОКЕН В ЗАГОЛОВОК АВТОРИЗАЦИИ
        if (this.accessToken) {
            config.headers['Authorization'] = `Bearer ${this.accessToken}`;
        }

        console.log('📤 Отправка запроса:', {
            method: config.method || 'GET',
            url: url,
            hasToken: !!this.accessToken
        });

        try {
            // 🚀 ВЫПОЛНЯЕМ HTTP ЗАПРОС
            const response = await fetch(url, config);
            clearTimeout(timeoutId); // Очищаем таймер при успешном ответе

            console.log('📥 Получен ответ:', {
                status: response.status,
                statusText: response.statusText,
                url: url
            });

            // 🔄 ОБРАБОТКА ПРОСРОЧЕННОГО ACCESS ТОКЕНА
            if (response.status === 401 && this.refreshToken) {
                console.log('🔄 Access токен просрочен, пробуем обновить...');
                const refreshed = await this.refreshTokens();
                if (refreshed) {
                    console.log('✅ Токены обновлены, повторяем запрос');
                    // Повторяем исходный запрос с новым access токеном
                    config.headers['Authorization'] = `Bearer ${this.accessToken}`;
                    return await fetch(url, config);
                }
            }

            // ❌ ПРОВЕРЯЕМ HTTP СТАТУС ОТВЕТА
            if (!response.ok) {
                const errorText = await response.text();
                console.error('❌ HTTP ошибка:', {
                    status: response.status,
                    statusText: response.statusText,
                    endpoint: endpoint,
                    response: errorText
                });
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }

            // ✅ УСПЕШНЫЙ ОТВЕТ - ПАРСИМ JSON
            const data = await response.json();
            console.log('✅ Запрос выполнен успешно:', {
                endpoint: endpoint,
                response: data
            });
            return data;

        } catch (error) {
            clearTimeout(timeoutId); // Всегда очищаем таймаут
            console.error('💥 Ошибка запроса:', {
                endpoint: endpoint,
                error: error.message,
                url: url
            });
            throw error;
        }
    }

    /**
     * 🔄 ОБНОВЛЕНИЕ JWT ТОКЕНОВ С ИСПОЛЬЗОВАНИЕМ REFRESH ТОКЕНА
     * Вызывается автоматически при получении 401 ошибки
     *
     * @returns {Promise<boolean>} - true если токены успешно обновлены
     */
    async refreshTokens() {
        console.log('🔄 Запуск обновления токенов...');

        try {
            // 📨 ОТПРАВЛЯЕМ REFRESH ТОКЕН НА ЭНДПОИНТ /refresh
            const response = await fetch(`${this.baseURL}/users/refresh`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.refreshToken}`,
                },
            });

            if (response.ok) {
                // ✅ ПОЛУЧАЕМ НОВЫЕ ТОКЕНЫ
                const data = await response.json();
                this.setTokens(data.access, data.refresh);
                console.log('✅ Токены успешно обновлены');
                return true;
            } else {
                // ❌ REFRESH ТОКЕН ТОЖЕ НЕВАЛИДЕН
                console.error('❌ Refresh токен недействителен');
                this.clearTokens(); // Полностью разлогиниваем пользователя
                return false;
            }
        } catch (error) {
            console.error('💥 Ошибка при обновлении токенов:', error);
            this.clearTokens();
            return false;
        }
    }

    /**
     * 💾 СОХРАНЕНИЕ ТОКЕНОВ В LOCALSTORAGE И ПАМЯТИ
     * Вызывается после успешной регистрации/логина/обновления токенов
     *
     * @param {string} access - Access JWT токен
     * @param {string} refresh - Refresh JWT токен
     */
    setTokens(access, refresh) {
        this.accessToken = access;
        this.refreshToken = refresh;

        // 💾 СОХРАНЯЕМ В LOCALSTORAGE ДЛЯ PERSISTENCE
        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);

        console.log('💾 Токены сохранены:', {
            accessLength: access?.length,
            refreshLength: refresh?.length
        });
    }

    /**
     * 🗑️ ОЧИСТКА ТОКЕНОВ (ЛОГАУТ)
     * Удаляет токены из памяти и localStorage
     */
    clearTokens() {
        this.accessToken = null;
        this.refreshToken = null;

        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');

        console.log('🗑️ Токены очищены, пользователь разлогинен');
    }

    /**
     * 🔐 ПРОВЕРКА АВТОРИЗАЦИИ ПОЛЬЗОВАТЕЛЯ
     *
     * @returns {boolean} - true если пользователь авторизован
     */
    isAuthenticated() {
        const hasToken = !!this.accessToken;
        console.log('🔐 Проверка авторизации:', hasToken);
        return hasToken;
    }

    /**
     * 📝 РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ
     */
    async register(userData) {
        console.log('👤 Начало регистрации пользователя:', {
            email: userData.email,
            organization: userData.organization_name
        });

        const requestData = {
            full_name: userData.full_name,
            email: userData.email,
            organization_name: userData.organization_name,
            position: userData.position,
            department: userData.department,
            password: userData.password
        };

        console.log('📤 Отправляемые данные (без id):', requestData);

        // 🚀 ОТПРАВЛЯЕМ POST ЗАПРОС НА РЕГИСТРАЦИЮ
        const response = await this.request('/users/register', {
            method: 'POST',
            body: JSON.stringify(requestData),
        });

        // ✅ СОХРАНЯЕМ ТОКЕНЫ ПОСЛЕ УСПЕШНОЙ РЕГИСТРАЦИИ
        this.setTokens(response.access, response.refresh);

        console.log('✅ Пользователь зарегистрирован:', {
            userId: response.user_id, // ⬅️ ID приходит ОТ сервера
            hasTokens: !!(response.access && response.refresh)
        });

        return response;
    }

    /**
     * 🔐 АВТОРИЗАЦИЯ ПОЛЬЗОВАТЕЛЯ
     * Использует UserLoginDTO на бэкенде: { email: string, password: string }
     * Получает JWTResponseDTO: { user_id: number, access: string, refresh: string }
     *
     * @param {Object} credentials - Учетные данные
     * @param {string} credentials.email - Email
     * @param {string} credentials.password - Пароль
     * @returns {Promise<Object>} - Ответ сервера с токенами и user_id
     */
    async login(credentials) {
        console.log('🔐 Начало авторизации:', {email: credentials.email});

        const response = await this.request('/users/login', {
            method: 'POST',
            body: JSON.stringify(credentials),
        });

        // ✅ СОХРАНЯЕМ ТОКЕНЫ ПОСЛЕ УСПЕШНОГО ВХОДА
        // JWTResponseDTO: { user_id, access, refresh }
        this.setTokens(response.access, response.refresh);

        console.log('✅ Пользователь авторизован:', {
            userId: response.user_id,
            hasTokens: !!(response.access && response.refresh)
        });

        return response;
    }

    /**
     * 👤 ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ПОЛЬЗОВАТЕЛЕ ПО ID
     * Требует действительный JWT токен
     * Получает UserResponseDTO: { id, full_name, email, organization_name, position, department, created_at }
     *
     * @param {number} userId - ID пользователя
     * @returns {Promise<Object>} - Данные пользователя в формате UserResponseDTO
     */
    async getUser(userId) {
        console.log('👤 Запрос данных пользователя:', {userId});

        // 🚀 GET ЗАПРОС С AUTHORIZATION HEADER
        // Возвращает UserResponseDTO
        return await this.request(`/users/${userId}`);
    }


    /**
     * 👤 ПОЛУЧЕНИЕ ДАННЫХ ТЕКУЩЕГО АВТОРИЗОВАННОГО ПОЛЬЗОВАТЕЛЯ
     * Автоматически извлекает user_id из JWT токена и запрашивает данные
     *
     * @returns {Promise<Object|null>} - UserResponseDTO или null если не авторизован
     */
    async getCurrentUser() {
        if (!this.isAuthenticated()) {
            console.log('❌ Пользователь не авторизован');
            return null;
        }

        try {
            // 🔍 ПОЛУЧАЕМ USER_ID ИЗ JWT ТОКЕНА
            const userId = this.getUserIdFromToken();

            if (!userId) {
                console.error('❌ Не удалось получить ID пользователя из токена');
                return null;
            }

            console.log('👤 Загрузка данных текущего пользователя ID:', userId);

            // 🚀 ЗАПРАШИВАЕМ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ
            const userData = await this.getUser(userId);

            console.log('✅ Данные текущего пользователя получены:', userData);
            return userData;

        } catch (error) {
            console.error('💥 Ошибка получения текущего пользователя:', error);
            return null;
        }
    }


    getUserIdFromToken() {
        if (!this.accessToken) {
            return null;
        }

        try {
            // JWT токен: header.payload.signature
            const payloadBase64 = this.accessToken.split('.')[1];

            // Декодируем base64 и парсим JSON
            const payloadJson = atob(payloadBase64);
            const payload = JSON.parse(payloadJson);

            console.log('🔍 Декодирован JWT payload:', payload);

            // В вашем бэкенде user_id хранится в поле "sub"
            const userId = parseInt(payload.sub);

            if (!userId || isNaN(userId)) {
                console.error('❌ Неверный user_id в токене:', payload.sub);
                return null;
            }

            return userId;

        } catch (error) {
            console.error('💥 Ошибка декодирования JWT токена:', error);
            return null;
        }
    }
}

export const apiService = new ApiService();