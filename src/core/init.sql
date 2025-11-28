-- Установка кодировки
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

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


CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) UNIQUE NOT NULL,
    document_type VARCHAR(255) NOT NULL,
    priority_level ENUM('low', 'normal', 'high', 'critical') DEFAULT 'normal',
    confidentiality ENUM('open', 'internal', 'confidential', 'strictly_confidential') DEFAULT 'internal',
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
    file_hash VARCHAR(64) NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    user_id INT NOT NULL,
    category_id INT NOT NULL,
    source_id INT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (source_id) REFERENCES source(id) ON UPDATE CASCADE ON DELETE RESTRICT,

    INDEX idx_file_hash (file_hash)
);

-- Таблица тегов
CREATE TABLE tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(100) UNIQUE NOT NULL,
    tag_type ENUM('auto', 'manual') DEFAULT 'manual',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица многие ко многим по file_id, tag_id< user_id
CREATE TABLE file_tags_users (
    file_id INT NOT NULL,
    tag_id INT NOT NULL,
    assigned_by INT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (file_id, tag_id),
    FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE SET NULL
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
('Договоры поставки', 'договор', 'normal', 'internal', 'Хозяйственные договоры с поставщиками'),
('Финансовые отчеты', 'отчет', 'high', 'confidential', 'Ежемесячные финансовые отчеты'),
('Внутренние приказы', 'приказ', 'high', 'internal', 'Приказы по основной деятельности'),
('Служебные записки', 'письмо', 'low', 'internal', 'Внутренняя переписка'),
('Коммерческие предложения', 'письмо', 'normal', 'open', 'Письма клиентам');

INSERT INTO files (title, file_path, first_lines, user_id, category_id, source_id) VALUES
('Договор поставки №1', '/files/documents/contract1.pdf', 'ДОГОВОР ПОСТАВКИ...', 1, 1, 1),
('Финансовый отчет за январь', '/files/reports/january.pdf', 'ОТЧЕТ О ПРИБЫЛИ...', 2, 2, 2);

INSERT INTO tags (tag_name, tag_type, description) VALUES
('срочный', 'manual', 'Требует немедленного внимания'),
('отчет', 'auto', 'Финансовый или операционный отчет'),
('договор', 'auto', 'Юридический документ'),
('конфиденциально', 'manual', 'Содержит конфиденциальную информацию'),
('архив', 'manual', 'Документ для архивного хранения');

INSERT INTO file_tags_users (file_id, tag_id, assigned_by) VALUES
(1, 1, 1),  -- файл 1 - срочный (назначил пользователь 1)
(1, 2, NULL), -- файл 1 - отчет (авто-назначение)
(2, 3, NULL), -- файл 2 - договор (авто-назначение)
(2, 4, 2);  -- файл 2 - конфиденциально (назначил пользователь 2)