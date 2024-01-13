from disnake.ext import commands
from sqlitedict import SqliteDict
import json

db = SqliteDict('db.sqlite', autocommit=True)

class DettachChannelCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="通知解除")
    async def dc(self,
                 inter,
                 genre: str = commands.Param(choices={
                     "スプラトゥーン": "splatoon",
                     "他ゲーム": "others",
                     "自習/雑談": "study"
                 })):
        """通知設定を解除します"""
        if str(inter.guild.id) in db.keys():
            cfg = json.loads(db[str(inter.guild_id)])
            if "send_channel_ids" in cfg:
                if genre in cfg["send_channel_ids"]:
                    cfg["send_channel_ids"][genre] = ""
                    db[str(inter.guild_id)] = json.dumps(cfg)
                    await inter.response.send_message("テキストチャンネルの通知設定を解除しました")
                else:
                    await inter.response.send_message(
                        "対応するテキストチャンネルは登録されていません", ephemeral=True)
            else:
                await inter.response.send_message("テキストチャンネルは登録されていません",
                                                  ephemeral=True)
            if "forum_channel_ids" in cfg:
                if genre in cfg["forum_channel_ids"]:
                    cfg["forum_channel_ids"][genre] = ""
                    db[str(inter.guild_id)] = json.dumps(cfg)
                    await inter.response.send_message("フォーラムチャンネルの通知設定を解除しました")
                else:
                    await inter.response.send_message(
                        "対応するフォーラムチャンネルは登録されていません", ephemeral=True)
            else:
                await inter.response.send_message("フォーラムチャンネルは登録されていません",
                                                  ephemeral=True)
        else:
            await inter.response.send_message("データベースにサーバーが登録されていません",
                                              ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(DettachChannelCommand(bot))
