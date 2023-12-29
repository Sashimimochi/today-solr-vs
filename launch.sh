#!/bin/bash

set -eu

usage() {
  cat <<EOM
Usage: $(basename "$0") [OPTION]...
  -h          Display help
  -c VALUE    Collection names wrapped by double quote mini/mini_dual/food/food2/illust/text/text_short/basic/wiki/wiki_org/text_large
  -d VALUE    Dowload data type: mini/basic/food/food2/full
  -e VALUE    Launch solr-exporter
EOM

  exit 2
}

# 引数別の処理定義
while getopts ":c:d:e:h" optKey; do
  case "$optKey" in
    c)
      export collections="${OPTARG}"
      ;;
    d)
      export dlType="${OPTARG}"
      ;;
    e)
      export solrExporter="${OPTARG}"
      ;;
    '-h'|'--help'|* )
      usage
      ;;
  esac
done

download_data() {
  # インデックスデータ/モデルデータのダウンロード
  FOOD_DIR="python/img/food/"
  FOOD2_DIR="python/img/food2/"
  WIKI_DIR="python/index/"

  if [ "$dlType" = "full" -o "$dlType" = "food" -o "$dlType" = "wiki" -o "$dlType" = "food2" ]; then
    if [ ! -d $FOOD_DIR -a "$dlType" != "wiki" -a "$dlType" != "food2" ]; then
        make food
    else
        echo "[INFO] $FOOD_DIR is already existing. If you want to download again, please remove $FOOD_DIR"
    fi
    if [ ! -d $FOOD2_DIR -a "$dlType" != "wiki" -a "$dlType" != "food" ]; then
        make food2
    else
        echo "[INFO] $FOOD2_DIR is already existing. If you want to download again, please remove $FOOD2_DIR"
    fi
    if [ `find $WIKI_DIR -name "jamwiki-*-cirrussearch-content.json.gz" 2>&1 | wc -l` -eq 0 -a "$dlType" != "food" ]; then
        sh ./download_scripts/download_wiki.sh
    else
        echo "[INFO] wiki data is already existing. If you want to download again, please remove file jamwiki-*-cirrussearch-content.json.gz from $WIKI_DIR"
    fi
    make tsv
  elif [ "$dlType" = "basic" ]; then
    make tsv
  fi

  if [ ! -d "python/model/" ]; then
    make model
  fi
}

create_log_dir() {
  LOG_DIR=./solr/logs/
  if [ ! -d $LOG_DIR ]; then
    make log
  fi
}

# Solrのコレクション作成
create_collection() {
    if [ `curl -LI "http://localhost:8983/solr/$1/admin/ping?distrib=true" -o /dev/null -w '%{http_code}\n' -s` -ne 200 ]; then
        docker-compose exec solr_node1 server/scripts/cloud-scripts/zkcli.sh -zkhost zookeeper1:2181 -cmd upconfig -confdir /opt/solr/server/solr/configsets/$1/conf -confname $1_conf
        curl "http://localhost:8983/solr/admin/collections?action=CREATE&name=$1&collection.configName=$1_conf&numShards=$2&replicationFactor=1&maxShardsPerNode=$2"
    fi
}

# solr-exporterの起動
start_solr_exporter() {
    docker-compose exec solr_node1 bash -c "cd ./prometheus-exporter && ./bin/solr-exporter -p 9854 -z zookeeper1:2181 -f ./conf/solr-exporter-config.xml -n 16"
}

# Solrのコンテナ起動待機
wait_lanch_services() {
    while [ `curl -LI http://localhost:8983/solr -o /dev/null -w '%{http_code}\n' -s` -ne 200 ]; do
        echo "[INFO] waiting launch services. retry in 30s"
        sleep 30
    done
    echo "[INFO] successfully launch services!"
}

check_array() {
  array=$2
  local i
  for i in $array; do
      if [ ${i} = ${1} ]; then
          return 0
      fi
  done
  return 1
}

create_collections() {
  large_collections="wiki wiki_org"
  for c in $collections; do
    if check_array $c $large_collections; then
      create_collection $c 2
    else
      create_collection $c 1
    fi
  done
}

echo "[INFO] Data Download Type: ${dlType:=basic}"
download_data
create_log_dir
docker-compose up -d
echo "[INFO] Launch solr-exporter: ${solrExporter:=false}"
echo "[INFO] Create collections: ${collections:=mini text_short}"
wait_lanch_services
create_collections

$solrExporter && start_solr_exporter
