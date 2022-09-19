FROM python:3.8.0
USER root

# install heroku cli
RUN curl https://cli-assets.heroku.com/install.sh | sh

# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN apt-get update && apt-get install -y \
    && apt-get install -y libfluidsynth1 fluid-soundfont-gm build-essential libasound2-dev libjack-dev \
    && pip install --upgrade pip

# change dir
WORKDIR /home/flask

# install module
COPY requirements.txt /home
RUN pip install -r /home/requirements.txt

# flask setting
ENV FLASK_APP '/home/flask/app.py'
ENV FLASK_DEBUG 1