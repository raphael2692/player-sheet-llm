# Pull python image
FROM python:3.10-alpine

# Pull python image
FROM python:3.10-alpine

# Set work directory
COPY . /app 
WORKDIR /app

# Set python env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install pip package dependencies
RUN apk update \
    && apk upgrade


CMD ["sh",  "start_docker.sh"]