# Ikastool

スプラトゥーン等の募集を通知する Discord bot  
一応複数サーバで動くように作ってあります
replit+GASでの運用を想定しています。

## 機能(未更新)
### 通知設定・解除
- /通知設定 [ジャンル] [テキストチャンネル]
  - [ジャンル]の募集メッセージ投稿先を[テキストチャンネル]に設定します
- /通知解除 [ジャンル]
  - [ジャンル]の募集メッセージ投稿先の設定を解除します
### 募集
それぞれ募集をかけます
- スプラトゥーン
  - /リグマ
  - /プラべ
  - /ナワバリ
  - /サモラン
  - /フェス
  - /対抗戦
  - /スプラなんでも
- 他ゲーム
  - /他ゲー
- 雑談・自習
  - /雑談

コマンド送信者（募集設定者）は募集にリアクションをつけることで後から変更を加えることができます  
:x:で削除、:one:～:nine:で@の人数変更、:end:で募集を〆ることができます

### その他
180日以上スラッシュコマンドが使われていないサーバーのデータは随時データベースから削除されます  
削除された場合は再度通知登録等を行ってください



## ファイル構成

    main.py・・・botの低層処理。Discordとの接続, Cogの登録, DB更新など   
    
    cogs・・・各コマンドの具体的な処理  
    └host・・・募集をかけるコマンド
      └modules
            └host.py・・・募集処理
      └another_game.py
        ...
      └turf_war.py
    └dettachchannel.py・・・/通知解除 
    └echo.py・・・/echo (sample)  
    └ping.py・・・/ping (sample)  
    └setchannnel.py・・・/通知設定  

defaultcfg.py・・・デフォルトで記録する設定ファイルの形式  

gas-code.js・・・Google Apps Script用のコード

server.py・・・replitサーバ接続処理

---
各cogの内容はそれぞれこんな感じ  
| Cog | 処理 |
| :-: | :-: |
| setchannel | 通知チャンネルを設定し、DBに書き込む |
| dettachchannel | DBの通知チャンネル設定を解除する |
| host/hoge.py | DBからジャンルに応じた通知チャンネルを取得し、投稿で通知する。<br>元の書き込みを行った人が特定のリアクションをつけたらそれに応じた処理を行う。 |

## 動かし方

1. botのトークンを入手(scopeはbotとapplication.commands,permissionsはsend messagesとembed linksがあればおそらく大丈夫)
2. トークンを環境変数の`TOKEN`に設定する(鍵マークからできる)
3. main.pyの`test_guilds=[...]`にテスト用のギルドIDを入力する
5. Google Apps Scriptにgas-code.jsをコピペしてウェブアプリとしてデプロイ
6. `SERVER`にURLを入れて定期実行トリガーで`wake()`を1分ごとに叩く
7. 招待リンクから招待したら動くハズ
  
## Note
  
環境変数とreplitDB以外は公開されることに注意してください  
