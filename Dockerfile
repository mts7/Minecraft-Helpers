FROM python:3.8
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
WORKDIR /app
RUN pip install -r /app/requirements.txt
EXPOSE "${PORT}"
COPY src/ /app/src/
#COPY .env /app
RUN mkdir -p /home/minecraft/minecraft && wget https://papermc.io/api/v2/projects/paper/versions/1.16.5/builds/592/downloads/paper-1.16.5-592.jar && mv paper-1.16.5-592.jar /home/minecraft/minecraft/
RUN apt update && apt install default-jre screen -y
CMD python -m src.web
