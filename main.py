import logging
import re
import asyncio
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

def external_links(phone_number: str):
    phone = phone_number.strip().replace("+", "")
    links = []

    # OLX
    links.append(f"🔍 OLX: https://www.olx.ua/list/q-{phone}/")

    # Facebook
    links.append(f"🔍 Facebook: https://www.facebook.com/search/top?q={phone}")

    # Google
    links.append(f"🔍 Google: https://www.google.com/search?q=\"{phone}\"")

    # GetContact (через web)
    links.append(f"🔍 GetContact (web): https://www.getcontact.com/search?phone={phone}")

    # Nomerogram (база звонков)
    links.append(f"🔍 Nomerogram: https://nomerogram.com/number/{phone}")

    # Telegram (поиск)
    links.append(f"🔍 Telegram Search: tg://search?query={phone}")

    return links

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("👋 Привет! Отправь номер телефона для проверки.")

@dp.message()
async def check_phone(message: Message):
    phone_raw = message.text.strip()
    phone = normalize_phone(phone_raw)
    await message.answer(f"🔍 Проверяю номер: <b>{phone}</b>")

    links = external_links(phone)
    result = "<b>🔗 Найденные источники:</b>\n\n" + "\n".join(links)
    await message.answer(result)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
