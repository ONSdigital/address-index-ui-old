FROM python:3

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENV FLASK_ENV ui
ENV PORT 5000
ENV HOST='0.0.0.0'
# host.docker.internal wouldn't be required if we run the API in another container
ENV API_URL='http://host.docker.internal:9000'
ENV SWAGGER_URL=$API_URL'/assets/swagger.json'
ENV SECRET_KEY='you-will-never-guess'

ENTRYPOINT [ "python" ]

CMD [ "/app/addressindex.py" ]