FROM python:3.8
COPY requirements.txt /src/requirements.txt
RUN pip install --upgrade pip
WORKDIR /src
RUN pip install -r /src/requirements.txt
COPY src/ /src/src/
#COPY .env /src
CMD python -m src.web
