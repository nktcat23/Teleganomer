import logging
import re
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
import requests
from bs4 import BeautifulSoup

API_TOKEN = "8149882262:AAEMCuzHHgyqpyWpgH7jmYR3jC6tCG9y4_g"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

def normalize_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("0"):
        digits = "380" + digits[1:]
    if not digits.startswith("380"):
        digits = "380" + digits
    return "+" + digits

def google_search_links(query: str):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=5)
    except Exception:
        return []
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for g in soup.find_all('a'):
        href = g.get('href')
        if href and href.startswith('http'):
            results.append(href)
        if len(results) >= 5:
            break
    return results

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("👋 Привет! Отправь номер телефона для проверки.")

@dp.message()
async def check_phone(message: Message):
    phone_raw = message.text.strip()
    phone = normalize_phone(phone_raw)
    await message.answer(f"🔍 Проверяю номер: <b>{phone}</b>")

    links = google_search_links(f'"{phone}"')
    if not links:
        await message.answer("❌ Ничего не найдено.")
    else:
        result = "<b>🔗 Найденные ссылки:</b>\n" + "\n".join(links)
        await message.answer(result)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
