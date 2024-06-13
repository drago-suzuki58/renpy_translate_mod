# RenPy Translate Mod

## 事前準備

Pythonをインストールし、```pip install -r requirements.txt```とコマンドを打ってください。

## 注意点

動作確認済のPythonバージョンは3.10です。Python2では動きません。

RenPyのバージョンによってはPython2でしか動作しないものもあるので、ゲームからのセリフ抽出のみPython2でも対応していますが動作の保証はできません。

## コマンド説明

### 基本

#### 基本構文

このフォルダでコマンドプロンプトを開いて

``` bash
python main.py {mode}
```

モードについては後にある解説を参照してください。

#### ヘルプ

``` bash
python main.py -h
python main.py --help
```

また、各モードについてのヘルプテキストを知りたい場合は

``` bash
python main.py {mode} -h
python main.py {mode} --help
```

### 設定

このプログラムでは、設定ファイルを操作することにより長いコマンドを毎回打たなくても設定を直接変えられるようになっています。

```modules/settings.py```をテキストエディタ等で開いて編集してください。

これより先の説明では対応した変数名を表記しますので、それを参照してください。

### ログオプション

```--log```(```-l```)

このプログラム全体におけるログが有効化されます。  
デフォルト値：```False```  
設定：```LOG_ENABLED```

```--log_file```(```-lf```)

ログファイルの名前を変更できます。  
デフォルト値：```'log.txt'```  
設定：```LOG_FILE```

```--log_level```(```-lv```)

出力されるログファイルのログレベルを変更できます。  
ログレベルは5つあり、```DEBUG, INFO, WARNING, ERROR, CRITICAL``` です。この5つ以外が挿入された場合は正常に動作しません。  
デフォルト値：```'INFO'```  
設定：```LOG_LEVEL```

ログオプションは、必ずmodeよりも前に入れる必要があります。  
例：

``` bash
python main.py --log --log_level DEBUG {mode}
python main.py --l {mode}
```

### モード

#### tsv_translate

このモードでは、ツールで取得したゲーム内のセリフ一覧TSVを利用して自動翻訳をして結果を出力します。  
変数名や特殊なタグなどは翻訳されないようにエスケープされ、翻訳後に復元されます。  
入力ファイルと出力ファイルのどちらも以下の形式になります。(タブはスペース4つで表記)  

``` tsv
filename    linenumber    identifier    contents
```

##### オプション

```--input```(```-i```)

このプログラムの入力ファイルの名前を変更できます。  
入力ファイルの形式は、先述の形式と同じものでなければなりません。  
デフォルト値：```'untranslated.tsv'```  
設定：```TSV_TRANSLATE_INPUT```

```--output```(```-o```)

このプログラムの出力ファイルの名前を変更できます。  
デフォルト値：```'translated.tsv'```  
設定：```TSV_TRANSLATE_OUTPUT```

```--fromlang```(```-fr```)

このプログラムの翻訳前言語を変更できます。  
入力は、Google翻訳で使用される言語コードを用いてください。  
デフォルト値：```'en'```  
設定：```FROM_LANG```

```--tolang```(```-to```)

このプログラムの翻訳後言語を変更できます。  
入力は、同じくGoogle翻訳で使用される言語コードを用いてください。  
デフォルト値：```'ja'```  
設定：```TO_LANG```

```--target```(```-t```)

翻訳の対象とするファイル名を複数指定できます。  
inputオプションとは異なり、TSVの中のfilenameを参照しています。  
ファイル例(タブはスペース4つで表記)  

``` tsv
filename    linenumber    identifier    contents
game/scene1.rpy    15    scene1_sample1    a "sample1"
game/scene1.rpy    16    scene1_sample2    a "sample2"
game/scene1.rpy    18    scene1_sample3    b "sample3"
game/scene2.rpy    19    scene1_sample4    c "sample4"
game/scene2.rpy    20    scene1_sample5    b "sample5"
```

この場合、```--target game/scene1.rpy```と入力すれば```game/scene1.rpy```のセリフのみが翻訳され、```game/scene2.rpy```などの他のファイルは翻訳されません。  
また、```--target game/scene1.rpy game/scene2.rpy```で複数ファイルの選択ができます。  
なお、このオプションを使用しなければ自動で全てのファイルが読み込まれて全て翻訳されます。  
デフォルト値：```[]```  
設定：```TARGET```

