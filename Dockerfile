# This is a multi-stage build which requires Docker 17.05 or higher.
FROM python:3.7-alpine as boxliner-builder

WORKDIR /usr/src/boxliner

ENV PACKAGES="\
    git \
    "
RUN apk add --update --no-cache ${PACKAGES}

ADD . .
RUN pip wheel -w dist .

# This is the target container.

FROM python:3.7-alpine
LABEL maintainer "John Dewey <john@dewey.ws>"

ARG GEM_SOURCE=https://rubygems.org

ENV PACKAGES="\
    docker \
    ruby \
    "
ENV BUILD_DEPS="\
    build-base \
    libffi-dev \
    ruby-dev \
    "
ENV GEM_PACKAGES="\
    inspec \
    etc \
    io-console \
    "

COPY --from=boxliner-builder /usr/src/boxliner/dist /usr/src/boxliner/dist

RUN \
    apk add --update --no-cache ${BUILD_DEPS} ${PACKAGES} \
    && pip install --only-binary :all: --no-index -f /usr/src/boxliner/dist box_liner \
    && pip install docker-compose \
    && gem install --no-document --source ${GEM_SOURCE} ${GEM_PACKAGES} \
    && apk del --no-cache ${BUILD_DEPS} \
    && rm -rf /root/.cache

ENV SHELL /bin/bash
