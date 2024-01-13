from disnake.ext import commands
import textwrap


class HelpCommand(commands.Cog):
    """スラッシュコマンドサンプル:Ping"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="ヘルプ")
    async def help(self, inter):
        """募集コマンドのヘルプを表示します.これはあなただけに表示されます."""
        help_text = textwrap.dedent("""\
        [募集コマンド]
        ・/○○ に続いて、各パラメータを設定することで募集投稿ができます
        --スプラトゥーン募集
          - /オープン
          - /オープンorプラベ
          - /イベント
          - /プラべ
          - /ナワバリ
          - /しゃけ
          - /ナワバトラー
          - /フェス
          - /対抗戦
          - /スプラなんでも
        --他ゲーム募集
          - /他ゲー
        --雑談・自習募集
          - /雑談
        
        [募集に対するリアクション]
        ・自身が設定した募集投稿にリアクションをつけることで、内容を編集/削除できます。
         - 募集削除：　　:x:
         - 募集の〆：　　:end:
         - 募集人数変更：:one:～:nine:
        """)
        await inter.response.send_message(help_text, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(HelpCommand(bot))
