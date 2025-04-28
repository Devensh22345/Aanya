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
        # Check force subscribe
        if await force_sub(bot, message) == False:
            return

        # Get associated channels for this group
        group_data = await get_group(message.chat.id)
        channels = group_data.get("channels", [])
        if not channels:
            return

        # Ignore commands
        if message.text.startswith("/"):
            return

        query = message.text

        # Search and copy the first matching message
        for channel in channels:
            async for msg in User.search_messages(chat_id=channel, query=query):
                await bot.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=msg.chat.id,
                    message_id=msg.id
                )
                break  # Forward only the first match per query
    except Exception as e:
        print(f"Error in search function: {e}")