```--start_line```(```-sl```)

翻訳を開始する行数を指定することができます。  
ヘッダー行は含まず、データの中身の行数だけで認識するので気をつけてください。

例：```python main.py tsv_translate -sl 3```

翻訳前ファイル(タブはスペース4つで表記)

``` tsv
filename    linenumber    identifier    contents
game/scene1.rpy    15    scene1_sample1    a "sample1"
game/scene1.rpy    16    scene1_sample2    a "sample2"
game/scene1.rpy    18    scene1_sample3    b "sample3"
game/scene2.rpy    19    scene1_sample4    c "sample4"
game/scene2.rpy    20    scene1_sample5    b "sample5"
```

翻訳後ファイル

``` tsv
filename    linenumber    identifier    contents
game/scene1.rpy    18    scene1_sample3    b "サンプル3"
game/scene2.rpy    19    scene1_sample4    c "サンプル4"
game/scene2.rpy    20    scene1_sample5    b "サンプル5"
```

デフォルト値：```0```  
設定：```START_LINE```

##### 使用例

``` bash
python main.py tsv_translate -i example.tsv -fr en -t game/scene1.rpy game/scene2.rpy
python main.py -l tsv_translate
```

#### tsv2rpy

このモードでは、以下の形式で保存されているTSVファイルを読み込み、以下のRenPyが読み取れるファイル形式に変換します。

TSV

``` tsv
filename    linenumber    identifier    contents
```

RenPy

``` rpy
translate {tl_lang} {identifier}:

    {contents}
```

##### オプション

```--input```(```-i```)

このプログラムの入力ファイルの名前を変更できます。  
入力ファイルの形式は、先述の形式と同じものでなければなりません。  
デフォルト値：```'translated.tsv'```  
設定：```TSV2RPY_INPUT```

```--output```(```-o```)

このプログラムの出力ファイルの名前を変更できます。  
デフォルト値：```'converted.rpy'```  
設定：```TSV2RPY_OUTPUT```

```--tl_lang```(```-tl```)

出力ファイルに記載する、RenPyが認識できるゲーム固有の言語名を変更できます。  
大抵の場合、デフォルトでも動くと思いますが、一部のゲームでは異なる場合があるので適宜変更してください。  
デフォルト値：```'japanese'```  
設定：```TL_LANG```

```--comment```(```-c```)

出力ファイル内の翻訳支援用の、行数やファイル名に関するコメントをつけるかどうかを変更できます。  
Falseの場合の例

``` rpy
translate japanese scene1_sample1:

    a "sample1"

translate japanese scene1_sample2:

    a "sample2"

translate japanese scene1_sample3:

    b "sample3"

```

Trueの場合の例

``` rpy
# game/scene1.rpy
# line:15
translate japanese scene1_sample1:

    a "sample1"

# line:16
translate japanese scene1_sample2:

    a "sample2"

# line:18
translate japanese scene1_sample3:

    b "sample3"
```

デフォルト値：```False```  
設定：```COMMENT```

```--split_file```(```-sf```)

TSV一番左の```filename```に応じて、出力するファイルを変更することができるようになり、分割したファイルの生成ができるようになります。  
デフォルト値：```False```  
設定：```SPLIT_FILE```

```--split_prefix```(```-sp```)

分割するファイルにつける接頭詞を変更できます。  
デフォルト値：```'convert_'```  
設定：```SPLIT_PREFIX```

##### 使用例

``` bash
python main.py tsv2rpy -o example.rpy -tl japanesetl -c
python main.py tsv2rpy -i edited.tsv
```

#### extract_menu

このモードでは、逆コンパイルやそのままコンパイルなどされていない```.rpy```拡張子のファイルから、```menu:```ラベルの中から選択肢を全て抽出し、TSVファイルに保存します。  

出力は以下の通りです。(タブはスペース4つで表記)

``` tsv
filename    linenumber    choice    translated
```

このモードでは、他のモードとの互換性のために4つめの項目にtranslatedというのを指定していますが、実際のところはそれにあたるデータがないので、全て```Untranslated```という文字列が入ります。

##### オプション

```--input```(```-i```)

