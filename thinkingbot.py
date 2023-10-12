import discord
import beforerun as set
import file
from discord.ext import commands

prefix = ":>"
admin_id = "861132651151097866"
ussr = 0

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

@bot.event
async def on_message(message):
    if message.content.startswith(prefix + 'help admin'):
        if message.channel.guild and message.author.guild_permissions.administrator:
            await message.channel.send("이 명령어는 도움말을 제공하지 않습니다. ")
        else:
            await message.channel.send("권한이 어ㅄ습니다. ")
    else:
        await bot.process_commands(message)

@bot.event
async def on_raw_message_delete(message):
    if ussr:
        await message.channel.send(message.author.nick + " 님이 " + message.content + " 메시지를 삭제했습니다. ")

@bot.event
async def on_raw_message_edit(before, after):
    if ussr:
        await after.channel.send( after.author.nick + " 님이 " + before.content + " 메시지를 " + after.content + " 로 수정함.")

@bot.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(round(bot.latency, 4)*1000)}ms')

ping.help = "테스트"

@bot.command()
async def version(ctx):
    info = file.openfile("res", "versioninfo").replace("[빌드번호]", str(set.build)).replace("[빌드날짜]", str(set.day))
    embed = discord.Embed(title = "버전 정보", description = info, color = 0x00a84d)
    embed.set_footer(text = "볼타봇 버전 v"+set.versionm+"."+str(set.build))
    await ctx.send(embed = embed)

version.help = "버전 정보를 출력합니다. "

@bot.command()
async def echo(ctx, *, abc):
    await ctx.send(abc)

echo.help = "입력한 내용을 출력합니다"

@bot.command(name = "print")
async def printctx(ctx, *, abc):
    await ctx.channel.purge(limit=1)
    await ctx.send(abc)

printctx.help = "입력한 내용을 출력합니다 (원본 메시지 삭제)"

@bot.group()
async def memo(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("명령어가 올바르지 않습니다. ")

memo.help = "메모 입출력 관련"

@memo.command()
async def open(ctx, *, filename):
    if file.ismemo(filename):
        embed = discord.Embed(title = filename, description = file.openfile("memo", filename), color = 0xbdb092)
        embed.set_footer(text = file.memover('memo', filename, 0))
        await ctx.send(embed = embed)
    else:
        await ctx.send(filename+" 메모가 없습니다. "+filename+" 메모를 생성하려면 \n```"+prefix+"memo edit "+filename+" [메모 내용]```\n 을 입력하세요.")

open.help = "메모를 출력합니다."

@memo.command()
async def edit(ctx, filename, *, memo):
    isexist = file.ismemo(filename)
    file.editfile("memo", filename, memo)
    file.rev("rev", filename, memo)
    if isexist:
        await ctx.send("수정됨")
    else:
        await ctx.send("생성됨")

edit.help = "메모를 작성/수정합니다. "

@memo.command()
async def delete(ctx, *, filename):
    file.delfile("memo", filename)
    await ctx.send("삭제됨")

delete.help = "메모를 삭제합니다. "

@bot.command()
async def profile(ctx, user = " "):
    if user == " ":
        name = ctx.message.author.nick
        userid = ctx.message.author.id
        embed = discord.Embed(title = name, description = file.openfile("profile", str(userid), True), color = getusercolor(ctx, userid))
    else:
        name = await commands.MemberConverter.convert(self=commands.MemberConverter, ctx=ctx, argument=user)
        userid = getuserid(user)
        embed = discord.Embed(title = name.nick, description = file.openfile("profile", str(getuserid(user)), True), color = getusercolor(ctx, getuserid(user)))
    embed.set_footer(text = file.memover('profile', str(name), 0))
    await ctx.send(embed = embed)

profile.help = "맨션한 사람(또는 자신)의 유저 정보를 출력합니다. "

@bot.command()
async def introduce(ctx, *, memo):
    userid = ctx.message.author.id
    file.editfile("profile", str(userid), memo)
    file.rev("profilerev", str(userid), memo)
    await ctx.send("수정 완료")

introduce.help = "자기소개를 작성/수정합니다. "

@bot.group()
async def rev(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("명령어가 올바르지 않습니다. ")

rev.help = "메모 리버전 관련"

@rev.command()
async def memo(ctx, filename, ver):
    if file.isrev("rev", filename, ver):
        embed = discord.Embed(title = filename, description = file.openrev("rev", filename, ver), color = 0xbdb092)
        embed.set_footer(text = file.memover('memo', filename, ver))
        await ctx.send(embed = embed)
    else:
        await ctx.send("해당 버전이 없습니다. ")

memo.help = "메모 리버전을 엽니다. "

@rev.command(name = "profile")
async def pfrev(ctx, user, ver):
    try:
        name = await commands.MemberConverter.convert(self=commands.MemberConverter, ctx=ctx, argument=user)
        embed = discord.Embed(title = name.nick, description = file.openrev("profilerev", str(getuserid(user)), ver), color = getusercolor(ctx, getuserid(user)))
        embed.set_footer(text = file.memover('profile', str(getuserid(user)), ver))
        await ctx.send(embed = embed)
    except Exception as err:
        await ctx.send(err)

pfrev.help = "맨션한 유저의 유저 정보 리버전을 불러옵니다. "

@rev.command(name="myprofile")
async def mypfrev(ctx, ver):
    name = ctx.message.author.name
    userid = ctx.message.author.id
    embed = discord.Embed(title = name, description = file.openrev("profilerev", str(userid), ver), color = getusercolor(ctx, userid))
    embed.set_footer(text = file.memover('profile', str(userid), 0))
    await ctx.send(embed = embed)

mypfrev.help = "자신의 유저 정보 리버전을 불러옵니다. "

@bot.group()
async def admin(ctx):
    if not (ctx.guild and ctx.message.author.guild_permissions.administrator):
        await ctx.send("권한이 어ㅄ습니다. ")
    else:
        if ctx.invoked_subcommand is None:
            await ctx.send("명령어가 올바르지 않습니다. ||~~당신 관리자 맞습니까?~~||")

admin.help = "관리자 전용 명령어"

@admin.command(name = "clear")
async def clearmessage(ctx, num = -6974):
    if ctx.guild and ctx.message.author.guild_permissions.administrator:
        if num > 0:
            await ctx.channel.purge(limit=num)
        else:
            await ctx.send("전 그런 거 못하니까 님이 {}개 지워보세요".format(num))
    else:
        await ctx.send("권한이 어ㅄ습니다. ")

clearmessage.help = "메시지를 삭제합니다. "

@admin.command(name = "hello")
async def changehellomessage(ctx, *, text):
    if ctx.guild and ctx.message.author.guild_permissions.administrator:
        hellotext = open("hello.txt", "w", encoding = "utf8")
        hellotext.write(text)
        hellotext.close()
    else:
        await ctx.send("권한이 어ㅄ습니다. ")

clearmessage.help = "메시지를 삭제합니다. "

@admin.command(name = "record")
async def savedeleteedit(ctx, *, text):
    if ctx.guild and ctx.message.author.guild_permissions.administrator:
        hellotext = open("hello.txt", "w", encoding = "utf8")
        hellotext.write(text)
        hellotext.close()
    else:
        await ctx.send("권한이 어ㅄ습니다. ")

savedeleteedit.help = "수정/삭제 기록을 남깁니다. "

bot.run('MTE1MzYyMDgzODI0ODA5OTk1MA.GwSrCb.uN_yBaHK4Gi8cER71OZ4PKrerQ3oEbxUd3asaU')