import discord
from discord.ext import commands
import asyncio

class Genel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Cog içindeki olaylar (Event) böyle yazılır:
    @commands.Cog.listener()
    async def on_ready(self):
        print("Genel komutları yüklendi!")

    # Cog içindeki komutlar böyle yazılır:
    @commands.command()
    async def selam(self, ctx): # 'self' eklemeyi unutma!
        await ctx.send(f"Selam {ctx.author.name}, ben bir Cog dosyasından geliyorum! 🚀")
        
    @commands.command()
    async def arigatou(self, ctx): # 'self' eklemeyi unutma!
        await ctx.send(f"Douitashimashite {ctx.author.name}, I am always here to help you darling! 🚀")
    
    @commands.command()
    async def hatirlat(self, ctx, sure: int, *, mesaj):
        """Kullanıcıya belirli bir süre sonra hatırlatma yapar. Örn: !hatirlat 10 Sınavın var!"""
        
        await ctx.send(f"✅ Tamamdır {ctx.author.mention}! {sure} saniye sonra sana hatırlatacağım.")

        # 1. Bekleme Aşaması (Saniyeye çevirmek için süre bilgisini kullanıyoruz)
        await asyncio.sleep(sure)

        # 2. Hatırlatma Aşaması (Özel Mesaj Gönderimi)
        try:
            await ctx.author.send(f"⏰ **HATIRLATICI:** {mesaj}")
        except discord.Forbidden:
            # Kullanıcının DM'leri kapalıysa kanala mesaj atarız
            await ctx.send(f"⚠️ {ctx.author.mention}, DM kutun kapalı olduğu için buradan söylüyorum: {mesaj}")


# Bu fonksiyon Cog'un main.py tarafından tanınmasını sağlar
async def setup(bot):
    await bot.add_cog(Genel(bot))