""" Telegram bot integration module to send this app's output straight to your Telegram chat. """

import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()

async def _send_message_async(message: str) -> None:
    """Internal async function to send message."""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("Error: Telegram credentials not found in environment variables")
        return
    
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

def send_telegram_message(message: str) -> None:
    """Send a message to Telegram using the configured bot.
    
    Args:
        message: The text message to send to Telegram
    """
    try:
        asyncio.run(_send_message_async(message))
        print("✓ Message sent to Telegram successfully")
    except TelegramError as e:
        print(f"Telegram API error: {str(e)}")
    except Exception as e:
        print(f"Error sending message to Telegram: {str(e)}")

