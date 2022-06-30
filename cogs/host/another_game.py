import disnake
from disnake.ext import commands
from .modules.host import host

class AnotherGameCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="他ゲー")
    async def another_game(self,
                inter: disnake.ApplicationCommandInteraction,
                game: str = commands.Param(name="ゲーム名"),
                at: str = commands.Param(default="", name="at"),
                hour: int = commands.Param(default=-1, name="時", ge=-1, le=23, choices=[i for i in range(0,24,1)]),
                min: int = commands.Param(default=-1, name="分", ge=-1, le=59, choices=[i for i in range(0,60,10)]),
                description: str = commands.Param(name="備考", default="")):
        """
        スプラトゥーン以外のゲームの募集を行います

        Parameters
        ----------
        game:募集するゲーム
        at: 募集人数
        hour: 開始時刻(時)
        min: 開始時刻(分)
        description: 補足事項
        """
        at = f'@{at}' if at else ''
        
        await host(
            bot = self.bot,
            inter = inter,
            genre = 'others',
            content = game,
            at = at,
            color = 0xffffff,
            hour = hour,
            min = min,
            description = description
        )

    @another_game.autocomplete("at")
    async def at_autocomp(self, inter, string: str):
        return [str(n) for n in list(range(1, 10, 1))+["∞"] if string in str(n)]

def setup(bot: commands.Bot):
    bot.add_cog(AnotherGameCommand(bot))
