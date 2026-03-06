FROM python:3.11

WORKDIR /app
COPY . /app

CMD ["python", "election_bot.py"]