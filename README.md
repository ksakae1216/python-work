# python-work

- wikipediaからリンク抽出してツリー作成
- キーワード重複は@を付与
- 未探索は$を付与
- キーワードは上位優先
- 語、学は探索せず$付与
- 探索は1秒以上間隔あける

※`<div class="mw-parser-output">`直下で最初の`<p>`タグ対象

※リンク先がwikiで始まる

※hrefの方をキーワードにする

## 環境

PC：MAC

使用言語：Python 3.9.0

## 準備（パッケージインストール）

```
pip install requests
pip install beautifulsoup4
