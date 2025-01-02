FROM alpine:3.21

RUN apk update && \
    apk add --no-cache python3 py3-pip

WORKDIR /app

COPY . /app

RUN python3 -m pip config set global.break-system-packages true \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "./main.py"]