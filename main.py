import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

# 1. KONFİGÜRASYON (Ayarlar)
logging.basicConfig(
    level=logging.INFO, # Hangi seviyedeki mesajlar kaydedilsin? (INFO ve üstü)
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s', # Mesaj formatı (Zaman:Seviye:İsim:Mesaj)
    handlers=[
        logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a'), # Dosyaya yaz (mode='a' üzerine ekler)
        logging.StreamHandler() # Aynı zamanda konsola (ekrana) da yaz
    ]
)

logger = logging.getLogger('discord') # Discord'un kendi iç olaylarını da yakalayalım

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
    # --- BURAYA EKLEDİK (BEYNİN HATA MERKEZİ) ---
    async def on_command_error(self, ctx, error):
        # 1. Komut Bulunamadı
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("🕵️ Böyle bir komut bulamadım gardash. `!yardim` yazarak bakabilirsin.")
        
        # 2. Eksik Bilgi (Argüman)
        elif isinstance(error, commands.MissingRequiredArgument):
            # ctx.command.signature otomatik olarak '!say <mesaj>' gibi kullanımı gösterir
            await ctx.send(f"⚠️ Eksik bilgi! Doğru kullanım: `{self.command_prefix}{ctx.command.name} {ctx.command.signature}`")
        
        # 3. Yetki Hatası
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 Bu işi yapmaya yetkin yetmez be ya!")

        # 4. Diğer Beklenmedik Hatalar
        else:
             logging.error(f"Beklenmedik bir hata oluştu: {error}")
             await ctx.send("💥 Bir şeyler ters gitti!")

bot = MyBot()

@bot.event
async def on_ready():
    logging.info(f"--- BOT HAZIR ---")
    logging.info(f"Kullanıcı: {bot.user}")
    logging.info(f"ID: {bot.user.id}")

bot.run(os.getenv("BOT_TOKEN"))