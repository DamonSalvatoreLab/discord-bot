from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
import datetime

# --- RENDER İÇİN CANLI TUTMA SUNUCUSU ---
app = Flask('')

@app.route('/')
def home():
    return "Bot aktif ve çalışıyor!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
-----------------------------------------

import discord
from discord.ext import commands
import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} aktif ve tüm komutlar başarıyla yüklendi!')
    await bot.change_presence(activity=discord.Game("!yardım | Güvenlik Aktif 🚀"))

# ==========================================
# 1. YARDIM MENÜSÜ
# ==========================================
@bot.command(name='yardım', aliases=['help'])
async def yardim(ctx):
    embed = discord.Embed(
        title="🤖 Bot Komutları ve Yardım Menüsü",
        description="Sunucuyu yönetmek için kullanabileceğin komutlar aşağıdadır:",
        color=discord.Color.purple()
    )
    embed.add_field(
        name="🛠️ Yetkili / Moderasyon Komutları",
        value="`!ban @Kullanıcı` - Kullanıcıyı banlar\n"
              "`!unban [KullanıcıID]` - Banı kaldırır\n"
              "`!kick @Kullanıcı` - Sunucudan atar\n"
              "`!mute @Kullanıcı [Dakika]` - Susturur\n"
              "`!unmute @Kullanıcı` - Susturmayı açar\n"
              "`!temizle [Sayı]` - Mesaj siler\n"
              "`!kilitle` - Kanalı mesaja kapatır\n"
              "`!kilitac` - Kanalı açar\n"
              "`!yavasmod [Saniye]` - Yavaş mod ayarlar",
        inline=False
    )
    embed.add_field(
        name="👑 Rol ve İsim Komutları",
        value="`!rolver @Kullanıcı @Rol` - Rol verir\n"
              "`!rolal @Kullanıcı @Rol` - Rol alır\n"
              "`!isim @Kullanıcı [Yeniİsim]` - İsim değiştirir",
        inline=False
    )
    embed.add_field(
        name="👤 Kullanıcı ve Bilgi Komutları",
        value="`!avatar [@Kullanıcı]` - Profil resmini gösterir\n"
              "`!bilgi [@Kullanıcı]` - Detaylı kullanıcı bilgisi\n"
              "`!sunucubilgi` - Sunucu hakkında bilgi verir\n"
              "`!ping` - Botun gecikme süresini ölçer\n"
              "`!yaz [Mesajın]` - Bota yazı yazdırır",
        inline=False
    )
    
    # Güvenli avatar kontrolü
    footer_icon = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
    embed.set_footer(text=f"İsteyen: {ctx.author.name}", icon_url=footer_icon)
    await ctx.send(embed=embed)

# ==========================================
# 2. AVATAR / PROFİL RESMİ GÖSTERME
# ==========================================
@bot.command(name='avatar', aliases=['profil', 'pp'])
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    
    user_avatar = member.avatar.url if member.avatar else member.default_avatar.url
    author_avatar = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url

    embed = discord.Embed(
        title=f"{member.name} adlı kullanıcının profil fotoğrafı",
        color=discord.Color.blue()
    )
    embed.set_image(url=user_avatar)
    embed.set_footer(text=f"İsteyen: {ctx.author}", icon_url=author_avatar)
    await ctx.send(embed=embed)

