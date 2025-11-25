# 変更履歴
2025/11/25:
- Dockerイメージやコンテナの整理に関する説明を追記しました．-> [Docker環境を整理する](#Dockerイメージやプロセスがいっぱいある?)

2025/11/21:
- htmlファイルに関する説明をコーディング規則に追記しました．

2025/11/19:
- `feature/*`ブランチの削除を禁止しました．
- `release`ブランチへのプルリクエストで，4人以上の承認を得るようにしました．
- `develop`ブランチへのプルリクエストで，2人以上の承認を得るようにしました．

---

# コーディング規則
- 関数の宣言では，**スネークケース**を用いてください. <br>
  e.g. `def map_view():`, `def stamp_list_view():`
- クラスの宣言では，**パスカルケース**を用いてください. <br>
  e.g. `class MapPin():`
- HTMLリクエストを指定する際, `POST` / `GET` を用いてください. `post` / `get` は使用しないでください. (小文字が交じると動かなくなったりするものがある(あった)ので，念の為.)
- HTMLファイル名やviews.pyで宣言される関数は**スネークケース**を用いてください．また，これらの末尾は`_view`としてください.  <br>
  e.g. `map_view.html`, `get_stamp_view.html` etc.

## HTMLファイルについて
- `{% extends base.html %}` をhtmlファイルの先頭に記述して，`{% block ??? %}`で書くのをメインにしてください．
- head: 個別のhtmlファイルに`head`タグを追加する場合用のブロック．
- title: どの画面にいるかを`h1`タグで表示(必須)．その他ヘッダ情報．
- content: コンテンツのメインとなる部分．基本自由にかいていい.
- redirect: 画面遷移用ブロック．`<div><a href="{% url: '???' %}">???</a></div>` の形で書くこと．
- script: htmlファイルに個別にスクリプトを埋め込む場合のブロック．`script`タグで囲むのを忘れないように．
- 装飾を行う場合に備えて，Bootstrapという，あらかじめデザインされたテンプレートなどを使って装飾できます．
- ログインを必要とする画面を作成するには，`views.py`内の関数に，`@login_required`デコレータを付与することで実装できます．

# GitHubの使い方
> [!IMPORTANT]
> 前提
> - vscodeの拡張機能で，`Dev Container`をインストールする.
> - WSLに`git`をインストールする.
> ```
> $ git --version # 確認
> $ sudo apt update
> $ sudo apt install git # インストール
> ```

## クローン
WSLで任意のディレクトリに移動して，`develop`ブランチをクローン.
```
$ git clone -b develop https://github.com/N-Ruma/StampCollection.git
```
> [!NOTE]
> `-b`オプションで任意のブランチからクローンできる. デフォルトは`release`

## Docker
vscodeでwslを開き，"フォルダを開く"から, `StampCollection/`を選択. (`.git/`があるところ.) <br>
開いたら，"コンテナで再度開く"を選択.

## ユーザ登録
開いたらコマンドを実行して，アカウントを設定.
```
$ git config --local user.name <USERNAME>
$ git config --local user.email <EMAIL>
```
> [!NOTE]
> 確認
> ```
> $ git config --local user.name
> $ git config --local user.email
> ```

## ブランチを切る
```
$ git checkout -b feature/<FEATURE>
```
> [!NOTE]
> `-b`オプションでブランチの新規作成と移動を同時にできる. <br>
> `<FEATURE>`には追加する機能や修正する点などを入れるとわかりやすくていい. <br>
> e.g.
> ```
> $ git checkout -b feature/add_map_view
> ```

## ファイルを編集・追加する
ファイルを編集，追加などする. 
> [!NOTE]
> `.gitignore`の設定で，`db.sqlite3`や`migrations/`をバージョン管理から除外しているので，最初に`makemigrations`と`migrate`を行う必要がある.
> また，`$ myvenv/bin/activate`などをする必要はなく，はじめから`$ python manage.py`を実行できる.

## ステージング
```
$ git add .
```
> [!NOTE]
> `.`でカレントディレクトリ下のすべてのファイルをステージングする.

## コミット
```
$ git commit
```
```
$ git commit -m "<COMMIT_MESSAGE>"
```
> [!NOTE]
> `-m`オプションを付けない場合, `vim`が起動する. <br>
> 他のエディタを使いたい場合はそれをインストールして,
> ```
> $ git config --global core.editor <EDITOR_NAME>
> ```
> で変更.

## プッシュ
```
$ git push -u origin feature/<FEATURE>
```

## プルリクエスト
1. リポジトリにアクセス
1. `pull requests`をクリック
1. `New pull request`をクリック
1. 統合元ブランチ(`base:develop`など)と，統合するブランチ(`compare:feature/<FEATURE>`など)を選択.
1. `Create pull request`をクリック
1. 作業内容などを記入して，右の`Reviewers`から，レビュアーを1人以上選択. (マージしていいかを確認してもらうため.)
1. `Create pull request`をクリック
1. Approveをもらったら，`Merge pull request`をクリックして，マージする.

---

# ローカルリポジトリの内容をリモートリポジトリの内容で更新する方法
リモートリポジトリの内容を，**現在のブランチ**(`$ git branch`)に統合する場合:
```
$ git pull origin <REMOTE_BRANCH_NAME>
```

# Dockerイメージやプロセスがいっぱいある?
リポジトリをコピーしてDockerコンテナを起動して...としていると，いつの間にかイメージやコンテナがいっぱいになって，動作が重くなることがあるかもしれません．
確認方法は以下です．

- Dockerイメージの確認: `$ docker images`
- Dockerコンテナの確認(停止中も含む): `$ docker ps -a`

イメージの削除やコンテナの削除を行うときは，以下の手順で削除できるはずです．

- Dockerイメージの削除:
1. `$ docker images`で削除したいイメージの，`IMAGE ID`または`REPOSITORY`を確認．
1. `$ docker rmi <IMAGE ID> or <REPOSITORY>`で指定したイメージを削除.
1. `$ docker images`でイメージを削除できたか確認.

- Dockerコンテナの削除:
1. `$ docker ps -a`で削除したいコンテナの`CONTAINER ID`または`NAMES`を確認．
1. `$ docker rm <CONTAINER ID> or <NAMES>`で指定したコンテナを削除．
1. `$ docker ps -a`でコンテナを削除できたか確認．

適宜Dockerイメージやコンテナの整理を行うことでリソース削減ができるかもしれません．
参考までに．
