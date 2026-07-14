import disnake
from disnake.ext import commands
from cogs.lfg.modules.create_lfg import create_lfg

class RaidersCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="レイダース")
    async def raiders(self,
                inter: disnake.ApplicationCommandInteraction,
                at: str = commands.Param(default="", name="at", choices=(["1-3","1-2"] + [str(i) for i in reversed(range(1, 3 + 1))])),
                hour: int = commands.Param(default=-1, name="時", ge=-1, le=23, choices=[i for i in range(0,24,1)]),
                min: int = commands.Param(default=-1, name="分", ge=-1, le=59, choices=[i for i in range(0,60,10)]),
                description: str = commands.Param(name="備考", default="")):
        """
        オタカラハントの募集を行います

        Parameters
        ----------
        at: 募集人数
        hour: 開始時刻(時)
        min: 開始時刻(分)
        description: 補足事項
        """
        at = f'@{at}' if at else ''

        await create_lfg(
            bot = self.bot,
            inter = inter,
            genre = 'splatoon',
            content = f'オタカラハント',
            at = at,
            color = 0x17CFAE,
            hour = hour,
            min = min,
            description = description
        )

def setup(bot: commands.Bot):
    bot.add_cog(RaidersCommand(bot))
