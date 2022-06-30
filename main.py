import os
import disnake
from disnake.ext import commands
from replit import db
import json
import defaultcfg
from pytz import timezone
from datetime import datetime as dt
from server import keep_alive

# .envからTOKENを取ってくる
TOKEN = os.getenv("TOKEN")

# 接続するためのオブジェクト
bot = commands.Bot(
    activity=disnake.Game(name="イカしたゲーム"),
    command_prefix='.',
    intents=disnake.Intents.all(),
    sync_commands_debug=True)
# -- sample
# bot.load_extension("cogs.ping")
# bot.load_extension("cogs.echo")

bot.load_extension("cogs.set_channel")
bot.load_extension("cogs.dettach_channel")

bot.load_extension("cogs.host.any_spla")
bot.load_extension("cogs.host.league")
bot.load_extension("cogs.host.leag_or_priv")
bot.load_extension("cogs.host.plzsp")
bot.load_extension("cogs.host.private")
bot.load_extension("cogs.host.salmon")
bot.load_extension("cogs.host.splatfest")
bot.load_extension("cogs.host.turf_war")

bot.load_extension("cogs.host.another_game")
bot.load_extension("cogs.host.study_chat")


# 起動時にログする
@bot.event
async def on_ready():
    print(f' logged in as {bot.user}')


# bot招待時、keyを作成
@bot.event
async def on_guild_join(guild):
    db[str(guild.id)] = json.dumps(defaultcfg.CFG_DEFAULT)
    print(f' db[{guild.id}]を作成')


# Guildごとにスラッシュコマンドの最終時刻をdbに記録
@bot.event
async def on_slash_command(inter):
    if str(inter.guild.id) in db.keys():
        cfg = json.loads(db[str(inter.guild_id)])
        if "last_executed" in cfg:
            cfg["last_executed"] = inter.created_at.strftime(
                '%Y-%m-%d %H:%M:%S')
            db[str(inter.guild_id)] = json.dumps(cfg)

# 一定期間コマンド未使用で削除
    for guild_id in db.keys():
        cfg = json.loads(db[guild_id])
        last_executed = timezone('UTC').localize(
            dt.strptime(cfg["last_executed"], '%Y-%m-%d %H:%M:%S'))
        td = dt.now(timezone('UTC')) - last_executed
        if td.days > 180:
            del db[guild_id]

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    embed = msg.embeds[0] if msg.embeds else None
    if not embed:
        return
    embi = embed.author.icon_url
    reai = bot.get_user(payload.user_id).display_avatar.url
    if msg.author.id == bot.user.id:
        if embi == reai:
            if ord(str(payload.emoji)[0]) in (0x274c, 0x2716):
                await msg.delete()
# ウェブサーバーを起動する
keep_alive()

# Discordへ接続
bot.run(TOKEN)
