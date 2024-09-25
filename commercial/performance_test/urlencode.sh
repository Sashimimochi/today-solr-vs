#!/bin/bash

docker run --rm -v `pwd`:/usr/local/src -w /usr/local/src python:3.7 python urlencode.py >> query.log
