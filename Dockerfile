# pull official base image
FROM python:3-alpine

# set work directory
WORKDIR /usr/src/app

# install psycopg2 dependencies
RUN apk update
RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN apk add build-base

# install dependencies
RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt --no-cache-dir

RUN apk --purge del .build-deps

# copy project
COPY . .

# define command to start container
CMD ["waitress-serve", "--port=$PORT", "--call", "app:create_app"]