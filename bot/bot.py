import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from decouple import config

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
API_TOKEN = config('TELEGRAM_BOT_TOKEN', default='YOUR_BOT_TOKEN_HERE')
MINI_APP_URL = config('MINI_APP_URL', default='https://your-domain.com') # Replace with actual URL

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    args = message.get_args()
    if args.startswith('driver_'):
        profile_id = args.split('_')[1]
        
        # Django ORM orqali ma'lumotni olish (sync_to_async kerak bo'lishi mumkin)
        # profile = await get_profile_from_db(profile_id)
        
        # MarkdownV2 yoki HTML formatida profilga havola yuborish
        # Bu yerda tg://user?id= orqali profilga o'tiladi
        text = f"Haydovchi profili: [Profilni ko'rish](tg://user?id={profile_id})"
        
        await message.answer(text, parse_mode="MarkdownV2")
        return

    markup = InlineKeyboardMarkup()
    # Adding a button that opens the Mini App
    webapp_button = InlineKeyboardButton(
        text="Open Mini App",
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    markup.add(webapp_button)
    
    await message.reply(
        f"Welcome! Click the button below to open the Mini App.",
        reply_markup=markup
    )    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
