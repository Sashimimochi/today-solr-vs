#!/bin/bash

senario=./test.yml

docker run -it --rm -v `pwd`:/bzt-configs blazemeter/taurus:latest $senario
