from disnake.ext import commands


class PingCommand(commands.Cog):
    """スラッシュコマンドサンプル:Ping"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def ping(self, inter):
        """Pingを送信します."""
        await inter.response.send_message(
            f"📶 {round(self.bot.latency * 1000)}ms", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(PingCommand(bot))
