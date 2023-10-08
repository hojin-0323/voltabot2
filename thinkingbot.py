import discord
import beforerun as set
import file
from discord.ext import commands

prefix = ":>"

set.varset(doUpdate=True)

def getuserid(user):
    return int(user[2:len(user)-1])

def getusercolor(ctx, userid):
    color = 0x000000
    for i in ctx.guild.roles:
        if userid in [j.id for j in i.members]:
            color = str(i.color)
    return int("0x"+color[1:], 16)

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')
    print("version v"+set.versionm+"."+str(set.build)+" ("+set.day+")")

@bot.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(round(bot.latency, 4)*1000)}ms')

@bot.command()
async def version(ctx):
    info = file.openfile("res", "versioninfo").replace("[빌드번호]", str(set.build)).replace("[빌드날짜]", str(set.day))
    embed = discord.Embed(title = "버전 정보", description = info, color = 0x00a84d)
    embed.set_footer(text = "볼타봇 버전 v"+set.versionm+"."+str(set.build))
    await ctx.send(embed = embed)

@bot.command()
async def echo(ctx, abc):
    await ctx.send(abc)

@bot.command()
async def openmemo(ctx, *, filename):
    if file.ismemo(filename):
        embed = discord.Embed(title = filename, description = file.openfile("memo", filename), color = 0xbdb092)
        embed.set_footer(text = file.memover('memo', filename))
        await ctx.send(embed = embed)
    else:
        await ctx.send(filename+" 메모가 없습니다. "+filename+" 메모를 생성하려면 \n```"+prefix+"editmemo "+filename+" [메모 내용]```\n 을 입력하세요.")

@bot.command()
async def editmemo(ctx, filename, *, memo):
    isexist = file.ismemo(filename)
    file.editfile("memo", filename, memo)
    if isexist:
        await ctx.send("수정됨")
    else:
        await ctx.send("생성됨")

@bot.command()
async def delmemo(ctx, *, filename):
    file.delfile("memo", filename)
    await ctx.send("삭제됨")

@bot.command()
async def profile(ctx, user):
    try:
        name = await commands.MemberConverter.convert(self=commands.MemberConverter, ctx=ctx, argument=user)
        embed = discord.Embed(title = name.nick, description = file.openfile("profile", str(getuserid(user)), True), color = getusercolor(ctx, getuserid(user)))
        embed.set_footer(text = file.memover('profile', str(getuserid(user))))
        await ctx.send(embed = embed)
    except Exception as err:
        await ctx.send(err)

@bot.command()
async def myprofile(ctx):
    name = ctx.message.author.name
    userid = ctx.message.author.id
    embed = discord.Embed(title = name, description = file.openfile("profile", str(userid), True), color = getusercolor(ctx, userid))
    embed.set_footer(text = file.memover('profile', str(userid)))
    await ctx.send(embed = embed)

@bot.command()
async def isadmin(ctx):
    if ctx.guild and ctx.message.author.guild_permissions.administrator:
        await ctx.send('?')
    else:
        await ctx.send("권한이 어ㅄ습니다. ")

bot.run('MTE1MzYyMDgzODI0ODA5OTk1MA.GwSrCb.uN_yBaHK4Gi8cER71OZ4PKrerQ3oEbxUd3asaU')