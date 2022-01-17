FROM python:3.9.0-alpine3.12

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app:/app/_deps"

ADD src /app

RUN pip install pip==20.2.4 --upgrade
RUN mkdir /app/_deps \
    && pip install --no-cache-dir \
    -r /app/requirements.txt \
    -t /app/_deps 


WORKDIR /app

ENTRYPOINT ["python3", "app.py"]

