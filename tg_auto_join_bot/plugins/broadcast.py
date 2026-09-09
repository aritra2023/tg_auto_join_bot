import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID
from database.db import get_all_users
from utils.font import to_small_caps

BROADCAST_STATE = {}

@Client.on_message(filters.command("cast") & filters.user(OWNER_ID))
async def cast_cmd(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("⚠️ Kripya kisi post ya message ko reply karke `/cast` command dein.")
        return
    BROADCAST_STATE[message.from_user.id] = {
        "message_id": message.reply_to_message.id,
        "from_chat_id": message.chat.id,
        "pin": False
    }
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"📌 {to_small_caps('Yes, Pin it')}", callback_data="cast_pin_yes"), InlineKeyboardButton(f"❌ {to_small_caps('No Pin')}", callback_data="cast_pin_no")],
        [InlineKeyboardButton(f"🚫 {to_small_caps('Cancel')}", callback_data="cast_cancel")]
    ])
    await message.reply_text(f"❓ **{to_small_caps('Broadcast Confirmation Step 1')}**\n\nKya aap broadcast message ko sabhi chats me **PIN** karna chahte hain?", reply_markup=buttons)

@Client.on_callback_query(filters.regex(r"^cast_pin_"))
async def cast_pin_callback(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id != OWNER_ID or user_id not in BROADCAST_STATE: return await callback.answer("Unauthorized!", show_alert=True)
    choice = callback.data.split("_")[-1]
    BROADCAST_STATE[user_id]["pin"] = (choice == "yes")
    pin_status = "HAAN (Pin Hoga)" if choice == "yes" else "NAHI (Normal)"
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🚀 {to_small_caps('Yes, Send Now')}", callback_data="cast_confirm_send")],
        [InlineKeyboardButton(f"❌ {to_small_caps('Cancel Broadcast')}", callback_data="cast_cancel")]
    ])
    await callback.message.edit_text(f"⚠️ **{to_small_caps('Final Confirmation Step 2')}**\n\n• **Pin Status:** `{pin_status}`\n\nKya aap broadcast start karna chahte hain?", reply_markup=buttons)

@Client.on_callback_query(filters.regex("cast_confirm_send"))
async def cast_execute(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id != OWNER_ID or user_id not in BROADCAST_STATE: return await callback.answer("Session expired!", show_alert=True)
    data = BROADCAST_STATE.pop(user_id)
    await callback.message.edit_text(f"⏳ {to_small_caps('Broadcast In Progress')}...")
    users = await get_all_users()
    successful, failed = 0, 0
    for uid in users:
        try:
            sent_msg = await client.copy_message(chat_id=uid, from_chat_id=data["from_chat_id"], message_id=data["message_id"])
            if data["pin"]:
                try: await sent_msg.pin(both_sides=True)
                except: pass
            successful += 1
            await asyncio.sleep(0.04)
        except: failed += 1
    await client.send_message(chat_id=OWNER_ID, text=f"✅ **{to_small_caps('Broadcast Completed')}**\n\n• **Total:** `{len(users)}`\n• **Success:** `{successful}`\n• **Failed:** `{failed}`")

@Client.on_callback_query(filters.regex("cast_cancel"))
async def cast_cancel(client: Client, callback: CallbackQuery):
    BROADCAST_STATE.pop(callback.from_user.id, None)
    await callback.message.edit_text(f"🚫 {to_small_caps('Broadcast Cancelled')}.")
