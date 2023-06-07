FROM python:3.11-bullseye
WORKDIR /
RUN pip install pipx
RUN pipx install poetry
COPY . .
RUN poetry install --no-dev
CMD poetry run anycode-recognizer-bot
