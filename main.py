import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler 

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

# 1. KONFİGÜRASYON (Ayarlar)
logging.basicConfig(
    level=logging.INFO, # Hangi seviyedeki mesajlar kaydedilsin? (INFO ve üstü)
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s', # Mesaj formatı (Zaman:Seviye:İsim:Mesaj)
    handlers=[
    RotatingFileHandler(
        filename='bot.log', 
        encoding='utf-8', 
        mode='a', 
        maxBytes=5 * 1024 * 1024, # 5MB olunca dosyayı döndür
        backupCount=5             # En fazla 5 tane eski log dosyası tut
    ),
    logging.StreamHandler()
]

)

logger = logging.getLogger('discord') # Discord'un kendi iç olaylarını da yakalayalım

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    # Bot başlarken dosyaları otomatik yükler
    async def setup_hook(self):
         cog_path = "./cogs"
        # 1. Klasör var mı kontrol et! Yoksa botun çökmesin.

         if not os.path.exists(cog_path):
            logging.error(f"Kritik Hata: '{cog_path}' dizini bulunamadı!")
            return
        # cogs klasöründeki genel.py dosyasını yükle
          # cogs klasöründeki her dosyaya bak
         for filename in os.listdir("./cogs"):

          # 2. Sadece .py dosyalarını al ve __init__.py gibi dosyaları ele!
            # Ayrıca 'utils' veya 'helpers' gibi dosyaları yüklememek için 
            # belirli bir isimlendirme kuralı (prefix) koyabilirsin.
            if filename.endswith(".py") and not filename.startswith("__"):

             try:
                  cog_name = f"cogs.{filename[:-3]}"
                  await self.load_extension(cog_name)
                    # Bak burada PRINT kullanmıyorum, LOG kullanıyorum!
                  logging.info(f"Cog yüklendi: {cog_name}")
             except Exception as e:
                  logging.error(f"{filename} yüklenirken patladı!", exc_info=True)

    async def on_ready(self):
       logging.info(f"--- BOT HAZIR ---")
       logging.info(f"Kullanıcı: {self.user} (ID: {self.user.id})")
       
       
        # --- BURAYA EKLEDİK (BEYNİN HATA MERKEZİ) ---


    async def on_command_error(self, ctx, error):
        # 1. Eğer komutun kendi içinde hata yakalayıcısı varsa (local error handler), burayı pas geç.bir functionin errorini gozle
        if hasattr(ctx.command, 'on_error'):
            return

        # 2. Cog içindeki local error handler'lar için de aynı durum.hemme cogs folderindeki hemme functionalrin errori barmy diyip gozle
        cog = ctx.cog  # shol bir cogun ichindaki bir klas cog=MOdersyon,yada cog=Genel.... sheyle sheyle shonun ichndakini gozle shol clasalrin ichini gozle
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        # 3. Hangi hataları görmezden geleceğiz? 
        # CommandNotFound en büyük spam kaynağıdır. Sessizce logla geç.
        ignored = (commands.CommandNotFound, )
        if isinstance(error, ignored):
            logging.info(f"Sessizce geçilen hata: {error} (User: {ctx.author})")
            return

        # 4. Kullanıcıya bilgi verilecek hatalar
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"⚠️ Eksik bilgi! Kullanım: `{ctx.prefix}{ctx.command.name} {ctx.command.signature}`")

        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send("🚫 Bu komut için yetkin yok!")

        # 5. Beklenmedik hatalar (İşte burası kritik!)
        else:
            # Kullanıcıya sadece "hata oldu" de, detayı verme!
            await ctx.send("💥 Sistemde bir hata oluştu, teknik ekibe (yani bana) bildirildi.")
            
            # Detayı sadece log dosyasına yaz (az önce öğrettiğim exc_info ile!)
            logging.error(f"KOMUT HATASI! Komut: {ctx.command} | Kullanıcı: {ctx.author}", exc_info=error)
            
            # İstersen burada kendine bir DM veya özel admin kanalına mesaj atabilirsin.

bot = MyBot()



bot.run(os.getenv("BOT_TOKEN"))