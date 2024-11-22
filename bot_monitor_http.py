#!/usr/bin/env python3

import asyncio
import requests
from telegram import Bot

# Параметры
TELEGRAM_TOKEN = "ВАШ_ТОКЕН"
CHAT_ID = "ВАШ_ЧАТ_id"
IP_ADDRESS = "IP_URL_ДЛЯ_МОНИТОРИНГА"
CHECK_INTERVAL = 60  # Интервал проверки доступности (в секундах)
NOTIFY_INTERVAL = 300  # Интервал повторных уведомлений о недоступности (в секундах)


async def is_ip_reachable(ip):
    """Проверяет доступность IP-адреса."""
    try:
        response = requests.get(f"http://{ip}", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


async def notify(bot, chat_id, message):
    """Отправляет сообщение в Telegram."""
    await bot.send_message(chat_id=chat_id, text=message)


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    ip_unreachable = False
    last_notify_time = 0

    while True:
        if await is_ip_reachable(IP_ADDRESS):
            if ip_unreachable:  # Если IP стал доступен, уведомить
                await notify(bot, CHAT_ID, f"IP {IP_ADDRESS} снова доступен.")
                ip_unreachable = False
        else:
            current_time = asyncio.get_event_loop().time()
            if not ip_unreachable or (current_time - last_notify_time >= NOTIFY_INTERVAL):
                await notify(bot, CHAT_ID, f"ВНИМАНИЕ: IP {IP_ADDRESS} недоступен!")
                ip_unreachable = True
                last_notify_time = current_time

        await asyncio.sleep(CHECK_INTERVAL)


# Запуск
if __name__ == "__main__":
    asyncio.run(main())
