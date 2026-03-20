import discord
from discord.ext import commands

class Notlar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Hafıza burası! {kullanici_id: [not1, not2]} şeklinde tutacak.
        self.not_defteri = {}

    # 1. NOT ALMA KOMUTU
    @commands.command()
    async def not_al(self, ctx, *, metin):
        kullanici_id = ctx.author.id
        
        # Eğer kullanıcının daha önce hiç notu yoksa, ona boş bir liste açalım
        if kullanici_id not in self.not_defteri:
            self.not_defteri[kullanici_id] = []
        
        # Notu listeye ekle
        self.not_defteri[kullanici_id].append(metin)
        await ctx.send(f"✅ Notun kaydedildi {ctx.author.mention}!")

    # 2. NOTLARIM KOMUTU
    @commands.command()
    async def notlarim(self, ctx):
        kullanici_id = ctx.author.id
        
        if kullanici_id not in self.not_defteri or len(self.not_defteri[kullanici_id]) == 0:
            return await ctx.send("🕵️ Hiç notun yok gibi görünüyor.")

        # Notları numaralandırarak janti bir Embed içinde gösterelim (4. Gün bilgisi!)
        not_listesi = ""
        for sira, not_metni in enumerate(self.not_defteri[kullanici_id], 1):
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
        kullanici_id = ctx.author.id
        if kullanici_id in self.not_defteri:
            self.not_defteri[kullanici_id] = [] # Listeyi temizle
            await ctx.send("🗑️ Bütün notların silindi!")
        else:
            await ctx.send("Zaten silinecek bir notun yok.")

async def setup(bot):
    await bot.add_cog(Notlar(bot))