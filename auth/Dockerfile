FROM python:3.11.9-slim

WORKDIR /opt/auth

RUN apt update && apt upgrade && apt install -y \
     python3-dev \
     netcat-openbsd \
     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
    && pip install -r requirements.txt --no-cache-dir

COPY .env app/

COPY run.sh .

COPY app/ app/

RUN chmod +x /opt/auth/run.sh
ENTRYPOINT [ "/opt/auth/run.sh" ]
