import os
import beforerun as set
import discord
from discord.ext import commands

set.varset(doUpdate=True)

def ismemo(filename):
    name = "memo"+os.path.sep+filename+".txt"
    if os.path.isfile(name):
        return True
    else:
        return False

def open_file(filename):
    name = "memo"+os.path.sep+filename+".txt"
    if os.path.isfile(name):
        with open(name, "r", encoding="utf8") as file:
            return file.read()

def open_profile(filename):
    name = "userprofile"+os.path.sep+filename+".txt"
    if os.path.isfile(name):
        with open(name, "r", encoding="utf8") as file:
            return file.read()
    else:
        with open(name, "w", encoding="utf8") as file:
            file.write('')
            return ''

def open_res(filename):
    name = filename+".txt"
    with open(name, "r", encoding="utf8") as file:
        return file.read()

def getuserid(user):
    return int(user[2:len(user)-1])

def getusercolor(ctx, userid):
    color = 0x000000
    for i in ctx.guild.roles:
        if userid in [j.id for j in i.members]:
            color = str(i.color)
    return int("0x"+color[1:], 16)

def memover(tp, name):
    return "볼타봇 메모 서비스 (베타)"

bot = commands.Bot(command_prefix='#', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')
    print("version v"+set.versionm+"."+str(set.build)+" ("+set.day+")")

@bot.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(round(bot.latency, 4)*1000)}ms')

@bot.command()
async def version(ctx):
    info = open_res("versioninfo").replace("[빌드번호]", str(set.build)).replace("[빌드날짜]", str(set.day))
    embed = discord.Embed(title = "버전 정보", description = info, color = 0x00a84d)
    embed.set_footer(text = "볼타봇 버전 v"+set.versionm+"."+str(set.build))
    await ctx.send(embed = embed)

@bot.command()
async def test(ctx, abc):
    await ctx.send(abc)

@bot.command()
async def openmemo(ctx, filename):
    if ismemo(filename):
        embed = discord.Embed(title = filename, description = open_file(filename), color = 0xbdb092)
        embed.set_footer(text = memover('memo', filename))
        await ctx.send(embed = embed)

@bot.command()
async def profile(ctx, user):
    try:
        name = await commands.MemberConverter.convert(self=commands.MemberConverter, ctx=ctx, argument=user)
        embed = discord.Embed(title = name.nick, description = open_profile(str(getuserid(user))), color = getusercolor(ctx, getuserid(user)))
        embed.set_footer(text = memover('profile', str(getuserid(user))))
        await ctx.send(embed = embed)
    except Exception as err:
        await ctx.send(err)

@bot.command()
async def myprofile(ctx):
    name = ctx.message.author.name
    userid = ctx.message.author.id
    embed = discord.Embed(title = name, description = open_profile(str(userid)), color = getusercolor(ctx, userid))
    embed.set_footer(text = memover('profile', str(userid)))
    await ctx.send(embed = embed)

# @bot.command()
# async def asdf(ctx, user=str(discord.Message.author)):
#     name = await commands.MemberConverter.convert(self=commands.MemberConverter, ctx=ctx, argument=user)
#     await ctx.send(type(user))

@bot.command()
async def versionupdatelog(ctx):
    if ctx.guild and ctx.message.author.guild_permissions.administrator:
        await ctx.send('?')
    else:
        await ctx.send("권한이 어ㅄ습니다. ")

bot.run('MTE1MzYyMDgzODI0ODA5OTk1MA.GwSrCb.uN_yBaHK4Gi8cER71OZ4PKrerQ3oEbxUd3asaU')