FROM python:3.10-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "gunicorn", "-b 0.0.0.0", "-p 8080", "app:app" ]
