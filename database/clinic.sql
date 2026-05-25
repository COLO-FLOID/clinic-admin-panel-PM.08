-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Май 25 2026 г., 23:11
-- Версия сервера: 10.4.32-MariaDB
-- Версия PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `clinic_db`
--

-- --------------------------------------------------------

--
-- Структура таблицы `activity_logs`
--

CREATE TABLE `activity_logs` (
  `id` int(11) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `action_text` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `activity_logs`
--

INSERT INTO `activity_logs` (`id`, `username`, `action_text`, `created_at`) VALUES
(1, 'admin', 'Добавлен врач', '2026-05-24 23:13:31'),
(2, 'admin', 'Изменены данные врача', '2026-05-24 23:13:35'),
(3, 'admin', 'Изменены данные пациента', '2026-05-24 23:34:38'),
(4, 'admin', 'Добавлен пациент', '2026-05-24 23:34:38'),
(5, 'admin', 'Изменены данные пациента', '2026-05-24 23:38:11'),
(6, 'admin', 'Изменены данные врача', '2026-05-24 23:43:36'),
(7, 'admin', 'Изменены данные врача', '2026-05-24 23:43:48'),
(8, 'admin', 'Добавлен пациент', '2026-05-24 23:54:03'),
(9, 'viewer', 'Вход в систему', '2026-05-24 23:55:14'),
(10, 'viewer', 'Добавлен врач', '2026-05-24 23:55:38'),
(11, 'admin', 'Вход в систему', '2026-05-24 23:57:40'),
(12, 'admin', 'Удалён врач', '2026-05-24 23:57:45'),
(13, 'viewer', 'Вход в систему', '2026-05-25 00:08:34'),
(14, 'manager', 'Вход в систему', '2026-05-25 00:09:59'),
(15, 'admin', 'Вход в систему', '2026-05-25 00:11:48'),
(16, 'admin', 'Удалён врач', '2026-05-25 00:18:57'),
(17, 'admin', 'Удалён врач', '2026-05-25 00:19:00'),
(18, 'manager', 'Вход в систему', '2026-05-25 00:24:16'),
(19, 'admin', 'Вход в систему', '2026-05-25 00:25:24'),
(20, 'admin', 'Удалена услуга', '2026-05-25 00:25:29'),
(21, 'admin', 'Изменена услуга', '2026-05-25 00:31:49'),
(22, 'admin', 'Изменена запись на приём', '2026-05-25 00:32:18'),
(23, 'admin', 'Изменён статус пользователя', '2026-05-25 01:11:13'),
(24, 'admin', 'Изменён статус пользователя', '2026-05-25 01:11:15'),
(25, 'admin', 'Добавлен пользователь', '2026-05-25 01:12:50'),
(26, 'blocked people', 'Вход в систему', '2026-05-25 01:13:02'),
(27, 'admin', 'Вход в систему', '2026-05-25 01:13:20'),
(28, 'admin', 'Изменён статус пользователя', '2026-05-25 01:13:27'),
(29, 'admin', 'Вход в систему', '2026-05-25 01:14:45'),
(30, 'viewer', 'Вход в систему', '2026-05-25 01:22:16'),
(31, 'admin', 'Вход в систему', '2026-05-25 01:22:36'),
(32, 'admin', 'Добавлен врач', '2026-05-25 01:40:23'),
(33, 'admin', 'Изменены данные врача', '2026-05-25 01:40:31'),
(34, 'admin', 'Удалён врач', '2026-05-25 01:40:39');

-- --------------------------------------------------------

--
-- Структура таблицы `appointments`
--

CREATE TABLE `appointments` (
  `id` int(11) NOT NULL,
  `doctor_id` int(11) DEFAULT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `appointment_date` date DEFAULT NULL,
  `appointment_time` time DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `appointments`
--

INSERT INTO `appointments` (`id`, `doctor_id`, `patient_id`, `appointment_date`, `appointment_time`, `status`) VALUES
(1, 3, 2, '2026-05-12', '15:30:00', 'Запланирована'),
(2, 1, 1, '2026-06-01', '10:00:00', 'Запланирована'),
(3, 2, 2, '2026-06-01', '11:00:00', 'Завершена'),
(4, 3, 3, '2026-06-02', '09:30:00', 'Запланирована'),
(5, 4, 4, '2026-06-02', '14:00:00', 'Отменена'),
(6, 5, 5, '2026-06-03', '13:00:00', 'Запланирована'),
(7, 6, 6, '2026-06-03', '15:30:00', 'Завершена'),
(8, 7, 7, '2026-06-04', '12:00:00', 'Запланирована'),
(9, 8, 8, '2026-06-04', '16:00:00', 'Запланирована');

-- --------------------------------------------------------

--
-- Структура таблицы `doctors`
--

CREATE TABLE `doctors` (
  `id` int(11) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `specialization` varchar(255) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `doctors`
--

INSERT INTO `doctors` (`id`, `full_name`, `specialization`, `phone`, `email`) VALUES
(3, 'Владимир Пономарёв', 'Хирург', '235487', 'ponomorev@gmail.com'),
(4, 'Иван Петров', 'Терапевт', '+79990000001', 'petrov@clinic.ru'),
(5, 'Анна Смирнова', 'Кардиолог', '+79990000002', 'smirnova@clinic.ru'),
(6, 'Дмитрий Волков', 'Хирург', '+79990000003', 'volkov@clinic.ru'),
(7, 'Екатерина Орлова', 'Невролог', '+79990000004', 'orlova@clinic.ru'),
(8, 'Максим Соколов', 'Офтальмолог', '+79990000005', 'sokolov@clinic.ru'),
(9, 'Мария Кузнецова', 'Педиатр', '+79990000006', 'kuznetsova@clinic.ru'),
(13, 'Иван Петров', 'Терапевт', '+79990000001', 'petrov@clinic.ru'),
(14, 'Анна Смирнова', 'Кардиолог', '+79990000002', 'smirnova@clinic.ru'),
(16, 'Иван Петров', 'Терапевт', '+79990000001', 'petrov@clinic.ru'),
(17, 'Анна Смирнова', 'Кардиолог', '+79990000002', 'smirnova@clinic.ru'),
(18, 'Дмитрий Волков', 'Хирург', '+79990000003', 'volkov@clinic.ru'),
(19, 'Екатерина Орлова', 'Невролог', '+79990000004', 'orlova@clinic.ru'),
(20, 'Максим Соколов', 'Офтальмолог', '+79990000005', 'sokolov@clinic.ru'),
(21, 'Мария Кузнецова', 'Педиатр', '+79990000006', 'kuznetsova@clinic.ru'),
(22, 'Алексей Морозов', 'Стоматолог', '+79990000007', 'morozov@clinic.ru'),
(23, 'Ольга Фёдорова', 'Дерматолог', '+79990000008', 'fedorova@clinic.ru');

-- --------------------------------------------------------

--
-- Структура таблицы `patients`
--

CREATE TABLE `patients` (
  `id` int(11) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `address` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `patients`
--

INSERT INTO `patients` (`id`, `full_name`, `birth_date`, `phone`, `address`) VALUES
(1, 'Александр Иванов', '1998-04-12', '+79991111111', 'Москва'),
(2, 'Мария Петрова', '2001-08-25', '+79991111112', 'Санкт-Петербург'),
(3, 'Никита Сидоров', '1995-02-10', '+79991111113', 'Казань'),
(4, 'Елена Козлова', '1989-11-30', '+79991111114', 'Новосибирск'),
(5, 'Владимир Павлов', '1992-07-15', '+79991111115', 'Екатеринбург'),
(6, 'Татьяна Васильева', '2000-01-20', '+79991111116', 'Самара'),
(7, 'Сергей Михайлов', '1997-06-05', '+79991111117', 'Краснодар'),
(8, 'Алина Романова', '2003-09-18', '+79991111118', 'Тюмень'),
(9, 'Павел Андреев', '1985-03-22', '+79991111119', 'Воронеж'),
(10, 'Юлия Николаева', '1999-12-01', '+79991111120', 'Пермь'),
(11, 'Лунин Георгий', '2001-07-11', '2365890', 'Елец'),
(12, 'Александр Иванов', '1998-04-12', '+79991111111', 'Москва'),
(13, 'Мария Петрова', '2001-08-25', '+79991111112', 'Санкт-Петербург'),
(14, 'Александр Иванов', '1998-04-12', '+79991111111', 'Москва'),
(15, 'Мария Петрова', '2001-08-25', '+79991111112', 'Санкт-Петербург'),
(16, 'Никита Сидоров', '1995-02-10', '+79991111113', 'Казань'),
(17, 'Елена Козлова', '1989-11-30', '+79991111114', 'Новосибирск'),
(18, 'Владимир Павлов', '1992-07-15', '+79991111115', 'Екатеринбург'),
(19, 'Татьяна Васильева', '2000-01-20', '+79991111116', 'Самара'),
(20, 'Сергей Михайлов', '1997-06-05', '+79991111117', 'Краснодар'),
(21, 'Алина Романова', '2003-09-18', '+79991111118', 'Тюмень'),
(22, 'Павел Андреев', '1985-03-22', '+79991111119', 'Воронеж'),
(23, 'Юлия Николаева', '1999-12-01', '+79991111120', 'Пермь');

-- --------------------------------------------------------

--
-- Структура таблицы `services`
--

CREATE TABLE `services` (
  `id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `services`
--

INSERT INTO `services` (`id`, `title`, `price`, `description`) VALUES
(2, 'Консультация терапевта', 1400.00, 'Первичный приём врача'),
(3, 'ЭКГ', 2500.00, 'Диагностика сердца'),
(4, 'Консультация терапевта', 1500.00, 'Первичный приём врача'),
(5, 'Консультация кардиолога', 2500.00, 'Осмотр и диагностика сердца'),
(6, 'ЭКГ', 1800.00, 'Электрокардиография'),
(7, 'УЗИ брюшной полости', 3200.00, 'Ультразвуковое исследование'),
(8, 'Стоматологический осмотр', 1200.00, 'Профилактический осмотр'),
(9, 'Общий анализ крови', 900.00, 'Лабораторный анализ'),
(10, 'МРТ головного мозга', 8500.00, 'Магнитно-резонансная томография'),
(11, 'Приём невролога', 2700.00, 'Консультация невролога');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`, `status`) VALUES
(1, 'admin', 'ClinicAdmin2026!', 'admin', 'active'),
(2, 'manager', 'manager123', 'manager', 'active'),
(3, 'viewer', 'viewer123', 'viewer', 'active'),
(4, 'blocked people', 'block123456789', 'viewer', 'blocked'),
(5, 'admin2', 'admin123', 'admin', 'active'),
(6, 'manager2', 'manager123', 'manager', 'active'),
(7, 'viewer2', 'viewer123', 'viewer', 'active'),
(8, 'blocked_user', 'test123', 'viewer', 'blocked');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `activity_logs`
--
ALTER TABLE `activity_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT для таблицы `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT для таблицы `doctors`
--
ALTER TABLE `doctors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT для таблицы `patients`
--
ALTER TABLE `patients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT для таблицы `services`
--
ALTER TABLE `services`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
