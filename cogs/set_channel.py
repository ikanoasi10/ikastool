import disnake
from disnake.ext import commands
from replit import db
import json
import defaultcfg

GENRES = {
        "スプラトゥーン": "splatoon",
        "他ゲーム": "others",
        "自習/雑談": "study"
    }

class SetChannelCommand(commands.Cog):
    """This will be for a setchannel command."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="通知設定")
    async def sc(self, inter, genre: commands.option_enum(GENRES), channel: disnake.TextChannel):
        """テキストチャンネルを設定"""
        if not str(inter.guild.id) in db.keys():
            db[str(inter.guild.id)] = json.dumps(defaultcfg.CFG_DEFAULT)
            print(f' db[{inter.guild.id}]を作成')
        cfg = json.loads(db[str(inter.guild_id)])
        cfg["send_channel_ids"][genre] = channel.id
        db[str(inter.guild_id)] = json.dumps(cfg)

        await inter.response.send_message(
            f"{[k for k, v in GENRES.items() if v == genre][0]}についての募集投稿先を{channel.mention}チャンネルにしました")


def setup(bot: commands.Bot):
    bot.add_cog(SetChannelCommand(bot))
