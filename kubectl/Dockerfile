FROM python:2.7-alpine3.6

MAINTAINER Yifeng Xiao <xiaoy@vmware.com>

ENV KUBE_LATEST_VERSION="v1.7.0"
ENV PIP_INDEX_URL=http://p3-pypi.eng.vmware.com:3141/slave/dev/+simple
ENV PIP_TRUSTED_HOST=p3-pypi.eng.vmware.com

RUN apk add --update ca-certificates \
 && apk add --update -t deps curl \
 && curl -L https://storage.googleapis.com/kubernetes-release/release/${KUBE_LATEST_VERSION}/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl \
 && chmod +x /usr/local/bin/kubectl \
 && apk del --purge deps \
 && rm /var/cache/apk/*

RUN pip install --no-cache-dir shell-util pyyaml

RUN sed -i 's|/bin/bash|/bin/sh|' /usr/local/lib/python2.7/site-packages/shellutil/shell.py

ENTRYPOINT ["kubectl"]
CMD ["help"]