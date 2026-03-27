FROM ubuntu:24.04 AS base

LABEL maintainer="Daniel Dias"
LABEL email="ddr.dan98@gmail.com"

RUN set -xe && \
    apt update && \
    apt install -y curl tar git \
    binutils gcc ffmpeg \
    python3-pip python3-venv python3-tk && \
    apt clean all && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN python -m pip config set global.break-system-packages true 
RUN pip install aiohttp nodejs_wheel pytube
