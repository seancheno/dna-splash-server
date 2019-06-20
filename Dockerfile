FROM python:3.6-alpine
LABEL maintainer "Sean"

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add --no-cache postgresql-dev && \
    apk add postgresql-dev && \
    rm -rf /var/cache/apk/*

RUN apk --update add \
    build-base \
    jpeg-dev \
    zlib-dev

# Defines where the application source code will be located within the docker image
ENV INSTALL_PATH /api
RUN mkdir -p $INSTALL_PATH    

WORKDIR $INSTALL_PATH

# Save time by having docker copy the req.txt file into the docker image, then installing the dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory into the docker image. This is how applications code gets inside of docker
COPY . .

# The default command that this docker image will run when you start it
# -b 0.0.0.0:8000 = Bind to all IP addresses on local server
# --access-logfile tells gunicorn to log everything to standard out - All gunicorn log files will be written to terminal instead of dedicated log file.
CMD gunicorn -b 0.0.0.0:5000 --access-logfile - "api.app:app"