import logging
import re
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
import requests
from bs4 import BeautifulSoup

API_TOKEN = "8149882262:AAEMCuzHHgyqpyWpgH7jmYR3jC6tCG9y4_g"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Нормализация номера телефона
def normalize_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("0"):
        digits = "380" + digits[1:]
    if not digits.startswith("380"):
        digits = "380" + digits
    return "+" + digits

# Поиск ссылок через Google (пример)
def google_search_links(query: str):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for g in soup.find_all('a'):
        href = g.get('href')
        if href and href.startswith('http'):
            results.append(href)
        if len(results) >= 5:
            break
    return results

# Обработка команды /start
@dp.message(commands=["start"])
async def start_handler(message: Message):
    await message.answer("Привет! Отправь номер телефона для проверки.")

# Обработка всех остальных сообщений
@dp.message()
async def phone_check_handler(message: Message):
    phone_raw = message.text.strip()
    phone = normalize_phone(phone_raw)
    await message.answer(f"Проверяю номер: <b>{phone}</b>\nИщу в открытых источниках...")

    links = google_search_links(f'"{phone}"')

    if not links:
        await message.answer("Не найдено упоминаний по номеру.")
        return

    text = "<b>Вот найденные ссылки:</b>\n" + "\n".join(links)
    await message.answer(text)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
