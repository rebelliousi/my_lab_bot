import discord
from discord.ext import commands

class Notlar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Hafıza burası! {kullanici_id: [not1, not2]} şeklinde tutacak.
        self.not_defteri = {}
        
       # --- SENIOR DOKUNUŞU ---
    # Bu klasördeki HER komut çalışmadan önce buraya uğrar
    async def cog_before_invoke(self, ctx):
        # ID'yi alıp ctx içine "uid" adıyla bir etiket yapıştırıyoruz
        ctx.uid = ctx.author.id
        
        # Hazır gelmişken "Çekmece Kontrolünü" de burada yapalım mı?
        # Her seferinde 'if id not in...' yazmaktan da kurtuluruz!
        if ctx.uid not in self.not_defteri:
            self.not_defteri[ctx.uid] = []
    

    # 1. NOT ALMA KOMUTU
    @commands.command()
    async def not_al(self, ctx, *, metin):
      
    # Artık ID almakla uğraşmıyoruz, yukarısı halletti!

        self.not_defteri[ctx.uid].append(metin)
        await ctx.send(f"✅ Notun kaydedildi {ctx.author.mention}!")

    # 2. NOTLARIM KOMUTU
    @commands.command()
    async def notlarim(self, ctx):
        
        if  len(self.not_defteri[ctx.uid]) == 0:
            return await ctx.send("🕵️ Hiç notun yok gibi görünüyor.")

        # Notları numaralandırarak janti bir Embed içinde gösterelim (4. Gün bilgisi!)
        not_listesi = ""
        for sira, not_metni in enumerate(self.not_defteri[ctx.uid], 1):
            not_listesi += f"**{sira}.** {not_metni}\n"

        embed = discord.Embed(
            title=f"📝 {ctx.author.name} Not Defteri",
            description=not_listesi,
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    # 3. NOT SİLME KOMUTU
    @commands.command()
    async def not_sil(self, ctx):
        if  len(self.not_defteri[ctx.uid])>0:
            self.not_defteri[ctx.uid] = [] # Listeyi temizle
            await ctx.send("🗑️ Bütün notların silindi!")
        else:
            await ctx.send("Zaten silinecek bir notun yok.")

async def setup(bot):
    await bot.add_cog(Notlar(bot))