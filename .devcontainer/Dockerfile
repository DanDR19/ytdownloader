FROM ubuntu:24.04 AS base

LABEL maintainer="Daniel Dias"
LABEL email="ddr.dan98@gmail.com"

RUN apt update && \
    apt install -y curl tar git \
    binutils gcc \
    python3 python3-dev python3-venv python3-tk && \
    apt clean all
