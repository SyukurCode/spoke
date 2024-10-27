FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    pulseaudio \
    alsa-utils \
    libasound2-dev \
    ffmpeg \
    vlc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN mkdir tmp && chmod 777 -R tmp

CMD [ "python3", "index.py"]
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3000", "index:app"]
