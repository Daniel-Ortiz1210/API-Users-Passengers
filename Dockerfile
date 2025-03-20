FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 3001

CMD [ "python3", "main.py" ]
