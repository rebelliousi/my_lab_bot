import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} hazır!")

@bot.command()
async def merhaba(ctx):
    await ctx.send("Merhaba! Ben çalışıyorum! 🎉")

@bot.command()
async def hi(ctx):
    await ctx.send("Hi! 👋")
    
@bot.command()
async def ping(ctx):
    gecikme = round(bot.latency * 1000)
    await ctx.send(f"Pong! 🏓 ({gecikme}ms)")

@bot.command()
async def say(ctx, *, mesaj):
    await ctx.send(mesaj)


@bot.command()
async def selam(ctx, isim):
    await ctx.send(f"Selam {isim}! Bugün nasılsın?")

bot.run(os.getenv("BOT_TOKEN"))