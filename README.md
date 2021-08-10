# api_sp1_bot - Бот-ассистент, проверяет готовность домашней работы по Яндекс.Практикуму.

Стек: Python, python-telegram-bot, Telegram Bot API.

Телеграм-бот, который:
  - обращается к API сервиса Практикум.Домашка;
  - узнает, взята ли ваша домашка в ревью, проверена ли она, провалена или принята;
  - отправляет результат в ваш Телеграм-чат.

Бот регулярно опрашивает API домашки и при получении обновлений парсит ответ и отправлять сообщение в ваш аккаунт Телеграм.

Бот логирует момент своего запуска (уровень DEBUG) и каждую отправку сообщения (уровень INFO). Сообщения уровня ERROR бот логирует и (дополнительно) отправлять Вам в Телеграм. опрос проводиться раз в 5 минут.

Используется библиотека для написания telegram-ботов python-telegram-bot.

