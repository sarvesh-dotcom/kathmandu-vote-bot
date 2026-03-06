FROM python:3.11

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "election_bot.py"]