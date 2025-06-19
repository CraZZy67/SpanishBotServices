FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./

CMD [ "uvicorn", "fast_server:app", "--port", "80", "--host", "0.0.0.0"]