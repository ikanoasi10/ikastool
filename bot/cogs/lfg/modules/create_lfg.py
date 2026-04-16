import disnake
from disnake.ext import commands
from typing import Optional
from sqlitedict import SqliteDict
import requests
import json
import datetime
import re
import traceback

db = SqliteDict("db.sqlite3", autocommit=True)


# 募集投稿を行う
async def create_lfg(
    bot: commands.Bot,
    inter: disnake.ApplicationCommandInteraction,
    genre: str,  # チャンネル分けのkeyになるジャンル
    content: str,  # 募集内容(ex.'オープン')
    color: int = 0x000000,  # 埋め込みに使う色
    at: str = "",  # 募集人数(ex.'@3')
    hour: Optional[int] = None,  # 開始時刻(時)
    min: Optional[int] = None,  # 開始時刻(分)
    description: str = "",  # 備考
    is_thread: bool = False,  # フォーラムorスレッド
):
    # コマンドしたユーザへの返信予約
    await inter.response.defer(with_message=False, ephemeral=True)

    # 埋め込み用ステータス
    color = getColor(content) if color == 0x000000 else color
    at_nums = re.findall(r"\d+", at)
    at_max_num = int(at_nums[-1]) if at_nums else None
    start_time = f"{get_start_time(hour, min)}～"

    try:
        # DBに該当ギルドの設定ファイルがあるか
        if not str(inter.guild.id) in db.keys():
            raise Exception
        # ある場合は設定ファイルをロード
        cfg = json.loads(db[str(inter.guild_id)])
        debug("db loaded")
        # 設定ファイルに投稿先チャンネルの設定があるか
        if not ("send_channel_ids" in cfg and genre in cfg["send_channel_ids"]):
            raise Exception
        # ある場合はチャンネルをロード
        send_channel = bot.get_channel(cfg["send_channel_ids"][genre])
        debug("text ch cfg file loaded")
        if not send_channel:
            raise Exception
        debug("detect send_channnel")

        #  設定ファイルに投稿先フォーラムチャンネルの設定があるか
        if not is_thread:
            if not ("forum_channel_ids" in cfg and genre in cfg["forum_channel_ids"]):
                raise Exception
            # ある場合はチャンネルをロード
            forum_channel = bot.get_channel(cfg["forum_channel_ids"][genre])
            debug("forum ch cfg file loaded")

            if not forum_channel:
                raise Exception
        debug("detect forum_channel")

        # コマンドに対して反応する
        if is_thread:
            await inter.followup.send(
                "募集を設定しました。\nメッセージ通知を受け取るには、作成したスレッドに書きこみをしてください```\nリアクションで編集できます\n❌：募集取消\n1️⃣2️⃣…：人数変更\n🔚：〆をつける\n```",
                ephemeral=True,
            )
        else:
            # コマンドに対して反応する
            await inter.followup.send(
                "募集を設定しました。\nメッセージ通知を受け取るには、作成したスレッドを開いて「フォローする」を押してください```\nリアクションで編集できます\n❌：募集取消\n1️⃣2️⃣…：人数変更\n🔚：〆をつける\n```",
                ephemeral=True,
            )
        debug("command response")

        # 埋め込みの設定
        embed = disnake.Embed(
            title=f"{content}{at}", description=f"{description}", color=color
        )
        embed.set_author(
            name=inter.author.display_name, icon_url=inter.author.display_avatar.url
        )
        embed.add_field(name="Start", value=start_time)

        # フォーラム募集の場合
        if not is_thread:
            # タグの設定
            tags = forum_channel.available_tags
            forum_thread_tag_name = {
                "splatoon": "スプラトゥーン募集",
                "others": "他ゲーム募集",
                "study": "自習・雑談募集",
            }[genre]
            forum_thread_tag = forum_channel.get_tag_by_name(forum_thread_tag_name)
            if forum_thread_tag is None:
                tags.append(disnake.ForumTag(name=forum_thread_tag_name))
                await forum_channel.edit(available_tags=tags)
                forum_thread_tag = forum_channel.get_tag_by_name(forum_thread_tag_name)
            # フォーラム投稿用埋め込み
            forum_thread_embed = embed.copy()

            # フォーラムに投稿作成
            forum_thread, forum_thread_msg = await forum_channel.create_thread(
                name=f"[{start_time}] {content}",
                content=f"[{start_time}] {content}{at} by {inter.author.display_name}",
                embed=forum_thread_embed,
                auto_archive_duration=60,
                applied_tags=[forum_thread_tag],
            )

            # 募集チャンネル用埋め込みを更新
            embed.url = forum_thread.jump_url
            embed.add_field(
                name="スレッド", value=f"<#{forum_thread.id}>", inline=False
            )

        # 募集チャンネルに投稿する
        msg = await send_channel.send(
            f"[{start_time}] {content}{at} by {inter.author.display_name}", embed=embed
        )
        debug("send message finished")

        if is_thread:
            # スレッド作成
            await send_channel.create_thread(
                name=f"[{start_time}] {content}", message=msg, auto_archive_duration=60
            )

        # リアクション処理
        # 作成者のリアクションを受け取る
        def check(reaction, user):
            return user == inter.author and reaction.message == msg

        reaction, user = await bot.wait_for("reaction_add", check=check)
        # # 削除
        # if ord(reaction.emoji[0]) in (0x274c, 0x2716):
        #     if not is_thread:
        #         await forum_thread.delete()
        #     await msg.delete()

        # 人数の編集
        if ord(reaction.emoji[0]) in (0x0031 + i for i in range(10)):
            num = int(reaction.emoji[0])
            if (not at_max_num) or (at_max_num and num < at_max_num):
                at = f"@{num}"
                embed.title = f"{content}{at}"
                await msg.edit(
                    f"[{start_time}] {content}{at} by {inter.author.display_name}",
                    embed=embed,
                )
                if not is_thread:
                    await forum_thread_msg.edit(
                        f"[{start_time}] {content}{at} by {inter.author.display_name}",
                        embed=forum_thread_embed,
                    )
                reaction, user = await bot.wait_for("reaction_add", check=check)
        # 〆
        if ord(reaction.emoji[0]) == 0x1F51A:
            embed.title = f"(〆){content}{at}"
            await msg.edit(
                f"(〆) [{start_time}] {content}{at} by {inter.author.display_name}",
                embed=embed,
            )
            if not is_thread:
                await forum_thread_msg.edit(
                    f"(〆) [{start_time}] {content}{at} by {inter.author.display_name}",
                    embed=forum_thread_embed,
                )
            reaction, user = await bot.wait_for("reaction_add", check=check)
        else:
            reaction, user = await bot.wait_for("reaction_add", check=check)
    except Exception:
        print(traceback.format_exc())
        await inter.followup.send(
            f"エラー：投稿作成先となるチャンネルが見つかりません…\n/通知設定 で投稿先チャンネルを設定してください",
            ephemeral=True,
        )


def get_start_time(h: int, m: int):
    if h == -1:
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        time = dt.time()
    elif h != -1 and m == -1:
        time = datetime.time(h, 0)
    else:
        time = datetime.time(h, m)
    return time.strftime("%H:%M")


def getColor(word):
    url = "https://kotoba-palette.takanakahiko.me/api/getColors"
    try:
        res = requests.get(url, params={"word": word}, timeout=5)
        data = res.json()
        max_population = 0
        max_population_color = None
        for key, value in data.items():
            if key not in ["DarkMuted", "LightMuted"]:
                if value["population"] > max_population:
                    max_population = value["population"]
                    max_population_color = value["rgb"]
            r, g, b = max_population_color
        return int(f"{r:02x}{g:02x}{b:02x}", 16)
    except:
        return 0xFFFFFF


def debug(s):
    dt = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    now = dt.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {s}")
    return
