import discord
from discord.ext import commands
import aiosqlite 

class Notlar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Hafıza burası! {kullanici_id: [not1, not2]} şeklinde tutacak.
        self.db_name = "bot.db"
        
    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect(self.db_name) as db:
            # 'notlar' tablosu yoksa oluştur: id (otomatik), user_id, metin
            await db.execute("""
                CREATE TABLE IF NOT EXISTS notlar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    metin TEXT
                )
            """)
            await db.commit() # Değişiklikleri kaydet
        print("🗄️ Veritabanı ve Tablo Hazır!")
        
 
    

    # 1. NOT ALMA KOMUTU
    @commands.command()
    async def not_al(self, ctx, *, metin):
      
    # Artık ID almakla uğraşmıyoruz, yukarısı halletti!
        async with aiosqlite.connect(self.db_name) as db:
                await db.execute("INSERT INTO notlar (user_id, metin) VALUES (?, ?)", (ctx.author.id, metin))
                await db.commit()
        await ctx.send(f"✅ Notun veritabanına mühürlendi {ctx.author.mention}!")




    # 2. NOTLARIM KOMUTU
    @commands.command()
    async def notlarim(self, ctx):
        
        async with aiosqlite.connect(self.db_name) as db:
             cursor = await db.execute("SELECT metin FROM notlar WHERE user_id = ?", (ctx.author.id,))
             notlar = await cursor.fetchall() # Bütün sonuçları al
        if not notlar:
            return await ctx.send("🕵️ Veritabanında sana ait bir not bulamadım.")


        # Notları numaralandırarak janti bir Embed içinde gösterelim (4. Gün bilgisi!)
        not_listesi = ""
        for sira, veri in enumerate(notlar, 1):
            not_listesi += f"**{sira}.** {veri[0]}\n"

        embed = discord.Embed(
            title=f"📝 {ctx.author.name} Not Defteri",
            description=not_listesi,
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    # 3. NOT SİLME KOMUTU
    @commands.command()
    async def not_sil(self, ctx):
        async with aiosqlite.connect(self.db_name) as db:
           
         cursor = await db.execute("DELETE FROM notlar WHERE user_id = ?", (ctx.author.id,))
         await db.commit()
         if cursor.rowcount > 0:
            await ctx.send(f"🗑️ Senin adına kayıtlı {cursor.rowcount} adet not silindi!")
         else:
            await ctx.send("⚠️ Veritabanında senin adına kayıtlı bir not bulunamadı.")

async def setup(bot):
    await bot.add_cog(Notlar(bot))