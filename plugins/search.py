import asyncio
from info import *
from utils import *
from client import User
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from rapidfuzz import fuzz

@Client.on_message(filters.text & filters.group & filters.incoming & ~filters.command(["verify", "connect", "id"]))
async def search(bot, message):
    try:
        if await force_sub(bot, message) == False:
            return

        if message.text.startswith("/"):
            return

        if len(message.text) < 2:  # Allow even small typo queries
            return

        group_data = await get_group(message.chat.id)
        channels = group_data.get("channels", [])
        if not channels:
            return

        query = message.text.lower()
        best_match = None
        best_score = 0

        for channel in channels:
            async for msg in User.search_messages(chat_id=channel, query=query):
                if not msg.text:
                    continue
                title = msg.text.lower()
                # Use token_sort_ratio for better handling of typos and word order variations
                score = fuzz.token_sort_ratio(query, title)

                if score > best_score:
                    best_score = score
                    best_match = msg

            # Keep searching all channels to find the absolute best match

        if best_match and best_score >= 40:  # If score is decent (even if not perfect)
            copied = await bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=best_match.chat.id,
                message_id=best_match.message_id
            )
            asyncio.create_task(delete_after_delay(bot, message.chat.id, copied.message_id))
        else:
            # Optional: Send a "Not Found" message
            await message.reply_text("No related post found. Please try again with different words.")

    except Exception as e:
        print(f"Error in search function: {e}")

async def delete_after_delay(bot, chat_id, message_id):
    try:
        await asyncio.sleep(600)
        await bot.delete_messages(chat_id, message_id)
    except Exception as e:
        print(f"Failed to delete message: {e}")
