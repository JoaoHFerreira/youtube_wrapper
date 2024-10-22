FROM python:3.9-slim


WORKDIR /app

COPY . /app



RUN apt-get update && \
     apt-get install -y postgresql-client && \
     apt-get install -y ffmpeg && \
     apt-get install -y libasound2 &&\
     apt-get install -y libasound2-plugins && \
     apt-get install -y alsa-utils && \
     pip install --no-cache-dir scrapy psycopg2-binary

     


RUN pip install -r requirements


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]