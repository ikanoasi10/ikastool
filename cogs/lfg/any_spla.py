import disnake
from disnake.ext import commands
from .modules.create_lfg import create_lfg

class AnySplaCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="スプラなんでも")
    async def any_spla(self,
                inter: disnake.ApplicationCommandInteraction,
                at: str = commands.Param(default="", name="at", choices=(["∞"]+[str(i) for i in reversed(range(1, 9 + 1))])),
                hour: int = commands.Param(default=-1, name="時", ge=-1, le=23, choices=[i for i in range(0,24,1)]),
                min: int = commands.Param(default=-1, name="分", ge=-1, le=59, choices=[i for i in range(0,60,10)]),
                description: str = commands.Param(name="備考", default="")):
        """
        スプラトゥーンの募集を行います

        Parameters
        ----------
        at: (最低)募集人数
        hour: 開始時刻(時)
        min: 開始時刻(分)
        description: 備考(補足事項)
        """
                    
        at = f'@{at}' if at else ''
        
        await create_lfg(
            bot = self.bot,
            inter = inter,
            genre = 'splatoon',
            content = f'スプラなんでも',
            at = at,
            color = 0xd0f721,
            hour = hour,
            min = min,
            description = description
        )

def setup(bot: commands.Bot):
    bot.add_cog(AnySplaCommand(bot))
