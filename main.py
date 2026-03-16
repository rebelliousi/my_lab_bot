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
          # cogs klasöründeki her dosyaya bak
       for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    print(f"✅ {filename} başarıyla yüklendi.")
                except Exception as e:
                    print(f"❌ {filename} yüklenirken hata oluştu: {e}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı.")

bot.run(os.getenv("BOT_TOKEN"))