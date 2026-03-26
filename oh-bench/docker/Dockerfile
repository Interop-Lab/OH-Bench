FROM node:18-slim

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || \
    sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    default-jre \
    python3 \
    git \
    cppcheck \
    bash \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY tools_archive/codelinter /opt/codelinter
COPY tools_archive/ohos-sdk /opt/ohos-sdk

RUN dos2unix /opt/codelinter/bin/codelinter 2>/dev/null || true && \
    sed -i '1s|.*|#!/usr/bin/env bash|' /opt/codelinter/bin/codelinter && \
    chmod +x /opt/codelinter/bin/codelinter && \
    find /opt/codelinter -type f -name "*.sh" -exec dos2unix {} \; 2>/dev/null || true && \
    find /opt/codelinter -type f -name "*.sh" -exec chmod +x {} \;

ENV OHOS_SDK_HOME=/opt/ohos-sdk
ENV PATH="/opt/codelinter/bin:${PATH}"

COPY repositories_slim /app/repositories

RUN git config --global --add safe.directory '*'

COPY scripts/evaluate_in_docker.py /usr/local/bin/evaluate
RUN chmod +x /usr/local/bin/evaluate

CMD ["/bin/bash"]