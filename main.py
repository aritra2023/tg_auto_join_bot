import asyncio
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from database.db import init_db

app = Client("auto_accept_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins=dict(root="plugins"))

async def main():
    await init_db()
    await app.start()
    me = await app.get_me()
    print(f"@{me.username} successfully live hai!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
