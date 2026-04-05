import discord
from discord.ext import commands
from discord import app_commands # Slash komutları için bu kütüphane şart!

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. BASİT SLASH KOMUTU (/merhaba)
    @app_commands.command(name="merhaba", description="Botun sana selam vermesini sağlar")
    async def merhaba(self, interaction: discord.Interaction):
        # Slash komutlarında cevap verme şekli budur:
        await interaction.response.send_message(f"Merhaba {interaction.user.mention}! Slash komutları dünyasına hoş geldin! 👋")

    # 2. ARGÜMANLI SLASH KOMUTU (/say mesaj:merhaba)
    @app_commands.command(name="say", description="Yazdığın şeyi tekrar eder")
    @app_commands.describe(mesaj="Tekrar etmemi istediğin cümle") # Kullanıcı yazarken kutucukta görünen ipucu
    async def say(self, interaction: discord.Interaction, mesaj: str):
        await interaction.response.send_message(f"Söylediğin mesaj: **{mesaj}**")

async def setup(bot):
    await bot.add_cog(Slash(bot))