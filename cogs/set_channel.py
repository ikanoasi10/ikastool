import disnake
from disnake.ext import commands
from sqlitedict import SqliteDict
import json
import defaultcfg
db = SqliteDict('db.sqlite', autocommit=True)
GENRES = {"スプラトゥーン": "splatoon", "他ゲーム": "others", "自習/雑談": "study"}


class SetChannelCommand(commands.Cog):
    """This will be for a setchannel command."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="通知設定")
    async def sc(self, inter, genre: commands.option_enum(GENRES),
                 text_channel: disnake.TextChannel,
                 forum_channel: disnake.ForumChannel):
        """テキストチャンネルを設定"""
        await inter.response.defer(with_message=False, ephemeral=False)

        if not str(inter.guild.id) in db.keys():
            db[str(inter.guild.id)] = json.dumps(defaultcfg.CFG_DEFAULT)
            print(f' db[{inter.guild.id}]を作成')
        cfg = json.loads(db[str(inter.guild_id)])
        cfg.setdefault("send_channel_ids",
                       defaultcfg.CFG_DEFAULT["send_channel_ids"])
        cfg["send_channel_ids"][genre] = text_channel.id
        cfg.setdefault("forum_channel_ids",
                       defaultcfg.CFG_DEFAULT["forum_channel_ids"])
        cfg["forum_channel_ids"][genre] = forum_channel.id
        db[str(inter.guild_id)] = json.dumps(cfg)

        await inter.followup.send(
            f"{[k for k, v in GENRES.items() if v == genre][0]}についての募集投稿先を{text_channel.mention}チャンネルに、フォーラム投稿作成先を{forum_channel.mention}にしました"
        )


def setup(bot: commands.Bot):
    bot.add_cog(SetChannelCommand(bot))
