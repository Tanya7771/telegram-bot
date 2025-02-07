import openai
import requests
import aiosqlite
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import executor

# 🔑 Токены для API
API_TOKEN = "7946096138:AAEXkWbDiyaaxwbB8dGS-Fwjh4Do0j83BXY"
OPENAI_API_KEY = "ВАШ_КЛЮЧ_OPENAIsk-proj-VVVxu5QtZI-YM8Bx6EL2qYngH_vUMZ5Sme-7N0mNoRgntQQL5sMPDcc-eWmqa7-OG2tucNqIkQT3BlbkFJfmamxDtFoUus8MJRBQ2Mrjeg6GelmQdhVmsghqDF2-G30b8j8bGomRGORNNJVXpuPieYvUwQ4A"

# 🤖 Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

# 🎯 Фильтр: какие темы бот поддерживает?
ALLOWED_TOPICS = [
    "SMM", "контент", "соцсети", "Instagram", "TikTok", "YouTube",
    "маркетинг", "реклама", "вовлечение", "аудитория", "таргетинг",
    "SEO", "визуал", "посты", "Stories", "Reels", "сторителлинг"
]

# 🗄 Функция для работы с базой данных
async def init_db():
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT
        )""")
        await db.commit()

# 💾 Сохранение пользователя в базу
async def save_user(user_id, username):
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)", (user_id, username))
        await db.commit()

# 🎭 Inline-кнопки меню
menu_inline = InlineKeyboardMarkup(row_width=2)
menu_inline.add(
    InlineKeyboardButton("📌 Идеи для постов", callback_data="post_ideas"),
    InlineKeyboardButton("🎬 Сценарии для видео", callback_data="video_scenarios"),
    InlineKeyboardButton("📝 Контент-план", callback_data="content_plan"),
    InlineKeyboardButton("🎯 Заголовки и лид-магниты", callback_data="headlines"),
    InlineKeyboardButton("📊 Анализ аудитории", callback_data="audience_analysis"),
    InlineKeyboardButton("📈 SEO-оптимизация", callback_data="seo_tips"),
    InlineKeyboardButton("📷 Идеи для визуала", callback_data="visual_ideas"),
    InlineKeyboardButton("📖 Маркетинг и сторителлинг", callback_data="storytelling"),
    InlineKeyboardButton("🤖 Генерация текста", callback_data="generate_text")
)

# 🚀 Генерация контента с GPT-4 (только по SMM)
async def generate_ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return "Ошибка при генерации текста."

# 🎉 Приветствие
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await save_user(message.from_user.id, message.from_user.username)
    welcome_text = """
👋 Привет! Я – SocialMind AI.
Я помогу тебе с контентом, маркетингом и продвижением в соцсетях.

Выбери категорию или задай мне вопрос по SMM!
    """
    await message.answer(welcome_text, reply_markup=menu_inline)

# 📝 Функции кнопок
@dp.callback_query_handler(lambda call: call.data == "post_ideas")
async def post_ideas(call: types.CallbackQuery):
    await call.message.answer("💡 Идеи для постов:\n1. История бренда\n2. Закулисье\n3. Полезный совет")

@dp.callback_query_handler(lambda call: call.data == "video_scenarios")
async def video_scenarios(call: types.CallbackQuery):
    await call.message.answer("🎥 Сценарии для видео:\n1. До/После\n2. Челленджи\n3. Реакции на тренды")

@dp.callback_query_handler(lambda call: call.data == "content_plan")
async def content_plan(call: types.CallbackQuery):
    await call.message.answer("📅 Контент-план:\n1. Пн: История бренда\n2. Вт: Полезный совет\n3. Ср: Разбор ошибки")

@dp.callback_query_handler(lambda call: call.data == "headlines")
async def headlines(call: types.CallbackQuery):
    await call.message.answer("⚡️ Заголовки:\n1. 'Ты не поверишь, но…'\n2. 'Как сделать X за 10 минут?'")

@dp.callback_query_handler(lambda call: call.data == "audience_analysis")
async def audience_analysis(call: types.CallbackQuery):
    await call.message.answer("📊 Анализ ЦА:\n1. Изучи комментарии клиентов\n2. Проведи опросы")

@dp.callback_query_handler(lambda call: call.data == "seo_tips")
async def seo_tips(call: types.CallbackQuery):
    await call.message.answer("🔎 SEO:\n1. Ключевые слова в описании\n2. Используй alt-теги")

@dp.callback_query_handler(lambda call: call.data == "visual_ideas")
async def visual_ideas(call: types.CallbackQuery):
    await call.message.answer("📷 Идеи для визуала:\n1. Минимализм\n2. Цветовые акценты\n3. Динамичные коллажи")

@dp.callback_query_handler(lambda call: call.data == "storytelling")
async def storytelling(call: types.CallbackQuery):
    await call.message.answer("📖 Сторителлинг:\n1. Герой + конфликт\n2. Проблема → решение")

# ✍️ Генерация текста
@dp.callback_query_handler(lambda call: call.data == "generate_text")
async def ask_generate_text(call: types.CallbackQuery):
    await call.message.answer("🔹 Введи тему для генерации контента:")

@dp.message_handler(lambda message: message.reply_to_message and "🔹 Введи тему" in message.reply_to_message.text)
async def process_generate_text(message: types.Message):
    prompt = f"Напиши текст для поста на тему: {message.text}"
    response = await generate_ai_response(prompt)
    await message.answer(response)

# 🧠 AI-ответ (только по теме SMM)
@dp.message_handler()
async def handle_user_message(message: types.Message):
    if any(topic.lower() in message.text.lower() for topic in ALLOWED_TOPICS):
        response = await generate_ai_response(f"Ответь как SMM-эксперт: {message.text}")
        await message.answer(response)
    else:
        await message.answer("❌ Я отвечаю только на вопросы, связанные с соцсетями, контентом и маркетингом!")

# 🎯 Запуск бота
if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    executor.start_polling(dp, skip_updates=True)
    
    
    
    
    
    
    
    API_TOKEN = "7836824191:AAFQzh2w3cLrwsoP0WxRfsfAd1g7VbIIW-s"
OPENAI_API_KEY = "Isk-proj-VVVxu5QtZI-YM8Bx6EL2qYngH_vUMZ5Sme-7N0mNoRgntQQL5sMPDcc-eWmqa7-OG2tucNqIkQT3BlbkFJfmamxDtFoUus8MJRBQ2Mrjeg6GelmQdhVmsghqDF2-G30b8j8bGomRGORNNJVXpuPieYvUwQ4A"