import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
#case_intensive bash setir harp tapawudy yok
bot = commands.Bot(command_prefix="!", intents=intents,case_insensitive=True)

@bot.event
async def on_ready():
    print(f"{bot.user} hazır!")

@bot.command()
async def merhaba(ctx):
    await ctx.send("Merhaba! Ben çalışıyorum! 🎉")

@bot.command()
async def hi(ctx):
    await ctx.send("Hi! 👋")
    
# @bot.command()
# async def ping(ctx):
#     gecikme = round(bot.latency * 1000)
#     await ctx.send(f"Pong! 🏓 ({gecikme}ms)")

@bot.command()
async def say(ctx, *, mesaj):
    await ctx.send(mesaj)


@bot.command()
async def selam(ctx, isim):
    await ctx.send(f"Selam {isim}! Bugün nasılsın?")

@bot.command()
async def ping(ctx):
    embed=discord.Embed(
        
        title=f"{round(bot.latency*1000)} gecikmesi",
        description="ping ping ",
        color=discord.Color.green()
        
)
    await ctx.send(embed=embed)
    

    
@bot.command()
async def profil(ctx):
    # Embed oluşturma
    embed = discord.Embed(
        title=f"{ctx.author.name} Profil Bilgileri",
        description="İşte senin hakkında bildiklerim:",
        color=discord.Color.purple()
    )
   

    # Profil fotoğrafını (Thumbnail) ekle
    if ctx.author.avatar:
        # embed.set_image(url=ctx.author.avatar.url)
        embed.set_thumbnail(url=ctx.author.avatar.url)
        
    
    # Bilgi alanlarını (Fields) ekle
    embed.add_field(name="Kullanıcı Adı", value=ctx.author.name, inline=False)
    embed.add_field(name="ID", value=ctx.author.id, inline=True)
    embed.add_field(name="Sunucuya Katılma", value=ctx.author.joined_at.strftime("%d/%m/%Y"), inline=False)

    # Alt bilgi (Footer) ekle
    embed.set_footer(text="4. Gün: Embed Sistemi Başarıyla Çalışıyor!")

    # Mesajı gönder
    await ctx.send(embed=embed)

bot.run(os.getenv("BOT_TOKEN"))