# ==========================================
# 3. DETAYLI KULLANICI BİLGİSİ
# ==========================================
@bot.command(name='bilgi', aliases=['userinfo', 'whois'])
async def bilgi(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
    role_list = ", ".join(roles) if roles else "Rolü yok"
    user_avatar = member.avatar.url if member.avatar else member.default_avatar.url

    embed = discord.Embed(title=f"Kullanıcı Bilgisi: {member.name}", color=discord.Color.green())
    embed.set_thumbnail(url=user_avatar)
    embed.add_field(name="Kullanıcı Adı", value=member.mention, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Sunucuya Katılma Tarihi", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="Hesap Oluşturma Tarihi", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name=f"Roller ({len(roles)})", value=role_list, inline=False)
    
    await ctx.send(embed=embed)

# ==========================================
# 4. SUNUCU BİLGİSİ
# ==========================================
@bot.command(name='sunucubilgi', aliases=['serverinfo'])
async def sunucubilgi(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"📊 {guild.name} Sunucu Bilgileri", color=discord.Color.gold())
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Sunucu Sahibi", value=guild.owner.mention, inline=True)
    embed.add_field(name="Sunucu ID", value=guild.id, inline=True)
    embed.add_field(name="Üye Sayısı", value=guild.member_count, inline=True)
    embed.add_field(name="Kanal Sayısı", value=len(guild.channels), inline=True)
    embed.add_field(name="Rol Sayısı", value=len(guild.roles), inline=True)
    embed.add_field(name="Kuruluş Tarihi", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    await ctx.send(embed=embed)

# ==========================================
# 5. PİNG ÖLÇME
# ==========================================
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Gecikme süresi: `{round(bot.latency * 1000)}ms`')

# ==========================================
# 6. DUYURU / YAZI YAZDIRMA
# ==========================================
@bot.command()
@commands.has_permissions(manage_messages=True)
async def yaz(ctx, *, mesaj):
    await ctx.message.delete()
    await ctx.send(mesaj)

# ==========================================
# 7. BANLA
# ==========================================
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Başarılı! {member.mention} sunucudan banlandı.')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bunun için **Üyeleri Yasakla** yetkin yok.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Eksik kullanım! Örnek: `!ban @Kullanıcı`")

# ==========================================
# 8. BAN KALDIRMA (UNBAN)
# ==========================================
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f'Başarılı! `{user.name}` adlı kullanıcının banı kaldırıldı.')

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bunun için yetkin yok.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Eksik kullanım! Örnek: `!unban KullanıcıID`")

# ==========================================
# 9. SUNUCUDAN AT (Kick)
# ==========================================
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Başarılı! {member.mention} sunucudan atıldı.')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bunun için **Üyeleri At** yetkin yok.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Eksik kullanım! Örnek: `!kick @Kullanıcı`")

# ==========================================
# 10. MUTE / ZAMANAŞIMI
# ==========================================
@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int, *, reason=None):
    duration = datetime.timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f'Başarılı! {member.mention} adlı kullanıcı **{minutes} dakika** süreyle susturuldu.')

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bunun için yetkin yok.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Eksik kullanım! Örnek: `!mute @Kullanıcı 5`")

# ==========================================
# 11. UNMUTE (Susturmayı Kaldırma)
# ==========================================
@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f'Başarılı! {member.mention} adlı kullanıcının susturulması kaldırıldı.')

# ==========================================
# 12. İSİM DEĞİŞTİRME (Nickname)
# ==========================================
@bot.command(aliases=['nick'])
@commands.has_permissions(manage_nicknames=True)
async def isim(ctx, member: discord.Member, *, new_name):
    await member.edit(nick=new_name)
    await ctx.send(f'Başarılı! {member.mention} adlı kişinin ismi **{new_name}** olarak değiştirildi.')

# ==========================================
# 13. MESAJLARI TEMİZLE
# ==========================================
@bot.command(aliases=['sil'])
@commands.has_permissions(manage_messages=True)
async def temizle(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'{amount} adet mesaj silindi!', delete_after=3)

# ==========================================
# 14. KANALI KİLİTLEME
# ==========================================
@bot.command()
@commands.has_permissions(manage_channels=True)
async def kilitle(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Bu kanal mesaj gönderimine kapatıldı.")

# ==========================================
# 15. KANALIN KİLİDİNİ AÇMA
# ==========================================
@bot.command()
@commands.has_permissions(manage_channels=True)
async def kilitac(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=None)
    await ctx.send("🔓 Bu kanalın kilidi açıldı.")

# ==========================================
# 16. YAVAŞ MOD
# ==========================================
@bot.command(aliases=['yavaşmod'])
@commands.has_permissions(manage_channels=True)
async def yavasmod(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f'⏱️ Yavaş mod **{seconds}** saniye olarak ayarlandı.')

# ==========================================
# 17. ROL VER
# ==========================================
@bot.command()
@commands.has_permissions(manage_roles=True)
async def rolver(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f'İşlem tamam! {member.mention} adlı kullanıcıya **{role.name}** rolü verildi.')

# ==========================================
# 18. ROL AL
# ==========================================
@bot.command()
@commands.has_permissions(manage_roles=True)
async def rolal(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f'İşlem tamam! {member.mention} adlı kişiden **{role.name}** rolü alındı.')

# Botunu çalıştırmak için token'ını buraya yaz
bot.run('MTUzMDYwOTc1NzI1MjA5MjAzNQ.GvxJiZ.-bqiVwFGPC4in6TG1LIL-jpf5oZnV4IajiQPdA')
from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
import datetime

# --- RENDER İÇİN CANLI TUTMA SUNUCUSU ---
app = Flask('')

@app.route('/')
def home():
    return "Bot aktif ve çalışıyor!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
-----------------------------------------