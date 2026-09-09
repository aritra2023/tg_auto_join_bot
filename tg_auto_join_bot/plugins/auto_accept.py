from pyrogram import Client
from pyrogram.types import ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton
from utils.font import to_small_caps
from database.db import add_user, get_fsub_channel

@Client.on_chat_join_request()
async def accept_join_request(client: Client, req: ChatJoinRequest):
    await req.approve()
    await add_user(req.from_user.id)
    chat_title = req.chat.title or "Channel"
    first_name = req.from_user.first_name
    _, fsub_link = await get_fsub_channel()
    channel_link = fsub_link if fsub_link else f"https://t.me/{req.chat.username}" if req.chat.username else "https://t.me/"
    me = await client.get_me()
    
    text = (
        f"{to_small_caps('Welcome')}, {first_name.upper()}!\n\n"
        f"{to_small_caps('Your Respected Request Of Joining')} {chat_title} 🦋✨ {to_small_caps('Has Been Already Accepted')}.\n\n"
        f"☑️ {to_small_caps('Tap Button Below To Check I\'m Alive Or Not')}."
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"⏱ {to_small_caps('Visit Channel')}", url=channel_link)],
        [InlineKeyboardButton(f"🧑‍💼 {to_small_caps('Check I\'m Alive Or Not')}", url=f"https://t.me/{me.username}?start=start")]
    ])
    try:
        await client.send_message(chat_id=req.from_user.id, text=text, reply_markup=buttons, disable_web_page_preview=True)
    except Exception:
        pass
