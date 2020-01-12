FROM python:3.7

WORKDIR /app

RUN pip install pipenv && pipenv --python 3.7

COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install --deploy --dev

COPY . .
CMD pipenv run python -m manager run-worker
