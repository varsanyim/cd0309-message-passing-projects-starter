FROM python:3.12.10-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000
EXPOSE 50051

COPY . .

CMD ["python", "wsgi.py"]
