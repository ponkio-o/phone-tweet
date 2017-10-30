<?php
// 録音ファイルURLの取得
$recordingUrl = $_GET['RecordingUrl'];
$recordingUrl .= ".wav";

//録音ファイルの保存
$cmd = "wget -N -O ./record.wav $recordingUrl";
exec("$cmd");

//ツイート処理
$cmd2 = "python ./tweet.py";
exec("$cmd2");

//TwiMLを返す
echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
echo '<Response>';
echo '<Say voice="woman" language="ja-jp">';
  echo '終了します。';
echo '</Say>';
echo '<Hangup/>';
echo '</Response>';

?>
