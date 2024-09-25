#!/bin/bash

function get_os() {
    if [ "$(uname)" == 'Darwin' ]; then
        export OS='Mac'
    elif [ "$(expr substr $(uname -s) 1 5)" == 'Linux' ]; then
        export OS='Linux'
    elif [ "$(expr substr $(uname -s) 1 10)" == 'MINGW32_NT' ]; then
        export OS='Cygwin'
    else
        echo "Your platform ($(uname -a)) is not supported."
        exit 1
    fi
}

function lcc() {
    WORKSPACE=$(pwd)
    RELATIVE_DIR="mysql/data/lcc"
    ROOT_DIR="$WORKSPACE/$RELATIVE_DIR"
    O_DIR=$ROOT_DIR
    O_FILE="lcc.tsv"
    DATA_DIR="$ROOT_DIR/text"

    if [ ! -e "$O_DIR/$O_FILE" ];then
        mkdir -p ${ROOT_DIR}
        wget https://www.rondhuit.com/download/ldcc-20140209.tar.gz -O - | tar xfz - -C ${ROOT_DIR}

        DIRS=$(find $DATA_DIR/* -maxdepth 0 -type d)
        i=1
        for dir in $DIRS; do
            DIR=$(basename $dir)
            media=$DIR
            cd ${DATA_DIR}/${DIR}
            echo "[$i/9] start $media"
            for file in `\find . -maxdepth 1 -name '*.txt'`; do
                if [ $file != "./LICENSE.txt" ]; then
                    url=$(head -n 1 ${file})
                    write_date=$(head -n 2 ${file} | tail -n 1)
                    title=$(head -n 3 ${file} | tail -n 1)
                    text=$(tail -n +4 ${file} | sed -e s/　//g | tr -d '\n')
                    if [ ${OS} == "Mac" ]; then
                        echo "$media\t$url\t$write_date\t$title\t$text" >> ${O_DIR}/${O_FILE}
                    else
                        echo -e "$media\t$url\t$write_date\t$title\t$text" >> ${O_DIR}/${O_FILE}
                    fi
                fi
            done
            echo "[$i/9] end $media"
            cd $WORKSPACE
            i=`expr $i + 1`
        done

        rm -rf $DATA_DIR
    else
        echo "[INFO] ./$RELATIVE_DIR/$O_FILE is already existing. Skip download data."
    fi
}

function knbc() {
    WORKSPACE=$(pwd)
    RELATIVE_DIR="mysql/data/knbc"
    ROOT_DIR="$WORKSPACE/$RELATIVE_DIR"
    I_FILE=KNBC_v1.0_090925_utf8.tar.bz2
    I_DIR="$ROOT_DIR/KNBC_v1.0_090925_utf8"
    O_DIR="$ROOT_DIR"
    O_FILE="knbc.tsv"
    DATA_DIR="$I_DIR/corpus2"

    if [ ! -e "$O_DIR/$O_FILE" ];then
	    mkdir -p ${ROOT_DIR}
	    wget http://nlp.ist.i.kyoto-u.ac.jp/kuntt/${I_FILE}
	    tar -jxf ${I_FILE} -C ${ROOT_DIR} > /dev/null
        cd $DATA_DIR
        cat ./*.tsv | sed -e 's/\\n//g' > $O_DIR/knbc.tsv

        cd ${WORKSPACE}
        rm -rf ${I_DIR} ${I_FILE}
    else
        echo "[INFO] ./$RELATIVE_DIR/$O_FILE is already existing. Skip download data."
    fi
}

function kwdlc() {
    WORKSPACE=$(pwd)
    RELATIVE_DIR="mysql/data/kwdlc"
    ROOT_DIR="$WORKSPACE/$RELATIVE_DIR"
    I_FILE=master.zip
    I_DIR="$ROOT_DIR/KWDLC-master"
    O_DIR=$ROOT_DIR
    O_FILE="kwdlc.tsv"
    DATA_DIR="$I_DIR/org"

    if [ ! -e "$O_DIR/$O_FILE" ];then
        mkdir -p ${ROOT_DIR}
        wget https://github.com/ku-nlp/KWDLC/archive/refs/heads/${I_FILE}
        unzip $I_FILE "*.org" -d ${ROOT_DIR} > /dev/null

        DIRS=$(find $DATA_DIR/* -maxdepth 0 -type d)
        for dir in $DIRS; do
            DIR=$(basename $dir)
            media=$DIR
            cd ${DATA_DIR}/${DIR}

            for file in `\find . -maxdepth 1 -name '*.org'`; do
                awk 'NR%2==0' $file | tr -d '\n' >> $O_DIR/$O_FILE
                echo "" >> $O_DIR/$O_FILE
            done
            cd $WORKSPACE
        done

        rm -rf ${I_DIR} ${I_FILE}
    else
        echo "[INFO] ./$RELATIVE_DIR/$O_FILE is already existing. Skip download data."
    fi
}

get_os
echo "[INFO] OS: ${OS}"
lcc
sleep 10
knbc
sleep 10
kwdlc
