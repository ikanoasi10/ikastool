from disnake.ext import commands


class EchoCommand(commands.Cog):
    """スラッシュコマンドサンプル:オウム返し"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def echo(self, inter, text):
        """おうむがえし"""
        await inter.response.send_message(text, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(EchoCommand(bot))
