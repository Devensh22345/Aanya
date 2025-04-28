import asyncio
from info import *
from utils import *
from time import time
from client import User
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.text & filters.group & filters.incoming & ~filters.command(["verify", "connect", "id"]))
async def search(bot, message):
    try:
        if await force_sub(bot, message) == False:
            return

        group_data = await get_group(message.chat.id)
        channels = group_data.get("channels", [])
        if not channels:
            return

        if message.text.startswith("/"):
            return

        query = message.text

        for channel in channels:
            async for msg in User.search_messages(chat_id=channel, query=query):
                copied = await bot.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=msg.chat.id,
                    message_id=msg.id
                )
                # Wait 10 minutes and delete the copied message
                asyncio.create_task(delete_after_delay(bot, message.chat.id, copied.id))
                break  # Only forward/copy the first matching message
    except Exception as e:
        print(f"Error in search function: {e}")

async def delete_after_delay(bot, chat_id, message_id):
    try:
        await asyncio.sleep(60)  # 10 minutes
        await bot.delete_messages(chat_id, message_id)
    except Exception as e:
        print(f"Failed to delete message: {e}")
