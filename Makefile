LCC_DIR=./mysql/data/lcc/
KNBC_DIR=./mysql/data/knbc/
KWDLC_DIR=./mysql/data/kwdlc/
LOG_DIR=./solr/logs/
MODEL_DIR=./python/model/
PYCACHE_DIR=./python/__pycache__/
FOOD_DIR=./python/img/food/

tsv:
	bash ./download_scripts/make_data.sh
food:
	mkdir -p $(FOOD_DIR)
	wget http://data.vision.ee.ethz.ch/cvl/food-101.tar.gz -O - | tar xvz - -C $(FOOD_DIR)
model:
	mkdir -p $(MODEL_DIR)
	wget http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/data/20170201.tar.bz2 -O - | tar -jxvf - -C $(MODEL_DIR)
log:
	mkdir -p $(LOG_DIR)
	sudo chmod 777 $(LOG_DIR)
clean:
	docker-compose down
	rm -rf $(LCC_DIR)
	rm -rf $(KNBC_DIR)
	rm -rf $(KWDLC_DIR)
	rm -f $(LOG_DIR)/*
	rm -rf $(MODEL_DIR)
	sudo rm -rf $(PYCACHE_DIR)
	rm -rf $(FOOD_DIR)
