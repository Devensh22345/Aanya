import asyncio
from info import *
from utils import *
from time import time
from client import User
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from rapidfuzz import fuzz

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

        query = message.text.lower()

        best_match = None
        best_score = 0

        for channel in channels:
            async for msg in User.search_messages(chat_id=channel, query=query):
                if not msg.text:
                    continue
                title = msg.text.lower()
                score = fuzz.partial_ratio(query, title)

                if score > best_score:
                    best_score = score
                    best_match = msg

                if best_score >= 80:  # not too strict
                    break

            if best_score >= 80:
                break

        if best_match:
            copied = await bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=best_match.chat.id,
                message_id=best_match.id
            )
            asyncio.create_task(delete_after_delay(bot, message.chat.id, copied.id))
        else:
            pass  # no match found, no reply

    except Exception as e:
        print(f"Error in search function: {e}")

async def delete_after_delay(bot, chat_id, message_id):
    try:
        await asyncio.sleep(600)  # 10 minutes
        await bot.delete_messages(chat_id, message_id)
    except Exception as e:
        print(f"Failed to delete message: {e}")
