# コーディング規則
- 関数の宣言では，**スネークケース**を用いてください. <br>
  e.g. `def map_view():`, `def stamp_list_view():`
- クラスの宣言では，**パスカルケース**を用いてください. <br>
  e.g. `class MapPin():`
- HTMLリクエストを指定する際, `POST` / `GET` を用いてください. `post` / `get` は使用しないでください.
- HTMLファイル名やviews.pyで宣言される関数は**スネークケース**を用いてください．また，これらの末尾は`_view`としてください.  <br>
  e.g. `map_view.html`, `get_stamp_view.html` etc.

# GitHubの使い方
> [!IMPORTANT]
> 前提
> - vscodeの拡張機能で，`Dev Container`をインストールする.
> - WSLに`git`をインストールする.
> ```
> $ git --version # 確認
> $ sudo apt update
> $ sudo apt git # インストール
> ```

## クローン
WSLで任意のディレクトリに移動して，コマンドを実行.
```
$ git clone -b develop https://github.com/N-Ruma/StampCollection.git
```
> [!NOTE]
> `-b`オプションで任意のブランチからクローンする. デフォルトは`main`.

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
1. 統合元ブランチ(`base:develop`など)と，統合するブランチ(`compare:feature<FEATURE>`など)を選択.
1. `Create Pull request`をクリック
1. 作業内容などを記入して，右の`Reviewers`から，レビュアーを1人以上選択. (マージしていいかを確認してもらうため.)
1. `Create Pull request`をクリック
1. Approveをもらったら，`Merge pull request`をクリックして，マージする.
