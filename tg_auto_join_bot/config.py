import os

# Telegram API credentials from my.telegram.org
API_ID = int(os.getenv("API_ID", "1234567"))
API_HASH = os.getenv("API_HASH", "your_api_hash_here")

# Bot token from @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")

# Owner Telegram User ID (Numbers only)
OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))

# Database path
DATABASE_PATH = "bot.db"
