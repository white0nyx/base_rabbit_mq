import os

from dotenv import load_dotenv
from pika import ConnectionParameters, BlockingConnection

load_dotenv()
RMQ_HOST = os.getenv("RMQ_HOST")
RMQ_PORT = os.getenv("RMQ_PORT")

connection_params = ConnectionParameters(
    host=RMQ_HOST,
    port=RMQ_PORT,
)

def main():
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue="messages")

            for i in range(1, 4):
                ch.basic_publish(
                    exchange="",
                    routing_key="messages",
                    body=f"Привет, RabbitMQ! {i}",
                )
                print("Сообщение отправлено в RabbitMQ")

if __name__ == "__main__":
    main()