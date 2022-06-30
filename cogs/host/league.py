import disnake
from disnake.ext import commands
from .modules.host import host

class LeagueCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="リグマ")
    async def league(self,
                inter: disnake.ApplicationCommandInteraction,
                at: str = commands.Param(default="", name="at", choices=(["1-3"] + [str(i) for i in reversed(range(1, 3 + 1))])),
                type: str = commands.Param(default="",name="チームorペア", choices=(["チーム","ペア"])),
                hour: int = commands.Param(default=-1, name="時", ge=-1, le=23, choices=[i for i in range(0,24,1)]),
                min: int = commands.Param(default=-1, name="分", ge=-1, le=59, choices=[i for i in range(0,60,10)]),
                description: str = commands.Param(name="備考", default="")):
        """
        リーグマッチの募集を行います

        Parameters
        ----------
        at: 募集人数
        type:チーム(4リグ)またはペア(2リグ)
        hour: 開始時刻(時)
        min: 開始時刻(分)
        description: 補足事項
        """
        type = f'({type})' if type else ''
        at = f'@{at}' if at else ''
        
        await host(
            bot = self.bot,
            inter = inter,
            genre = 'splatoon',
            content = f'リグマ{type}',
            at = at,
            color = 0xf02d7d,
            hour = hour,
            min = min,
            description = description
        )

def setup(bot: commands.Bot):
    bot.add_cog(LeagueCommand(bot))
