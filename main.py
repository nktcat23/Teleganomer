# Teleganomer
import logging
import re
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Text
from aiogram.types import Message
import requests
from bs4 import BeautifulSoup

API_TOKEN = "8149882262:AAEMCuzHHgyqpyWpgH7jmYR3jC6tCG9y4_g"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Простая нормализация номера
def normalize_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("0"):
        digits = "380" + digits[1:]
    if not digits.startswith("380"):
        digits = "380" + digits
    return "+" + digits

# Поиск в Google (только пример, без API)
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

@dp.message(commands=["start"])
async def cmd_start(message: Message):
    await message.answer("Привет! Отправь номер телефона для проверки.")

@dp.message()
async def phone_check(message: Message):
    phone_raw = message.text.strip()
    phone = normalize_phone(phone_raw)
    await message.answer(f"Проверяю номер: {phone}\nИщу в открытых источниках...")

    # Поиск ссылок в Google (простой пример)
    links = google_search_links(f'"{phone}"')

    if not links:
        await message.answer("Не найдено упоминаний по номеру.")
        return

    text = "Вот первые найденные ссылки:\n" + "\n".join(links)
    await message.answer(text)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
