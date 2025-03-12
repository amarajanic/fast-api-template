FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
LABEL maintainer="https://github.com/amarajanic"

WORKDIR /app  # Changed from /usr/src/app

COPY requirements.txt /tmp/requirements.txt  # Ensure correct path
COPY ./app /app

RUN apt-get update && apt-get install -y gcc  # Fixed package install

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]