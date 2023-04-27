FROM python:3.8.9

LABEL maintainer="inhun321@khu.ac.kr"



COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu



RUN apt-get update
RUN apt-get install fonts-nanum*

RUN cp /usr/share/fonts/truetype/nanum/Nanum* /usr/local/lib/python3.8/site-packages/matplotlib/mpl-data/fonts/ttf/
RUN rm -rf /root/.cache/matplotlib/fontlist-v330.json

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

ENTRYPOINT ["python3", "main.py"]