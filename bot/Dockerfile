FROM python:3.10.7-slim-buster

# install libraries for FFmpeg
RUN apt-get update && apt-get install -y python3-dev build-essential
RUN apt-get install -y libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev libmagic1
RUN if [ ! -e /lib/libz.so ]; then \
    ln -s /usr/lib/x86_64-linux-gnu/libz.so /lib/ \
    ;fi
RUN if [ ! -e /lib/libjpeg.so ]; then \
    ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /lib/ \
    ;fi

# install FFmpeg
RUN apt-get install -y ffmpeg && ffmpeg -version

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/usr/src/app \
    CI_PIPELINE_URL=$CI_PIPELINE_URL \
    CI_COMMIT_SHORT_SHA=$CI_COMMIT_SHORT_SHA

WORKDIR /usr/src/app

ADD . .
RUN pip3 install --no-cache-dir --upgrade -r ./requirements.txt
