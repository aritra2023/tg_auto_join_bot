from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.font import to_small_caps
from database.db import add_user

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await add_user(message.from_user.id)
    first_name = message.from_user.first_name
    me = await client.get_me()
    text = (
        f"> **{to_small_caps('Hello')}, {first_name.upper()} \" \"**\n\n"
        f"🤖 {to_small_caps('Welcome To Auto Request Accept Bot')}!\n\n"
        f"{to_small_caps('This Bot Automatically Accepts All Join Request From Your Channel Or Group')}.\n\n"
        f"{to_small_caps('Just Add Me To Your Group Or Channel And Make It Admin With Full Rights')}."
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"➕ {to_small_caps('Add Me To Your Group')}", url=f"https://t.me/{me.username}?startgroup=true")],
        [InlineKeyboardButton(f"➕ {to_small_caps('Add Me To Your Channel')}", url=f"https://t.me/{me.username}?startchannel=true")]
    ])
    await message.reply_text(text=text, reply_markup=buttons, disable_web_page_preview=True)
