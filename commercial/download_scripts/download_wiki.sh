#!/bin/bash

WIKI_DIR=python/index/

latest=$(date --date 'this week last monday' +'%Y%m%d')
wget -P $WIKI_DIR https://dumps.wikimedia.org/other/cirrussearch/$latest/jamwiki-$latest-cirrussearch-content.json.gz
