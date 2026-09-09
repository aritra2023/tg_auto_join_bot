import aiosqlite
from config import DATABASE_PATH

async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
        await db.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
        await db.commit()

async def add_user(user_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def get_all_users():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("SELECT user_id FROM users")
        rows = await cursor.fetchall()
        return [row[0] for row in rows]

async def set_fsub_channel(channel_id: int, invite_link: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('fsub_id', ?)", (str(channel_id),))
        await db.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('fsub_link', ?)", (invite_link,))
        await db.commit()

async def remove_fsub_channel():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM settings WHERE key IN ('fsub_id', 'fsub_link')")
        await db.commit()

async def get_fsub_channel():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("SELECT key, value FROM settings WHERE key IN ('fsub_id', 'fsub_link')")
        rows = await cursor.fetchall()
        data = {row[0]: row[1] for row in rows}
        if "fsub_id" in data and "fsub_link" in data:
            return int(data["fsub_id"]), data["fsub_link"]
        return None, None
