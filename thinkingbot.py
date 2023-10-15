import discord
import os
import beforerun as set
import file
from discord.ext import commands

prefix = ":>"
# admin_id = "861132651151097866"
ussr = 0
vsc = "Beta 2.1"

set.varset(doUpdate=False, vsc = vsc)

def getuserid(user):
    return int(user[2:len(user)-1])

def getusercolor(ctx, userid):
    color = 0x000000
    for i in ctx.guild.roles:
        if userid in [j.id for j in i.members]:
            color = str(i.color)
    return int("0x"+color[1:], 16)

async def sendprofileembed(ctx, userinfo, pfver = -1):
    name = userinfo.nick
    userid = userinfo.id
    if pfver + 1:
        ver = pfver
    else:
        ver = file.getver('profilerev', str(userid))
    embed = discord.Embed(title = name, description = file.openrev("profilerev", str(userid), ver), color = getusercolor(ctx, userid))
    embed.set_footer(text = file.memover('profile', name, ver))
    await ctx.send(embed = embed)

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')
    print("version v"+set.versionm+"."+str(set.build)+" ("+set.day+")")
    await bot.change_presence(activity=discord.Game(name='전류 생산'))

@bot.event
async def on_message(message):
   if message.content.startswith(prefix + 'help admin'):
       if message.channel.guild and message.author.guild_permissions.administrator:
           admindm = await bot.create_dm(message.author)
           await commands.HelpCommand.command_callback(command="admin")
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
    info = file.openfile("res", "versioninfo").replace("[빌드번호]", str(set.build)).replace("[빌드날짜]", str(set.day)).replace("[버전 코드]", str(vsc))
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
        embed.set_footer(text = file.memover('memo', filename, file.getver('rev', filename)))
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
        userinfo = ctx.message.author
    else:
        userinfo = await commands.MemberConverter.convert(self=commands.MemberConverter, ctx=ctx, argument=user)
    await sendprofileembed(ctx, userinfo, -1)

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
async def pfrev(ctx, user, pfver = -1):
    userinfo = await commands.MemberConverter.convert(self=commands.MemberConverter, ctx=ctx, argument=user)
    await sendprofileembed(ctx, userinfo, pfver)
pfrev.help = "맨션한 유저의 유저 정보 리버전을 불러옵니다. "

@rev.command(name = "myprofile")
async def mypfrev(ctx, pfver = -1):
    userinfo = ctx.message.author
    await sendprofileembed(ctx, userinfo, pfver)

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
    if num > 0:
        await ctx.channel.purge(limit=num)
    else:
        await ctx.send("전 그런 거 못하니까 님이 {}개 지워보세요".format(num))

clearmessage.help = "메시지를 삭제합니다. "

@admin.command(name = "hello")
async def changehellomessage(ctx, *, text):
    hellotext = open("hello.txt", "w", encoding = "utf8")
    hellotext.write(text)
    hellotext.close()

clearmessage.help = "메시지를 삭제합니다. "

@admin.command(name = "record")
async def savedeleteedit(ctx, *, text):
    global ussr
    sv = ussr
    svc = 0
    if text in ["0", "1"]:
        ussrfile = open("ussr.txt", "w")
        ussrfile.write(text)
        ussrfile.close()
        ussr = int(text)
        svc = 2 * sv + ussr
        if svc == 0:
            ctx.send("이미 잠복근무 중이었습니다. ")
        elif svc == 1:
            ctx.send("앞으로 삭제/수정된 메시지를 도청하겠습니다. ")
        elif svc == 2:
            ctx.send("앞으로 삭제/수정된 메시지를 도청하지 않겠습니다. ")
        else:
            ctx.send("이미 도청 중이었습니다. ")
    else:
        await ctx.send("너같은 짭관리자 말 안 들을건데")

savedeleteedit.help = "수정/삭제 기록을 남길지 말지 설정합니다. "

bot.run(set.token)