FROM python:3.11.3-slim-buster

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

COPY . .

ENTRYPOINT [ "./entrypoint.sh" ]