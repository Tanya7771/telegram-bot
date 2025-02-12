import openai
import requests
import aiosqlite
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import executor

# 🔑 Токены для API
API_TOKEN = "7836824191:AAFQzh2w3cLrwsoP0WxRfsfAd1g7VbIIW-s"
OPENAI_API_KEY = "Isk-proj-VVVxu5QtZI-YM8Bx6EL2qYngH_vUMZ5Sme-7N0mNoRgntQQL5sMPDcc-eWmqa7-OG2tucNqIkQT3BlbkFJfmamxDtFoUus8MJRBQ2Mrjeg6GelmQdhVmsghqDF2-G30b8j8bGomRGORNNJVXpuPieYvUwQ4A"

# 🤖 Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

# 🎯 Фильтр: какие темы бот поддерживает?
ALLOWED_TOPICS = {
    "post_ideas": "Напиши свой вопрос в формате: \"Напиши мне идеи для постов [какие]\". ВАЖНО! Ответ будет зависеть от точности запроса. Уточни цель задачи, стиль, длину и примеры. Чем детальнее запрос, тем точнее ответ",
    "video_scenarios": "Напиши свой вопрос в формате: \"Напиши мне сценарии для видео [какому]\". ВАЖНО! Ответ будет зависеть от точности запроса. Укажи цель, стиль и примеры. Чем детальнее запрос, тем точнее ответ",
    "content_plan": "Напиши свой вопрос в формате: \"Напиши мне контент-план для [ваша ниша]\". ВАЖНО! Чем детальнее запрос, тем точнее ответ.",
    "headlines": "Напиши свой вопрос в формате: \"Напиши мне заголовки для [ваша ниша]\"  ВАЖНО! Укажи формат (например, продающие, инфопост). Чем детальнее запрос, тем точнее ответ",
    "audience_analysis": "Напиши свой вопрос в формате: \"Сделай мне анализ аудитории для [ваша ниша]\  ВАЖНО! Чем детальнее запрос, тем точнее ответ. Опишите её подробно.",
    "seo_tips": "Напиши свой вопрос в формате: \"Как мне настроить или улучшить SEO-оптимизацию для [ваша ниша]. ВАЖНО! Чем детальнее запрос, тем точнее ответ(например, ключевые слова, оптимизация сайта).",
    "visual_ideas": "Напиши свой вопрос в формате: \"Напиши мне идеи для визуала для [ваша ниша] ВАЖНО! Чем детальнее запрос, тем точнее ответ (например, минимализм, яркие цвета).",
    "storytelling": "Напиши свой вопрос в формате: \"Напиши мне идеи сторитейллинга для [ваша ниша] ВАЖНО!  Уточните тематику и цель. Чем детальнее запрос, тем точнее ответ",
    "generate_text": "Напиши свой вопрос в формате: \"Напиши мне текст для [ваша ниша] ВАЖНО! Чем детальнее запрос, тем точнее ответ (например, пост, статья)."
}
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
    InlineKeyboardButton("🎯 Заголовки", callback_data="headlines"),
    InlineKeyboardButton("📊 Анализ аудитории", callback_data="audience_analysis"),
    InlineKeyboardButton("📈 SEO-оптимизация", callback_data="seo_tips"),
    InlineKeyboardButton("📷 Идеи для визуала", callback_data="visual_ideas"),
    InlineKeyboardButton("📖 Сторителлинг", callback_data="storytelling"),
    InlineKeyboardButton("🤖 Генерация текста", callback_data="generate_text")
)

# 🚀 Генерация контента с GPT-4 (по SMM)
async def generate_ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка при генерации текста: {str(e)}"

# 🎉 Приветствие
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    print(f"Бот получил команду /start от {message.from_user.username}")
    await save_user(message.from_user.id, message.from_user.username)
    welcome_text = """
👋 Привет! Я – SocialMind AI.
SMM-помощник для бизнеса, контента и идей.

Что я умею:
🔹 Генерирую идеи для постов и Stories
🔹 Пишу сценарии для Reels, TikTok и YouTube
🔹 Создаю контент-планы для любой ниши
🔹 Разрабатываю цепляющие заголовки и лид-магниты
🔹 Помогаю с маркетинговыми воронками и сторителлингом
🔹 Анализирую аудиторию и тренды
🔹 Делаю SEO-оптимизацию и подбираю ключевые слова

Выберите нужную функцию в меню или напишите, чем я могу помочь!
    """
    await message.answer(welcome_text, reply_markup=menu_inline)

# 📝 Обработка кнопок меню
@dp.callback_query_handler(lambda call: call.data in ALLOWED_TOPICS)
async def ask_user_input(call: types.CallbackQuery):
    question = ALLOWED_TOPICS[call.data]
    await call.message.answer(f"{question} Напишите свой вопрос.")
    dp.register_message_handler(handle_user_response, state=call.data)

# 📥 Обработка ответов пользователей
async def handle_user_response(message: types.Message):
    response = await generate_ai_response(f"Ответь по теме {message.text}")
    await message.answer(response)

# ✍️ Генерация текста
@dp.message_handler(lambda message: message.reply_to_message and "Введи тему" in message.reply_to_message.text)
async def process_generate_text(message: types.Message):
    prompt = f"Напиши текст для поста на тему: {message.text}"
    response = await generate_ai_response(prompt)
    await message.answer(response)

# 🧠 AI-ответ на вопросы пользователей
@dp.message_handler(lambda message: message.text.lower() in ALLOWED_TOPICS)
async def handle_user_message(message: types.Message):
    topic = [key for key in ALLOWED_TOPICS if key.lower() in message.text.lower()]
    if topic:
        # Переписываем тут логику для обработки запроса по найденной теме
        response = await generate_ai_response(f"Ответь как SMM-эксперт на запрос по теме {topic[0]}: {message.text}")
        await message.answer(response)
    else:
        await message.answer("💬 Уточните ваш вопрос по теме SMM, контента или маркетинга.")

# 🎯 Запуск бота
if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    executor.start_polling(dp, skip_updates=True)
