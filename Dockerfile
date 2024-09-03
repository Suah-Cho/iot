FROM python:3.9
RUN apt-get update && apt-get install -y docker.io
WORKDIR /
COPY . .
RUN pip install -r requirements.txt
ENV DEVICE_CONNECT_STRING=""
CMD [ "python", "main.py" ]