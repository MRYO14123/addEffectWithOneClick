# サンプル動画
https://github.com/user-attachments/assets/5a5a4efb-03df-41ef-be8e-9f1d15bbe2dc


# 利用方法
1. ソースコードとiconフォルダをダウンロードします。
2. Substance Painterの「Pythonタブ＞Plugins Folder」をクリックします。
3. フォルダ内のpluginsフォルダを開き、ダウンロードしてきたiconフォルダとaddEffectButton.py を置きます。
4. Substance Painter「Reload Plugins Folder」をクリックし、「addEffectButon」スクリプトを有効にすると使えます。

<br>
3のファイル配置イメージ<br>
<img width="781" height="231" alt="image" src="https://github.com/user-attachments/assets/0a19f2c5-50bc-4e09-a677-28b222eb8702" />
<br>
<br>


4スクリプトの有効化<br>
<img width="301" height="118" alt="image" src="https://github.com/user-attachments/assets/7d9f53a7-086e-490c-91af-424a5b283c3e" />
<br>
<br>



#### ■できること

<span style="color: #000000; ">・ワンクリックでレイヤー、マスク、エフェクトを追加<br>・エフェクト追加は、新規レイヤー / 既存レイヤーどちらにも対応<br>・複数選択にエフェクト追加<br>
・塗りつぶしレイヤー、ペイントレイヤーにもエフェクトを追加可能</span>


#### ■機能

**・新規追加ボタン**<br>
ON：新規で塗りつぶしレイヤーとマスクを追加します。<br>
　　マスクに任意で選択したエフェクトを付与します。<br>
OFF：選択しているレイヤーにマスクとエフェクトを付与します。<br>
　　レイヤーが選択されていない場合は、動作しません。<br>

**・塗りつぶしレイヤーボタン**<br>
有効な時、塗りつぶしレイヤーにエフェクトを付与します。<br>
この時、マスクは付与されません。<br>

**・マスクレイヤーボタン**<br>
有効な時、レイヤーのマスクに対してエフェクトを付与します。<br>
レイヤーにマスクが付いていない場合、合わせてマスクも作成します。<br>
