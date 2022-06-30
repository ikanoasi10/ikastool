import disnake
from disnake.ext import commands
from .modules.host import host


class StudyChatCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="雑談")
    async def study_chat(
        self,
        inter: disnake.ApplicationCommandInteraction,
        title: str = commands.Param(default="雑談", name="題名"),
        at: str = commands.Param(default="", name="at"),
        hour: int = commands.Param(default=-1,
                                   name="時",
                                   ge=-1,
                                   le=23,
                                   choices=[i for i in range(0, 24, 1)]),
        min: int = commands.Param(default=-1,
                                  name="分",
                                  ge=-1,
                                  le=59,
                                  choices=[i for i in range(0, 60, 10)]),
        description: str = commands.Param(name="備考", default="")):
        """
        雑談・勉強会の募集を行います

        Parameters
        ----------
        title:話題(雑談 or 課題名など)
        at: 募集人数
        hour: 開始時刻(時)
        min: 開始時刻(分)
        description: 補足事項
        """
        at = f'@{at}' if at else ''

        await host(bot=self.bot,
                   inter=inter,
                   genre='study',
                   content=title,
                   at=at,
                   color=0xffffff,
                   hour=hour,
                   min=min,
                   description=description)

    @study_chat.autocomplete("at")
    async def at_autocomp(self, inter, string: str):
        return [n for n in ["∞"] if string in n]


def setup(bot: commands.Bot):
    bot.add_cog(StudyChatCommand(bot))
