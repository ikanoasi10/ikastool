// 注：これはGoogle Apps Script用のファイルです。

// https://hoge.fuga.repl.coを入れる
const SERVER = "YOUR_REPLIT_URL"

// この関数をGASの定期実行トリガーで1分おきに叩く
function wake(){
  const json = {
    'type': 'wake'
  };
  sendRequest(SERVER, json)
}

function sendRequest(uri, json){
  const params = {
    'contentType':'application/json; charset=utf-8',
    'method':'post',
    'payload':json,
    'muteHttpExceptions':true
  };
  response = UrlFetchApp.fetch(uri, params);
}