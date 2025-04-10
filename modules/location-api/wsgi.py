import os
from kafka import KafkaProducer
from flask import g   
from app import create_app

app = create_app(os.getenv("FLASK_ENV") or "test")

if __name__ == "__main__":
    app.run(debug=True)

@app.before_request
def before_request():
    TOPIC_NAME = "udaconnect"
    g.kafka_producer = KafkaProducer(
        bootstrap_servers="kafka:9092",
        value_serializer=lambda x: x.encode("utf-8"),
    )
    g.topic_name = TOPIC_NAME