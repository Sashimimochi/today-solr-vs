FROM python:3.7

# mecabの導入
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y mecab libmecab-dev mecab-ipadic-utf8 \
    git make curl xz-utils file sudo locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

ENV LANG='ja_JP.UTF-8'
ENV LANGUAGE='ja_JP:ja'
ENV LC_ALL='ja_JP.UTF-8'
ENV TZ JST-9
ENV TERM xterm

WORKDIR /workspace/app

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir && \
    pip install -r requirements.txt --no-cache-dir
