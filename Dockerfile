FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
LABEL maintainer="https://github.com/amarajanic"

WORKDIR /usr/src/app

COPY ./app/requirements.txt /tmp/requirements.txt
COPY ./app /app
EXPOSE 8000

RUN apt-get install gcc

RUN pip3 install -r /tmp/requirements.txt

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]