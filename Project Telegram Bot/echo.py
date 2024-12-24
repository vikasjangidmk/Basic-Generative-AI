import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def Command_start(message: types.Message):
    """
    This handler receives messages with '/start' or '/help' command
    """
    await message.reply("Hii\nI'm Echo Bot!\nPowered by Vikas.")
    
@dp.message_handler()
async def echo_message(message: types.Message):
    """
    This will return echo
    """
    await message.answer(message.text)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)