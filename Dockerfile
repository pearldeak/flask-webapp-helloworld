# Pull a pre-built alpine docker image with nginx and python3 installed
# this image is from docker community, its small so our upload to contain will be faster
FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

ENV LISTEN_PORT=8000
EXPOSE 8000

COPY /app /app

# Uncomment to install additional requirements from a requirements.txt file
#COPY requirements.txt /
#RUN pip install --no-cache-dir -U pip
#RUN pip install --no-cache-dir -r /requirements.txt