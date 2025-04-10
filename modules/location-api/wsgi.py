import os
from kafka import KafkaProducer
from flask import g   
from app import create_app
import threading
from grpc_server import serve

app = create_app(os.getenv("FLASK_ENV") or "test")

if __name__ == "__main__":
    # Start gRPC server in background thread
    grpc_thread = threading.Thread(target=lambda: serve(app), daemon=True)
    grpc_thread.start()


    # Start Flask server (accessible from container network)
    app.run(host="0.0.0.0", port=5000, debug=False)

@app.before_request
def before_request():
    TOPIC_NAME = "udaconnect"
    g.kafka_producer = KafkaProducer(
        bootstrap_servers="kafka:9092",
        value_serializer=lambda x: x.encode("utf-8"),
    )
    g.topic_name = TOPIC_NAME