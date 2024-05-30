FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000 5001

CMD ["sh", "-c", "if [ \"$FLASK_ENV\" = \"development\" ]; then python LoadBalancer.py; else python WebServer.py; fi"]
