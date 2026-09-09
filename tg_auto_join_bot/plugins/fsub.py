from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_ID
from database.db import set_fsub_channel, remove_fsub_channel, get_fsub_channel
from utils.font import to_small_caps

@Client.on_message(filters.command("setchannel") & filters.user(OWNER_ID))
async def set_channel_cmd(client: Client, message: Message):
    args = message.text.split()
    if len(args) < 3:
        await message.reply_text(f"⚠️ **Usage:** `/setchannel <channel_id> <invite_link>`")
        return
    try:
        channel_id = int(args[1])
        invite_link = args[2]
        await set_fsub_channel(channel_id, invite_link)
        await message.reply_text(f"✅ {to_small_caps('Force channel configured successfully')}!")
    except ValueError:
        await message.reply_text("❌ Invalid Channel ID.")

@Client.on_message(filters.command("removechannel") & filters.user(OWNER_ID))
async def remove_channel_cmd(client: Client, message: Message):
    await remove_fsub_channel()
    await message.reply_text(f"🗑️ {to_small_caps('Force channel removed successfully')}!")
