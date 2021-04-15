FROM python:3.8
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
WORKDIR /app
RUN pip install -r /app/requirements.txt
COPY src/ /app/src/
#COPY .env /app
CMD python -m src.web
