FROM openjdk:slim
COPY --from=python:3.7 / /

ENV PIPENV_VENV_IN_PROJECT 1

RUN apt-get update && apt-get install -qq -y nginx tesseract-ocr tesseract-ocr-fra \
  && python3.7 -m pip install pipenv

COPY .docker/entrypoint.sh /entrypoint.sh
COPY .docker/nginx.conf /etc/nginx/sites-available/default

WORKDIR /app

COPY Pipfile* .

RUN  python3.7 -m pipenv install

COPY . .

EXPOSE 80

ENTRYPOINT [ "/entrypoint.sh" ]