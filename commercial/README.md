# 今日から始める Solr ベクトル検索

この度は、[今日から始める AI 検索技術～ Solr エンジニアのための最先端ガイド～](https://nextpublishing.jp/book/18504.html)をお手に取っていただきありがとうございます。

本リポジトリは同書に記載のサンプルコードを公開しているリポジトリです。
書籍と内容と照らし合わせながらご活用ください。

もし、サンプルコードの実装エラーなどを見つけた際は、issue からご連絡ください。

## 環境概要

環境は Docker で構築する想定になっています。

| Service    | Version |
| :--------- | :------ |
| SolrCloud  | 9.4.1   |
| Zookeeper  | 3.7     |
| MySQL      | 5.7     |
| Grafana    | 9.4.7   |
| Prometheus | 2.43.0  |
| cAdvisor   | 0.32.0  |
| Python     | 3.7     |
| Taurus     |         |

## Quick Start

ディレクトリトップから以下のコマンドを実行します。
実行すると、必要なデータのダウンロード、コンテナの起動、Solr のコレクション作成が行われます。

```bash
$ sh ./launch.sh -[option]
# ex
$ sh ./launch.sh -c "basic text_short" -d basic -e true
```

### Option

必要に応じて適当なオプションを指定してください。

- `-c`: 作成するコレクション名を指定する。複数指定する場合は`""`でくるる
- `-d`: データダウンロードの種類を指定する
  - `mini`: 外部データを使用しない
  - `basic`: `text` コア用の外部データをダウンロードする (default)
  - `open_images`: `open_images` コア用の外部データをダウンロードする
  - `full`: 全コア用の外部データをダウンロードする
- `-e`: solr-exporter を起動するかを選択する `true/false`

各種外部データダウンロードは、すでにローカルにダウンロード済みのデータがある場合は、ダウンロード処理がスキップされます。

- model: 15m

## Clean

いらなくなったデータの削除方法は以下の通りです。
`launch.sh` によってダウンロードしたファイルを中心にリポジトリ clone 後に作成したデータが削除されます。

```bash
$ make clean
```

# Solr

Solr の管理画面には以下でアクセスできます。

http://localhost:8983/solr/

## Maintenance

あまり触る機会はないと思いますが、Solr の実態は `opt/solr/bin/solr` にあります。
コンテナのホームディレクトリは `opt/solr` なので、`bin/solr`でたどり着けます。

例えば、以下のコマンドで Solr のステータス確認ができます。

```bash
$ docker-compose exec solr_node1 /opt/solr/bin/solr status
```

# Frontend(Streamlit)

ベクトル検索用画面には以下でアクセスできます。

http://localhost:8501

# Prometheus

メトリクス収集ミドルウェアである Prometheus には以下でアクセスできます。

http://localhost:9090

# Grafana

可視化ダッシュボード Grafana には以下でアクセスできます。

http://localhost:3000

初期 IP/PW は、admin/admin です。
必要に応じて変更してください。

ダッシュボードは以下のものを改変して使用しています。

- https://grafana.com/grafana/dashboards/12456-solr-dashboard/
- https://grafana.com/grafana/dashboards/12928-sisense-cluster-detail-dashboard/
- https://grafana.com/grafana/dashboards/1860-node-exporter-full/
- https://grafana.com/grafana/dashboards/405-node-exporter-server-metrics/

# cAdvisor

コンテナメトリクス収集ツール cAdvisor には以下でアクセスできます。

http://localhost:9854

# MySQL

UI を持たないので省略します。

# Performance Test

パフォーマンステストを実行したい場合は、以下を実行してください。

```bash
# インデックスデータのダウンロード
$ sh launch.sh -d wiki # あるいは -d all
# パフォーマンステスト実行
$ cd performance_test
$ sh performance_test.sh
```

テストシナリオを変更する場合は、`test.yml` を修正してください。
