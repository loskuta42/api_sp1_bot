import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv


load_dotenv()

PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
STATUSES = {
    'approved': ('Ревьюеру всё понравилось, '
                 'можно приступать к следующему уроку.'),
    'rejected': 'К сожалению в работе нашлись ошибки.',
    'reviewing': 'Работа взята в ревью.'
}


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    if homework.get('status') in STATUSES:
        key = homework.get('status')
        verdict = STATUSES.get(key)
        return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'
    else:
        logging.error('Неизвестный статус работы')
        return f'Неизвестный статус работы'


def get_homework_statuses(current_timestamp):
    from_date = current_timestamp
    url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
    try:
        homework_statuses = requests.get(
            url,
            params={'from_date': from_date},
            headers={'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
        )
        return homework_statuses.json()
    except requests.exceptions.RequestException as e:
        logging.error(f'Ошибка запроса страницы {url}')
        raise SystemExit(e)


def send_message(message, bot_client):
    return bot_client.send_message(CHAT_ID, message)


def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    logging.debug('Бот инициализизован.')
    current_timestamp = int(time.time())
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                if new_homework.get('homeworks') is not None and\
                        new_homework.get('homeworks')[0]:
                    send_message(parse_homework_status(
                        new_homework.get('homeworks')[0]),
                        bot
                    )
            current_timestamp = new_homework.get(
                'current_date',
                current_timestamp
            )
            time.sleep(300)
            logging.info('Бот отправил сообщение.')
        except Exception as e:
            logging.error(f'Бот столкнулся с ошибкой: {e}')
            send_message(f'Бот столкнулся с ошибкой: {e}', bot)
            time.sleep(5)


if __name__ == '__main__':
    main()
