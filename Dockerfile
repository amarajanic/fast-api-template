FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
LABEL maintainer="https://github.com/amarajanic"

WORKDIR /app

COPY app/requirements.txt /tmp/requirements.txt 
COPY ./app /app

RUN apt-get update && apt-get install -y gcc

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]