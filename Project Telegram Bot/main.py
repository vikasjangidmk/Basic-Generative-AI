import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import openai
import sys

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

openai.api_key = openai_api_key

class Reference:
    """
    A class to store the conversation history from the OpenAI API.
    """
    def __init__(self):
        self.history = []

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

    def get_history(self):
        return self.history


reference = Reference()
model_name = "gpt-3.5-turbo"
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

def clear_past():
    """
    A function to clear the past conversation and context.
    """
    reference.history.clear()

@dp.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    This handler clears the past conversation and context.
    """
    clear_past()
    await message.reply("Past conversation and context have been cleared.")

@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    """
    This handler receives messages with the '/start' command
    """
    await message.reply("Hi! I'm Echo Bot!\nPowered by Vikas. How can I assist you?")

@dp.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    This handler displays the help menu.
    """
    help_command = """
    Hi there, I'm a Telegram bot created by Vikas! Please follow these commands:
    /start - To start the conversation.
    /clear - To clear the past conversation and context.
    /help - To get the help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)

@dp.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the ChatGPT API.
    """
    logger.info(f"User: {message.text}")
    
    # Add user message to the conversation history
    reference.add_message("user", message.text)

    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=reference.get_history()  # Pass the entire conversation history
        )

        bot_response = response.choices[0].message['content']
        logger.info(f"ChatGPT: {bot_response}")

        # Add assistant response to the conversation history
        reference.add_message("assistant", bot_response)

        await bot.send_message(chat_id=message.chat.id, text=bot_response)

    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        await bot.send_message(chat_id=message.chat.id, text="Sorry, I couldn't process your request. Please try again later.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
