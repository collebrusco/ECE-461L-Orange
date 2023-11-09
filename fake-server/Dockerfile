FROM python:3.10-slim

WORKDIR /flask
COPY . /flask

RUN pip install -r requirements.txt

EXPOSE 8888

CMD ["python", "main.py"]
