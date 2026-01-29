FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    python3 \
    python3-pip \
    jq \
    bash \
 && rm -rf /var/lib/apt/lists/*

# Install detect-secrets pinned to 1.3.0
RUN python3 -m pip install --upgrade pip && python3 -m pip install --upgrade detect-secrets==1.3.0

WORKDIR /home/ci/workspace

COPY .ci-local/run-local-ci.sh /home/ci/workspace/.ci-local/run-local-ci.sh
RUN chmod +x /home/ci/workspace/.ci-local/run-local-ci.sh

ENTRYPOINT ["/home/ci/workspace/.ci-local/run-local-ci.sh"]
