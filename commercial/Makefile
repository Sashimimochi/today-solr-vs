LCC_DIR=./mysql/data/lcc/
KNBC_DIR=./mysql/data/knbc/
KWDLC_DIR=./mysql/data/kwdlc/
LOG_DIR=./solr/logs/
MODEL_DIR=./python/model/
PYCACHE_DIR=./python/__pycache__/
OPEN_IMAGES_DIR=./python/img/open_images
DOWNLOAD_SCRIPTS=./download_scripts
USERNAME=`whoami`

tsv:
	bash ./$(DOWNLOAD_SCRIPTS)/make_data.sh
open_images:
	mkdir -p $(OPEN_IMAGES_DIR)
	docker build -t image_downloader ./download_scripts
	docker run --rm -v `pwd`/$(DOWNLOAD_SCRIPTS):/workspace/app image_downloader python image_downloader.py
	@echo "Change authrize from root to exec user"
	sudo chown -R $(USERNAME).$(USERNAME) $(DOWNLOAD_SCRIPTS)
	mv $(DOWNLOAD_SCRIPTS)/images/* $(OPEN_IMAGES_DIR)
	rm -rf $(DOWNLOAD_SCRIPTS)/images
	docker rmi image_downloader
model:
	mkdir -p $(MODEL_DIR)
	wget http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/data/20170201.tar.bz2 -O - | tar -jxvf - -C $(MODEL_DIR)
log:
	mkdir -p $(LOG_DIR)
	@echo "Add authrize to $(LOG_DIR) from local and container"
	sudo chmod 777 $(LOG_DIR)
clean:
	docker-compose down
	rm -rf $(LCC_DIR)
	rm -rf $(KNBC_DIR)
	rm -rf $(KWDLC_DIR)
	rm -f $(LOG_DIR)/*
	rm -rf $(MODEL_DIR)
	@echo "Delete PYCACHE_DIR"
	sudo rm -rf $(PYCACHE_DIR)
	rm -rf $(OPEN_IMAGES_DIR)
