-- Установка кодировки
SET NAMES utf8mb4;

USE db;

-- Таблица пользователей
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    organization_name VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    department VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица источников
CREATE TABLE source (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_name VARCHAR(255) NOT NULL UNIQUE,
    source_type ENUM('website', 'email', 'scan', 'EDO', 'ERP') NOT NULL
);

-- Таблица категорий С РУССКИМИ ENUM
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) UNIQUE NOT NULL,
    document_type VARCHAR(255) NOT NULL,
    priority_level ENUM('низкий', 'обычный', 'высокий', 'критический') DEFAULT 'обычный',
    confidentiality ENUM('открытый', 'внутренний', 'конфиденциальный', 'строго_конфиденциальный') DEFAULT 'внутренний',
    description TEXT
);

-- Таблица файлов
CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    first_lines TEXT,
    file_size INT,
    file_type VARCHAR(50),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    source_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (source_id) REFERENCES source(id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ТЕСТОВЫЕ ДАННЫЕ
INSERT INTO users (full_name, email, password, organization_name, position, department) VALUES
('Администратор Системы', 'admin@company.com', 'hashed_password_123', 'ООО "Тестовая Компания"', 'Администратор', 'ИТ'),
('Иванов Иван Иванович', 'ivanov@company.com', 'hashed_password_456', 'ООО "Тестовая Компания"', 'Менеджер', 'Отдел продаж');

INSERT INTO source (source_name, source_type) VALUES
('Корпоративная почта', 'email'),
('Сайт компании', 'website'),
('Сканер документов', 'scan'),
('Электронный документооборот', 'EDO'),
('ERP система', 'ERP');

INSERT INTO categories (category_name, document_type, priority_level, confidentiality, description) VALUES
('Договоры поставки', 'договор', 'обычный', 'внутренний', 'Хозяйственные договоры с поставщиками'),
('Финансовые отчеты', 'отчет', 'высокий', 'конфиденциальный', 'Ежемесячные финансовые отчеты'),
('Внутренние приказы', 'приказ', 'высокий', 'внутренний', 'Приказы по основной деятельности'),
('Служебные записки', 'письмо', 'низкий', 'внутренний', 'Внутренняя переписка'),
('Коммерческие предложения', 'письмо', 'обычный', 'открытый', 'Письма клиентам');