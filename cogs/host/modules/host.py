import disnake
from disnake.ext import commands
from typing import Optional
from replit import db
import json
import datetime
import re

# 募集投稿を行う
async def host(
        bot: commands.Bot,
        inter: disnake.ApplicationCommandInteraction,
        genre: str,  # チャンネル分けのkeyになるジャンル
        content: str,  # 募集内容(ex.'リグマ')
        color: int = 0x000000,  # 埋め込みに使う色
        at: str = '',  # 募集人数(ex.'@3')
        hour: Optional[int] = None,  # 開始時刻(時)
        min: Optional[int] = None,  # 開始時刻(分)
        description: str = ''  # 備考
):   
    await inter.response.defer(with_message=False, ephemeral=True)
    at_nums = re.findall(r"\d+", at)
    at_max_num = int(at_nums[-1]) if at_nums else None
    start_time = f"{get_start_time(hour,min)}～"
    # DBに該当ギルドの設定ファイルがあるか
    if str(inter.guild.id) in db.keys():
        # ある場合は設定ファイルをロード
        cfg = json.loads(db[str(inter.guild_id)])
        # 設定ファイルに投稿先チャンネルの設定があるか
        if "send_channel_ids" in cfg and genre in cfg["send_channel_ids"]:
            # ある場合はチャンネルをロード
            send_channel = bot.get_channel(cfg["send_channel_ids"][genre])
            if send_channel:
                # コマンドに対して反応する
                await inter.followup.send("募集を設定しました", ephemeral=True)
                # 埋め込みリンクの設定
                embed = disnake.Embed(title=f'{content}{at}',
                                      description=description,
                                      color=color)
                embed.set_author(name=inter.author.display_name,
                                 icon_url=inter.author.display_avatar.url)
                embed.add_field(name="Start",
                                value=start_time)

                # 指定チャンネルに投稿する
                msg = await send_channel.send(
                    f"[{start_time}] {content}{at} by {inter.author.display_name}",
                    embed=embed)

                # リアクション処理
                try:
                    # 作成者のリアクションを受け取る
                    def check(reaction, user):
                        return user == inter.author and reaction.message == msg

                    while True:
                        reaction, user = await bot.wait_for('reaction_add',
                                                            check=check)
                        # # 削除
                        # if ord(reaction.emoji[0]) in (0x274c, 0x2716):
                        #     await msg.delete()

                        # 人数編集
                        if ord(reaction.emoji[0]) in (0x0031 + i
                                                        for i in range(10)):
                            num = int(reaction.emoji[0])
                            if (not at_max_num) or (at_max_num
                                                    and num < at_max_num):
                                at = f'@{num}'
                                embed = disnake.Embed(title=f'{content}{at}',
                                                      description=description,
                                                      color=color)
                                embed.set_author(
                                    name=inter.author.display_name,
                                    icon_url=inter.author.display_avatar.url)
                                embed.add_field(
                                    name="Start",
                                    value=start_time)
                                await msg.edit(
                                    f"[{start_time}] {content}{at} by {inter.author.display_name}",
                                    embed=embed)
                        # 〆
                        elif ord(reaction.emoji[0]) == 0x1f51a:
                            embed = disnake.Embed(title=f'(〆){content}{at}',
                                                  description=description,
                                                  color=color)
                            embed.set_author(name=inter.author.display_name,
                                             icon_url=inter.author.display_avatar.url)
                            embed.add_field(
                                name="Start",
                                value=start_time)
                            await msg.edit(
                                f"(〆) [{start_time}] {content}{at} by {inter.author.display_name}",
                                embed=embed)
                        else:
                            continue
                except Exception as e:
                    print('=== エラー内容 ===')
                    print('type:' + str(type(e)))
                    print('args:' + str(e.args))
                    print('e自身:' + str(e))
        

    await inter.followup.send(
        f"エラー：設定テキストチャンネルが見つかりません…\n/通知設定 で送信先チャンネルを設定してください", ephemeral=True)

def get_start_time(h: int, m: int):
    if h == -1:
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        time = dt.time()
    elif h != -1 and m == -1:
        time = datetime.time(h, 0)
    else:
        time = datetime.time(h, m)
    return time.strftime('%H:%M')
