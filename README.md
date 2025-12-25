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
<br>

# ■ボタンの追加・削除方法
現状、目についたエフェクトを片っ端から追加したので、ボタンだらけになってます。<br>
そこで、個人でカスタマイズしたい人向けに、新たにエフェクトを追加する方法と
表示されてるボタンを減らす方法について説明します。<br>

## ボタンの追加方法
<br>
①アイコンとなる画像を`icon`フォルダに入れます。（アイコンサイズ32px）<br>
　アイコンは頑張って作ってください！<br>
<br>
<img width="645" height="320" alt="image" src="https://github.com/user-attachments/assets/ca023d47-3ee8-4b87-a252-93d46c1b4841" /><br>

<br>
<img width="37" height="34" alt="image" src="https://github.com/user-attachments/assets/81376042-4ba5-4bcc-b4f0-4b7b0203b440" /><br>
TEST.png<br><br>


②`addEffectButton.py`を開き、`effect_info_map`変数を見つけ出し、それに追加したいエフェクト情報を入力します。<br>
　入力する内容としては、下記の四つです。<br>
 <br>


1. エフェクトの名前（ホバーしたときに表示されるだけなので正直なんでもいい）<br>
2. アイコンのファイル名<br>
3. フィルター or ジェネレーター<br>
4. 検索する際に使うやつ<br>

<img width="579" height="115" alt="image" src="https://github.com/user-attachments/assets/2726debb-cd36-4a10-82f6-4d05e205dab3" /><br>


試しに、`effect_info_map`変数の一番下にフィルターの`Blur Directional`を追加してみます。<br>
（追加する場所によってボタンが表示される位置が変わってくるので注意）<br>

追加したのがこちら<br>
<img width="486" height="104" alt="image" src="https://github.com/user-attachments/assets/9e508e48-ba96-434d-81ea-1a598c5166e8" /><br><br>

③あとは変更したソースコードを保存し、Substance painter上で、プラグインフォルダをリロードします。<br>
　addEffectButtonがすでに有効になっている場合は、無効にして再度有効にするとボタンが表示されると思います。<br>
　以上が追加方法でした！<br>
<br>
<img width="303" height="384" alt="image" src="https://github.com/user-attachments/assets/a22398e9-2c95-4a01-af19-f783a689e19d" />


## ボタンの削除方法<br>
削除方法は簡単で、`effect_info_map`変数の中身をコメントアウトするか、削除することでボタンが表示されなくなります。<br>
コメントアウトは、コードの前に`#` を付けることでできます。<br><br>

WhiteMaskからGeneratorまでをコメントアウトした状態で、再リロードすると<br>
<img width="428" height="781" alt="image" src="https://github.com/user-attachments/assets/a7580897-b157-455e-b470-39033e0da349" />

<br>

ボタンの数を減らすことができます。<br>
<img width="1111" height="422" alt="image" src="https://github.com/user-attachments/assets/d1fa2ffa-d902-4344-b4d0-e85be0b8a731" />

<br>



