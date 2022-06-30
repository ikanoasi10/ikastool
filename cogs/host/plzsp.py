import disnake
from disnake.ext import commands
from .modules.host import host


class PlzspCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="対抗戦")
    async def plzsp(self, inter):
        pass

    @plzsp.sub_command(name="味方")
    async def plzsp_good_guys(
        self,
        inter: disnake.ApplicationCommandInteraction,
        at: str = commands.Param(
            default="",
            name="at",
            choices=([str(i) for i in reversed(range(1, 3 + 1))])),
        power: str = commands.Param(default="", name="凸パワー帯"),
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
        対抗戦の味方募集を行います

        Parameters
        ----------
        at: 募集人数
        power: 凸パワー帯
        hour: 開始時刻(時)
        min: 開始時刻(分)
        description: 補足事項(編成情報やブキ,パワー希望など)
        """
        at = f'@{at}' if at else ''

        await host(bot=self.bot,
                   inter=inter,
                   genre='splatoon',
                   content=f'対抗戦味方',
                   at=at,
                   color=0x5f04e5,
                   hour=hour,
                   min=min,
                   description=f"{power}\n{description}")

    @plzsp.sub_command(name="相手")
    async def plzsp_bad_guys(
        self,
        inter: disnake.ApplicationCommandInteraction,
        at: str = commands.Param(
            default="",
            name="at",
            choices=([str(i) for i in reversed(range(1, 4 + 1))] + ["1チーム"])),
        power: str = commands.Param(default="", name="パワー帯"),
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
        対抗戦の相手募集を行います

        Parameters
        ----------
        at: 募集人数orチーム
        power: パワー帯についての情報
        hour: 開始時刻(時)
        min: 開始時刻(分)
        description: 補足事項(ルールなど)
        """
        at = f'@{at}' if at else ''

        await host(bot=self.bot,
                   inter=inter,
                   genre='splatoon',
                   content=f'対抗戦相手',
                   at=at,
                   color=0x5f04e5,
                   hour=hour,
                   min=min,
                   description=f"{power}\n{description}")


def setup(bot: commands.Bot):
    bot.add_cog(PlzspCommand(bot))
