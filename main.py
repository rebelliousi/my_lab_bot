import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    # Bot başlarken dosyaları otomatik yükler
    async def setup_hook(self):
        # cogs klasöründeki genel.py dosyasını yükle
        await self.load_extension("cogs.genel")
        print("Cogs yüklendi!")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı.")

bot.run(os.getenv("BOT_TOKEN"))