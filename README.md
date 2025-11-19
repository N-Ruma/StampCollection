# コーディング規則
- 関数の宣言では，**スネークケース**を用いてください. <br>
  e.g. `def map_view():`, `def stamp_list_view():`
- クラスの宣言では，**パスカルケース**を用いてください. <br>
  e.g. `class MapPin():`
- HTMLリクエストを指定する際, `POST` / `GET` を用いてください. `post` / `get` は使用しないでください. (小文字が交じると動かなくなったりするものがある(あった)ので，念の為.)
- HTMLファイル名やviews.pyで宣言される関数は**スネークケース**を用いてください．また，これらの末尾は`_view`としてください.  <br>
  e.g. `map_view.html`, `get_stamp_view.html` etc.



# 変更履歴
2025/11/19:
- `feature/*`ブランチの削除禁止,
- `release`ブランチへのプルリクエストで，4人以上の承認を得るようにした．
- `develop`ブランチへのプルリクエストで，2人以上の承認を得るようにした．



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



# ローカルリポジトリの内容をリモートリポジトリの内容で更新する方法
リモートリポジトリの内容を，**現在のブランチ**(`$ git branch`)に統合する場合:
```
$ git pull origin <REMOTE_BRANCH_NAME>
```