このプログラムの入力ファイルの名前を複数指定できます。  
リストが空の場合は、実行しているフォルダと、その下層の全てのフォルダを探索して全ての選択肢を抽出します。  
デフォルト値：```[]```  
設定：```EXTRACT_MENU_INPUT```

```--output```(```-o```)

このプログラムの出力ファイルの名前を変更できます。  
デフォルト値：```'menu_untranslated.tsv'```  
設定：```EXTRACT_MENU_OUTPUT```

##### 使用例

``` bash
python main.py extract_menu -i scene1.rpy
python main.py extract_menu -o output.tsv
```

#### tsv_translate_menu

このモードでは、ツールで取得したゲーム内のセリフ一覧TSVを利用して自動翻訳をして結果を出力します。  
変数名や特殊なタグなどは翻訳されないようにエスケープされ、翻訳後に復元されます。  
入力ファイルと出力ファイルのどちらも以下の形式になります。(タブはスペース4つで表記)  

``` tsv
filename    linenumber    choice    translated
```

ほぼ、先述の```tsv_translate```モードと同じで、入力出力ファイルが異なるだけです。

##### オプション

```--input```(```-i```)

このプログラムの入力ファイルの名前を変更できます。  
入力ファイルの形式は、先述の形式と同じものでなければなりません。  
デフォルト値：```'menu_untranslated.tsv'```  
設定：```MENU_TSV_TRANSLATE_INPUT```

```--output```(```-o```)

このプログラムの出力ファイルの名前を変更できます。  
デフォルト値：```'menu_translated.tsv'```  
設定：```MENU_TSV_TRANSLATE_OUTPUT```

```--fromlang```(```-fr```)

このプログラムの翻訳前言語を変更できます。  
入力は、Google翻訳で使用される言語コードを用いてください。  
デフォルト値：```'en'```  
設定：```FROM_LANG```

```--tolang```(```-to```)

このプログラムの翻訳後言語を変更できます。  
入力は、同じくGoogle翻訳で使用される言語コードを用いてください。  
デフォルト値：```'ja'```  
設定：```TO_LANG```

```--target```(```-t```)

翻訳の対象とするファイル名を複数指定できます。  
inputオプションとは異なり、TSVの中のfilenameを参照しています。  
ファイル例(タブはスペース4つで表記)  

``` tsv
filename    linenumber    choice    translated
scene1.rpy    17    "sample1"    Untranslated
scene1.rpy    23    "sample2"    Untranslated
scene1.rpy    26    "sample3"    Untranslated
scene2.rpy    30    "sample4"    Untranslated
scene2.rpy    55    "sample5"    Untranslated
```

この場合、```--target scene1.rpy```と入力すれば```scene1.rpy```のセリフのみが翻訳され、```scene2.rpy```などの他のファイルは翻訳されません。  
また、```--target scene1.rpy scene2.rpy```で複数ファイルの選択ができます。  
なお、このオプションを使用しなければ自動で全てのファイルが読み込まれて全て翻訳されます。  
デフォルト値：```[]```  
設定：```TARGET```

```--start_line```(```-sl```)

翻訳を開始する行数を指定することができます。  
ヘッダー行は含まず、データの中身の行数だけで認識するので気をつけてください。

例：```python main.py tsv_translate_menu -sl 3```

翻訳前ファイル(タブはスペース4つで表記)

``` tsv
filename    linenumber    choice    translated
scene1.rpy    17    "sample1"    Untranslated
scene1.rpy    23    "sample2"    Untranslated
scene1.rpy    26    "sample3"    Untranslated
scene2.rpy    30    "sample4"    Untranslated
scene2.rpy    55    "sample5"    Untranslated
```

翻訳後ファイル

``` tsv
filename    linenumber    choice    translated
scene1.rpy    26    "sample3"    サンプル3
scene2.rpy    30    "sample4"    サンプル4
scene2.rpy    55    "sample5"    サンプル5
```

デフォルト値：```0```  
設定：```START_LINE```

##### 使用例

``` bash
python main.py tsv_translate_menu -i example.tsv -fr en -t scene1.rpy scene2.rpy
python main.py -l tsv_translate_menu
```

#### tsv2rpy_menu

このモードでは、以下の形式で保存されているTSVファイルを読み込み、以下のRenPyが読み取れるファイル形式に変換します。

