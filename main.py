import os
import disnake
from disnake.ext import commands
from sqlitedict import SqliteDict
import json
import defaultcfg
from pytz import timezone
from datetime import datetime as dt
from server import keep_alive

db = SqliteDict('db.sqlite', autocommit=True)

# .envからTOKENを取ってくる
TOKEN = os.getenv("TOKEN")

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

# 接続するためのオブジェクト
bot = commands.Bot(activity=disnake.Game(name="イカしたゲーム"),
                   command_prefix='.',
                   # test_guilds=[],
                   intents=disnake.Intents.all(),
                   command_sync_flags=command_sync_flags)
# -- sample
# bot.load_extension("cogs.ping")
# bot.load_extension("cogs.echo")
bot.load_extension("cogs.help")

bot.load_extension("cogs.set_channel")
bot.load_extension("cogs.dettach_channel")

bot.load_extension("cogs.lfg.any_spla")

bot.load_extension("cogs.lfg.anarchy_open")
bot.load_extension("cogs.lfg.open_or_priv")
bot.load_extension("cogs.lfg.event")
bot.load_extension("cogs.lfg.plzsp")
bot.load_extension("cogs.lfg.private")
bot.load_extension("cogs.lfg.salmon")
bot.load_extension("cogs.lfg.splatfest")
bot.load_extension("cogs.lfg.turf_war")
bot.load_extension("cogs.lfg.tableturf")

bot.load_extension("cogs.lfg.another_game")
bot.load_extension("cogs.lfg.study_chat")


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
    if channel.type != disnake.ChannelType.text:
        return
    msg = await channel.fetch_message(payload.message_id)
    embed = msg.embeds[0] if msg.embeds else None
    if not embed:
        return
    embi = embed.author.icon_url
    reai = bot.get_user(payload.user_id).display_avatar.url
    embt = embed.fields
    if msg.author.id == bot.user.id:
        if embi == reai:
            if ord(str(payload.emoji)[0]) in (0x274c, 0x2716):
                try:
                    if embt[1]:
                        thread = bot.get_channel(int(embt[1].value[2:-1]))
                        await thread.delete()
                except IndexError:
                    pass
                except AttributeError:
                    pass
                await msg.delete()


# ウェブサーバーを起動する
keep_alive()

# Discordへ接続
try:
    bot.run(TOKEN)
except disnake.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system("python restarter.py")
    os.system('kill 1')
