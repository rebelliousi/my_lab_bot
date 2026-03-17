import discord
from discord.ext import commands

class Moderasyon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # !temizle [sayı] komutu - Mesajları toplu siler
    @commands.command()
    @commands.has_permissions(manage_messages=True) # Sadece mesaj yönet yetkisi olanlar!
    async def temizle(self, ctx, miktar: int):
        await ctx.channel.purge(limit=miktar + 1)
        await ctx.send(f"✅ {miktar} mesaj temizlendi!", delete_after=5) # 5 saniye sonra bu mesaj da silinir

async def setup(bot):
    await bot.add_cog(Moderasyon(bot))