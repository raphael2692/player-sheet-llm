# Pull python image
FROM python:3.10

# Pull python image
FROM python:3.10

# Set work directory
COPY . /app 
WORKDIR /app

# Set python env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install pip package dependencies
# RUN apt update \
#     && apt upgrade \
#     && apt install python3-dev build-essentials- -y


CMD ["sh",  "start_docker.sh"]