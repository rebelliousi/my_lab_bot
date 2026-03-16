import discord
from discord.ext import commands

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

# Bu fonksiyon Cog'un main.py tarafından tanınmasını sağlar
async def setup(bot):
    await bot.add_cog(Genel(bot))