TSV

``` tsv
filename    linenumber    choice    translated
```

RenPy

``` rpy
translate {tl_lang} strings:

    old {choice}
    new {translated}

    old {choice}
    new {translated}

    .....
```

こちらもほぼ、先述の```tsv2rpy```モードと同じで、入力出力ファイルが異なるだけです。

##### オプション

```--input```(```-i```)

このプログラムの入力ファイルの名前を変更できます。  
入力ファイルの形式は、先述の形式と同じものでなければなりません。  
デフォルト値：```'menu_translated.tsv'```  
設定：```MENU_TSV2RPY_INPUT```

```--output```(```-o```)

このプログラムの出力ファイルの名前を変更できます。  
デフォルト値：```'menu_converted.rpy'```  
設定：```MENU_TSV2RPY_OUTPUT```

```--tl_lang```(```-tl```)

出力ファイルに記載する、RenPyが認識できるゲーム固有の言語名を変更できます。  
大抵の場合、デフォルトでも動くと思いますが、一部のゲームでは異なる場合があるので適宜変更してください。  
デフォルト値：```'japanese'```  
設定：```TL_LANG```

```--comment```(```-c```)

出力ファイル内の翻訳支援用の、行数やファイル名に関するコメントをつけるかどうかを変更できます。  
Falseの場合の例

``` rpy
translate japanese strings:

    old "sample1"
    new "サンプル1"

    old "sample2"
    new "サンプル2"

    old "sample3"
    new "サンプル3"
```

Trueの場合の例

``` rpy
translate japanese strings:

# scene1.rpy
# line:17
    old "sample1"
    new "サンプル1"

# line:26
    old "sample2"
    new "サンプル2"

# line:30
    old "sample3"
    new "サンプル3"
```

デフォルト値：```False```  
設定：```COMMENT```

```--split_file```(```-sf```)

TSV一番左の```filename```に応じて、出力するファイルを変更することができるようになり、分割したファイルの生成ができるようになります。  
デフォルト値：```False```  
設定：```SPLIT_FILE```

```--split_prefix```(```-sp```)

分割するファイルにつける接頭詞を変更できます。  
デフォルト値：```'menu_convert_'```  
設定：```MENU_SPLIT_PREFIX```

##### 使用例

``` bash
python main.py tsv2rpy -o example.rpy -tl japanesetl -c
python main.py tsv2rpy -i edited.tsv
```

## ゲーム内からのセリフ抽出

このModでは、オプションを正しく変更することにより、未翻訳のセリフのみを抽出したり多くのことができます。

ルートディレクトリの```__init__.py```でオプションを操作することができるので、次のオプションの項目を読んで設定してください。  
前の項目のコマンドの設定とは異なり、```modules/settings.py```では設定することができません。

### 使用方法

この```renpy_translate_mod```リポジトリをダウンロードして、該当ゲームのgameディレクトリの中にそのまま入れてください。

ディレクトリ図の例

``` dir
├ game/
│    ├ cache/
│    ├ renpy_translate_mod/  ←このフォルダをここでダウンロードして追加
│    │        ├ modules/
│    │        ├ __init__.py
│    │        └ bootstrap.rpy
│    │
│    └ saves/
│
├ lib/
├ renpy/
├ game.exe
└ log.txt
```

### オプション

動作設定```WORK```

この設定をTrueにすれば、ゲームの起動時にセリフが抽出されます。  
ファイルを上書きされたくない場合などはFalseにしておくと誤爆を防げます。  
デフォルト値：```True```

出力ファイル設定```EXTRACT_DIALOGUE_OUTPUT```

この設定では、出力ファイルの名前を変更できます。  
セリフを小分けにして保存などする等の用途で使用できます。
デフォルト値：```'untranslated.tsv'```

言語設定```EXTRACT_DIALOGUE_TO_LANG```

この設定では```tsv2rpy```や```tsv2rpy_menu```モードの```--tl_lang```と同じRenPyが言語を認識するときの識別子を使用して、翻訳されていないセリフのみを抜き出します。  
この設定がうまく行かないと全て抽出されてしまいます。
デフォルト値：```'japanese'```

## 疑問点について

何か疑問点がある場合は、drago-suzuki58までご連絡ください。
