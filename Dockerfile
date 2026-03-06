FROM python:3.11

WORKDIR /app
COPY . /app

CMD ["python3", "-u", "election_bot.py"]