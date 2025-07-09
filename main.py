import logging
import re
import asyncio
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode

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

def get_nomerogram_data(phone: str):
    url = f"https://nomerogram.com/number/{phone}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        h1 = soup.find("h1")
        name = h1.text.strip() if h1 else "Не найдено"
        bad_keywords = ["мошенник", "спам", "обман", "лохотрон"]
        comments = soup.find_all("div", class_="comment")
        complaint_count = sum(1 for c in comments if any(k in c.text.lower() for k in bad_keywords))
        return {"name": name, "complaints": complaint_count}
    except:
        return {"name": "Ошибка", "complaints": -1}

def get_olx_data(phone: str):
    url = f"https://www.olx.ua/list/q-{phone}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        titles = soup.select("div[data-cy='l-card'] h6")
        return titles[0].text.strip() if titles else None
    except:
        return None

def get_getcontact_web(phone: str):
    url = f"https://www.getcontact.com/search?phone={phone}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        return "Данные найдены" if "result" in r.text.lower() else "Не найдено"
    except:
        return "Ошибка"

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("👋 Привет! Отправь номер телефона для проверки.")

@dp.message()
async def check_phone(message: Message):
    raw = message.text.strip()
    phone = normalize_phone(raw)
    phone_plain = phone.replace("+", "")
    await message.answer(f"🔍 Проверяю номер: <b>{phone}</b>")

    nom = get_nomerogram_data(phone_plain)
    olx = get_olx_data(phone_plain)
    getc = get_getcontact_web(phone_plain)

    result = f"<b>📊 Результаты по номеру {phone}</b>\n\n"

    result += f"👤 Имя (nomerogram): {nom['name']}\n"
    if nom["complaints"] > 0:
        result += f"⚠️ Жалоб: {nom['complaints']}\n"
    elif nom["complaints"] == 0:
        result += f"✅ Жалоб не найдено\n"
    else:
        result += f"⚠️ Не удалось получить жалобы\n"

    result += f"📬 GetContact Web: {getc}\n"
    result += f"📦 OLX: {'Объявление найдено: ' + olx if olx else 'Нет объявлений'}"

    await message.answer(result)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())