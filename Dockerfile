FROM python:3.8-slim

ENV VAR1=10
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN useradd --create-home --shell /bin/bash app_user
WORKDIR /home/app_user
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy
RUN pipenv install 
WORKDIR /app
COPY . /app
USER app_user
COPY . .
CMD ["python", "main.py"]